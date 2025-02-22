双面的python影视爬虫,资源均来自于第三方网站,里面的广告与作者无关,切勿相信
部署:
1、首先需要安装python3环境
2、模块安装 pip install -r requirements.txt
3、在win系统下已经内置了一套浏览器与浏览器驱动,模块与python安装好后开箱即用
4、其他系统你需要自行安装谷歌浏览器与对应版本,然后在根目录下的init.ini修改好路径后即可使用

使用:
配置文件是init.ini可以设置保存路径(支持中文),下载速度(多线程下载,n表示开n个线程),浏览器路径,浏览器驱动路径
默认配置如下:
[Settings]
  dow_path = .\\下载\\
  n = 100
  chrome_path = .\\Chrome-bin\\chrome.exe
  chromedriver_path = .\\Chrome-bin\\chromedriver.exe
