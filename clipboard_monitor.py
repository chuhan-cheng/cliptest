import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import os
import time
from urllib.parse import unquote

# 初始化 Gtk
Gtk.init(None)

def get_atom_name(atom):
    """
    穩健地取得 Atom 的名稱字串
    """
    try:
        # 嘗試使用 .name() 方法
        if hasattr(atom, 'name'):
            return atom.name()
        # 嘗試使用 Gdk 提供的靜態轉換方法
        return Gdk.Atom.to_string(atom)
    except:
        return str(atom)

def check_clipboard():
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    target_atom = Gdk.Atom.intern("TARGETS", False)
    targets = clipboard.wait_for_contents(target_atom)
    
    # 這裡放你的斷點
    # import ipdb; ipdb.set_trace()

    if targets is not None:
        try:
            # import ipdb; ipdb.set_trace()
            raw_targets = targets.get_targets()
            # 將整個回傳值轉成一個大字串，不管它是列表還是物件
            all_targets_str = str(raw_targets)
            
            # 只要字串裡出現 text/uri-list，就代表有檔案要傳
            if 'text/uri-list' in all_targets_str:
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