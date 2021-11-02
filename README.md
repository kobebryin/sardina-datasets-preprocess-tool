# Sardina Datasets Preprocessing Tools

## Project Information
- Author: Jimmy Liang
- Email: jimmyliang@iii.org.tw
- Organization: III
- Create Date: 2021.11.02

## Contents
- [Requirements](#requirements)
- [Sardina datasets NAS information](#sardina-datasets-nas-information)
- [Step 1. 將資料(image/annotation)從NAS文件架構中解析出來](#step-1-將資料imageannotation從nas文件架構中解析出來)
- [Step 2. 解析出標記檔中所有出現過之類別，並製成類別文字檔 ](#step-2-解析出標記檔中所有出現過之類別並製成類別文字檔)
- [Step 3. 將Sardina格式之標記檔(同VOC格式.xml)轉換成Yolo格式之標記檔(.txt)](#step-3-將sardina格式之標記檔同voc格式xml轉換成yolo格式之標記檔txt)
- [Step 4. (選項)標記檔類別合併/捨棄處理](#step-4-選項標記檔類別合併捨棄處理)
- [Step 5. 拆分訓練、驗證、測試資料集](#step-5-拆分訓練驗證測試資料集)
- [Step 6. 計算各類別物件數](#step-6-計算各類別物件數)

## Requirements
- **tqdm >= 4.39**: https://github.com/tqdm/tqdm
- **python >= 3.6.7**: https://www.python.org/downloads/release/python-367/

## Sardina datasets NAS information
```
    IP: 10.22.22.52
    Port: 21
    Sardina data path: /ITS/交付RD項目
```

## Step 1. 將資料(image/annotation)從NAS文件架構中解析出來 
- 1. 需先將資料從NAS中拉到本機端
- 2. 本機端資料夾架構範例如下(同NAS)

```
    2020 交付項目
    └───2020-02-17 交付項目 (物件)
    │   └───物件
    │       └───KH-A001-20200108-0000_F14112000
    │       │   └───KH-A001-20200108-0000
    │       │   │   └───images
    │       │   │   └───xml
    │       │   │   KH-A001-20200108-0000.mp4
    │       │   │   LabelVideoDB_KH-A001-20200108-0000_F14112000.db
    │       └───KH-A001-20200108-0001_F15173133
    │       │   ...
    │   
    └───2020-04-07 交付項目 (物件)
        │  ...
```

- 3. 修改本機端Sardina資料存放根目錄路徑至變數[`root_path`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step1_parse_nas_data.py#L15)
- 4. 修改欲存放影像(.jpg)之目錄變數[`targetDir_images`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step1_parse_nas_data.py#L16)
- 5. 修改欲存放標記檔(.xml)之目錄變數[`targetDir_annotation`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step1_parse_nas_data.py#L17)
- 6. 執行 `python3 step1_parse_nas_data.py`

## Step 2. 解析出標記檔中所有出現過之類別，並製成類別文字檔
- 1. 修改標記檔路徑變數[`annotation_path`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step2_get_classes_names.py#L16)
- 2. 修改欲存放類別檔(.names)之路徑[`class_files_save_path`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step2_get_classes_names.py#L17)
- 3. 修改類別檔(.names)檔名變數[`class_names_filename`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step2_get_classes_names.py#L18)
- 4. 執行 `python3 step2_get_classes_names.py`
- 5. 若執行成功將會於指定存放路徑中新增一個類別檔(.names)

## Step 3. 將Sardina格式之標記檔(同VOC格式.xml)轉換成Yolo格式之標記檔(.txt)
- 0. darknet-yolo規定格式每行欄位為 `label_idx x_center y_center width height`
- 1. 修改欲使用之類別檔(.names)路徑(ex: 可使用步驟二產出之類別檔)[`classes_names_file_path`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step3_make_yolo_format_label.py#L17)
- 2. 修改Sardina格式之標記檔路徑[`annotation_path`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step3_make_yolo_format_label.py#L18)
- 3. 修改欲存放轉換後yolo格式之標記檔路徑[`label_save_path`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step3_make_yolo_format_label.py#L19)
- 4. 執行 `python3 step3_make_yolo_format_label.py`

## Step 4. (選項)標記檔類別合併/捨棄處理
- 1. 修改原標記檔(步驟三產出之yolo格式txt標記檔)路徑至變數[`labels_path`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step4_labels_type_transfer.py#L15)
- 2. 修改合併/捨棄特定類別後新標記檔存放路徑[`new_labels_save_path`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step4_labels_type_transfer.py#L16)
- 3. 原標記檔之類別檔(.names)路徑[`original_classes_file_path`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step4_labels_type_transfer.py#L17)
- 4. 欲更換之新標記檔之類別檔(.names)路徑[`new_classes_file_path`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step4_labels_type_transfer.py#L18)
- 5. 撰寫類別轉換邏輯文件，給程式讀取使用，範例文件如: [`transfer_logic.txt`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step4/transfer_logic.txt)
- 6. 將類別轉換文件路徑修改至變數[`transfer_logic_file`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step4_labels_type_transfer.py#L19)
- 7. 執行 `python3 step4_labels_type_transfer.py`

## Step 5. 拆分訓練、驗證、測試資料集
- 1. 將此次模型名稱(自行命名)輸入至變數[`model_name`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step5_split_train_val_test.py#L17)
- 2. 修改標記檔路徑至變數[`labels_path`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step5_split_train_val_test.py#L18)
- 3. 修改儲存資料集各自之圖片檔名文字清單路徑至變數[`data_list_file_save_path`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step5_split_train_val_test.py#L19)
- 4. 將欲挑選之【訓練集】資料數/幀數修改至變數[`train_datasets_qty`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step5_split_train_val_test.py#L20)
- 5. 將欲挑選之【驗證集】資料數/幀數修改至變數[`val_datasets_qty`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step5_split_train_val_test.py#L21)
- 6. 修改【訓練集】、【驗證集】、【測試集】之標記檔路徑至變數`train_labels_path`、`val_labels_path`、`test_labels_path`
    - [`train_labels_path`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step5_split_train_val_test.py#L22)
    - [`val_labels_path`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step5_split_train_val_test.py#L23)
    - [`test_labels_path`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step5_split_train_val_test.py#L24)
- 7. 執行 `python3 step5_split_train_val_test.py`
- **Note:** 若不需【測試集】，只需要拆分【訓練集】、【驗證集】的話，可使用 [`step5_split_train_val.py`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step5_split_train_val.py)

## Step 6. 計算各類別物件數
- 1. 修改欲計算之標記檔(.txt)目錄路徑至變數[`labels_path`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step6_get_obj_qty.py#L14)
- 2. 將對應之類別檔(.names)路徑輸入至變數[`classes_file_path`](http://140.92.63.109/jimmyliang/sardina-datasets-preprocess/blob/master/step6_get_obj_qty.py#L15)
- 3. 執行 `python3 step6_get_obj_qty.py`
- 4. 輸出格式範例如下:

```
    Total frames: 15519 frames
    Bicycle: 5930
    Bus: 1872
    Motorcycle: 70120
    MotorcycleWithRider: 72064
    People: 27457
    Sedan: 100254
    Taxi: 10922
    Truck: 14826
    Total Object Qty: 303445
```