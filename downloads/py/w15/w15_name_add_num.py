# 讀取完整名單與出席人員名單，輸出學號與姓名（以 tab 分隔）

def read_full_list(filename):
    """
    讀取完整名單檔案，建立一個字典（dict），
    以姓名為鍵（key），學號為值（value）方便後續查找。
    參數:
        filename: str, 完整名單檔案名稱（如 '2b.txt'）
    回傳:
        dict，key為姓名，value為學號
    """
    d = {}
    with open(filename, encoding='utf-8') as f:               # 以utf-8編碼開啟檔案
        for line in f:                                        # 逐行讀取
            line = line.strip()                               # 去掉每行首尾的空白和換行
            if not line or line.startswith('學號'):           # 跳過空行或標題行
                continue
            parts = line.split('\t')                          # 以tab分割欄位
            if len(parts) >= 2:                               # 確保有學號和姓名欄位
                student_id, name = parts[0], parts[1]         # 取得學號與姓名
                d[name] = student_id                          # 以姓名為key, 學號為value存入字典
    return d

def read_name_list(filename):
    """
    讀取只有姓名的檔案，將每個姓名存入list。
    參數:
        filename: str, 只有姓名的檔案名稱（如 '2b_w15.txt'）
    回傳:
        list，內容為姓名字串
    """
    names = []
    with open(filename, encoding='utf-8') as f:               # 以utf-8編碼開啟檔案
        for line in f:                                        # 逐行讀取
            name = line.strip()                               # 去掉空白與換行
            if name:                                          # 若不是空行
                names.append(name)                            # 加入姓名清單
    return names

def main():
    # 讀取完整學員名單，回傳姓名對應學號的字典
    full_list = read_full_list('2b.txt')
    # 讀取出席名單，回傳姓名清單
    present_names = read_name_list('2b_w15.txt')
    # 逐一檢查出席名單中的姓名
    for name in present_names:
        if name in full_list:                                 # 若姓名在完整名單中
            print(f"{full_list[name]}\t{name}")               # 輸出學號與姓名（tab分隔）

if __name__ == "__main__":
    main()                                                    # 程式進入點，開始執行main()