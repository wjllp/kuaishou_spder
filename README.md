# kuaishou_spder
批量下载快手任意主播的作品

# 使用环境
Python 3.*

# 使用方法
- 下载本项目到电脑
- 运行```pip3 install -r requirements.txt```安装所需环境
- 修改douyin.py中```main```方法中```download(args1, args2)```中的两个参数，参数1表示你的id（即app里的id），参数2表示想要下载的数量。
- 本地执行更改```download.sh```的权限，使其具有运行权限。本地执行```sudo chmod +x download.sh```
