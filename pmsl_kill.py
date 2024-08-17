import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
import os

os.system("taskkill /f /im pmslcn.exe")
os.system("taskkill /f /im pmslcn_kill.py")

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
        self.setWindowTitle('Minecraft Server Manager')

        layout = QVBoxLayout()

        # Java Path
        self.java_path_label = QLabel('Java Path:')
        self.java_path_entry = QLineEdit()
        layout.addWidget(self.java_path_label)
        layout.addWidget(self.java_path_entry)

        # Min Memory
        self.min_mem_label = QLabel('Min Memory (MB):')
        self.min_mem_entry = QLineEdit()
        layout.addWidget(self.min_mem_label)
        layout.addWidget(self.min_mem_entry)

        # Max Memory
        self.max_mem_label = QLabel('Max Memory (MB):')
        self.max_mem_entry = QLineEdit()
        layout.addWidget(self.max_mem_label)
        layout.addWidget(self.max_mem_entry)

        # JAR Path
        self.jar_path_label = QLabel('JAR Path:')
        self.jar_path_entry = QLineEdit()
        layout.addWidget(self.jar_path_label)
        layout.addWidget(self.jar_path_entry)

        # Start Button
        self.start_button = QPushButton('Start Server')
        self.start_button.clicked.connect(self.start_server)
        layout.addWidget(self.start_button)

        # Console Output
        self.console_text = QTextEdit()
        self.console_text.setReadOnly(True)
        layout.addWidget(self.console_text)

        # Command Input
        self.command_label = QLabel('Command:')
        self.command_entry = QLineEdit()
        self.send_command_button = QPushButton('Send Command')
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
            QMessageBox.warning(self, "Java Not Found", "Java is not installed or not found in PATH. Please enter the Java path manually.")

    def start_server(self):
        java_path = self.java_path_entry.text()
        min_mem = self.min_mem_entry.text()
        max_mem = self.max_mem_entry.text()
        jar_name = self.jar_path_entry.text()
        jar_path = os.path.join(os.getcwd(), jar_name)

        # 检查输入是否有效
        if not java_path or not jar_name:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        if not os.path.isfile(jar_path):
            QMessageBox.warning(self, "File Error", f"The JAR file '{jar_path}' does not exist.")
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
