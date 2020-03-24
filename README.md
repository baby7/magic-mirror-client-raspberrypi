# 魔镜智能家居系统-树莓派客户端

## 目录结构
```menu
client-raspberrypi/
|-- bin/    项目的可执行文件
|   |-- __init__
|　 |-- start.py   启动程序
|
|-- core/   核心代码1.所有模块放在此目录 2.tests/存放单元测试代码
|   |-- tests/   
|   |   |-- __init__.py
|   |   |-- test_main.py  
|   |-- dialogue/               传感器模块
|   |   |-- __init__.py
|   |   |-- dialogue.py  
|   |-- face_detection/         人脸检测模块
|   |   |-- __init__.py
|   |   |-- face_detection.py  
|   |-- sensor/                 传感器模块
|   |   |-- __init__.py
|   |   |-- sensor.py  
|   |-- view/                   显示模块
|   |   |-- __init__.py
|   |   |-- view.py  
|   |-- __init__.py
|   |-- test_main.py            核心逻辑  
|
|-- conf/    配置文件
|   |-- __init__.py
|   |-- setting.py   相关配置
|
|---db/    数据库文件
|   |--db.json    数据库文件
|   
|-- docs/   一些文档
|   
|-- lib/   库文件，放自定义模块和包
|   |-- __init__.py
|   |-- common.py    常用的功能
|
|-- log/   日志文件
|   |-- access.log    日志
|
|-- __init__.py
|-- README    项目说明文件
```

## 暂定启动子程序列表
> 启动显示程序⬇
>
> 人脸识别线程⬇
>
> 传感器__线程⬇
>
> 语音识别线程