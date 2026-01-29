import uiautomator2 as u2
import time
from lxml import etree
import re

# 创建Dxpath类，封装一些操作安卓app的lxl元素的方法
class Dxpath:
    # 初始化安卓设备信息
    def __init__(self, d):
        self.d = d

# 定义一个通过参数返回app界面特定元素的方法
    def dxpath(self, arg):
        # 捕获当前屏幕的所有UI元素及其属性，并以XML的形式输出
        xml_content = self.d.dump_hierarchy()
        # 将字符串形式的 XML 数据解析成一个ElementTree对象
        root = etree.fromstring(xml_content.encode('utf-8'))
        return root.xpath(arg)

# 定义一个通过元素其他参数返回元素文本内容的方法
    def dxpath_text(self, t, arg, one=True, time_out=False):
        # t为dxpath迭代的对象
        # 定义文本参数的xpath格式
        args = '{}/@text'.format(arg)
        text = []
        # 将t对象中所有符合args规则的文本导入到列表中
        for txt in t.xpath(args):
            text.append(str(txt))
        # one/time_out的布尔值是根据所需要的内容来的：网名、数据内容或朋友圈日期
        if one:
            return text[0]
        elif time_out:
            return text[2]
        else:
            return text

    # 判断输入的xpath路径下是否有元素
    def dxpath_exist(self, t, arg):
        element = self.dxpath(arg)
        return len(element) > 0


# 创建一个类用来存储朋友圈的三个属性信息
class Item(object):
    name = None  # 更：网名
    comment = None  # 更：数据内容
    date = None  # 朋友圈日期


data_value = set()  # 记录已填入数据
items = []  # 数据汇总

# 正式开始，用u2库进行操作
phone_id = input("phone id:")
d = u2.connect(phone_id)
print(d.device_info)
mi = Dxpath(d)
# 打开微信app，等待界面加载完成
sess = d.app_start('com.tencent.mm', wait=True)  # start

d(resourceId="com.tencent.mm:id/icon_tv", text="发现").click()    # 点击‘发现’控件
d(resourceId="com.tencent.mm:id/m38").click()                    # 点击‘朋友圈’控件
d(resourceId="com.tencent.mm:id/n9a").exists()                   # 判断朋友圈界面是否存在
time.sleep(2)
# 刷新朋友圈
if d(resourceId="com.tencent.mm:id/ef").exists():
    d.double_click(0.522, 0.066)
d.swipe_ext('down', 3)
time.sleep(5)

match = False

while not match:
    # 循环每一个朋友圈个体内容
    for t in mi.dxpath('//*[@resource-id="com.tencent.mm:id/n9a"]'):
        try:
            # 分别找到该个体的网名、数据内容和朋友圈日期
            comment = mi.dxpath_text(t, './/*[@resource-id="com.tencent.mm:id/cut"]')
            name = mi.dxpath_text(t, './/*[@resource-id="com.tencent.mm:id/kbq"]')
            # 用weditor发现date的日期文本数据在text[2]中，所以更改对应布尔值
            date = mi.dxpath_text(t, './/*[@resource-id="com.tencent.mm:id/n93"]/', one=False, time_out=True)
            # 当日期数据为一天前内容时，停止循环
            match = re.search(r"天", date)
            # 确保数据不重复并且非朋友圈广告信息
            if comment not in data_value and not mi.dxpath_exist(t,'.//*[@resource-id="com.tencent.mm:id/egc"]'):  # 不能是广告
                print("抓取到{}朋友圈数据：\n{}\n时间为：{}".format(name, comment, date))
                item = Item()
                item.name = name
                item.comment = comment
                item.date = date
                items.append(item)
                data_value.add(comment)
                # 输出目前总共收集了多少天数据
                print('*' * 25 + str(len(data_value)))
        except:
            pass
    # 滑动
    d.swipe(300, 800, 300, 300, 0.1)

# 输出汇总数据
print(items)
