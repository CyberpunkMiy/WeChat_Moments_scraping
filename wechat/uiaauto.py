import time

import uiautomator2 as u2

device = u2.connect("f6fb7c04")


print(device.device_info)
print(device.window_size())
# device.screenshot('test.png')
# device.press('camera')
# device.press('volume_mute')
# device.press('recent')
# device.press('power')


# device.  'package': 'com.ss.android.ugc.aweme', 'activity': '.splash.SplashActivity', 'pid': 18056
# device.app_start('com.ss.android.ugc.aweme')
# device.app_start('com.xingin.xhs')
device.app_start('com.tencent.mm', wait=True)
# device(text='我').click()

device(resourceId="com.tencent.mm:id/icon_tv", text="发现").click()
device(resourceId="com.tencent.mm:id/m38").click()

device.wait_activity()

# content = device(resourceId="com.tencent.mm:id/cut").info
screen = device(resourceId="com.tencent.mm:id/hbs")
body = screen.child(resourceId="com.tencent.mm:id/n9a")
body_next = body.child(className="android.widget.RelativeLayout")
body_next2 = body_next.child(resourceId="com.tencent.mm:id/n95")
body_next3 = body_next2.child(className="android.view.ViewGroup")
name = body_next3.child(resourceId="com.tencent.mm:id/kbq").info
text = body_next3.child(resourceId="com.tencent.mm:id/cut").info
image = body_next3.child(resourceId="com.tencent.mm:id/n96").info



# d.xpath('//*[@resource-id="com.tencent.mm:id/hbs"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]')
# d.xpath('//*[@resource-id="com.tencent.mm:id/hbs"]/android.widget.LinearLayout[2]/android.widget.RelativeLayout[1]')
print(name)
print(text)
print(image)
# print(device.app_current())
# time.sleep(10)
# device.app_stop('com.tencent.mm')


# d.xpath('//*[@resource-id="com.tencent.mm:id/hbs"]/android.widget.LinearLayout[1]')
# device.xpath('//*[@resource-id="com.tencent.mm:id/hbs"]/android.widget.LinearLayout')

# device.swipe(0.5,0.9,0.5,0.1)
# pyq = device(className='android.widget.RelativeLayout')
# pyq.swipe('up', steps=1000)
while True:
    device.swipe_ext('up', scale=0.9)
    time.sleep(2)

