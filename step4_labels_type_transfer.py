import os
from tqdm import tqdm

###
# Author: Jimmy Liang
# Email: jimmyliang@iii.org.tw
# Organization: III
# Create Date: 2019.12.12
# Modified Date: 2021.11.02
# Content: 第4步，通常訓練資料不會依照所有原類別使用，
#          將轉換成yolo格式之標記label檔之原始idx轉換為訓練需求之idx(類別融合、類別捨棄)。
###

''' Edit Here Start '''
labels_path = 'B:/Sardina_Data_Preprocess/ori_labels'  # 移動路徑至資料夾目錄
new_labels_save_path = 'B:/Sardina_Data_Preprocess/new_labels'
original_classes_file_path = './step4/type30_classes.names'
new_classes_file_path = './step4/type8_classes.names'
transfer_logic_file = './step4/transfer_logic.txt'
''' Edit Here End '''

# 檢查目標資料夾是否存在，若無則建立資料夾(防呆)
if os.path.isdir(new_labels_save_path):
    print('%s exists! , continue process...' % new_labels_save_path)
else:
    print('%s not exists, create it! continue process...' % new_labels_save_path)
    os.mkdir(new_labels_save_path)
for file_chk in [original_classes_file_path, new_classes_file_path, transfer_logic_file]:
    if not os.path.isfile(file_chk):
        raise SystemExit('%s not exist, this is necessary file please check it again...' % os.path.basename(file_chk))
    else:
        print('%s exist, check success, continue process...' % os.path.basename(file_chk))


# 獲取原類別檔案內各類別名並存進list中
with open(original_classes_file_path) as file:
    lines = file.readlines()
    original_classNames = [line.rstrip() for line in lines]
original_classNames_len = len(original_classNames)

# 獲取欲更換類別檔案內各類別名並存進list中
with open(new_classes_file_path) as file:
    lines = file.readlines()
    new_classNames = [line.rstrip() for line in lines]
new_classNames_len = len(new_classNames)

# 獲取更換類別邏輯檔案並存進dictionary中
transfer_logic_dict = {}
with open(transfer_logic_file) as file:
    lines = file.readlines()
    for line in lines:
        if line.strip().startswith("#"):
            continue
        old_class = line.rstrip().split(':')[0]
        new_class = line.rstrip().split(':')[1]
        transfer_logic_dict[old_class] = new_class
transfer_logic_dict_len = len(transfer_logic_dict)

# 檢查轉換類別邏輯是否有包含原始類別中的所有類別(防呆)
if transfer_logic_dict_len != original_classNames_len:
    raise SystemExit('transfer_logic_file length is not match with original_classNames_len, please check logic file!')

files = os.listdir(labels_path)  # 得到資料夾下的所有檔名稱
print('Start scan all labels then doing classes transfer: ')
for file_names in tqdm(files):  # 遍歷資料夾
    if not os.path.isdir(file_names):  # 判斷是否是資料夾,不是資料夾才打開
        f = open(os.path.join(labels_path, file_names), "r+", encoding='utf-8')
        string = ""
        for line in f.readlines():
            check_boolean = 0   # 0:更換idx  1:刪除/忽略
            content = line.split()
            ori_class = original_classNames[int(content[0])]
            # Start comparing and transfer record
            if transfer_logic_dict[ori_class] == 'X':
                content[0] = "nan"
                check_boolean = 1
            else:
                content[0] = str(new_classNames.index(transfer_logic_dict[ori_class]))
                check_boolean = 0 
            
            # save in temp string variable and wait for write file
            if(check_boolean == 0):
                string += " ".join(content) + "\n"
            elif(check_boolean == 1):
                string = string
            else:
                string = string
            f.close()   # close labels file reader
            wf = open(os.path.join(new_labels_save_path, file_names),'w+', encoding='utf-8')  # write new transfer label
            wf.write(string)
            wf.close()  # close labels file writer