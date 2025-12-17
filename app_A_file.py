import tkinter as tk

# 虛擬檔案路徑（必須是絕對路徑，並使用 URI 格式）
# 假設要複製兩個檔案：
VIRTUAL_FILES = [
    "/home/user/Documents/report_2025.pdf",
    "/home/user/Pictures/vacation_photo.jpg"
]

def format_as_uri_list(files):
    """
    將本機檔案路徑轉換為 text/uri-list 格式所需的 URI 列表字串。
    每個 URI 必須以 CRLF (\r\n) 結尾。
    """
    uri_list = []
    for file_path in files:
        # 將標準路徑轉換為 file:///URI 格式
        uri = "file://" + file_path.replace("\\", "/") 
        uri_list.append(uri)
    
    # 組合並以 CRLF 分隔
    return "\r\n".join(uri_list) + "\r\n"

# 準備要傳輸的 text/uri-list 數據
URI_LIST_CONTENT = format_as_uri_list(VIRTUAL_FILES)

def provide_data(selection, requestor, format_name):
    """
    延遲渲染回調函數，提供 text/uri-list 格式的數據。
    """
    print(f"--- 檔案數據請求觸發！ ---")
    print(f"請求的格式: {format_name}")
    
    if format_name == 'text/uri-list':
        # 傳輸 URI 列表字串
        data = URI_LIST_CONTENT
        print(f"提供的 URI 列表:\n{data.strip()}")
        
    elif format_name == 'TEXT' or format_name == 'text/plain':
        # 作為降級選項，提供 URI 列表的純文字版本
        data = URI_LIST_CONTENT.replace("\r\n", "\n")
        
    else:
        print(f"無法提供格式: {format_name}")
        return

    # 將數據寫入 tkinter 內部緩衝區，準備傳輸給請求者
    # 注意：雖然是 URI 列表，tkinter 仍接受字串形式
    root.clipboard_append(data)
    print("數據已準備好並傳輸。")


# 1. 初始化 tkinter
root = tk.Tk()
root.withdraw() # 隱藏主視窗

try:
    root.clipboard_clear()

    # 2. 聲明可提供的數據格式
    # 這裡的關鍵是使用 'text/uri-list'
    root.clipboard_own_display(
        data_callback=provide_data,
        formats=('text/uri-list', 'text/plain')
    )

    print("程式 A 運行中...")
    print(f"已聲明為 CLIPBOARD 擁有者，並承諾提供 'text/uri-list' 檔案清單。")
    print("請嘗試在檔案總管（如 Nautilus/Dolphin）中按下 Ctrl+V 貼上。")
    print("--- 按下 Ctrl+C 或關閉視窗來釋放擁有權 ---")

    # 保持主循環運行
    root.mainloop()

except tk.TclError as e:
    print(f"發生錯誤: {e}")

finally:
    root.destroy()
    print("程式 A 結束。")
