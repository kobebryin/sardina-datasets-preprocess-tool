import os 
import shutil
import random

### 
# Author: Jimmy Liang
# Email: jimmyliang@iii.org.tw
# Organization: III
# Create Date: 2019.10.04
# Modified Date: 2021.11.01
# Content: 第5步，將資料中原始資料JPEGImages中的圖檔，拆分為訓練、驗證集(採不重複抽樣)，
#          且製作二個資料集各自之圖片檔名文字清單(train.txt、valid.txt)，並將各自資料集之圖檔和xml標籤檔
# 			分開複製到各自資料夾。
###

''' Edit Here Start '''
model_name = 'FY110_Mix40wType8'    # 此次欲訓練模型命名
labels_path = 'B:/Sardina_Data/全標資料整理/Type8_ModelData/20211014_日夜間混和全標模型_type8/labels_all(include_testset)' # 總labels路徑
data_list_file_save_path = './step5'    # 儲存資料集各自之圖片檔名文字清單路徑
train_datasets_qty = 12415  # 訓練集資料挑選幀數
train_labels_path = './labels_train'    # 訓練資料集標記檔存儲路徑
val_labels_path = './labels_val'    # 驗證資料集標記檔存儲路徑
''' Edit Here End '''

# 檢查目標資料夾是否存在，若無則建立資料夾(防呆)
for DIR in [data_list_file_save_path, train_labels_path, val_labels_path]:
    if os.path.isdir(DIR):
        print('%s exists! , continue process...' % DIR)
    else:
        print('%s not exists, create it! continue process...' % DIR)
        os.mkdir(DIR)


#拆分訓練集、驗證集和測試集(不重複採樣)
random.seed(319)
files= os.listdir(labels_path) #得到資料夾下的所有檔名稱 
TrainSet = [files.pop(random.randrange(len(files))) for _ in range(train_datasets_qty)] #利用pop指令抽出已取出的訓練樣本，避免重複採樣
ValidationSet = files #剩餘的圖檔為驗證資料


# #將Annotations Label檔依照訓練和驗證分別存進對應資料夾
for file_names in TrainSet:
	shutil.copyfile(os.path.join(labels_path, file_names), os.path.join(train_labels_path, file_names))
for file_names in ValidationSet:
	shutil.copyfile(os.path.join(labels_path, file_names), os.path.join(val_labels_path, file_names))


# 分別將Train and Val and Test 檔名寫入.txt(Local本機端)
# Trainning Datasets
fileObject = open(os.path.join(data_list_file_save_path, model_name + '_train.txt'), 'w') #開啟新檔
for TrainSet_names in TrainSet:  
    jpg_name = TrainSet_names.replace(".txt", ".jpg")
    fileObject.write('./' + model_name + '/images/' + jpg_name)
    fileObject.write('\n')
fileObject.close() #寫入完畢關檔

# Validation Datasets
fileObject = open(os.path.join(data_list_file_save_path, model_name + '_valid.txt'), 'w') #開啟新檔
for ValidationSet_names in ValidationSet:
    jpg_name = ValidationSet_names.replace(".txt", ".jpg")
    fileObject.write('./' + model_name + '/images/' + jpg_name)
    fileObject.write('\n')
fileObject.close() #寫入完畢關檔