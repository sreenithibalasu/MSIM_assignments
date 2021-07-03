import os
import pandas as pd
import re
import shutil
import math
import random
import json

# Declaring Variables
regex = re.compile("([a-zA-Z]+)([0-9]+)")

# Reading JSON Config File
with open('config_test.json') as f:
    config = json.load(f)

data_path = config["data_path"]
label_path = config["label_path"]
folder_labels = config["folders_and_labels"]
special_labels = config["special_labels"]

save_dir = config["save_dir"] + '/extracted_images'

if not os.path.exists(save_dir):
    print("Creating folder extracted_images in path: ", data_path)
    os.mkdir(save_dir)



# Separating aggregated data using labels

for folder_name, labels_name in folder_labels.items():
    print("\n Processing .... \n")
    print("Data Folder: ", folder_name, "\nLabels File: ", labels_name)

    folder = data_path + '/' + folder_name
    labels = label_path + '/' + labels_name
    # Read labels txt File
    df = pd.read_csv(labels, sep=',', header=None, names=['filename', 'label'])

    png_files = {}
    for png in os.listdir(folder):
        png_files[regex.match(png).groups()[1]] = png

    # Separating data

    for i in range(len(df)):

        if df.loc[i]['label'] in special_labels.keys():
            label = special_labels[df.loc[i]['label']]
        else:
            label = df.loc[i]['label']

        if os.path.exists(save_dir + '/' + label):

            #Set source and destination of png file
            src = folder + '/' + png_files[df.loc[i]['filename'].split('_')[-1]]
            dest = save_dir + '/' + label + '/' + png_files[df.loc[i]['filename'].split('_')[-1]]

            shutil.copyfile(src.encode('UTF-8'), dest.encode('UTF-8'))
        else:

            os.mkdir(save_dir + '/' + label)

            #Set source and destination of png file
            src = folder + '/' + png_files[df.loc[i]['filename'].split('_')[-1]]
            dest = save_dir + '/' + label + '/' + png_files[df.loc[i]['filename'].split('_')[-1]]

            shutil.copyfile(src.encode('UTF-8'), dest.encode('UTF-8'))
    print("\nDone!")

# Checking if all files are copied and segregted

for folder_name, labels_name in folder_labels.items():

    folder = data_path + '/' + folder_name
    labels = label_path + '/' + labels_name

    df = pd.read_csv(labels, sep=',', header=None, names=['filename', 'label'])

    df_entries = len(df)
    files_cnt = 0

    for files in os.listdir(folder):
        files_cnt += 1
    if df_entries == files_cnt:
        print("All files have been copied successfully for ", folder_name)
    else:
        print("Not all files were copied.")
