- [Mysql](#mysql)
  - [修改表数据](#修改表数据)
  - [跳过密码认证](#跳过密码认证)
  - [修改完配置刷新数据库](#修改完配置刷新数据库)
  - [navicat 连接mysql8](#navicat-连接mysql8)
# Mysql

## 修改表数据
```sql
-------------语法-----------
update table set column='' where column='';
-------------示例-----------
update user set name='张三' where id=1;
```

## 跳过密码认证

```bash
# 配置文件中加入
skip-grant-tables=1
# 重启MySQL服务
systemctl restart mysql
```

## 修改完配置刷新数据库

```bash
flush privileges;
```
## navicat 连接mysql8
```bash
1、修改mysql配置文件 
sed -i 's/127.0.0.1/0.0.0.0/g' mysql安装目录/conf/mysqld.cnf
2、进入mysql
use mysql; 
update user set host='%' where user ='root'; 
FLUSH PRIVILEGES;
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'WITH GRANT OPTION;