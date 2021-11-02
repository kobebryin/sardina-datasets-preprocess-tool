import os 
import xml.etree.cElementTree as ET
from tqdm import tqdm

### 
# Author: Jimmy Liang
# Email: jimmyliang@iii.org.tw
# Organization: III
# Create Date: 2019.12.12
# Modified Date: 2021.11.01
# Content: 第二步，將原始標籤資料.xml檔中所有的標籤類別(label classes)逐一parse出來，
#           並製成classes.names檔。
###

''' Edit Here Start '''
annotation_path = "B:/Sardina_Data/全標資料整理/OriginalData/夜晚全標資料/Annotations_modified" #移動路徑至資料夾目錄 
class_files_save_path = './'
class_names_filename = 'classes.names'
''' Edit Here End '''

files= os.listdir(annotation_path) # 得到資料夾下所有標記檔檔名 
class_list = [] # 宣告一個空List用來存各個Class names

#   抓取每個標記檔(.xml)出現之類別名稱
print('Start scan all annotation XML file:')
for file_names in tqdm(files): #遍歷資料夾 
    if not os.path.isdir(file_names): #判斷是否是資料夾,不是資料夾才打開
        tree = ET.ElementTree(file=os.path.join(annotation_path, file_names))
        for elem in tree.iterfind('object/name'):
            class_list.append(elem.text)

#   將List中重複的class name清除
class_list_unduplicated = list(set(class_list)) 

#   寫進classes.name檔
print('Start write %s file: ' % class_names_filename)
fileObject = open(os.path.join(class_files_save_path, class_names_filename), 'w') #開啟新檔
for class_list_unduplicated_text in tqdm(class_list_unduplicated):  #用迴圈逐一將Class list中的元素換行寫入classes.names
	fileObject.write(class_list_unduplicated_text)
	fileObject.write('\n')
fileObject.close() #寫入完畢關檔