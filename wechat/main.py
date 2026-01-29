import psutil  # 用于获取微信电脑版的进程信息；
import pywinauto  # 用于自动化控制微信电脑版
from pywinauto.application import Application
from pywinauto.mouse import click
import sys
import time

if __name__ == '__main__':
    PID = 0  # 用来保存微信的进程号

    for proc in psutil.process_iter():  # 循环电脑上的进程，获取进程号和名称
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:  # 没有运行微信程序
            pass
        else:
            if 'WeChat.exe' == pinfo['name']:  # 当进程名为WeChat.exe的时候，把进程号记下来
                PID = pinfo['pid']

    # 进程ID用来提供给 PyWinAuto.application 以连接微信电脑版，connect是要已经运行微信才行
    app = Application(backend='uia').connect(process=PID)
    # 获得微信窗口实例
    Win_wechat = app['微信']
    # win.print_control_identifiers()#以树形方式打印窗口上所有控件

    # 获取微信窗口上朋友圈按钮实例
    Button_pyq = Win_wechat['Pane6'].child_window(title="朋友圈", control_type="0xC358")
    # 获取按钮坐标
    cords = Button_pyq.rectangle()
    # 接着控制微信电脑版，把朋友圈窗口打开
    pywinauto.mouse.click(button='left', coords=(cords.left + 10, cords.top + 10))

    Win_pyq = app['朋友圈']  # 获取朋友圈窗口实例

    Win_pyq.draw_outline(colour='red', thickness=2)  # 在当前定位到的窗口围画出一条边界线，方便我们看出定位到了哪个控件
    Win_pyq.dump_tree()  # 树形打印