from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import QWidget
import systemInfo
import pygame
import ctypes
import webbrowser

class FadeEffectWithLoop:
    # 初始化FadeEffectWithLoop类，设置窗口、控件和动画时长
    def __init__(self, win, widget, duration=3500):
        self.widget = widget
        self.win = win
        self.effect = QGraphicsOpacityEffect(widget)
        self.widget.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(duration)

    # 淡入效果
    def fade_in(self):
        loop = QEventLoop(self.win)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.finished.connect(loop.exit)
        self.animation.start()
        loop.exec()

    # 淡出效果
    def fade_out(self):
        loop = QEventLoop(self.win)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(loop.exit)
        self.animation.start()
        loop.exec()

class Loading(QWidget):
    """加载页面"""
    def __init__(self):
        super().__init__()
        #total layout
        self.Vlay = QVBoxLayout()
        #text
        self.text1 = QTextBrowser()
        #应用
        self.setLayout(self.Vlay) 

    def startText1(self):
        #size
        self.text1.setFontPointSize(20)
        #color
        palet = self.text1.palette()
        palet.setColor(QPalette.ColorRole.Text, QColor(Qt.GlobalColor.gray))
        self.text1.setPalette(palet)
        #layout
        self.Vlay.addWidget(self.text1)
        #移除边框和填充
        self.text1.setFrameStyle(QFrame.Shape.NoFrame | QFrame.Shadow.Plain)
        #content
            # 获取CPU信息
        cpuInfo = systemInfo.GetCpuConstants()
            # 获取内存信息
        memInfo = systemInfo.GetMemInfo()
            # 获取磁盘信息
        diskInfoRaw = systemInfo.GetDiskInfo()
            # 获取磁盘总大小
        diskInfo = diskInfoRaw[0]['size']['total']
        content = (f"// SYSTEM SELF-TEST\nCPU_NAME: {cpuInfo['cpu_name']}\nCPU_CORES: "
                f"{cpuInfo['cpu_core']}\nCPU_THREADS: {cpuInfo['cpu_threads']}\nMEMORY: {memInfo['memTotal']} MB\n"
                f"DISK: {diskInfo} B\n// COMPLETE.")
        
        #逐行显示
        #设置文本1
        textcpp1 = '''
//////////////////////////////////////////////
// copyright(C)A.K.A Hollow Deep Dive System
// Led by Helios Reserch Institute
// Author:BW
// deep_dive_prototype_v4.h
//////////////////////////////////////////////

#ifndef DEEP_DIVE_PROTOTYPE_V4_H
#define DEEP_DIVE_PROTOTYPE_V4_H
#include <MAP>
#include <helios_signal.h>
namespace Hollow
{
    class DeepDivePrototypeV4 : public DeepDiveBase:
    {
        private:
            HELIOS::BangbooHandle m_handle
            HChessboardMap<EHDomainType.EHSensorType> m_crossDomainSensorMap;
            HSensorContainer<VisualSensor> m_visualSensorContainer;
        public:
            virtual void RegisterBangbooHandle(HollowSignal signal) override;
            HCRESULI SyncVisualSensor(const HHatrics matWorld,HLINT hollowIndex);
    }
}
#endif // DEEP_DIVE_PROTOTYPE_V4_H
'''
        #设置文本2
        textcpp2 = '''
//////////////////////////////////////////////
// copyright(C)A.K.A Hollow Deep Dive System
// Led by Helios Reserch Institute
// Author:BW
//////////////////////////////////////////////

#include "deep_dive_prototype_v4.h"
#include "hollow_toolkit.h"
#include "hollow_boost.h"
namespace Hollow
{
    void DeepDivePrototypeV4::RegisterBangbooHandle(Hollowsignal signal)
    {
        if(m_initState != HollowInitState.HIS_DUCCESS)
            return;
        EHBoostType boostType = signal->GetBoostType();
        switch(boostType)
        {
            case EHBoostType.DEFAULT:
                m_handle = HELIOS::BangbooHandle.DEFAULT;
                break;
            case EHBoostType.ERROR:
                break;
        }
    }
}'''
        #显示系统自检
        self.textLineShow(content,600)
        #音乐
        player = ctypes.windll.kernel32
        player.Beep(3000, 500)    
        #清屏
        self.text1.clear()

        # 加载音乐文件
        pygame.mixer.music.load("Fairy.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        #显示源代码
        self.textLineShow(textcpp1,47)
        self.textLineShow(textcpp2,47) 
        #清屏
        self.text1.clear()

    def textLineShow(self, text_lines: str, time_ms: int = 1000):
        current_line = 0
        text_lines = text_lines.split("\n")

        # 创建定时器  
        timer = QTimer(self)

        # 定时器超时时的回调函数  
        loop = QEventLoop(self)

        def on_timeout():
            #声明current_line为nonlocal，以便在内部函数中修改  
            nonlocal current_line
            if current_line < len(text_lines):
                #追加文本并换行  
                self.text1.append(text_lines[current_line])
                current_line += 1
            else:
                #所有文本都已显示，停止定时器  
                timer.stop()
                loop.quit()

        # 连接定时器超时信号到回调函数  
        timer.timeout.connect(on_timeout)

        # 启动定时器  
        timer.start(time_ms)
        loop.exec()

    def startHDDIcon(self):
        # 创建一个Qlabel用于显示图片
        self.hdd = QLabel()
        # 加载图片到hdd
        self.hdd.setPixmap(QPixmap("H.D.D.png"))
        #移除原text
        self.Vlay.removeWidget(self.text1)
        #居中
        self.center_lay = QHBoxLayout()
        self.center_lay.addStretch()
        self.center_lay.addWidget(self.hdd)
        self.center_lay.addStretch()
        self.Vlay.addLayout(self.center_lay)
        #淡入淡出
        self.fade = FadeEffectWithLoop(self, self.hdd)
        self.fade.fade_in()
        #停顿1800ms
        loop = QEventLoop(self)
        QTimer.singleShot(1800, loop.quit)
        loop.exec()
        self.fade.fade_out()

class mainWindow(QWidget):
    """主页面"""
    def __init__(self):
        super().__init__()
        #content
        #label
        self.label = QLabel()
        #加载字体文件
        font_id1 = QFontDatabase.addApplicationFont("black.ttf")
        # 添加字体文件
        self.font_name1 = QFontDatabase.applicationFontFamilies(font_id1)[0]
        # 获取字体文件名
        font = QFont(self.font_name1, pointSize=18)
        # 设置字体
        self.setFont(font)
        self.label.setFont(QFont(self.font_name1, pointSize=130))
        #main layout
        self.Vlay = QVBoxLayout()
        #设置标签文本
        self.Hlay1 = QHBoxLayout()
        self.Hlay1.addStretch()
        self.Hlay1.addWidget(self.label)
        self.Hlay1.addStretch()
        self.Vlay.addLayout(self.Hlay1)
        self.Vlay.addStretch()
        #绳网按钮
        self.button_web = QPushButton("绳网")
        self.Hlay2 = QHBoxLayout()
        self.Hlay2.addStretch(stretch=1)
        self.Hlay2.addWidget(self.button_web, stretch=2)
        self.Hlay2.addStretch(stretch=1)
        self.Vlay.addLayout(self.Hlay2)
        self.Vlay.addStretch()
        self.button_web.setFont(font)
        self.button_web.setStyleSheet("QPushButton { min-height: 70px; }")
        #日程
        self.button_schedule = QPushButton("日程")
        self.Hlay3 = QHBoxLayout()
        self.Hlay3.addStretch(stretch=1)
        self.Hlay3.addWidget(self.button_schedule, stretch=2)
        self.Hlay3.addStretch(stretch=1)
        self.Vlay.addLayout(self.Hlay3)
        self.Vlay.addStretch()
        self.button_schedule.setFont(font)
        self.button_schedule.setStyleSheet("QPushButton { min-height: 70px; }")
        #关于
        self.button_about = QPushButton("关于")
        self.Hlay4 = QHBoxLayout()
        self.Hlay4.addStretch(stretch=1)
        self.Hlay4.addWidget(self.button_about, stretch=2)
        self.Hlay4.addStretch(stretch=1)
        self.Vlay.addLayout(self.Hlay4)
        self.Vlay.addStretch()
        self.button_about.setFont(font)
        self.button_about.setStyleSheet("QPushButton { min-height: 70px; }")
        #退出
        self.button_exit = QPushButton("退出")
        self.Hlay5 = QHBoxLayout()
        self.Hlay5.addStretch(stretch=4)
        self.Hlay5.addWidget(self.button_exit, stretch=6)
        self.Hlay5.addStretch(stretch=1)
        self.Vlay.addLayout(self.Hlay5)
        self.button_exit.setFont(font)
        self.button_exit.setStyleSheet("QPushButton { min-height: 70px; }")
        #禁用音乐
        self.check_music = QCheckBox("禁用音乐")
        self.Hlay5.addWidget(self.check_music,stretch=1)
        self.Hlay5.addStretch(stretch=4)
        self.check_music.setFont(font)
        self.check_music.setStyleSheet("QPushButton { min-height: 70px; }")

        #边框
        self.Vlay.setContentsMargins(10, 20, 10, 30)
        #应用
        self.setLayout(self.Vlay)
        
    def startLabel(self):
        # 加载音乐文件
        pygame.mixer.music.load("zzzExplorer.mp3")
        # 播放音乐，设置淡入时间为3000毫秒，循环播放
        pygame.mixer.music.play(fade_ms=3000, loops=-1)

        self.label.setText("欢_")
        loop = QEventLoop(self)
        QTimer.singleShot(300, loop.quit)
        loop.exec()
        self.label.setText("欢迎_")
        loop = QEventLoop(self)
        QTimer.singleShot(300, loop.quit)
        loop.exec()
        self.label.setText("欢迎,_")
        loop = QEventLoop(self)
        QTimer.singleShot(600, loop.quit)
        loop.exec()
        self.label.setText("欢迎,「_")
        loop = QEventLoop(self)
        QTimer.singleShot(300, loop.quit)
        loop.exec()
        self.label.setText("欢迎,「法_")
        loop = QEventLoop(self)
        QTimer.singleShot(300, loop.quit)
        loop.exec()
        self.label.setText("欢迎,「法厄_")
        loop = QEventLoop(self)
        QTimer.singleShot(300, loop.quit)
        loop.exec()
        self.label.setText("欢迎,「法厄同_")
        loop = QEventLoop(self)
        QTimer.singleShot(300, loop.quit)
        loop.exec()
        self.label.setText("欢迎,「法厄同」_")
        loop = QEventLoop(self)
        QTimer.singleShot(300, loop.quit)
        loop.exec()

class aboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        #layout
        self.Vlay = QVBoxLayout()
        #text
        self.text = QTextBrowser()
        #设置字体
        font_id1 = QFontDatabase.addApplicationFont("black.ttf")
        self.font_name1 = QFontDatabase.applicationFontFamilies(font_id1)[0]
        font = QFont(self.font_name1, pointSize=22) 
        self.text.setFont(font)
        s = """
作者:
bilibili:-liuhanjin-

用途:
西安中学研究性学习

版权:
开源项目,没有版权,随便使用

特别鸣谢:
bilibili:Pickup_拾柒(提供灵感来源和部分代码)
"""
        self.text.setText(s)
        self.Vlay.addWidget(self.text)
        #close button
        self.button_close = QPushButton("close")
        self.Hlay = QHBoxLayout()
        self.Hlay.addStretch(stretch=1)
        self.Hlay.addWidget(self.button_close, stretch=2)
        self.Hlay.addStretch(stretch=1)
        self.button_close.setFont(font)
        self.Vlay.addLayout(self.Hlay)
        #边框
        self.Vlay.setContentsMargins(400, 250, 400, 250)
        #应用
        self.setLayout(self.Vlay)

class scheduleWindow(QWidget):
    def __init__(self):
        super().__init__()
        #layout
        self.Vlay = QVBoxLayout()
        #text
        self.text = QPlainTextEdit()
        #载入文件
        content = ""
        with open("content.txt") as f:
            content = f.read()
        self.text.setPlainText(content)
        #设置字体
        font = QFont()
        font.setPointSize(22)
        self.text.setFont(font)
        self.Vlay.addWidget(self.text)
        #close button
        self.button_close = QPushButton("close")
        self.Hlay = QHBoxLayout()
        self.Hlay.addStretch(stretch=1)
        self.Hlay.addWidget(self.button_close, stretch=2)
        self.Hlay.addStretch(stretch=1)
        #设置字体
        font_id1 = QFontDatabase.addApplicationFont("black.ttf")
        self.font_name1 = QFontDatabase.applicationFontFamilies(font_id1)[0]
        font = QFont(self.font_name1, pointSize=22) 
        self.button_close.setFont(font)
        self.Vlay.addLayout(self.Hlay)
        #边框
        self.Vlay.setContentsMargins(100, 100, 100, 100)
        #应用
        self.setLayout(self.Vlay)

class Main(QMainWindow):
    """主控件"""
    def __init__(self):
        super().__init__()
        #禁用控件，防止鼠标交互
        self.setEnabled(False)
        #全屏
        self.showFullScreen()
        #title
        self.setWindowTitle("H.D.D")
        #icon
        icon = QIcon("Icon.ico")
        self.setWindowIcon(icon)
        #窗口黑色
        self.backgroundColor()
        #创建一个堆叠窗口
        self.win = QStackedWidget(self)
        # 设置窗口中央部件
        self.setCentralWidget(self.win)
        #系统自检
        self.load = Loading()
        self.win.addWidget(self.load)
        #主界面
        self.mainWin = mainWindow()
        self.win.addWidget(self.mainWin)
        #关于界面
        self.aboutWin = aboutWindow()
        self.win.addWidget(self.aboutWin)
        #日程界面
        self.scheduleWin = scheduleWindow()
        self.win.addWidget(self.scheduleWin)
        #开始自检
        self.win.setCurrentWidget(self.load)
        self.load.startText1()
        #显示图标
        #启用控件
        self.setEnabled(True)
        self.load.startHDDIcon()
        #显示主页面
        #background
        self.backgroundHDD()
        self.win.setCurrentWidget(self.mainWin)
        self.mainWin.startLabel()
        #信号检测
        self.mainWin.button_exit.clicked.connect(self.exit)
        self.mainWin.button_about.clicked.connect(self.about)
        self.mainWin.button_web.clicked.connect(self.web)
        self.mainWin.button_schedule.clicked.connect(self.schedule)
        self.aboutWin.button_close.clicked.connect(self.backMainWinow)
        self.scheduleWin.button_close.clicked.connect(self.backMainWinow)
        self.mainWin.check_music.clicked.connect(self.banMusic)

    def backgroundColor(self):
        palet = self.palette()
        palet.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0))
        self.setPalette(palet)

    def backgroundHDD(self):
        #背景图片
        self.background = QPixmap("bg.png")
        # 创建一个QBrush对象，使用QPixmap作为纹理
        brush = QBrush(self.background)
        # 设置窗口的背景色为透明
        palette = self.palette()
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)
        # 确保窗口背景不会随着窗口大小变化而改变
        self.setAttribute(Qt.WA_StaticContents)

    def about(self):
        self.fade = FadeEffectWithLoop(self,self.win,500)
        #执行淡出效果
        self.fade.fade_out()
        #将win设置为aboutWin界面
        self.win.setCurrentWidget(self.aboutWin)
        #执行淡入效果
        self.fade.fade_in()

    def schedule(self):
        self.fade = FadeEffectWithLoop(self,self.win,500)
        #执行淡出效果
        self.fade.fade_out()
        #将win设置为scheduleWin界面
        self.win.setCurrentWidget(self.scheduleWin)
        #执行淡入效果
        self.fade.fade_in()
        
    def web(self):
        webbrowser.open("https://www.bilibili.com/")

    def backMainWinow(self):
        self.fade = FadeEffectWithLoop(self,self.win,500)
        #执行淡出效果
        self.fade.fade_out()
        #将win设置为mainWin界面
        self.win.setCurrentWidget(self.mainWin)
        #执行淡入效果
        self.fade.fade_in()

    def banMusic(self):
        if self.mainWin.check_music.isChecked():
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.play(fade_ms=3000, loops=-1)

    def exit(self):
        #记录日程内容
        content = self.scheduleWin.text.toPlainText()
        with open("content.txt","w") as f:
            f.write(content)
        
        #退出程序
        app.exit()

app = QApplication([])

#初始化pygame的混音器
pygame.mixer.init()
#设置混音器的音量
pygame.mixer.music.set_volume(1)

window = Main()
window.show()

app.exec()