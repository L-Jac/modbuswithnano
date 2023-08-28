

#### 1. 开发板与上位机连接  
板子通过串口助手与电脑连接，使用电脑初始化配置：  
设置MobaXterm串口连接  
波特率 115200，  
Advance Serial settings: Flow control->none  

#### 2. 将SD卡系统烧写到开发板  
[官方文档](https://wiki.friendlyelec.com/wiki/index.php/NanoPi_NEO_Core/zh#.E4.BB.8B.E7.BB.8D)   
根据步骤将SD卡系统烧写到emmc内存中  
(前侧和左侧需要引脚解核心板)  
用户名： root 密码：fa  
* 命令  
    >eflasher  
    >1  
    >yes  

拔出SD卡  
断电重启后，用户名pi，密码pi

#### 3. 配置系统（初次使用需连接网线）  
##### （1）更换下载源
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak  
sudo vim /etc/apt/sources.list

* 源：  
    >deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ focal main restricted  
    >deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ focal-updates main restricted  
    >deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ focal universe  
    >deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ focal-updates universe  
    >deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ focal multiverse  
    >deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ focal-updates multiverse  
    >deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ focal-backports main restricted universe multiverse  
    >deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ focal-security main restricted  
    >deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ focal-security universe  
    >deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ focal-security multiverse  

##### （2）更新系统软件  
sudo apt-get update

#### 4. 下载使用WIFI所需的固件并无线联网
sudo apt-get install linux-firmware  
拔插一下USB无线模块  
sudo nmcli dev  
* 若未显示新WiFi模块

    >su root进入root权限后修改配置文件（/etc/netplan/01-netcfg.yaml）  
    >sudo vim 01-netcfg.yaml
```
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: true
```
* 应用更改  
    >sudo netplan apply  

sudo nmcli dev wifi  

sudo nmcli dev wifi connect "WH-iot" password "wh213215"

#### 5. 用MobaXterm的SSH登录开发板
##### （1）查询板子的IP地址
ifconfig
##### （2）用MobaXterm的SSH登录
Session->new   
session->SSH  
Remote host: 板子的	IP地址  
用户名pi，密码pi。

* 原unbuntu源  
    >deb http://ports.ubuntu.com/ focal-backports main multiverse restricted universe  
    >deb http://ports.ubuntu.com/ focal-proposed main multiverse restricted universe  
    >deb http://ports.ubuntu.com/ focal-security main multiverse restricted universe  
    >deb http://ports.ubuntu.com/ focal-updates main multiverse restricted universe  
    >deb-src http://ports.ubuntu.com/ focal main multiverse restricted universe  
    >deb-src http://ports.ubuntu.com/ focal-backports main multiverse restricted univverse  
    >deb-src http://ports.ubuntu.com/ focal-proposed main multiverse restricted univeerse  
    >deb-src http://ports.ubuntu.com/ focal-updates main multiverse restricted univerrse

* unbuntu系统升级
    >sudo apt update  
    >sudo apt upgrade  
    >sudo do-release-upgrade
