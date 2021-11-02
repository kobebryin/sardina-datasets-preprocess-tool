import os 
import xml.etree.cElementTree as ET
from decimal import getcontext, Decimal
from tqdm import tqdm

### 
# Author: Jimmy Liang
# Email: jimmyliang@iii.org.tw
# Organization: III
# Create Date: 2019.12.12
# Modified Date: 2021.11.01
# Content: 第3步，將各Annotations_modified中的標籤.xml檔中的bndbox數值parse出來，
#           配合darknet-yolo規定格式(label_idx, x_center, y_center, width, height)並另存成.txt標記檔。
###

''' Edit Here Start '''
classes_names_file_path = './classes.names'
annotation_path = 'B:/Sardina_Data/全標資料整理/OriginalData/白天全標資料/Annotations_modified' #移動路徑至資料夾目錄 
label_save_path = 'B:/Sardina_Data_Preprocess/labels'
''' Edit Here End '''

# 檢查目標資料夾是否存在，若無則建立資料夾
if os.path.isdir(label_save_path):
    print('%s exists!' % label_save_path)
else:
    print('%s not exists, create it!' % label_save_path)
    os.mkdir(label_save_path)

# 獲取classes.names檔案內各類別名並存進list中
with open(classes_names_file_path) as file:
    lines = file.readlines()
    classNames = [line.rstrip() for line in lines]
files = os.listdir(annotation_path) #得到資料夾下的所有檔名稱 

print('Start parsing annotation(.xml) to yolo format label(.txt): ')
for file_names in tqdm(files): #遍歷資料夾 
    if not os.path.isdir(file_names): #判斷是否是資料夾,不是資料夾才打開
        tree = ET.ElementTree(file=os.path.join(annotation_path, file_names)) 
        img_width = tree.getroot()[4][0].text   #取出照片之寬度(用於正規劃座標值)
        img_height = tree.getroot()[4][1].text  #取出照片之高度(用於正規劃座標值) 
        fileObject = open(os.path.join(label_save_path, file_names.replace('.xml', '.txt')), 'w') #開啟新檔 (train2019 和 val2019兩個資料夾，自行修改)

        for elem_name in tree.iterfind('object'):  #取出xml檔內的Tag <object>部分
            count = 0   # bounding box欄位索引值(start from zero0)
            if(elem_name.getchildren()[0].text == 'PolicaeCar'):    # 標記端標記錯誤 - 跳過此錯誤命名方式
                print('PolicaeCar Appear, continue... :-(')
            else:
                label_idx = classNames.index(elem_name.getchildren()[0].text)   #get class name's index in list
                if(elem_name.getchildren()[1].tag == 'attribute'):  # 標記端新舊格式之annotation差別
                    bndbox_index = 7    # new annotation version
                else:
                    bndbox_index = 4    # old annotation version

                for object in elem_name.getchildren()[bndbox_index]:
                    if(count == 0): #parse xmin
                        xmin = object.text
                    if(count == 1): #parse ymin
                        ymin = object.text
                    if(count == 2): #parse xmax
                        xmax = object.text
                    if(count == 3): #parse ymax
                        ymax = object.text

                        #計算bndbox中心點(x,y)座標和bndbox的寬高
                        x_center = str(Decimal(((int(xmin) + int(xmax))/2)/int(img_width)).quantize(Decimal('0.000000')))   #取x座標中點，公式:(xmin + xmax)/2/img_width (只取到小數點六位)
                        y_center = str(Decimal(((int(ymin) + int(ymax))/2)/int(img_height)).quantize(Decimal('0.000000')))  #取y座標中點，公式:(ymin + ymax)/2/img_height (只取到小數點六位)
                        width = str(Decimal((int(xmax) - int(xmin))/int(img_width)).quantize(Decimal('0.000000')))  #取bndbox寬，公式:(xmax - xmin)/img_width (只取到小數點六位)
                        height = str(Decimal((int(ymax) - int(ymin))/int(img_height)).quantize(Decimal('0.000000')))    #取bndbox高，公式:(ymax - ymin)/img_height (只取到小數點六位)

                        # write file
                        fileObject.write(str(label_idx) + " " + x_center + " " + y_center + " " + width + " " + height)
                        fileObject.write('\n')

                    count += 1
        fileObject.close() #寫入完畢關檔