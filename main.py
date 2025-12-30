# backend.py
import sys
from PyQt5.QtCore import QObject, pyqtSlot, QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

class Backend(QObject):
    def __init__(self):
        super().__init__()

    @pyqtSlot(str)
    def printMessage(self, message):
        print(f"來自 QML 的訊息: {message}")

    @pyqtSlot(str)
    def handleInput(self, text):
        # 這是處理輸入框內容的函數
        print(f"後端接收到輸入內容: {text}")

    @pyqtSlot()
    def doSomething(self):
        print("Python 正在處理複雜的邏輯...")

def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # 1. 實體化後端
    backend = Backend()

    # 2. 將 Python 物件「注入」到 QML 的上下文（Context）中
    # 這樣在 QML 裡就能透過 "backend" 這個名字存取它
    engine.rootContext().setContextProperty("backend", backend)

    engine.load(QUrl.fromLocalFile("main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()