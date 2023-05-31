# centos7配置静态ip

```bash
# 打开网卡配置
vim /etc/sysconfig/network-scripts/ifcfg-ens18

# 添加以下内容
TYPE=Ethernet
BOOTPROTO=static # 设置网卡获得ip地址的方式 static代表静态
DEFROUTE=yes
PEERDNS=yes
PEERROUTES=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_PEERDNS=yes
IPV6_PEERROUTES=yes
IPV6_FAILURE_FATAL=no
NAME=ens18
UUID=70002612-4de4-4e20-9034-524981b6beb0
DEVICE=ens18 # 网卡名
ONBOOT=yes # 网卡启动方式
IPADDR=192.168.18.50 # ip地址
NETMASK=255.255.255.0 # 掩码
GATEWAY=192.168.18.254 # 网关
DNS1=114.114.114.114  # dns地址

# host地址映射
vim /etc/hosts

# 添加
1.1.1.1 www.baidu.com

# 重启服务
service network restart
```

# centos7安装docker

```bash
# 卸载旧版本
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
# 安装
sudo yum install -y yum-utils

sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo

 sudo yum install docker-ce docker-ce-cli containerd.io
# 启动
sudo systemctl start docker
```

# docker启动所有容器
```bash
docker start $(docker ps -a | awk '{ print $1}' | tail -n +2)
```

# tar解压指定目录

```bash
tar zxvf test.tgz -C 指定目录
# -C 指定目录
tar zxvf /source/kernel.tgz -C /source/linux-2.6.29
```

# nohup后台运行
```bash
nohup python -m SimpleHTTPServer 8080 &
```
# 查看当前目录下的各个文件夹大小
```bash
du -h --max-depth=1 /root
```
# 查看系统占用大小前10的文件
```bash
du -hsx * | sort -rh | head -10
```
# 查看某个目录下占用大小前10的文件
```bash
du -ah /root | sort -n -r | head -n 10
```
# 清理指定目录下n天前不使用的目录和文件
```bash
find /tmp -mtime +3 -exec rm -rf {} \;
```
# 修改指定网卡mac地址
```bash

# 关闭网卡
ifconfig eth1 down
# 修改mac地址
ifconfig eth1 hw ether 98:29:A6:56:56:33
# 重启网卡
ifconfig eth1
```