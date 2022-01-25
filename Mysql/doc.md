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



