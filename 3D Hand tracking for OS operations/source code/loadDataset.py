# importing libraries
import numpy as np
import cv2 as cv
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical

def load_dataset():
    # variables for files path
    train_path = r'dataset/sign_mnist_train.csv'
    test_path = r'dataset/sign_mnist_test.csv'
    # -----------------------------Train Data Csv File----------------------------
    # lists for train images and labels
    train_labels_list = list()
    train_images_list = list()
    # reading train data csv file
    train_data = pd.read_csv(train_path)
    # getting train data rows
    train_rows = train_data.values
    # separating labels and their corresponding images
    for row in train_rows:
        # only processing required images/signs
        # assigning labels 0-4, so it can be converted to_categorical
        if row[0] in [1, 18, 2, 23]:
            # S sign for open file
            if row[0] == 18:
                train_labels_list.append(0)
            # B sign for close file
            elif row[0] == 1:
                train_labels_list.append(1)
            # X sign for volume up
            elif row[0] == 23:
                train_labels_list.append(2)
            # C sign for volume down
            elif row[0] == 2:
                train_labels_list.append(3)
            # making 3 channel image for models that require 3 channel image
            # img = cv.merge((row[1:], row[1:], row[1:]))
            # reshaping the image
            img = row[1:].reshape(28, 28)
            # converting int64 to float32, so it can be accepted by resize func
            img = img.astype('float32')
            # resizing
            img = cv.resize(img, (32, 32))
            train_images_list.append(img)
    # -----------------------------Test Data Csv File----------------------------
    # lists for test images and labels
    test_labels_list = list()
    test_images_list = list()
    # reading test data csv file
    test_data = pd.read_csv(test_path)
    # getting test data rows
    test_rows = test_data.values
    # separating labels and their corresponding images
    for row in test_rows:
        # only processing required images/signs
        # assigning labels 0-4, so it can be converted to_categorical
        if row[0] in [1, 18, 2, 23]:
            # S sign for open file
            if row[0] == 18:
                test_labels_list.append(0)
            # B sign for close file
            elif row[0] == 1:
                test_labels_list.append(1)
            # X sign for volume up
            elif row[0] == 23:
                test_labels_list.append(2)
            # C sign for volume down
            elif row[0] == 2:
                test_labels_list.append(3)
            # making 3 channel image for models that require 3 channel image
            # img = cv.merge((row[1:], row[1:], row[1:]))
            # reshaping the image
            img = row[1:].reshape(28, 28)
            # converting int64 to float32, so it can be accepted by resize func
            img = img.astype('float32')
            # resizing
            img = cv.resize(img, (32, 32))
            test_images_list.append(img)

    images_dataset = list()
    labels_dataset = list()
    test_images = list()
    test_labels = list()
    # print('images taken from train set==', len(train_images_list))
    # print('images taken from test set==', len(test_images_list))
    # merging all the dataset together
    images_dataset.extend(train_images_list)
    images_dataset.extend(test_images_list)
    labels_dataset.extend(train_labels_list)
    labels_dataset.extend(test_labels_list)
    # separating around 10% for testing
    test_images.extend(images_dataset[5200: len(images_dataset)])
    test_labels.extend(labels_dataset[5200: len(labels_dataset)])
    # deleting the separated data to eliminate redundancy
    # print('total images before del ==', len(images_dataset), len(labels_dataset))
    del images_dataset[5200: len(images_dataset)]
    del labels_dataset[5200: len(labels_dataset)]
    # print('sign 18 (S) images==', labels_dataset.count(0), test_labels.count(0))
    # print('sign 1 (B) images==', labels_dataset.count(1), test_labels.count(1))
    # print('sign 23 (X) images==', labels_dataset.count(2), test_labels.count(2))
    # print('sign 22 (C) images==', labels_dataset.count(3), test_labels.count(3))
    # print('total images for splitting ==', len(images_dataset), len(labels_dataset))
    # print('total images for testing ==', len(test_images), len(test_labels))
    # print(np.unique(labels_dataset))

    # splitting dataset
    train_images, val_images, train_labels, val_labels = train_test_split(
        images_dataset,
        labels_dataset,
        test_size=0.1,
        random_state=42)
    # print("Train data: ", np.shape(train_images))
    # print("Test data:", np.shape(val_images))
    # print(train_labels.count(0))
    # print(train_labels.count(1))
    # print(train_labels.count(2))
    # print(train_labels.count(3))
    # print(val_labels.count(0))
    # print(val_labels.count(1))
    # print(val_labels.count(2))
    # print(val_labels.count(3))
    # print('total train images==', len(train_images))
    # print('sign 18 (S) images==', train_labels.count(0))
    # print('sign 1 (B) images==', train_labels.count(1))
    # print('sign 23 (X) images==', train_labels.count(2))
    # print('sign 22 (C) images==', train_labels.count(3))
    # print('total val images==', len(val_images))
    # print('sign 18 (S) images==', val_labels.count(0))
    # print('sign 1 (B) images==', val_labels.count(1))
    # print('sign 23 (X) images==', val_labels.count(2))
    # print('sign 22 (C) images==', val_labels.count(3))
    # print('total test images==', len(test_images))
    # print('sign 18 (S) images==', test_labels.count(0))
    # print('sign 1 (B) images==', test_labels.count(1))
    # print('sign 23 (X) images==', test_labels.count(2))
    # print('sign 22 (C) images==', test_labels.count(3))

    train_labels = to_categorical(train_labels)
    # print(train_labels[0])
    val_labels = to_categorical(val_labels)
    # print(val_labels[0])
    test_labels = to_categorical(test_labels)
    # print(test_labels[0])
    dataset = [train_images, train_labels, val_images, val_labels, test_images, test_labels]

    return dataset

