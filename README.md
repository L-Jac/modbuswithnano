

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

#### 3. 换源更新（初次使用需连接网线）  
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

* 原ubuntu源  
    >deb http://ports.ubuntu.com/ focal-backports main multiverse restricted universe  
    >deb http://ports.ubuntu.com/ focal-proposed main multiverse restricted universe  
    >deb http://ports.ubuntu.com/ focal-security main multiverse restricted universe  
    >deb http://ports.ubuntu.com/ focal-updates main multiverse restricted universe  
    >deb-src http://ports.ubuntu.com/ focal main multiverse restricted universe  
    >deb-src http://ports.ubuntu.com/ focal-backports main multiverse restricted univverse  
    >deb-src http://ports.ubuntu.com/ focal-proposed main multiverse restricted univeerse  
    >deb-src http://ports.ubuntu.com/ focal-updates main multiverse restricted univerrse

* ubuntu系统升级
    >sudo apt update  
    >sudo apt upgrade  
    >sudo do-release-upgrade

#### 6. 所需环境配置
##### (1)创建虚拟环境
>apt install python3.10-venv  
>python3 -m venv nano_project  
>source nano_project/bin/activat  (activat路径)  

##### (2)requirement.txt的使用
* 生成项目requirement.txt
>opencv 建议单独 sudo apt install python3-opencv  
>pip install pipreqs  
>对应目录下生成  
>pipreqs ./ --encoding=utf8  
>覆盖原requirement.txt  
>pipreqs ./ --encoding=utf8 --force  

* 使用requirement.txt
>pip install -r requirements.txt

##### (3)安装libopencv-dev
>sudo apt-get install libopencv-dev..

##### (4)安装RPi.GPIO
>sudo apt-get install python3-dev  
>sudo git clone https://github.com/friendlyarm/RPi.GPIO_NP  
* 生成whl文件方便使用(GPIO文件夹内已有whl文件)
> cd RPi.GPIO_NP  
> pip install wheel  
> pip install build  
> python3 -m build --wheel -n -x  
> cd dist  
> 保存whl文件  
* 使用whl文件安装
> cd GPIO 对应路径  
> pip install RPi.GPIO-0.5.8-cp38-cp38-linux_armv7l.whl  
 