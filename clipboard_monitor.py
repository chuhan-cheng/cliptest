import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

def monitor_clipboard():
    # 取得系統剪貼簿
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    
    print("=== 正在監控剪貼簿，請在 Windows 複製檔案後觀察 Linux 端 ===")

    def callback(cb, selection_data):
        # 取得目前剪貼簿宣告的所有格式 (Targets)
        # 檔案複製通常會顯示為 'text/uri-list'
        targets = cb.wait_for_contents("TARGETS")
        if targets:
            print(f"\n[偵測到新宣告] 擁有者提供的格式包含: {targets.get_targets()}")
        
        # 嘗試讀取檔案路徑 (URI List)
        # 注意：在 VMware 中，這通常會在「貼上」動作發生時才動態生成路徑
        text_data = cb.wait_for_text()
        if text_data:
            print(f"[內容細節]: {text_data}")
        else:
            print("[訊息]: 目前剪貼簿內沒有文字或路徑資訊（可能尚未觸發傳輸）")

    # 監控剪貼簿內容變更
    clipboard.connect("owner-change", callback)
    Gtk.main()

if __name__ == "__main__":
    monitor_clipboard()
