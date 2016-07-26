# CrawlerANJUKE

Dear All,

运行爬虫脚本需要以下几个步骤，我尽量写明白些，大家有不清楚的可以回复邮件或者微信我。

1. 安装python解释器，网址：https://www.python.org/downloads/
选择“Download Python 3.5.2”
下载完毕后安装在默认路径，安装过程中的选项都选择默认即可，安装完成后重启电脑。

2. 下载爬虫脚本（已经上传在teambition上）：“CrawlerANJUKE”，解压在C盘根目录下（WINDOWS），MAC系统解压在桌面

3. 修改爬虫的目标城市
使用文本工具打开CrawlerANJUKE\CrawlerApplication.py，找到以下字段
untitled6.png

CITY和CITY_NAME是相对应的，小火箭爬烟台市的，因此对应的fangchenggang改为yantai，防城港市改为烟台市，莫文蔚爬德州市，对应的fangchenggang改为dezhou，防城港市改为德州市。段韵有空爬下潍坊市的，相应改为weifang，潍坊市。
保存，退出。

4. 运行脚本。
运行方法：
(1) 进入脚本目录
MAC：打开终端工具（Terminal），输入： cd Desktop/CrawlerANJUKE
Windows： 按住ctrl＋r，然后输入cmd，出现命令行界面之后输入： cd C:\CrawlerANJUKE

(2) 安装依赖库
MAC: 在终端下输入: python get-pip.py 
安装完后输入: pip install lxml
安装完后输入: pip install bs4

windows 参考下方NOTE

(3) 运行脚本
在终端输入： python3 CrawlerApplication.py
看到“Start.....” 的信息后，脚本即已经开始执行，如下图     

untitled1.png


5. 脚本运行完毕后会显示Success！ 数据存储在CrawlerANJUKE\Data\目录下
运行会比较久，因为网站有防爬机制，一分钟只能爬6个小区。

NOTE：
＊一定把电脑的休眠取消掉，不然休眠后电脑是不联网的。

＊如果运行脚本失败，显示没有安装BS4或者LXML可以参考安装以下文件：

BS4:     http://www.pythonlibrary.org/data/VS2003/BeautifulSoup-3.0.5.win32.exe

LXML：https://pypi.python.org/packages/18/c0/ce50496ce5dc131d0303d95ab64d3f230d9ffe329a287951cc9829e74b9e/lxml-2.3.win32-py3.2.exe#md5=d20af7a1a2b47433fbbc549ee5b635f4



祝大家一切顺利！