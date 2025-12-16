import tkinter as tk

def get_html_from_clipboard():
    root = tk.Tk()
    root.withdraw()

    try:
        # 嘗試從 CLIPBOARD 選擇區獲取 'text/html' 格式的數據
        # get_clipboard() 內部會向擁有者（app_A）發送 SelectionRequest
        
        # 注意：這裡使用 'text/html' 作為格式名
        html_data = root.clipboard_get(type='text/html')
        
        print("--- 程式 B 請求結果 ---")
        print("成功取得數據！")
        print("數據格式: text/html")
        print("--- 內容片段 ---")
        print(html_data[:200] + "...") # 顯示前 200 個字符
        
        if "<h1>" in html_data:
            print("\n✔️ 驗證成功：內容包含 HTML 標籤。")
        else:
            print("\n❌ 驗證失敗：貼上內容似乎不是 HTML。")

    except tk.TclError as e:
        print("--- 程式 B 請求結果 ---")
        print(f"錯誤：無法取得 'text/html' 剪貼簿數據。")
        print(f"原因可能為：{e}")
        print("請確保程式 A 正在運行，並且剪貼簿中沒有其他內容覆蓋。")
    
    root.destroy()

if __name__ == "__main__":
    get_html_from_clipboard()
