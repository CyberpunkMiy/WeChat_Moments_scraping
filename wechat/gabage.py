import uiautomator2 as u2
import time
from lxml import etree
from PIL import Image
import re


class Dxpath:
    def __init__(self, d):
        self.d = d

    def dxpath(self, arg):
        # 通过xpath获得etree.module，可以继续使用xpath定位，适用于从某一区域继续检索
        xml_content = self.d.dump_hierarchy()
        root = etree.fromstring(xml_content.encode('utf-8'))
        return root.xpath(arg)


    def center(self, arg, t=None):
            bounds = '{}/@bounds'.format(arg)
            try:
                if t is not None:
                    coord = str(t.xpath(bounds)[0])
                else:
                    coord = str(self.dxpath(bounds)[0])
                lx, ly, rx, ry = map(int, re.findall(r"\d+", coord))
                return lx, ly, rx, ry
            except:
                raise Exception("未找到控件")

    def click(self, arg, timeout=10, at_once=False, set_x=0, set_y=0,
              picture=False, picture_name='crop', t=None):
        # char代表识别的字符串，timeout为响应时间,at_once为只判别一次,repetition代表重复点击次数
        # ,set_x代表x坐标调整,picture是保存图像,picture_name为保存图片名, #t为dxpath迭代的对象
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                lx, ly, rx, ry = self.center(arg, t)
                x, y = (lx + rx) // 2, (ly + ry) // 2
                x = set_x + x
                y = set_y + y
                self.d.click(x, y)
                if picture:
                    catIm = Image.open('screenshot.jpg')
                    croppedIm = catIm.crop((lx + set_x, ly + set_y,
                                            lx + set_x + rx, ly + set_y + ry))
                    croppedIm.save('%s.jpg' % picture_name)
                return x, y
            except:
                if at_once:
                    raise Exception("未找到控件")
                else:
                    time.sleep(0.1)
        raise Exception("未找到控件")

    def dxpath_text(self, t, arg, one=True, time_out=False):
        # t为dxpath迭代的对象
        # for t in dxpath('')
        args = '{}/@text'.format(arg)
        text = []
        for txt in t.xpath(args):
            text.append(str(txt))
        if one:
            return text[0]
        elif time_out:
            return text[2]
        else:
            return text

    def dxpath_exist(self, t, arg):
        # 通过xpath获得etree.module，可以继续使用xpath定位，适用于从某一区域继续检索
        # xml_content = self.d.dump_hierarchy()
        # root = etree.fromstring(xml_content.encode('utf-8'))
        element = self.dxpath(arg)
        return len(element) > 0

class Item(object):
    name = None  # 更：网名
    comment = None  # 更：数据内容
    date = None  # 朋友圈日期

data_value = set()  # 纪录已填入数据
items = []  # 数据汇总

# 正式开始
phone_id = input("phone id:")
d = u2.connect(phone_id)
print(d.device_info)
mi = Dxpath(d)
sess = d.app_start('com.tencent.mm', wait=True)  # start

d(resourceId="com.tencent.mm:id/icon_tv", text="发现").click()
d(resourceId="com.tencent.mm:id/m38").click()
d(resourceId="com.tencent.mm:id/n9a").exists()
time.sleep(2)
if d(resourceId="com.tencent.mm:id/ef").exists():
    d.double_click(0.522, 0.066)

d.swipe_ext('down', 3)
time.sleep(5)

match = False

while not match:
    for t in mi.dxpath('//*[@resource-id="com.tencent.mm:id/n9a"]'):
        try:
            comment = mi.dxpath_text(t, './/*[@resource-id="com.tencent.mm:id/cut"]')
            name = mi.dxpath_text(t, './/*[@resource-id="com.tencent.mm:id/kbq"]')
            date = mi.dxpath_text(t, './/*[@resource-id="com.tencent.mm:id/n93"]/', one=False, time_out=True)
            match = re.search(r"天", date)
            if comment not in data_value and not mi.dxpath_exist(t,
                                                                 './/*[@resource-id="com.tencent.mm:id/egc"]'):  # 不能是广告
                print("抓取到{}朋友圈数据：\n{}\n时间为：{}".format(name, comment, date))
                item = Item()
                item.name = name
                item.comment = comment
                item.date = date
                items.append(item)
                data_value.add(comment)
                print('*' * 25 + str(len(data_value)))
        except:
            pass
        # 滑动
    d.swipe(300, 800, 300, 300, 0.1)

print(items)