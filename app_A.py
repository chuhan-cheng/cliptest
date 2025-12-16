import tkinter as tk

# 承諾要提供的 HTML 內容
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <title>Clip Test</title>
</head>
<body>
    <h1>這是 Python 程式 A 提供的 HTML 內容</h1>
    <p>這段內容以 text/html 格式被延遲渲染。</p>
    <ul>
        <li>由 app_A.py 擁有剪貼簿。</li>
    </ul>
</body>
</html>
"""

def provide_data(selection, requestor, format_name):
    """
    這個回調函數會在外部應用程式（B 程式）請求數據時被觸發。
    它實現了 X11 的延遲渲染機制。
    """
    print(f"--- 數據請求觸發！ ---")
    print(f"請求的選擇區: {selection}")
    print(f"請求的格式: {format_name}")
    
    # 這裡必須將數據編碼為 bytes
    if format_name == 'text/html':
        data = HTML_CONTENT.encode('utf-8')
    elif format_name == 'text/plain':
        # 為了相容性，通常也需要提供純文字版本
        data = "這是由 app_A 提供的 HTML 內容的純文字版本。".encode('utf-8')
    else:
        # 如果請求了其他格式，則無法提供
        print(f"無法提供格式: {format_name}")
        return

    # 將數據寫入 tkinter 內部緩衝區，準備傳輸給請求者
    # tkinter 會將這個數據通過 X11 的 Properties 機制傳輸給 B 程式
    root.clipboard_append(data.decode('utf-8'))
    print("數據已準備好並傳輸。")


# 1. 初始化 tkinter
root = tk.Tk()
root.withdraw() # 隱藏主視窗，因為我們只需要後台功能

try:
    # 2. 宣告擁有 CLIPBOARD 選擇區
    # `root.clipboard_clear()` 呼叫後會自動宣告 ownership
    root.clipboard_clear()

    # 3. 聲明可提供的數據格式（關鍵步驟）
    # 這裡告訴系統：「當有人請求 CLIPBOARD 數據時，我可以提供 'text/html' 和 'text/plain' 格式」
    # set_selection_owner 函數的內部會處理 X11 的 Atom 聲明
    root.clipboard_own_display(
        data_callback=provide_data,
        formats=('text/html', 'text/plain') 
        # 注意：在某些版本的 tkinter 或某些桌面環境中，
        # 實際可用的 MIME 類型可能需要使用 'HTML' 或特定於桌面環境的 Atom 名稱。
    )

    print("程式 A 運行中...")
    print("已成功聲明為 CLIPBOARD 擁有者，並承諾提供 'text/html' 格式。")
    print("請在另一個應用程式中按下 Ctrl+V 貼上。")
    print("--- 按下 Ctrl+C 或關閉視窗來釋放擁有權 ---")

    # 保持主循環運行，以便處理外部應用程式發來的 SelectionRequest
    root.mainloop()

except tk.TclError as e:
    print(f"發生錯誤: {e}")
    print("請確保您的環境中 tkinter 可以正常運行，並且沒有其他應用程式正在鎖定剪貼簿。")

finally:
    # 釋放資源
    root.destroy()
    print("程式 A 結束。")
