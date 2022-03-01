- [time_utils](#time_utils)
  - [convert_time.py 时间相互转换](#convert_timepy-时间相互转换)
- [ip utils](#ip-utils)
  - [verify_ip.py 验证ip](#verify_ippy-验证ip)
- [logs](#logs)
  - [log.py logging 二次封装 支持按日期分割日志、按天分割日志,支持多进程安全](#logpy-logging-二次封装-支持按日期分割日志按天分割日志支持多进程安全)
- [captcha](#captcha)
  - [captcha.py 生成图片验证码](#captchapy-生成图片验证码)
# time_utils

```reStructuredText
时间处理
```

## [convert_time.py](./time_utils/convert_time.py) 时间相互转换

- str_to_timestamp 字符串时间转换为时间戳
  
- str_to_datetime  字符串时间转换为datetime
  
- timestamp_to_str 时间戳转换为时间字符串
  
- timestamp_to_datetime 时间戳转换为datetime
  
- datetime_to_str datetime转换为时间字符串
  
- datetime_to_timestamp datetime转换为时间戳

# ip utils

```reStructuredText
ip处理
```
## [verify_ip.py](./ip_utils/verify_ip.py) 验证ip

- is_ipv4 判断是否为ipv4地址
- is_ipv6 判断是否为ipv6地址
- is_ipv4_cidr 判断是否为ipv4断
- is_ipv6_cidr 判断是否为ipv6段
- is_ipv4_range 验证字符串是否为ipv4范围
- is_ipv6_range 验证字符串是否为ipv6范围
- ip_in_cidr  判断ip是否属于一个网段
- is_loopback 判断ip是否为本地回环地址

# logs
```text
日志相关操作
```
## [log.py](./logs/log.py) logging 二次封装 支持按日期分割日志、按天分割日志,支持多进程安全

# captcha
```text
图片验证码
```
## [captcha.py](./captcha/captcha.py) 生成图片验证码