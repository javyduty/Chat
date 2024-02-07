import sys
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class ClientThread(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket

    def run(self):
        try:
            while True:
                message = self.client_socket.recv(1024).decode()
                self.message_received.emit(message)

        except Exception as e:
            print(f"Error receiving messages: {e}")

        finally:
            self.client_socket.close()

class ChatClientGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chat Client")
        self.setGeometry(100, 100, 400, 300)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)

        self.input_box = QLineEdit()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)

        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.text_area)
        central_layout.addWidget(self.input_box)
        central_layout.addWidget(self.send_button)
        central_widget.setLayout(central_layout)

        self.setCentralWidget(central_widget)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_thread = ClientThread(self.client_socket)
        self.client_thread.message_received.connect(self.update_text_area)

        self.start_client()

    def send_message(self):
        message = self.input_box.text()
        self.input_box.clear()
        self.client_socket.send(message.encode())

    def update_text_area(self, message):
        self.text_area.append(message)

    def start_client(self):
        username = input("Enter your username: ")
        self.client_socket.connect(('127.0.0.1', 5555))
        self.client_socket.send(username.encode())

        self.client_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client_gui = ChatClientGUI()
    client_gui.show()
    sys.exit(app.exec_())
