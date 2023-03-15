import subprocess
import re
import os

# 获取文件地址的方法，可以不用单独提取成一个方法的，但是设计之初发现是需要多次调用，从而提取成一个方法。后续已经优化了，不用重复调用，所以可以将其添加到主要方法getoldfilepath（）下
def filepath():
    # 一个简单的输入方法，进行灵活获取文件目录
    path = input("filepaht:")
    return path

# 使用subprocess.Popen进行对电脑的控制台进行输入以及记录控制台反馈的内容，方便后期查看日志。
def ffmpeg(path):
    # 拼接ffmpeg执行语句
    ffmpeg = "ffmpeg -i "+ path
    # 调用subprocess.Popen方法，进行控制台操作。后面几个stdin，stderr暂时还不清楚是什么作用，从网络上抄来的
    ffmper = subprocess.Popen(ffmpeg, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    # 大致理解是用来获取控制面板返回的信息的，但是stderr暂时还不清楚是什么意思
    log = ffmper.stderr.read()
    print(log)
    return log

# 通过正则来获取我们想要的数据信息方法
# 这部分因为要获取四个重要信息，所以就直接复制了四个模块，分别是编码格式，码率，帧数，分辨率。因为里面只需要改动一小部分正则语法和部分参数，所以复制是最快的方式就没有进行优化
def data(log):
    # res_bianma 表示用来获取编码的正则语句
    res_bianma = r'Video\:\s\w*'
    # 通过re.search来进行筛选
    bianmadata = re.search(res_bianma,log)
    # 加一步判断,判断这个是否是None的,不是则按照下面方法进行输出我们想要的内容.如果不是的话就输出null
    if bianmadata != None:
        start = bianmadata.start()
        end = bianmadata.end()
        bianma = log[start:end][7:]
    else:
        bianma = 'null'

    # 码率部分
    res_bit = r'bitrate\:\s\w*'
    bitdata = re.search(res_bit,log)
    if bitdata != None:
        start = bitdata.start()
        end = bitdata.end()
        bitrate = log[start:end][9:]+'kbps'
    else:
        bitrate = 'null'

    # 帧数部分
    res_fps = r'[1-9]\d*.\d*\sfps|0\.\d*[1-9]\d*\sfps|\d*\sfps'
    fpsdata = re.search(res_fps,log)
    if fpsdata != None:
        start = fpsdata.start()
        end = fpsdata.end()
        fps = log[start:end]
        longfps = re.search('\d*\.',fps)
        # 如果是整数，则重新使用正则获取信息，再使用切片整理格式
        if longfps ==  None:
            fps1 = fps[:len(fps)-4]
            fps=fps1+'fps'
        # 取浮点的整数部分
        else:
            start = longfps.start()
            end  = longfps.end()
            fps2 = fps[start:end][:len(fps[start:end])-1]
            fps = fps2+'fps'
    else:
        fps = 'null'

    # 分辨率部分
    res_fenbianlv = r'\s\d*x\d*\s|\s[1-9]\d*x[1-9]\d*\,'
    fenbianlvdata = re.search(res_fenbianlv,log)
    if fenbianlvdata != None:
        start = fenbianlvdata.start()
        end = fenbianlvdata.end()
        a = len(log[start:end])-1
        fenbianlv = log[start:end][1:a]
    else:
        fenbianlv = 'null'
    # 最后进行组合成一个我们想要的内容:1920x1080_500kbps_30fps_hevc
    return fenbianlv + "_" + bitrate + "_" + fps + "_" + bianma

#主要方法！
def getoldfilepath():
    #地址调用filepath（）方法进行获取文件夹地址
    path = filepath()
    #使用os.listdir方法，将文件夹下的全部文件名称传递给filelist。使用的是列表储存
    filelist  = os.listdir(path)
    # 通过for对fileliest（文件名称列表）进行遍历
    for i in filelist:
        #获取到地址后，将地址和文件名称进行组合，生成文件的绝对地址oldfilepath
        oldfilepath = path + "/" + i
        #然后使用正则进行提取文件的后缀。（后续可以适配大多数文件的读取和名称修改，暂不支持m3u8格式。）
        houzhui = re.search('\.\w*',oldfilepath)
        # 通过判断使用re.start和re.end方法进行提取我们获取到的内容信息
        if houzhui != None:
            start = houzhui.start()
            end = houzhui.end()
            # 使用data方法进行获取视频内容信息，并且data方法返回的是我们目标文件名称的一个文案，然后通过字符串运算进行拼接;oldfilepath[start:end]这个是文件的后缀.mp4
            newfilepath = path + "/" + data(ffmpeg(oldfilepath)) + oldfilepath[start:end]
            # 使用os.rename方法进行对文件名的修改。
            os.rename(oldfilepath, newfilepath)


if __name__ == "__main__":
    print(getoldfilepath())
