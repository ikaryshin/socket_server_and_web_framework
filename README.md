# 基于 socket 的 Web 服务器和自制 Web 框架

## 部署

在根目录下添加 `config.py` 文件

```python
db_name = ''
```

在根目录下添加 `secret.py` 文件

```python
mysql_password = ''
```

## 架构

### 服务器与 Web 框架的通信
- `server.py` 是一个基于 socket 的 Web 服务器。
- `web_framework.py` 是一个自制的网络框架。
- `wsgi.py` 文件模仿 wsgi 协议，实现 Web 服务器和网络框架之间的通信。

### MVC 架构的 Web 框架
- `app.py` 中注册所有路由。
- `/routes` 中是路由函数，也就是 Controller 部分。 
- `/models` 中是 Model 部分。使用自制的 ORM，对 `pymysql` 库进行封装。
- `/templates` 中是模板，也就是 View 部分。使用 `Jinja2` 语法。

## 功能
1. 首页
![index.gif](https://i.loli.net/2019/09/03/oF9yvUYqc1LRDwX.gif)

2. 注册
![register.gif](https://i.loli.net/2019/09/03/2XwJEiYFHaKnLor.gif)

3. 登录
![login.gif](https://i.loli.net/2019/09/03/RVN5DsKZorFiCHT.gif)

4. 微博系统：发微博
![weibo_comment_new.gif](https://i.loli.net/2019/09/03/f37C4FyAw8T6KiG.gif)

5. 微博系统：编辑微博

  ![weibo_edit.gif](https://i.loli.net/2019/09/03/FAqSHXm3k97lcIi.gif)

6. 微博系统：发评论

  ![weibo_comment_new.gif](https://i.loli.net/2019/09/03/f37C4FyAw8T6KiG.gif)

7. 微博系统：修改评论

  ![weibo_comment_edit.gif](https://i.loli.net/2019/09/03/YszrhNOdFma4wo7.gif)

7. 微博系统：删除评论

   ![weibo_comment_delete.gif](https://i.loli.net/2019/09/03/CI6bS8m2LcTwVsP.gif)

8. 微博系统：删除微博（评论也会一并被删除）

   ![weibo_delete.gif](https://i.loli.net/2019/09/03/ByrV3xAuiQ1kqYN.gif)

## 技术栈

- Python socket
- Jinja2