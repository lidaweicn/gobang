
终端运行run.py启动客户端程序

Linux下Qt/PyQt5无法调用fcitx中文输入法解决办法
1、首先安装相关软件

sudo apt install fcitx-frontend-qt5 fcitx-libs-qt fcitx-libs-qt5

安装完成之后会在路径/usr/lib/x86_64-linux-gnu/qt5/plugins/platforminputcontexts/ 看到libfcitxplatforminputcontextplugin.so 

2、复制动态链接库.so文件到相应目录

因为写了个小软件发现QPlainTextEdit 调用不了fcitx中文输入法，同样将前面得到的动态链接库/usr/lib/x86_64-linux-gnu/qt5/plugins/platforminputcontexts/libfcitxplatforminputcontextplugin.so 复制到/usr/local/lib/python3.5/dist-packages/PyQt5/Qt/plugins/platforminputcontexts/

