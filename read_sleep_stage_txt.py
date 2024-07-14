import os
import numpy as np
import pandas as pd
folder_path = "OSA_datasets_label"

event_id = {
            "WK":0,
            "N1":1,
            "N2":2,
            "N3":3,
            "REM":4
        }

for subfolder_name in os.listdir(folder_path):
    #if subfolder_name != 'AHI 5-15':
    #    continue
    subfolder_path = os.path.join(folder_path, subfolder_name)
    # 检查是否是文件夹
    if os.path.isdir(subfolder_path):
        # 再次遍历每个子文件夹下的文件夹
        for sub_subfolder_name in os.listdir(subfolder_path):
            sub_subfolder_path = os.path.join(subfolder_path, sub_subfolder_name)
            # 检查是否是文件夹
            if os.path.isdir(sub_subfolder_path):
                # 获取 SleepStaging.csv 文件路径
                print (sub_subfolder_name, sub_subfolder_path)
                label_data = pd.read_csv(sub_subfolder_path + "/" + "SleepStaging.csv")
                label_data['label'] = label_data['睡眠阶段'].map(event_id)
                output_file = sub_subfolder_name + ".txt"
                label_data['label'].to_csv(output_file, index=False,header=False)
