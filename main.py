# backend.py
import sys
from time import sleep, time
from PyQt5.QtCore import QObject, pyqtSlot, QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QMimeData, QVariant
from PyQt5.QtGui import QClipboard
class LazyMimeData(QMimeData):
    def __init__(self):
        super().__init__()
        # 宣告我們可以提供純文字格式
        self.setData("text/plain", b"") 
        self.activated = False
        # self.setData("x-kde-passwordManagerHint", b"secret")
        # self.setData("application/x-copyq-ignore", b"")

    def retrieveData(self, mime_type, preferred_type):
        """
        這是核心 Callback！
        當其他程式按下「貼上」時，作業系統會來問我們要資料。
        """
        if self.activated:
            print("內容已經產生過一次，直接回傳快取的資料。")
            return super().retrieveData(mime_type, preferred_type)
        print(f"retrieveData 被呼叫，mime_type: {mime_type}, preferred_type: {preferred_type}")
        if mime_type == "text/plain":
            print("偵測到貼上動作！正在即時生成內容...")
            sleep(1)  # 模擬耗時操作
            self.activated = True
            # 在這裡執行你的邏輯，例如讀取資料庫或處理字串
            # current time
            currentTime = time()
            generated_text = f"這是由 A 程式即時產生的內容 (Lazy Copy) time: {currentTime}"
            self.setData("text/plain", generated_text.encode('utf-8')) 
            # print(f"內容生成完成，傳回給系統剪貼簿。 generated_text: {generated_text}")
            return QVariant(generated_text)
        
        return super().retrieveData(mime_type, preferred_type)

class Backend(QObject):
    def __init__(self, clipboard: QClipboard ):
        super().__init__()
        self.clipboard = clipboard

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
        # 建立 Lazy 物件
        lazy_data = LazyMimeData()
        # 注意：在某些平台上，這需要保持程式 A 運行，否則剪貼簿會遺失
        print("AAAA")
        self.clipboard.setMimeData(lazy_data)

def main():
    app = QGuiApplication(sys.argv)
    clipboard = app.clipboard()

    print("已宣告剪貼簿擁有權。請到其他程式（如記事本）按下貼上。")
    engine = QQmlApplicationEngine()

    # 1. 實體化後端
    backend = Backend(clipboard)

    # 2. 將 Python 物件「注入」到 QML 的上下文（Context）中
    # 這樣在 QML 裡就能透過 "backend" 這個名字存取它
    engine.rootContext().setContextProperty("backend", backend)

    engine.load(QUrl.fromLocalFile("main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()