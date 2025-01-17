#!/usr/bin/env python
# coding: utf-8

# In[1]:

# NOTE: this file is important as it runs the actual saccade experiment
# NOTE: Figure S16-18 in paper

import sys
sys.path.insert(0, "../")

import numpy as np
import cv2
from vs_model import VisualSearchModel as VisualSearchModel
from tqdm import tqdm
import matplotlib.pyplot as plt
from data_utils import get_data_paths, get_exp_info
import os
from tensorflow.keras.utils import plot_model
import tensorflow as tf
import time

t_start = time.time()

print("Starting experiment:", t_start)

physical_devices = tf.config.list_physical_devices('GPU')
for dev in physical_devices:
    tf.config.experimental.set_memory_growth(dev, True)

vgg_model_path = "../pretrained_model/vgg16_imagenet_filters.h5"
base_data_path = "dataset/"

eccParam = {}
eccParam['rf_min'] = [2]*5
eccParam['stride'] = [2]*5
eccParam['ecc_slope'] = [0, 0, 3.5*0.02, 8*0.02, 16*0.02]
eccParam['deg2px'] = [round(30.0), round(30.0/2), round(30.0/4), round(30.0/8), round(30.0/16)]
eccParam['fovea_size'] = 4
eccParam['rf_quant'] = 1
eccParam['pool_type'] = 'avg'

ecc_models = []

# eccNET
for out_layer in [[1, 1, 1]]:
    model_desc = {'eccParam': eccParam,
                  'ecc_depth': 5,
                  'out_layer': out_layer,
                  'comp_layer': 'diff',
                  'vgg_model_path': vgg_model_path,
                  'model_subname': ""}

    ecc_models.append(model_desc)

for model_desc in ecc_models:
    vsm = VisualSearchModel(model_desc)
    print(vsm.model_name)

    for task in ["ObjArr", "Waldo", "NaturalDesign"][1:]:
        exp_info = get_exp_info(task)
        vsm.load_exp_info(exp_info, corner_bias=16*4*1)

        NumStimuli = exp_info['NumStimuli']
        NumFix = exp_info['NumFix']

        data = np.zeros((NumStimuli, NumFix, 2))
        I_data = np.zeros((NumStimuli, 1), dtype=int)
        CP = np.zeros((NumStimuli, NumFix), dtype=int)

        # NOTE: num stimuli is the number objects to search through
        for i in tqdm(range(NumStimuli), desc=task):
            stim_path, gt_path, tar_path = get_data_paths(task, i)

            # NOTE: `saccade` is an array of all the saccades made to find the object i
            saccade = vsm.start_search(stim_path, tar_path, gt_path)

            j = saccade.shape[0]
            I_data[i, 0] = min(NumFix, j)
            if j < NumFix+1:
                CP[i, j-1] = 1
            data[i, :min(NumFix, j), 0] = saccade[:, 0].reshape((-1,))[:min(NumFix, j)]
            data[i, :min(NumFix, j), 1] = saccade[:, 1].reshape((-1,))[:min(NumFix, j)]

        if exp_info['s_ratio'] is not None:
            data[:, :, 0] = data[:, :, 0]*exp_info['s_ratio'][0]
            data[:, :, 1] = data[:, :, 1]*exp_info['s_ratio'][1]

        np.save('out/' + task + '/cp/CP_' + vsm.model_name + '.npy', CP)
        np.save('out/' + task + '/ifix/I_' + vsm.model_name + '.npy', I_data)
        np.save('out/' + task + '/fix/' + vsm.model_name + '.npy', data)

print("Total time taken:", time.time()-t_start)


# In[ ]:
