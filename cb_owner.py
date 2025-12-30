import subprocess
import os
import json
import time

# 要提供的檔案路徑
file_paths = ["/tmp/test1.txt", "/tmp/test2.txt"]
for p in file_paths:
    if not os.path.exists(p):
        raise FileNotFoundError(f"{p} 不存在")

# CopyQ command 名稱
ITEM_LABEL = "Lazy File Clipboard"

# 1️⃣ 建立 CopyQ item，先宣告存在，但不放資料
# 使用 JSON metadata 記錄原始檔案路徑
metadata = json.dumps({"paths": file_paths})
subprocess.run([
    "copyq", "add", "", "--note", metadata, "--label", ITEM_LABEL
])

print("Lazy clipboard item 已放入 CopyQ (無資料)")

# 2️⃣ 設定 hook：貼上時觸發 lazy 製作內容
# 這裡用 Python 直接輪詢監控 item（簡單版）
def lazy_populate_clipboard():
    """檢查 CopyQ item 是否空，如果空就生成資料"""
    # 取得 item 列表
    result = subprocess.run(
        ["copyq", "read", "0", "--json"], capture_output=True, text=True
    )
    try:
        item = json.loads(result.stdout)
    except Exception:
        return

    content, note, label = item.get("content", ""), item.get("note", ""), item.get("label", "")
    if label != ITEM_LABEL:
        return
    if content.strip() != "":
        return  # 已經生成過

    # 生成 URI 內容
    uris = "\r\n".join(f"file://{p}" for p in file_paths) + "\r\n"
    gnome_text = "copy\n" + "\n".join(file_paths) + "\n"

    # 更新 CopyQ item 的 content
    subprocess.run([
        "copyq", "write", "0", uris,
        "--mime", "text/uri-list"
    ])
    subprocess.run([
        "copyq", "write", "0", gnome_text,
        "--mime", "x-special/gnome-copied-files"
    ])
    print("Lazy clipboard item 現在生成了實際內容")

print("程式等待貼上，貼上時會生成內容...")
try:
    while True:
        lazy_populate_clipboard()
        time.sleep(0.5)
except KeyboardInterrupt:
    print("程式結束")
