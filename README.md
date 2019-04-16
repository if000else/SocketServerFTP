##高级FTP服务器开发：

### 作者介绍：

Author：Yaoqing Wang

Nickname:Huayiqiu

Blog:http://www.cnblogs.com/iforelse

Github: https://github.com/if000else

1. 用户加密认证
2. 多用户同时登陆
3. 每个用户有自己的家目录且只能访问自己的家目录
4. 对用户进行磁盘配额、不同用户配额可不同
5. 用户可以登陆server后，可切换目录
6. 查看当前目录下文件
7. 上传下载文件，保证文件一致性
8. 传输过程中现实进度条
9. 支持断点续传


    *admin 123456* to login in local system

    *admin 123456*  to login in server


运行：先运行server.py,启动服务，然后运行ftp.py

详细请看.jpg

目录结构：

`SimpleFTP/`

`　　|-- bin/`

`　　　　| |-- ftp.py`

`　　|`

`　　|-- conf/`

`　　　　| |-- settings.py`

`　　|-- database/`

`　　　　|　|-- client/`

`　　　　|　|-- server/`

`　　　　|　|-- users/`

`　　　　| `

`　　|-- report/`

`　　　　|　|-- log/`

`　　　　|　|  |-- access.log`

`　　　　|　|  |-- client.log`

`　　　　|　|  |-- server.log`

`　　　　|　|  |-- services.log`
        
`　　　　| `

`　　|-- modules/`

`　　　　| |-- display.py`

`　　　　| |-- log.py`

`　　　　| |-- main.py`

`　　　　| |-- server.py`

`　　　　| |-- funcs.py`


`　　　　|`

`　　|-- README`
