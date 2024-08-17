import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
import os

os.system("taskkill /f /im pmsl.exe")
os.system("taskkill /f /im pmsl_kill.py")

class ServerThread(QThread):
    output_signal = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        self.process = subprocess.Popen(self.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in self.process.stdout:
            self.output_signal.emit(line)

    def send_command(self, command):
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()

class MinecraftServerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PMSL服务器管理器')

        layout = QVBoxLayout()

        # Java Path
        self.java_path_label = QLabel('目标Java:')
        self.java_path_entry = QLineEdit()
        layout.addWidget(self.java_path_label)
        layout.addWidget(self.java_path_entry)

        # Min Memory
        self.min_mem_label = QLabel('最小内存 (MB):')
        self.min_mem_entry = QLineEdit()
        layout.addWidget(self.min_mem_label)
        layout.addWidget(self.min_mem_entry)

        # Max Memory
        self.max_mem_label = QLabel('最大内存 (MB):')
        self.max_mem_entry = QLineEdit()
        layout.addWidget(self.max_mem_label)
        layout.addWidget(self.max_mem_entry)

        # JAR Path
        self.jar_path_label = QLabel('jar路径:')
        self.jar_path_entry = QLineEdit()
        layout.addWidget(self.jar_path_label)
        layout.addWidget(self.jar_path_entry)

        # Start Button
        self.start_button = QPushButton('启动服务器')
        self.start_button.clicked.connect(self.start_server)
        layout.addWidget(self.start_button)

        # Console Output
        self.console_text = QTextEdit()
        self.console_text.setReadOnly(True)
        layout.addWidget(self.console_text)

        # Command Input
        self.command_label = QLabel('命令:')
        self.command_entry = QLineEdit()
        self.send_command_button = QPushButton('发送命令')
        self.send_command_button.clicked.connect(self.send_command)
        layout.addWidget(self.command_label)
        layout.addWidget(self.command_entry)
        layout.addWidget(self.send_command_button)

        self.setLayout(layout)

        # 尝试获取 Java 路径
        self.check_java_path()

    def check_java_path(self):
        try:
            result = subprocess.run(['java', '-version'], capture_output=True, text=True, check=True)
            java_path = subprocess.run(['where', 'java'], capture_output=True, text=True, check=True).stdout.strip()
            self.java_path_entry.setText(java_path)
        except subprocess.CalledProcessError:
            QMessageBox.warning(self, "糟糕！未找到Java！", "Java可能还没有安装或者不存在环境变量中. 请输入java.exe的路径")

    def start_server(self):
        java_path = self.java_path_entry.text()
        min_mem = self.min_mem_entry.text()
        max_mem = self.max_mem_entry.text()
        jar_name = self.jar_path_entry.text()
        jar_path = os.path.join(os.getcwd(), jar_name)

        # 检查输入是否有效
        if not java_path or not jar_name:
            QMessageBox.warning(self, "输入错误", "请输入所有需要输入的地方.")
            return

        if not os.path.isfile(jar_path):
            QMessageBox.warning(self, "输入错误", f"目标jar路径 '{jar_path}' 不存在.")
            return

        command = [java_path]
        if min_mem:
            command.append(f"-Xms{min_mem}M")
        if max_mem:
            command.append(f"-Xmx{max_mem}M")
        command.extend(["-jar", jar_path , "nogui"])

        self.server_thread = ServerThread(command)
        self.server_thread.output_signal.connect(self.update_console)
        self.server_thread.start()

    def update_console(self, text):
        self.console_text.append(text)

    def send_command(self):
        command = self.command_entry.text()
        self.server_thread.send_command(command)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MinecraftServerGUI()
    gui.show()
    sys.exit(app.exec_())
