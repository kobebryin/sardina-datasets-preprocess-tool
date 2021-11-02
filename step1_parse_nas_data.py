import os
import shutil
from tqdm import tqdm

###
# Author: Jimmy Liang
# Email: jimmyliang@iii.org.tw
# Organization: III
# Create Date: 2019.12.12
# Modified Date: 2021.11.01
# Content: 第一步，將原始NAS資料架構中之圖檔(.jpg)和個資料夾中標籤檔(.xml)全數匯總複製至對應資料夾
###

''' Edit Here Start '''
root_path = "B:/Sardina_Data/全標資料整理/OriginalData/白天全標資料/NAS/2020"
targetDir_images = "B:/Sardina_Data_Preprocess/images"
targetDir_annotation = "B:/Sardina_Data_Preprocess/annotation"
''' Edit Here End '''

# 檢查目標資料夾是否存在，若無則建立資料夾
for Dir in [targetDir_images, targetDir_annotation]:
    if os.path.isdir(Dir):
        print('%s exists!' % Dir)
    else:
        print('%s not exists, create it!' % Dir)
        os.mkdir(Dir)

print('Start copy & parse image/annotation file from %s: ' % root_path)
for path in tqdm(os.listdir(root_path)):
    full_path = os.path.join(root_path, path)

    # 判斷是否是資料夾,不是資料夾才打開
    if os.path.isdir(full_path):
        first_files = os.listdir(full_path)     # 得到資料夾下的所有檔名稱
    else:
        continue  

    # 複製所有圖檔至targetDir_images
    for file_names in first_files:  # 遍歷資料夾
        path_tmp = os.path.join(full_path, file_names)
        second_files = os.listdir(path_tmp)
        for file_names2 in second_files:  # 遍歷資料夾
            path_tmp2 = os.path.join(path_tmp, file_names2)
            if os.path.isdir(path_tmp2):
                third_files = os.listdir(path_tmp2)
                path_tmp3 = os.path.join(path_tmp2, file_names2.split('_')[0], 'images')
                final_files = os.listdir(path_tmp3)
                for file_names3 in final_files:
                    if not os.path.isdir(file_names3):  # 判斷是否是資料夾,不是資料夾才打開
                        shutil.copy(os.path.join(path_tmp3, file_names3), targetDir_images)

    # 複製所有標籤文件至targetDir_annotation
    for file_names in first_files:  # 遍歷資料夾
        path_tmp = os.path.join(full_path, file_names)
        second_files = os.listdir(path_tmp)
        for file_names2 in second_files:  # 遍歷資料夾
            path_tmp2 = os.path.join(path_tmp, file_names2)
            if os.path.isdir(path_tmp2):
                third_files = os.listdir(path_tmp2)
                path_tmp3 = os.path.join(path_tmp2, file_names2.split('_')[0], 'xml')
                final_files = os.listdir(path_tmp3)
                for file_names3 in final_files:
                    if not os.path.isdir(file_names3):  # 判斷是否是資料夾,不是資料夾才打開
                        shutil.copy(os.path.join(path_tmp3, file_names3), targetDir_annotation)