import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PMSL")
        self.setGeometry(100, 100, 400, 200)  # 设置窗口大小和位置

        # 创建两个按钮
        button1 = QPushButton("打开 pmsl.exe \n Open pmsl.exe", self)
        button1.setGeometry(50, 50, 150, 30)
        button1.clicked.connect(self.open_pmsl_exe)

        button2 = QPushButton("打开 pmslcn.exe \n Open pmslcn.exe", self)
        button2.setGeometry(50, 100, 150, 30)
        button2.clicked.connect(self.open_pmslcn_exe)

    def open_pmsl_exe(self):
        # 在这里添加打开 pmsl.exe 的代码
        os.system("pmsl.exe")
        os.system("taskkill /f /im cmd.exe")
        #pass

    def open_pmslcn_exe(self):
        # 在这里添加打开 pmslcn.exe 的代码
        os.system("pmslcn.exe")
        os.system("taskkill /f /im cmd.exe")
       # pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
