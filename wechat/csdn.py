import uiautomator2 as u2
import time

phone_id = input("phone id:")
d = u2.connect(phone_id)
print(d.device_info)

# # 打开微信app，等待界面加载完成
# sess = d.app_start('com.tencent.mm', wait=True)  # start
#
# d(resourceId="com.tencent.mm:id/icon_tv", text="发现").click()    # 点击‘发现’控件
# d(resourceId="com.tencent.mm:id/m38").click()                    # 点击‘朋友圈’控件
# d(resourceId="com.tencent.mm:id/n9a").exists()                   # 判断朋友圈界面是否存在
#
# # 刷新朋友圈
# if d(resourceId="com.tencent.mm:id/ef").exists():
#     d.double_click(0.522, 0.066)
while True:
    d.swipe_ext('down', 3)
    time.sleep(5)