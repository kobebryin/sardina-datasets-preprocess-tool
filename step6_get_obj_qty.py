import os
from tqdm import tqdm

###
# Author: Jimmy Liang
# Email: jimmyliang@iii.org.tw
# Organization: III
# Create Date: 2019.10.04
# Modified Date: 2021.11.01
# Content: 將指定資料集中的各個物件數計算統計。
###

''' Edit Here Start '''
labels_path = "B:/Sardina_Data/全標資料整理/Type8_ModelData/20211028_日夜間混和全標30萬模型_type8/labels"  # 移動路徑至資料夾目錄
classes_file_path = './step6/classes.names'
''' Edit Here End '''

# 檢查必要檔案是否存在(防呆)
if not os.path.isfile(classes_file_path):
    raise SystemExit('%s not exist, this is necessary file please check it again...' %
                     os.path.basename(classes_file_path))
else:
    print('%s exist, check success, continue process...' %
          os.path.basename(classes_file_path))

# 遍歷類別檔
with open(classes_file_path) as file:
    lines = file.readlines()
    classNames = [line.rstrip() for line in lines]
classNames_len = len(classNames)
obj_value = [0] * classNames_len    # 紀錄各類別數量清單initial

# 計算物件數
print('Start calculating object quantity: ')
files = os.listdir(labels_path)  # 得到資料夾下的所有檔名稱
for file_names in tqdm(files):  # 遍歷資料夾
    fp = open(labels_path + '/' + file_names, "r")
    line = fp.readline()
    # 用 while 逐行讀取檔案內容，直至檔案結尾
    while line:
        id_temp = line.split(" ")
        obj_value[int(id_temp[0])] += 1
        line = fp.readline()
    fp.close()

# 整理輸出文字
result_str = 'Total frames: ' + str(len(files)) + ' frames\n'
for idx, qty in enumerate(obj_value):
    result_str += classNames[idx] + ': ' + str(qty) + '\n'
qty_summary = sum(obj_value)
result_str += 'Total Object Qty: ' + str(qty_summary)
print(result_str)   # show the result on console log
