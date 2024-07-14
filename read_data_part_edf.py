import numpy as np
import mne
import os
import pandas as pd
import scipy.io as sio

# 定义文件夹路径
folder_path = "OSA_datasets_label"
total_count = [0,0,0,0,0]
total_sleep = 0

# 定义一个函数来统计特定列的值
def count_values_in_column(folder_path, column_name, value_to_count):
    zero_count = 0
    # 遍历每个子文件夹
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
                    edf_files = [f for f in os.listdir(sub_subfolder_path) if f.endswith('].edf')]
                    edf_files = sorted(edf_files)
                    print (edf_files)
                    raw_arrays = []
                    for edf_file in edf_files:
                        file_path = os.path.join(sub_subfolder_path, edf_file)
                        raw = mne.io.read_raw_edf(file_path, preload=True)

                        print (sub_subfolder_path, raw.get_data().shape, raw.info['ch_names'])

                        #new_shape = (raw.get_data().shape[1] // 30 // 1000, 33, 1000 * 30)
                        #sliced_data = np.array([raw.get_data()[:, i*1000*30:(i+1)*1000*30] for i in range(raw.get_data().shape[1] // 30//1000)])
                        #sliced_data = sliced_data[:,:,:30*200]
                        #print ("sliced_data shape:", sliced_data.shape)
                        #new_sliced_data = sliced_data.reshape((sliced_data.shape[0], sliced_data.shape[1] * sliced_data.shape[2]))
                        #print ("sliced_data:", sliced_data.shape, new_sliced_data.shape)
                        #raw.get_data() = new_sliced_data
                        raw_arrays.append(raw)

                    merged_raw = mne.concatenate_raws(raw_arrays)
                    # 选择要保留的前5个通道
                    selected_ch_names = merged_raw.ch_names[:9]

                    #print (sub_subfolder_name, merged_raw.shape)

                    selected_ch_indices = [merged_raw.ch_names.index(ch_name) for ch_name in selected_ch_names]

                    # 获取部分维度的数据和通道名称
                    partial_data = merged_raw._data[selected_ch_indices]
                    partial_ch_names = [merged_raw.ch_names[i] for i in selected_ch_indices]

                    info = mne.create_info(partial_ch_names, merged_raw.info['sfreq'], ch_types='eeg')

                    custom_raw = mne.io.RawArray(partial_data, info)

                    #mne.io.write_raw_edf(sub_subfolder_name+'.edf', custom_raw, picks=range(len(partial_ch_names)))
                    print (sub_subfolder_name, partial_data.shape, len(partial_ch_names[0]))

                    data_dict = {'data': partial_data, 'ch_names': partial_ch_names, 'sfreq': merged_raw.info['sfreq']}
                    import h5py
                    sio.savemat(sub_subfolder_name + '.mat', data_dict)

                    #sio.savemat(sub_subfolder_name + '.mat', data_dict)

                    # 创建 HDF5 文件
                    #with h5py.File(sub_subfolder_name+'.h5', 'w') as f:
                        # 将数据保存到 HDF5 文件中的数据集
                    #    for key, value in data_dict.items():
                    #        f.create_dataset(key, data=value)
    return total_count

# 统计第三列是“WK”的个数
count_wk = count_values_in_column('./OSA_datasets', column_name='睡眠阶段', value_to_count=['WK','N1','N2',"N3","REM"])
print("睡眠个数:", count_wk)
