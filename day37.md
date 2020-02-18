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
```

```
SQL:结构化查询语言(structured query language)
1.DDL语句 数据库定义语言：数据库、表、视图、索引、存储过程、列如create drop alter
2.DML语句 数据库操作语言：插入数据insert、删除数据delete、更新数据update、查询数据select
3.DCL语句 数据库控制语言：列如控制用户的访问权限grant、revoke
```



```
#mysql指令---DCL
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

#查看当前使用的数据库
	select database();
	
#切换到这个数据库(文件下)
	use 数据库的名字	

#删库
	drop database 数据库名字



####表操作--DDL

#创建表
	#create table student(id int,name char(10));

#查看当前表数
	#show tables;

#删除表
	#drop table 表名字

#查看表结构
	#desc student;



###操作表中的数据--DML

#数据的增加
	#insert into 表名字 values (1,'luwei')	#id=1,name='luwei';
	#insert into ftp values (1,'alex','alex3714');
	#insert into 表名字(字段名，字段名) values(值,值)#所有在字段位置填写了名字的字段和后面的值必须一一对应
	#insert into 表名字(字段名，字段名) values(值,值),(值,值),(值,值);	
#数据查看
	#select * from 表名字;

#修改数据
	#update 表名字 set 字段名字=值;		#将所有的字段名字全部改成 ‘值’
	#update 表名字 set name=值 where id=2;
	
#删除数据
	#delete from 表名字;
	#delete from 表名字 where id=1;
	
```

##### 总结

```
##顺序自上而下进行
select distinct 需要显示的列 from 表
						 where 条件
						 group by 分组
						 having 过滤组条件
						 order by 排序
						 limit 前n条 (n,m);== limit n offset m;
执行SQL						 
1.执行from 表;找表
2.执行where 条件;筛选条件
3.执行group by 分组;进行分组
4.执行having 过滤租条件;进行过滤
5.执行select ;对列进行筛选
6.order by;排序
7.limit n,m;分页显示
```

##### 2.1select 语句

```
#select 语句
	#select * from 表；
	#select 字段，字段 from 表；
	#select distinct 字段 .. from 表;去重
	#select 字段，字段(加减乘除)NUM from 表;
	#select 字段，字段(加减乘除)NUM as new_name from 表;==select 字段，字段(加减乘除)NUM new_name from 表;	
	#select concat('姓名：',name,'年薪：',salary*12) as new_name from 表名;#拼接
	#select concat_as (':',name,salary*12) as new_name from 表名;# 用：分割进行拼接
	#case语句
	
	select
	(
	case
		when 字段名 ='值1' then
			字段名
		when 字段名 ='值2' then
			concat(字段名,'_值3')
		else
			concat(字段名,'_值4')
	) as new_name
	from
		表名;
	
```

##### 2.2 where语句

```
where语句
	#不支持与分组连用 
		#因为执行顺序 总是先执行where 再执行group by分组
		#所以相关先分组 之后再根据分组做某些条件筛选的时候 where都用不上
		#只能用having
	#比较运算 >,<,=,>=,<=,!=,<>
		#select * from 表名 where 字段名>值1;
	#范围筛选
		#多选一
			#select * from 表名 where 字段名 in (值1,值2,值3...值n);
			#select * from 表名 where 字段名 not in (值1,值2,值3...值n);
		#在一个模糊的范围里
			#在一个数值区间 1000-2000之间的所有人的名字
				#select * from 表名 where 字段名 between 1000 and 2000;
			#字符串的模糊查询 like
				#通配符%,表示匹配任意长度的任意内容
				#通配符_,表示匹配一个字符长度的任意内容
				#select * from 表名 where 字段名 like 'X%';
				#select * from 表名 where 字段名 like 'X_';
			#正则匹配
				#select * from 表名 where 字段名 regexp '正则表达式';
	#逻辑运算-条件的拼接
		#与
			#select * from 表名 where 字段名=值1 and 字段名=值2;
		#非
			#select * from 表名 where 字段名=值1 or 字段名=值2;
	
	#身份运算符-null is null/is not null 
		#查看是否为null
		#select * from 表名 where 字段名 is null;
```

##### 2.3 group by 分组

```
#分组
	#select * from 表名 group by 字段名;
	#会把在group by后面的这个字段，也就是字段名中的每一个不同的项都保留下来，并且把值是这一项的所有行归为一组
```

##### 2.4 聚合

​	#把很多行的同一个字段进行一些统计，最终得到一个结果

```
select count(*) from 表名;
#count(字段)	统计这个字段有多少项，如果为null 不进行统计。
#sum(字段)	统计这个字段对应的数值的和
#avg(字段)	统计这个字段对应的数值的平均值
#min(字段)	求某个字段的最小值
#max(字段)	求某个字段的最大值

注意#求部门的最高薪资或求公司的最高薪资都可以通过聚合函数取到
   #但是要得到对应的人，就必须通过多表查询
```

##### 2.5 分组聚合

```
#求各个部门的人
#select count(*) from 表名 group by 字段名;
```

##### 2.6 having条件

```
#过滤 组 一般和group by一起连用

#各个部门人数大于3个的部门

select post from employee group by post having count(*)>3;

having 过滤组
	#在group by 之后执行
	#having 中可以使用聚合函数
	#having 后面条件要是么select的字段，要么是分组的字段
```

##### 2.7排序

```
#默认从小到大排序 asc
select * from 表名 order by 字段名;
#从大到小排序
select * from 表名 order by 字段名 desc;
#优先先进行字段1排序，再按字段2排序
select * from 表名 order by 字段1, 字段2 desc; 按照字段1 升序，按照字段2 降序
```



##### 2.8 LIMT限制查询

```
#显示3条
#select * from 表名 order by 字段名 desc limt 3;

分页功能
#select * from 表名 order by 字段名 desc limt 0,3; 1到3
#select * from 表名 order by 字段名 desc limt 3,3; 4到6

limt n,m ==limt n,offset m;
```

##### 2.9多表查询

```
表1.
mysql> select * from emp;
+----+------------+--------+------+--------+
| id | name       | sex    | age  | dep_id |
+----+------------+--------+------+--------+
|  1 | egon       | male   |   18 |    200 |
|  2 | alex       | female |   48 |    201 |
|  3 | wupeiqi    | male   |   38 |    201 |
|  4 | yuanhao    | female |   28 |    202 |
|  5 | liwenzhou  | male   |   18 |    200 |
|  6 | jingliyang | female |   18 |    204 |
+----+------------+--------+------+--------+

表2.
mysql> select * from department;
+------+--------------+
| id   | name         |
+------+--------------+
|  200 | 技术         |
|  201 | 人力资源     |
|  202 | 销售         |
|  203 | 运营         |
+------+--------------+

#多表查询
	#两张表是怎么连在一起的
	#select * from emp，department;
	#链接的语法
	#select 字段 from 表1 xxx join 表2 on 表1.字段=表2.字段;
	#连表查询
		#把两张表连在一起查
		#
		#内链接 inner join 两张表条件不匹配的项不会出现再结果中
			#select * from emp inner join department on emp.dep_id =department.id;
		#外连接
			#左外链接 left jion 永远显示全量的左表中的数据
				#select * from emp left join department on emp.dep_id=department.id;
			#右外链接 right join 永远显示全量的右表中的数据
				#select * from emp right join department on emp.dep_id=department.id;
			#全外链接
				#select * from emp left join department on emp.dep_id=department.id 
				#union
				#select * from emp right jion department on emp.dep_id=department.id;
				
	#子查询
		# 找技术部门的所有人的姓名
		# 先找到部门表技术部门的部门id
         #select id from department where name='技术';
         #再找emp表中部门id=200
         #select name from emp where dep_id=(select id from department where name='技术');
         
       带IN关键字的子查询
         # 找到技术部门和销售部门所有人的姓名
         # 先找到技术部门和销售部门的的部门id
         #select id from department where name='技术' or name='销售';
         #找到emp中部门id=200或者202的人名
         #select name from emp where dep_id in (select id from department where name='技术' or name='销售');
         #select emp.name from emp inner jion department on emp.dep_id =department.id where department.name in ('技术','销售');;
		
	  带比较运算符的子查询
	  	#比较运算符：=、!=、>、>=、<、<=、<>
	  	#查询大于所有人平均年龄的员工名与年龄
		mysql> select name,age from emp where age > (select avg(age) from emp);
	
	  带EXISTS关键字的子查询
		“EXISTS关字键字表示存在。在使用EXISTS关键字时，内层查询语句不返回查询的记录。
		而是返回一个真假值。True或False
		当返回True时，外层查询语句将进行查询；当返回值为False时，外层查询语句不进行查询”
		mysql> select * from employee
    	->     where exists
    	->     (select id from department where id=200);
```

#### 3.mysql 数据类型

```
#mysql的表操作
	#创建方式	存储---存储引擎
	#基础数据类型
	#表的约束
```

mysql version 5.6以上默认 存储引擎为InnoDB

- support
  - transactions 事物
  - row-level locking 行级锁
  - foreign keys 外键

![image-20200213133159201](C:\Users\davidlu\AppData\Roaming\Typora\typora-user-images\image-20200213133159201.png)

```
#表的存储方式
	#查看存储引擎配置项
		#show variables;/show variables like '%engine%';
	#存储方式1：myISAM
		#存储的文件个数：表结构、表中的数据、索引
		#支持表级锁
		#不支持行级锁，不支持事务，不支持外键
		
	#存储方式2：InnoDB
		#存储的文件个数：表结构、表中的数据
		#支持行级锁、表级锁
			#为表中每一行进行锁定，只允许一个人进行修改
			#适应高并发
		#支持事务
			#开启一个事务。将几个操作命令组合成一个事务，作为一个不可再分原子性操作，要么一起成功要么一起失败。
		#支持外键
			#一个表中的数据与另一个表数据产生关联，需要使用外键
			#表与表之间增加约束，安全，减少单表的大小
		
		
    #储存方式3：MEMORY 内存
    	#存储的文件个数：表结构
    	#优势：增删改查速度快
    	#劣势：重启数据消息，容量有限
   
   
   #InnoDB
   用于事务处理应用程序，支持外键和行级锁。如果应用对事务的完整性又比较高的要求，在并发条件下要求数据的一致性，数据操作处理插入和查询之外，还包括很多更新和删除操作，那么InnoDB存储引擎比较合适的，InnoDB除了有效的降低由删除和更新导致的锁定，还可以确保事务的完整提交和回滚，对于类似计费系统或者财务系统对数据准确要求性比较高的系统都是合适的选择。
  #MyISAM
    如果应用是以读操作和插入操作为主，只有很少的更新和删除操作，并对事务的完整性、并发性要求不高，那么可以选择这个存储引擎
  #Memory
    将所有的数据保存在内存中，在需要快速定位记录和其他类似数据的环境下，可以提供极快访问。Memory的缺陷是对表的大小有限制，虽然数据库因为异常终止的话数据可以正常恢复，但是一旦数据库关闭，存储在内存中的数据都会丢失。
```



```
#创建表
	#create table 表名1(id int,name char(4));
	#create table 表名2(id int,name char(4)) engine=myisam;
	
#查看表结构
	#desc 表名;				只能查看表的字段的基础信息
		#describe 表名;
	#show create table 表名;	 能够看到和这张表相关的所有信息
	
		mysql> show create table t1;
        +-------+------------------------------
        | Table | Create Table                   
        +-------+-----------------------------
        | t1    | CREATE TABLE `t1` (
          `id` int(11) DEFAULT NULL,
          `name` char(4) DEFAULT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 |
        +-------+------------------------------

#修改表
#删除表
```

##### 3.1数值类型

#create table 表名(字段名 类型[(宽度) 约束条件]);

###### 	3.1.1整数型 

![image-20200213170656816](C:\Users\davidlu\AppData\Roaming\Typora\typora-user-images\image-20200213170656816.png)



#create table tablename(id int(4) unsigned,id2 int(11));

​		#int 默认是有符号的

​		#他能表示的数字的范围不被宽度约束

​		#它只能约束数字的显示宽度

​		#unsigned无符号

###### 3.1.2 float

![image-20200213210743471](C:\Users\davidlu\AppData\Roaming\Typora\typora-user-images\image-20200213210743471.png)

#create table tablename(id float(25,3) ,id2 float(25,3) );

float(25,3)  #表示一共长度为25位，小数部分3位，整数部分22位。

###### 3.1.3double

![image-20200213210759308](C:\Users\davidlu\AppData\Roaming\Typora\typora-user-images\image-20200213210759308.png)

#create table tablename(id double(25,3) ,id2 double(25,3) );

double(25,3)  #表示一共长度为25位，小数部分3位，整数部分22位。

###### 3.1.4decimal

默认存储整数，decimal(10,0)。为什么能够存的准 底层是用字符来存储。

![image-20200213213449687](C:\Users\davidlu\AppData\Roaming\Typora\typora-user-images\image-20200213213449687.png)





##### 3.2日期与时间

​	#年（year)	年月日(DATA)	时分秒(TIME)	年月日时分秒(DATA TIME)

![image-20200213215754600](C:\Users\davidlu\AppData\Roaming\Typora\typora-user-images\image-20200213215754600.png)

###### 3.2.1 date 年月日 	time 时分秒  	date time 年月日时分秒



```
create table t5(y year,d date,t time,dt datetime,ts timestamp);
insert into t5 values(now(),now(),now(),now(),now());
insert into t5 values(2020,20200212,221415,20200212122425,20200202121224);
insert into t5 values(2020,20200212,221415,'2020-02-12 12:24:25','2020-02-02 12:12:24');

| t5    | CREATE TABLE `t5` (
  `y` year(4) DEFAULT NULL,
  `d` date DEFAULT NULL,
  `t` time DEFAULT NULL,
  `dt` datetime DEFAULT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 |
```

```
mysql> create table t4 (d date,t time,dt datetime);
Query OK, 0 rows affected (0.02 sec)

mysql> desc t4;
+-------+----------+------+-----+---------+-------+
| Field | Type     | Null | Key | Default | Extra |
+-------+----------+------+-----+---------+-------+
| d     | date     | YES  |     | NULL    |       |
| t     | time     | YES  |     | NULL    |       |
| dt    | datetime | YES  |     | NULL    |       |
+-------+----------+------+-----+---------+-------+
rows in set (0.01 sec)

mysql> insert into t4 values (now(),now(),now());
Query OK, 1 row affected, 1 warning (0.01 sec)

mysql> select * from t4;
+------------+----------+---------------------+
| d          | t        | dt                  |
+------------+----------+---------------------+
| 2018-09-21 | 14:51:51 | 2018-09-21 14:51:51 |
+------------+----------+---------------------+
row in set (0.00 sec)

mysql> insert into t4 values (null,null,null);
Query OK, 1 row affected (0.01 sec)

mysql> select * from t4;
+------------+----------+---------------------+
| d          | t        | dt                  |
+------------+----------+---------------------+
| 2018-09-21 | 14:51:51 | 2018-09-21 14:51:51 |
| NULL       | NULL     | NULL                |
+------------+----------+---------------------+
rows in set (0.00 sec)
```

###### 3.2.2 timestamp示例

```
mysql> create table t5 (id1 timestamp);
Query OK, 0 rows affected (0.02 sec)

mysql> desc t5;
+-------+-----------+------+-----+-------------------+-----------------------------+
| Field | Type      | Null | Key | Default           | Extra                       |
+-------+-----------+------+-----+-------------------+-----------------------------+
| id1   | timestamp | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
+-------+-----------+------+-----+-------------------+-----------------------------+
row in set (0.00 sec)

# 插入数据null，会自动插入当前时间的时间
mysql> insert into t5 values (null);
Query OK, 1 row affected (0.00 sec)

mysql> select * from t5;
+---------------------+
| id1                 |
+---------------------+
| 2018-09-21 14:56:50 |
+---------------------+
row in set (0.00 sec)

#添加一列 默认值是'0000-00-00 00:00:00'
mysql> alter table t5 add id2 timestamp;
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> show create table t5 \G;
*************************** 1. row ***************************
       Table: t5
Create Table: CREATE TABLE `t5` (
  `id1` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `id2` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8
row in set (0.00 sec)

ERROR: 
No query specified

# 手动修改新的列默认值为当前时间
mysql> alter table t5 modify id2 timestamp default current_timestamp;
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> show create table t5 \G;
*************************** 1. row ***************************
       Table: t5
Create Table: CREATE TABLE `t5` (
  `id1` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `id2` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8
row in set (0.00 sec)

ERROR: 
No query specified

mysql> insert into t5 values (null,null);
Query OK, 1 row affected (0.01 sec)

mysql> select * from t5;
+---------------------+---------------------+
| id1                 | id2                 |
+---------------------+---------------------+
| 2018-09-21 14:56:50 | 0000-00-00 00:00:00 |
| 2018-09-21 14:59:31 | 2018-09-21 14:59:31 |
+---------------------+---------------------+
rows in set (0.00 sec)
```



```
mysql> create table t6 (t1 timestamp);
Query OK, 0 rows affected (0.02 sec)

mysql> desc t6;
+-------+-----------+------+-----+-------------------+-----------------------------+
| Field | Type      | Null | Key | Default           | Extra                       |
+-------+-----------+------+-----+-------------------+-----------------------------+
| t1    | timestamp | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
+-------+-----------+------+-----+-------------------+-----------------------------+
row in set (0.01 sec)

mysql> insert into t6 values (19700101080001);
Query OK, 1 row affected (0.00 sec)

mysql> select * from t6;
+---------------------+
| t1                  |
+---------------------+
| 1970-01-01 08:00:01 |
+---------------------+
row in set (0.00 sec)
# timestamp时间的下限是19700101080001
mysql> insert into t6 values (19700101080000);
ERROR 1292 (22007): Incorrect datetime value: '19700101080000' for column 't1' at row 1

mysql> insert into t6 values ('2038-01-19 11:14:07');
Query OK, 1 row affected (0.00 sec)
# timestamp时间的上限是2038-01-19 11:14:07
mysql> insert into t6 values ('2038-01-19 11:14:08');
ERROR 1292 (22007): Incorrect datetime value: '2038-01-19 11:14:08' for column 't1' at row 1
mysql> 
```



###### 3.2.3 year示例

```
mysql> create table t7 (y year);
Query OK, 0 rows affected (0.02 sec)

mysql> insert into t7 values (2018);
Query OK, 1 row affected (0.00 sec)

mysql> select * from t7;
+------+
| y    |
+------+
| 2018 |
+------+
row in set (0.00 sec)
```

```
mysql> create table t8 (dt datetime);
Query OK, 0 rows affected (0.01 sec)

mysql> insert into t8 values ('2018-9-26 12:20:10');
Query OK, 1 row affected (0.01 sec)

mysql> insert into t8 values ('2018/9/26 12+20+10');
Query OK, 1 row affected (0.00 sec)

mysql> insert into t8 values ('20180926122010');
Query OK, 1 row affected (0.00 sec)

mysql> insert into t8 values (20180926122010);
Query OK, 1 row affected (0.00 sec)

mysql> select * from t8;
+---------------------+
| dt                  |
+---------------------+
| 2018-09-26 12:20:10 |
| 2018-09-26 12:20:10 |
| 2018-09-26 12:20:10 |
| 2018-09-26 12:20:10 |
+---------------------+
rows in set (0.00 sec)

datetime示例
```



##### 3.3字符串

![image-20200213224547097](C:\Users\davidlu\AppData\Roaming\Typora\typora-user-images\image-20200213224547097.png)

```
#char（15）定长的单位 ，15个字符
	#alex  alex       (空格补齐11个)
	#alex
	
#varchar（15）变长的单位
	#alex  alex4

哪一个存储方式好？
	#varchar:节省空间、存取效率相对低
	#char：长度变化小的，浪费空间，存取效率相对高
```

###### 3.3.1char/varchar示例

```
mysql> create table t9 (v varchar(4),c char(4));
Query OK, 0 rows affected (0.01 sec)

mysql> insert into t9 values ('ab  ','ab  ');
Query OK, 1 row affected (0.00 sec)

# 在检索的时候char数据类型会去掉空格
mysql> select * from t9;
+------+------+
| v    | c    |
+------+------+
| ab   | ab   |
+------+------+
row in set (0.00 sec)

# 来看看对查询结果计算的长度
mysql> select length(v),length(c) from t9;
+-----------+-----------+
| length(v) | length(c) |
+-----------+-----------+
|         4 |         2 |
+-----------+-----------+
row in set (0.00 sec)

# 给结果拼上一个加号会更清楚
mysql> select concat(v,'+'),concat(c,'+') from t9;
+---------------+---------------+
| concat(v,'+') | concat(c,'+') |
+---------------+---------------+
| ab  +         | ab+           |
+---------------+---------------+
row in set (0.00 sec)

# 当存储的长度超出定义的长度，会截断
mysql> insert into t9 values ('abcd  ','abcd  ');
Query OK, 1 row affected, 1 warning (0.01 sec)

mysql> select * from t9;
+------+------+
| v    | c    |
+------+------+
| ab   | ab   |
| abcd | abcd |
+------+------+
rows in set (0.00 sec)
```

##### 3.4 ENUM与SET类型

![image-20200213225923572](C:\Users\davidlu\AppData\Roaming\Typora\typora-user-images\image-20200213225923572.png)

```
ENUM中文名称叫枚举类型，它的值范围需要在创建表时通过枚举方式显示。ENUM只允许从值集合中选取单个值，而不能一次取多个值。

SET和ENUM非常相似，也是一个字符串对象，里面可以包含0-64个成员。根据成员的不同，存储上也有所不同。set类型可以允许值集合中任意选择1或多个元素进行组合。对超出范围的内容将不允许注入，而对重复的值将进行自动去重。
```

```
mysql> create table t10 (name char(20),gender enum('female','male'));
Query OK, 0 rows affected (0.01 sec)

# 选择enum('female','male')中的一项作为gender的值，可以正常插入
mysql> insert into t10 values ('nezha','male');
Query OK, 1 row affected (0.00 sec)

# 不能同时插入'male,female'两个值，也不能插入不属于'male,female'的值
mysql> insert into t10 values ('nezha','male,female');
ERROR 1265 (01000): Data truncated for column 'gender' at row 1

mysql> create table t11 (name char(20),hobby set('抽烟','喝酒','烫头','翻车'));
Query OK, 0 rows affected (0.01 sec)

# 可以任意选择set('抽烟','喝酒','烫头','翻车')中的项，并自带去重功能
mysql> insert into t11 values ('yuan','烫头,喝酒,烫头');
Query OK, 1 row affected (0.01 sec)

mysql> select * from t11;
+------+---------------+
| name | hobby        |
+------+---------------+
| yuan | 喝酒,烫头     |
+------+---------------+
row in set (0.00 sec)

# 不能选择不属于set('抽烟','喝酒','烫头','翻车')中的项，
mysql> insert into t11 values ('alex','烫头,翻车,看妹子');
ERROR 1265 (01000): Data truncated for column 'hobby' at row 1
```



#### 4.约束

```
#unsigned 设置某一个数字无符号
	#create table tablename(id int(4) unsigned,id2 int(11));
#not null 某一个字段不能为空
	# create table t6(id int not null,name char(10));
#default  给某个字段设置默认值
	# create table t6(id int not null default 999,name char(10));
	# insert into t6(name) values('alex');
#unique	 设置一个字段不能重复
	# create table t6(id int unique,name char(10));
	#联合唯一
#auto_increment  设置某一个int类型的字段，自动增加，自带非空（not null）效果
	# 自增字段 必须是数字 且 必须是唯一的
#primary key 设置某一个字段非空且不能重复
	#一张表只能设置一个主键
	#一张表最好设置一个主键
	#约束这个字段非空(not null) 且唯一(unique)
	#指定第一个非空且唯一的字段会被定义成主键
	#create tables t7(id int primary key ,name char(10) not null unique);
#foreign key 外键
	#	#create table t4(
	id int,
	ip char(15),
	server char(10),
	port int,
	foreign key (port) references t5(pid)
	)

#联合唯一
	#create table t4(
	id int,
	ip char(15),
	server char(10),
	port int,
	unique(ip,port)
	);
	
#联合主键
	#create table t8(
	id int,
	ip char(15),
	server char(10),
	port int,
	primary key(ip,port)
	);
	
#级联删除与级联更新
	#	#create table t4(
	id int,
	ip char(15),
	server char(10),
	port int,
	foreign key (port) references t5(pid) on update cascade on delete cascade/set null/set default
	);
```

![image-20200214133713316](C:\Users\davidlu\AppData\Roaming\Typora\typora-user-images\image-20200214133713316.png)





#### 5.修改表结构

```
#添加字段
	alter table 表名 add 字段名 数据类型(宽度) 约束;
	alter table 表名 add 字段名 数据类型(宽度) 约束 frist;
	alter table 表名 add 字段名 数据类型(宽度) 约束 after name;
#删除字段 
	alter table 表名 drop 字段名;
	
#修改已经存在的字段 的类型 宽度 约束，不能修改字段名字
	alter table 表名 modify 字段名 char(10) not null;
	
#修改已经存在的字段 的类型 宽度 约束 字段名字
	alter table 表名 change 字段名 new_name char(10) not null;

#字段名调整顺序
	alter table 表名 modify age int not null after id;
	alter table 表名 modify age int not null first;#调整到第一个位置

```

https://www.cnblogs.com/Eva-J/articles/9677452.html



#### 6.多张表的关系

##### 6.1多对一

```
#多个学生都是同一个班级
#学生表 关联 班级表
#学生多 班级唯一
```

##### 6.2一对一

```
#客户关系表
#学生表
```

##### 6.3多对多

```
#书 
#作者

#产生第三张表，把两个关联关系的字段作为第三张表的外键

```

![image-20200214161518588](C:\Users\davidlu\AppData\Roaming\Typora\typora-user-images\image-20200214161518588.png)



#### 7.索引

##### 7.1什么是索引

```
1.就是建立起的一个在存储表阶段
2.就有一个存储结构能在查询的时候加速

索引的重要性
	#读写比例： 10：1
	#读的速度就至关重要了
```

##### 7.2索引的原理

```
    # 数据库的存储方式
        # 新的数据结构 —— 树
        # 平衡树 balance tree - b树
        # 在b树的基础上进行了改良 - b+树
            # 1.分支节点和根节点都不再存储实际的数据了
                # 让分支和根节点能存储更多的索引的信息
                # 就降低了树的高度
                # 所有的实际数据都存储在叶子节点中
            # 2.在叶子节点之间加入了双向的链式结构
                # 每个叶子节点都指向相邻的叶子节点地址,(上一个指向下一个,形成闭环)
                # 方便在范围查找时,只需要查找两个节点
        # mysql当中所有的b+树索引的高度都基本控制在3层
            # 1.io操作的次数非常稳定
            # 2.有利于通过范围查询
        # 什么会影响索引的效率 —— 树的高度
            # 1.对哪一列创建索引，选择尽量短的列做索引
            # 2.对区分度高的列建索引，重复率超过了10%那么不适合创建索引

```

##### 7.3聚集与辅助索引

```
hash类型的索引：查询单条快，范围查询慢
btree类型的索引：b+树，层数越多，数据量指数级增长（我们就用它，因为innodb默认支持它）

#不同的存储引擎支持的索引类型也不一样
InnoDB 支持事务，支持行级别锁定，支持 B-tree、Full-text 等索引，不支持 Hash 索引；
MyISAM 不支持事务，支持表级别锁定，支持 B-tree、Full-text 等索引，不支持 Hash 索引；
Memory 不支持事务，支持表级别锁定，支持 B-tree、Hash 等索引，不支持 Full-text 索引；
NDB 支持事务，支持行级别锁定，支持 Hash 索引，不支持 B-tree、Full-text 等索引；
Archive 不支持事务，支持表级别锁定，不支持 B-tree、Hash、Full-text 等索引；
```

```
# 聚集索引和辅助索引
    # 在innodb中 聚集索引和辅助索引并存的
        # 聚集索引 - 主键 更快
            # 数据直接存储在树结构的叶子节点
        # 辅助索引 - 除了主键之外所有的索引都是辅助索引 稍慢
            # 数据不直接存储在树中
    # 在myisam中 只有辅助索引，没有聚集索引
    
    # 索引的种类
   	1.聚集索引
    #primary key 主键 聚集索引  约束的作用：非空 + 唯一
    #如果未定义主键，MySQL取第一个唯一索引（unique）而且只含非空列（not null）作为主键，InnoDB使用它作为聚簇索引。
    #如果没有这样的列，InnoDB就自己产生一个这样的ID值，它有六个字节，而且是隐藏的，使其作为聚集索引。
   		# -PRIMARY KEY(id,name):联合主键索引
   		
   	2.辅助索引
    # unique 自带索引 辅助索引   约束的作用：唯一
        -UNIQUE(id,name):联合唯一索引
    # index  辅助索引            没有约束作用
        -INDEX(id,name):联合普通索引
        
    '''# 除此之外还有全文索引，即FULLTEXT
		会员备注信息 ， 如果需要建索引的话，可以选择全文搜索。
		用于搜索很长一篇文章的时候，效果最好。'''
        
# 看一下如何创建索引、创建索引之后的变化
    # create index 索引名字 on 表(字段)
    # DROP INDEX 索引名 ON 表名字;
# 索引是如何发挥作用的
    # select * from 表 where id = xxxxx
        # 在id字段没有索引的时候，效率低
        # 在id字段有索引的之后，效率高
```

![image-20200217195119759](C:\Users\davidlu\AppData\Roaming\Typora\typora-user-images\image-20200217195119759.png)

##### 7.4 创建/删除索引的语法

```
#方法一：创建表时
    　　CREATE TABLE 表名 (
                字段名1  数据类型 [完整性约束条件…],
                字段名2  数据类型 [完整性约束条件…],
                [UNIQUE | FULLTEXT | SPATIAL ]   INDEX | KEY
                [索引名]  (字段名[(长度)]  [ASC |DESC]) 
                );


#方法二：CREATE在已存在的表上创建索引
        CREATE  [UNIQUE | FULLTEXT | SPATIAL ]  INDEX  索引名 
                     ON 表名 (字段名[(长度)]  [ASC |DESC]) ;
		#create index ix_age on t1(age);
	
	
#方法三：ALTER TABLE在已存在的表上创建索引
        ALTER TABLE 表名 ADD  [UNIQUE | FULLTEXT | SPATIAL ] INDEX
                             索引名 (字段名[(长度)]  [ASC |DESC]) ;
         #alter table t1 add index ix_sex(sex);
		#alter table t1 add index(sex);    
        
        
#删除索引：DROP INDEX 索引名 ON 表名字;
```



##### 7.6正确使用索引

```
#https://www.cnblogs.com/Eva-J/articles/10126413.html#_label1
1.范围问题
	#或者说条件不明确，条件中出现这些符号或关键字：>、>=、<、<=、!= 、between...and...、like、
        # > < >= <= != 
        # between and
            # select * from 表 order by age limit 0，5
            # select * from 表 where id between 1000000 and 1000005;
        # like
            # 结果的范围大 索引不生效
            # 如果 abc% 索引生效，%abc索引就不生效
            #注意 %在后面查的快，在前面慢。'xx%'快，'%xx'慢
```

```
2.如果一列内容的区分度不高，索引也不生效
	尽量选择区分度高的列作为索引,区分度的公式是count(distinct col)/count(*)，表示字段不重复的比例，比例越大我们扫描的记录数越少，唯一键的区分度是1，而一些状态、性别字段可能在大数据面前区分度就是0，那可能有人会问，这个比例有什么经验值吗？使用场景不同，这个值也很难确定，一般需要join的字段我们都要求是0.1以上，即平均1条扫描10条记录
```

```
3.索引列不能在条件中参与计算
	索引列不能在条件中参与计算，保持列“干净”，比如from_unixtime(create_time) = ’2014-05-29’就不能使用到索引，原因很简单，b+树中存的都是数据表中的字段值，但进行检索时，需要把所有元素都应用函数才能比较，显然成本太大。所以语句应该写成create_time = unix_timestamp(’2014-05-29’)

	# select * from s1 where id*10 = 1000000;  索引不生效
	# select * from s1 where id = 1000000/10;  索引生效
```

```
4.对两列内容进行条件查询
    # and and条件两端的内容，优先选择一个有索引的，并且树形结构更好的，来进行查询
    	# 两个条件都成立才能完成where条件，先完成范围小的缩小后面条件的压力
    	# select * from s1 where id =1000000 and email = 'eva1000000@oldboy';
    #and的工作原理
    条件：	a = 10 and b = 'xxx' and c > 3 and d =4
    索引： 制作联合索引(d,a,b,c)
    工作原理: 对于连续多个and：mysql会按照联合索引，从左到右的顺序找一个区分度高的索引字段(这样便可以快速锁定很小的范围)，加速查询，即按照d—>a->b->c的顺序
    
    
     '''经过分析，在条件为name='egon' and gender='male' and id>333 and email='xxx'的情况下，我们完全没必要为前三个条件的字段加索引，因为只能用上email字段的索引，前三个字段的索引反而会降低我们的查询效率'''
     
     
        
    # or or条件的，不会进行优化，只是根据条件从左到右依次筛选
    	# 条件中带有or的要想命中索引，这些条件中所有的列都是索引列
    	# select * from s1 where id =1000000 or email = 'eva1000000@oldboy';
    
    #or的工作原理
    条件：a = 10 or b = 'xxx' or c > 3 or d =4
    索引：制作联合索引(d,a,b,c)      
    工作原理:对于连续多个or：mysql会按照条件的顺序，从左到右依次判断，即a->b->c->d
    
    
```

```
5.联合索引  # create index ind_mix on s1(id,name,email);
	最左前缀匹配原则（详见第八小节），非常重要的原则，对于组合索引mysql会一直向右匹配直到遇到范围查询(>、<、between、like)就停止匹配(指的是范围大了，有索引速度也慢)，比如a = 1 and b = 2 and c > 3 and d = 4 如果建立(a,b,c,d)顺序的索引，d是用不到索引的，如果建立(a,b,d,c)的索引则都可以用到，a,b,d的顺序可以任意调整。
	
	# select * from s1 where id =1000000 and email = 'eva1000000@oldboy';
        # 在联合索引中如果使用了or条件索引就不能生效
            # select * from s1 where id =1000000 or email = 'eva1000000@oldboy';
        # 最左前缀原则 ：在联合索引中，条件必须含有在创建索引的时候的第一个索引列
            # select * from s1 where id =1000000;    能命中索引
            # select * from s1 where email = 'eva1000000@oldboy';  不能命中索引
            # (a,b,c,d)
                # a,b
                # a,c
                # a
                # a,d
                # a,b,d
                # a,c,d
                # a,b,c,d
        # 在整个条件中，从开始出现模糊匹配的那一刻，索引就失效了
            # select * from s1 where id >1000000 and email = 'eva1000001@oldboy';
            # select * from s1 where id =1000000 and email like 'eva%';

```







#### 8.数据备份和事务

```
# mysqldump -uroot -p123  day40 > D:\code\s21day41\day40.sql
# mysqldump -uroot -p123 --databases new_db > D:\code\s21day41\db.sql


# begin;  # 开启事务
# select * from emp where id = 1 for update;  # 查询id值，for update添加行锁；
# update emp set salary=10000 where id = 1; # 完成更新
# commit; # 提交事务
```



