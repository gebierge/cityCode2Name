# cityCode2Name
* 从国家统计局官网爬某个城市以下的所有地区，并保存数据到本地
* py文件为python代码
* code.txt文件为python文件运行后保存的本地代码;log.txt文件为运行的log
* 如果不需要看log,可以把saveLog赋值为False
* 如果你想跳过某些城市及以下城市，可以将该城市的城市编码添加到code_blacklist字典中
* 如果自己要爬某个地区，只需改为官网上进入该区的页面url赋值给fcurl,连接url赋值给ftourl
```
  例如：需要爬http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/65/6532.html 这个连接及以下的数据。
  方法一：可以前往进入该链接的上一页，上一页的页面url赋值给fcurl，即fcurl = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/65.html' ，进入该页面的href赋值给ftourl,即ftourl = '65/6532.html' 。
  方法二：直接将当前页面赋值给fcurl，即 fcurl = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/65/6532.html' ，tourl赋值空字符串，即tourl = ''。
``` 
  
