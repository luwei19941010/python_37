### day37

#### 1.内容回顾

```
#协程
    #协程的基础概念
        #什么是协程：多个任务在一条线程上来回切换
        #我们写协程：在一条线程上最大限度的提高CPU的使用率，
                    #在一个任务中遇到IO的时候就切换到其他任务
        #协程的特点:
            #开销很小，是用户级的(只能感知从用户级别能够感知的IO操作)
            #不能利用多核，数据共享，数据安全

    #模块和用法
        #gevent   基于greenlet切换（C语言）
            #先导入模块
            #导入monkey，执行patch_all
            #写入一个函数当做协程要执行的任务
            #协程对象=gevent.spawn(函数名，参数)
            #协程对象.jion()，gevent.joinall([g1,g2...])

            #分辨gevent是否识别了我们写的代码中IO操作的方法
                #在patchall前后打印涉及到io操作
                #如果地址一致说明不识别，如果地址不一致说明识别的了

        #asynci   基于yield机制切换的
            #async 标识一个协程函数
            #await 后面跟着一个asyncio模块提供的io操作的函数
            #loop 事件循环，负责在多个任务之间进行切换的

#3.
#进程 开销大     数据隔离    能利用多核                   数据不安全   操作系统控制
#线程 开销较小   数据共享    cpython解释器下不能用多核     数据不安全   操作系统控制
#协程 开销小     数据共享    不能用多核                   数据安全     用户控制

#哪些地方用到了线程和协程
    #1.自己用线程、协程完成爬虫任务
    #2.后面有了一些比较丰富的爬虫框架
        #了解到scrapy/beautyful soup/aiogttp 爬虫框架 哪些是线程哪些是协程？
    #3.web框架中的并发是如何实现的
        #传统框架：django多线程
        #         flask优先选用协程 其次使用线程
        #socket server:多线程
        #异步框架：tornado，sanic底层都是协程
```



#### 2.mysql

```
    #mysql的CS架构
        #mysqld install 安装数据库服务
        #net start mysql 启动数据库的server端
            #停止server   net stop mysql


#mysql指令
#查看当前用户是谁
	mysql>select user();
    
#设置密码
	mysql>set password =password('密码');
	
#创建用户
	create user 'username'@'192.168.12.%' identified by 'password';
	create user 'username'@'%' identified by 'password';
	
#远程登录
	mysql -uroot -p123 -h 192.168.10.3
	
#查看用户权限
show grants for 'username'@'192.168.1.%';
+---------------------------------------------------------------------------------------------------+
| Grants for luwei@%
                       |
+---------------------------------------------------------------------------------------------------+
| GRANT USAGE ON *.* TO 'luwei'@'%' IDENTIFIED BY PASSWORD '*84B83B0E233FE80A278
5F0271FEAACD9D953A9D2' |
+---------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

#查看当前有多少个数据库
	show databases;
	
#查看文件夹
	
#创建文件夹
	create database day37;

#给账号授权
	grant all on *.* to 'username'@'%';  
	# *.* 第一个*为数据库表示所有数据库，第二个*为表表示在某个数据库下所有表

#刷新使用授权立即生效
	flush privileges;

#创建账号并授权
	grant all on *.* 'usernmae'@'%' identified by 'password'






	
```

```

```

