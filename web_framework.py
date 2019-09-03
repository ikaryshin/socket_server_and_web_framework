# 解析 HTTP 请求，构建 HTTP 响应，和 server 进行沟通
# 提供对 Controller 和 View 部分的支持
# 提供某些框架带有的方便功能（比如权限控制等等）
import os

from jinja2 import FileSystemLoader, Environment

from models.session import Session
from models.user import User
from utils import log

# 路由映射
url_map = {}


# 根据不同的 HTTP 请求得到的不同路由调用不同的 Controller 函数，这是框架的核心，
def response_for_path(request):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    # 注册外部的路由
    response = url_map.get(request.path, error)
    log('request', request, response)
    return response(request)


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    # 之前上课我说过不要用数字来作为字典的 key
    # 但是在 HTTP 协议中 code 都是数字似乎更方便所以打破了这个原则
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def formatted_header(headers, code=200):
    header = 'HTTP/1.1 {} OK\r\n'.format(code)
    header += ''.join([
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    ])
    return header


def html_response(filename, **kwargs):
    body = Template.render(filename, **kwargs)

    # 下面 3 行可以改写为一条函数, 还把 headers 也放进函数中
    headers = {
        'Content-Type': 'text/html',
    }
    header = formatted_header(headers)
    r = header + '\r\n' + body
    return r.encode()


def initialized_environment():
    # 初始化 Jinja2 模板
    parent = os.path.dirname(__file__)
    path = os.path.join(parent, 'templates')
    # 创建一个加载器, jinja2 会从这个目录中加载模板
    loader = FileSystemLoader(path)
    # 用加载器创建一个环境, 有了它才能读取模板文件
    e = Environment(loader=loader)
    return e


class Template:
    # 这里作为一个单例使用
    e = initialized_environment()

    @classmethod
    def render(cls, filename, *args, **kwargs):
        # 调用 get_template() 方法加载模板并返回
        template = cls.e.get_template(filename)
        # 用 render() 方法渲染模板
        # 可以传递参数
        return template.render(*args, **kwargs)


def current_user(request):
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        s = Session.one(session_id=session_id)
        if s is None or s.expired():
            return User.guest()
        else:
            user_id = s.user_id
            u = User.one(id=user_id)
            if u is None:
                return User.guest()
            else:
                return u
    else:
        return User.guest()


def redirect(url, session_id=None):
    h = {
        'Location': url,
    }
    if isinstance(session_id, str):
        h.update({
            'Set-Cookie': 'session_id={}; path=/'.format(session_id)
        })
    response = formatted_header(h, 302) + '\r\n'
    return response.encode()


def login_required(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    def f(request):
        log('login_required')
        u = current_user(request)
        if u.is_guest():
            log('游客用户')
            return redirect('/user/login/view')
        else:
            log('登录用户', route_function)
            return route_function(request)

    return f
