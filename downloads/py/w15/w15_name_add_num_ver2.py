# 先讀取完整名單 2b.txt，建立姓名對應學號的 dict
student_dict = {}  # 建立一個空字典，準備存放「姓名」對應到「學號」的資料
with open('2b.txt', encoding='utf-8') as f:  # 以 utf-8 編碼方式開啟檔案 "2b.txt"，並將檔案物件指派給變數 f
    for line in f:  # 逐行讀取檔案 f
        line = line.strip()  # 去掉該行字串前後的空白字元與換行符號
        if not line or line.startswith('學號'):  # 如果這一行是空的，或以「學號」開頭（通常是標題行）
            continue  # 跳過這一行，不執行之後的處理，直接進入下一行
        parts = line.split('\t')  # 將這一行用 Tab 符號分割，得到一個字串列表
        if len(parts) >= 2:  # 如果分割後至少有兩個欄位（確保有學號和姓名）
            student_id, name = parts[0], parts[1]  # 將分割後的第一欄指定為學號，第二欄指定為姓名
            student_dict[name] = student_id  # 將姓名作為 key，學號作為 value，加入 student_dict 字典

# 讀取出席名單 2b_w15.txt，取得姓名清單
present_list = []  # 建立一個空清單，準備存放出席學生的姓名
with open('2b_w15.txt', encoding='utf-8') as f:  # 以 utf-8 編碼方式開啟檔案 "2b_w15.txt"，將檔案物件指派給變數 f
    for line in f:  # 逐行讀取檔案 f
        name = line.strip()  # 去掉該行字串前後的空白字元與換行符號，取得姓名
        if name:  # 如果這一行不是空行（即有姓名）
            present_list.append(name)  # 將姓名加入 present_list 清單

# 依學號由小到大排序，並輸出「學號<TAB>姓名」
result = []  # 建立一個空清單，準備存放（學號, 姓名）配對
for name in present_list:  # 針對出席清單中的每一個姓名
    if name in student_dict:  # 如果這個姓名存在於 student_dict 字典（即在完整名單中找得到）
        student_id = student_dict[name]  # 取得該姓名對應的學號
        result.append((student_id, name))  # 將（學號, 姓名）這個 tuple 加入 result 清單

# 按學號排序
result.sort(key=lambda x: x[0])  # 依據 tuple 的第一個元素（學號）進行升冪排序

for student_id, name in result:  # 針對 result 清單排序後的每一個（學號, 姓名）組合
    print(f"{student_id}\t{name}")  # 以 Tab 分隔學號和姓名，將其印出到螢幕