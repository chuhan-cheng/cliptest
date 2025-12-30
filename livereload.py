import sys
import os
from PyQt5.QtCore import QFileSystemWatcher, QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

class HotReloader:
    def __init__(self, qml_path):
        self.qml_path = qml_path
        self.engine = QQmlApplicationEngine()
        
        # 建立監控器
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(self.qml_path)
        self.watcher.fileChanged.connect(self.reload)
        
        # 第一次載入
        self.reload()

    def reload(self):
        print("\n--- 偵測到檔案變更，重新載入中 ---")
        
        # 1. 關閉並清理現有的根物件
        for obj in self.engine.rootObjects():
            obj.deleteLater()
        
        # 2. **核心關鍵**：清除組件快取
        # 如果不執行這行，Qt 會一直讀取舊的記憶體資料
        self.engine.clearComponentCache()
        
        # 3. 重新載入檔案
        self.engine.load(QUrl.fromLocalFile(self.qml_path))
        
        if not self.engine.rootObjects():
            print("錯誤：無法載入 QML，請檢查語法是否正確。")

def main():
    app = QGuiApplication(sys.argv)
    
    # 指定你的 QML 檔名
    reloader = HotReloader("main.qml")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()