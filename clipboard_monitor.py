import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import os
import time
from urllib.parse import unquote

# 初始化 Gtk
Gtk.init(None)

def check_clipboard():
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    '''
    在剪貼簿的運作機制中，TARGETS 是一個標準的預定義名稱。

    當你獲得剪貼簿的擁有權後，別的程式（請求者）會先問你：「你有 TARGETS 嗎？」 如果你回答有，對方就會接著請求 TARGETS 的內容。這時你的程式必須回傳一個清單，告訴對方你支援的格式，例如：

    UTF8_STRING (純文字)

    image/png (圖片)

    text/html (網頁格式)
    '''
    target_atom = Gdk.Atom.intern("TARGETS", False)
    # 它的意思是：「請去詢問目前的剪貼簿擁有者，問他目前一共可以提供哪些資料格式，並把結果存到 targets 變數中。」
    targets = clipboard.wait_for_contents(target_atom)
    
    if targets is None:
        return True  # 剪貼簿空的，繼續等下一次檢查

    try:
        # import ipdb; ipdb.set_trace()
        success, atoms = targets.get_targets()
        if not success:
            return False
        target_list = [atom.name() for atom in atoms]
        print(f"\n[{time.strftime('%H:%M:%S')}] 目前剪貼簿支援的格式：{target_list}")
        
        # 只要字串裡出現 text/uri-list，就代表有檔案要傳
        if 'text/uri-list' in target_list:
            print(f"\n[{time.strftime('%H:%M:%S')}] 偵測到 VMware 檔案宣告！")
            
            # 這一步是關鍵：強迫 vmtoolsd 把檔案寫入 /tmp
            print("正在要求具體路徑 (觸發 Lazy Transfer)...")
            uri_text = clipboard.wait_for_text() 
            print("取得的 URI 列表：", uri_text)
            if uri_text:
                uris = uri_text.strip().split('\n')
                for uri in uris:
                    if uri.startswith('file://'):
                        clean_path = unquote(uri.replace('file://', '').strip())
                        if os.path.exists(clean_path):
                            print(f"✅ 檔案已落地：{clean_path}")
                            print(f"   大小：{os.path.getsize(clean_path)} bytes")
                        else:
                            print(f"⚠️ 路徑已獲取，但檔案尚未出現在 /tmp (或正在傳輸)")
    except Exception as e:
        print(f"解析過程發生錯誤: {e}")
    
    return True

print("====================================================")
print("   VMware Clipboard Monitor (Robust Version)")
print("====================================================")
print("請在 Windows 複製一個檔案，然後觀察這裡...")

GLib.timeout_add(500, check_clipboard)

try:
    Gtk.main()
except KeyboardInterrupt:
    print("\n監控已停止。")