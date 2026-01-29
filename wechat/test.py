import psutil
from pywinauto.application import Application
from pywinauto import mouse
from pywinauto import keyboard
import requests
import time
import os
import json
import hashlib

PID = 0
for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict(attrs=['pid', 'name'])
    except psutil.NoSuchProcess:
        pass
    else:
        if 'WeChat.exe' == pinfo['name']:
            PID = pinfo['pid']
app = Application(backend='uia').connect(process=PID)
win = app['微信']

pengyouquan = win.child_window(title="朋友圈", control_type="Button")
cords = pengyouquan.rectangle()
mouse.click(button='left', coords=(cords.left + 10, cords.top + 10))
pyq_win = app["朋友圈"]


def makeDir():
    savePath = r"C:\wxScrapy"
    if not os.path.exists(savePath):
        os.mkdir(savePath)


# 获取单条朋友圈


def getItem():
    ppList = pyq_win.child_window(title="朋友圈", control_type="List")
    ppItemList = ppList.child_window(control_type="ListItem", ctrl_index=0)
    name = ppItemList.child_window(
        control_type="Button", ctrl_index=0).texts()[0]
    try:
        content = ppItemList.child_window(
            control_type="Text", ctrl_index=0).texts()[0]
        date = ppItemList.child_window(
            control_type="Text", ctrl_index=1).texts()[0]
    except:
        content = ''
        date = ppItemList.child_window(
            control_type="Text", ctrl_index=0).texts()[0]
    mediaList = []
    fileMd5 = ''
    hasMedia = ppItemList.child_window(control_type="Pane", ctrl_index=0).child_window(
        control_type="Pane", ctrl_index=0).child_window(control_type="Pane", ctrl_index=1)

    ad = hasMedia.child_window(control_type="Pane", ctrl_index=2).child_window(
        control_type="Button").exists()
    # 过滤视频号和链接
    if ad:
        print('视频号 或者 链接')
        print(name, content, date)
        return
    print(name, content)
    m = hasMedia.children()
    if len(m) >= 4:
        isVideo = hasMedia.child_window(control_type="Pane", ctrl_index=2).child_window(
            title="视频", control_type="Pane").exists()
        if isVideo:
            videoItem = hasMedia.child_window(control_type="Pane", ctrl_index=2).child_window(
                title="视频", control_type="Pane", ctrl_index=0)
            videoItem.click_input()
            fileName = getVideo(videoItem)
            if fileName == False:
                return
            fileMd5 = getFileMd5(fileName)
            media = uploadMedia(fileName, 'pic')
            mediaList.append(media)
        else:
            picList = hasMedia.child_window(
                control_type="Pane", ctrl_index=2).children()[0].children()
            for picItem in picList:
                picItem.click_input()
                fileName = getPic(picItem)
                if fileName == False:
                    return
                fileMd5 = getFileMd5(fileName)
                media = uploadMedia(fileName, 'video')
                mediaList.append(media)

    print(name, content, date, fileMd5, mediaList)
    # 上传服务接口，把抓取的内容上传到服务器
    url = "https://xxx/crawl/wx.json"
    data = {"name": name, "content": content,
            "media_list": mediaList, 'date': date, 'file_md5': fileMd5}
    headers = {'Content-type': 'application/json'}
    postRes = requests.post(url, headers=headers, json=data)
    print(data, postRes.json)


# 获取资源


def getPic(picItem):
    picItem.click_input()
    # cords = picItem.rectangle()
    # mouse.click(button='left', coords=(cords.left+10, cords.top+10))
    fileName = mediaDownload(1)
    return fileName


# 获取资源


def getVideo(videoItem):
    videoItem.click_input()
    # cords = videoItem.rectangle()
    # mouse.click(button='left', coords=(cords.left+10, cords.top+10))
    fileName = mediaDownload(2)
    return fileName


# 下载媒体文件


def mediaDownload(type):
    if type == 1:
        if app["图片查看"].exists() == False:
            return False
        mediaWin = app["图片查看"]
    else:
        if app["视频查看"].exists() == False:
            return False
        mediaWin = app["视频查看"]

    mediaWin.right_click_input()
    saveBtn = mediaWin.child_window(title="另存为...", found_index=0)
    saveBtn.wait('ready', timeout=5)
    saveBtn.click_input()

    # 保存到本地
    # saveasAppWindow.child_window(class_name='ToolbarWindow32', found_index=3).click_input()
    # keyboard.send_keys("C:\wxScrapy")
    # keyboard.send_keys("{VK_RETURN}")
    fileInput = mediaWin.child_window(title="文件名:", control_type="Edit")
    fileName = fileInput.get_value()

    mediaWin.child_window(class_name="Button",
                          title="保存(S)", found_index=0).click_input()
    if mediaWin.child_window(title="确认另存为").exists():
        mediaWin.child_window(title="确认另存为").child_window(
            control_type="Button", found_index=1).click_input()
    time.sleep(2)
    mediaWin.close()
    return fileName


# 上传媒体文件


def uploadMedia(fileName, type):
    # 上传到服务器
    url = "https://xxxx/common/upload.json"
    filePath = 'C:/wxScrapy/' + fileName

    payload = {}
    fileType = 'image/jpeg'
    if type == 'video':
        fileType = 'application/octet-stream'

    files = [
        ('upfile', (fileName, open(filePath, 'rb'), fileType))
    ]
    headers = {}
    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)
    uploadRes = response.json()
    if uploadRes['errno'] == 0:
        return uploadRes['data']
    return []


def getFileMd5(fileName):
    filePath = 'C:/wxScrapy/' + fileName
    fp = open(filePath, 'rb')
    content = fp.read()
    fp.close()
    return hashlib.md5(content).hexdigest()


def main():
    makeDir()
    pageNum = 1

    for i in range(50):
        pageNum += 1
        cords = pyq_win.child_window(
            title="朋友圈", control_type="List").rectangle()
        try:
            mouse.scroll(wheel_dist=-2, coords=(cords.left + 50, cords.top + 50))
            time.sleep(1)
            getItem()
        except:
            print('scroll faile')
            time.sleep(1)
        print('pageNum', pageNum)

    time.sleep(5)
    pyq_win.close()


if __name__ == "__main__":
    main()