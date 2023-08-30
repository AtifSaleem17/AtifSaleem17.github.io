# importing libraries
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
import cv2 as cv
import tensorflow as tf
import keras
import mediapipe as mp
import matplotlib.pyplot as plt
from my_model import my_model
from vgg16_model import vgg16_model
from resnetv2_model import resnetv2_model
from loadDataset import load_dataset
from modelEvaluation import model_performance

# ---------------------------- initializing volume library variables ---------------------
device = AudioUtilities.GetSpeakers()
interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# window volume object
volume = cast(interface, POINTER(IAudioEndpointVolume))
# setting window volume
volume.SetMasterVolumeLevel(-96, None)
# getting window volume range
vol_range = volume.GetVolumeRange()  # volume range -96 to 0
# print(volRange)
min_vol = vol_range[0]  # -96
max_vol = vol_range[1]  # 0
vol = 0
vol_bar = 297
vol_per = 0
def volume_control(gestures, frame):
    global min_vol, max_vol, vol, vol_bar, vol_per
    # -------------------------------- Volume Up Control -----------------------------
    if gestures[0] == 1:
        # print('volume up...')
        curVol = volume.GetMasterVolumeLevel()
        if curVol < max_vol:
            # vol = np.interp(curVol, [min_vol, max_vol], [min_vol, max_vol]) + 1
            vol = math.floor(curVol + 1)
            # print(vol)
            volume.SetMasterVolumeLevel(vol, None)
        # making volume bar in the frame
        cv.rectangle(frame, (60, 150), (85, 300), (173, 68, 142), 2)
        vol_bar = np.interp(vol, [min_vol, max_vol], [297, 153])
        vol_per = np.interp(vol, [min_vol, max_vol], [0, 100])
        cv.rectangle(frame, (63, int(vol_bar)), (82, 297), (219, 152, 52), cv.FILLED)
        cv.putText(frame, f'{int(vol_per)}', (60, 225), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (60, 76, 231), 0)
    # -------------------------------- Volume Down Control -----------------------------
    elif gestures[1] == 1:
        # print('volume down...')
        curVol = volume.GetMasterVolumeLevel()
        if curVol > min_vol:
            # vol = np.interp(curVol, [min_vol, max_vol], [min_vol, max_vol]) -1
            vol = math.floor(curVol - 1)
            # print(vol)
            volume.SetMasterVolumeLevel(vol, None)
        # making d volume bar in the frame
        cv.rectangle(frame, (60, 150), (85, 300), (173, 68, 142), 2)
        vol_bar = np.interp(vol, [min_vol, max_vol], [297, 153])
        vol_per = np.interp(vol, [min_vol, max_vol], [0, 100])
        cv.rectangle(frame, (63, int(vol_bar)), (82, 297), (219, 152, 52), cv.FILLED)
        cv.putText(frame, f'{int(vol_per)}', (60, 225), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (60, 76, 231), 0)

def main():
    # ------------------------------ Calling load_dataset function -----------------------
    dataset = load_dataset()
    train_images, train_labels, val_images, val_labels, test_images, test_labels = dataset
    data = [train_images, train_labels, val_images, val_labels]
    # print(np.shape(train_images))
    # print(np.shape(val_images))
    # print(np.shape(test_images))
    # # plot random 5 images in your dataset with their labels
    # import random
    # numbers = random.choices(range(len(train_images)), k=15)
    # plt.figure(figsize=(10, 10))
    # for i, number in enumerate(numbers):
    #     plt.subplot(3, 5, i + 1)
    #     plt.title(train_labels[number])
    #     plt.imshow(train_images[number], cmap='gray')
    # plt.show()

    # ---------------------------------CNN Model---------------------------
    # load saved model
    cnn_model = keras.models.load_model('cnn_model2.h5')
    # cnn_model = my_model(data)
    # # prediction for My_model
    # cnn_prediction = cnn_model.predict(np.array(test_images))
    # cnn_image = [np.argmax(i) for i in cnn_prediction]
    # cnn_label = [np.argmax(i) for i in test_labels]
    # model_performance(cnn_image, cnn_label, "CNN Model")

    # ---------------------------------VGG-16 Model---------------------------
    # vgg_model = vgg16_model(data)
    # #prediction for vgg16 model
    # vgg16_prediction = vgg_model.predict(np.array(test_images))
    # vgg16_image = [np.argmax(i) for i in vgg16_prediction]
    # vgg16_label = [np.argmax(i) for i in test_labels]
    # model_performance(vgg16_image, vgg16_label, "VGG-16 Model")

    #  ---------------------------------ResNet-v2 Model---------------------------
    # load saved model
    # resnet_model = keras.models.load_model('resnet_model.h5')
    # resizing the images, so it can be accepted by model
    # train_images_75 = [cv.resize(img, (75, 75)) for img in train_images]
    # val_images_75 = [cv.resize(img, (75, 75)) for img in val_images]
    # test_images_75 = [cv.resize(img, (75, 75)) for img in test_images]
    # data_75 = [train_images_75, train_labels, val_images_75, val_labels]
    # resnet_model = resnetv2_model(data_75)
    # # prediction for resnetv2 model
    # resnet_prediction = resnet_model.predict(np.array(test_images_75))
    # resnet_image = [np.argmax(i) for i in resnet_prediction]
    # resnet_label = [np.argmax(i) for i in test_labels]
    # model_performance(resnet_image, resnet_label, "ResNet-v2 Model")

    # -------------------------- Hand Detection & Tracking -------------------------
    # parameters for video window
    win_width = 1200
    win_height = 700
    win_brightness = 100
    # adding webcam
    cam = cv.VideoCapture(0)
    # set width
    cam.set(3, win_width)
    # set height
    cam.set(4, win_height)
    # set brightness
    cam.set(10, win_brightness)
    # initializing the hands class
    mp_hand = mp.solutions.hands
    # setting the hands function to hold the landmarks points
    hands = mp_hand.Hands(max_num_hands=1, min_detection_confidence=0.8)
    # setting up the drawing function
    mp_draw = mp.solutions.drawing_utils
    # from the webcam getting the frame dimensions
    _, frame = cam.read()
    height, width, _ = frame.shape
    # show video
    while cam.isOpened():
        # from the webcam getting the frame
        _, frame = cam.read()
        # flipping the image
        frame = cv.flip(frame, 1)
        # converting BGR to RGB order
        frame_RGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        # finding hand
        hand = hands.process(frame_RGB)
        # finding landmarks
        landmarks = hand.multi_hand_landmarks
        # crop hand image for passing it to classifier
        cropped_hand = np.empty((0, 0))
        # finding coordinates in order to draw rectangle around hand
        if landmarks:
            for hand_lms in landmarks:
                Xmax = 0
                Ymax = 0
                Xmin = width
                Ymin = height
                for lm in hand_lms.landmark:
                    # initial landmarks point
                    x_cor, y_cor = int(lm.x * width), int(lm.y * height)
                    if x_cor > Xmax:
                        Xmax = x_cor
                    if x_cor < Xmin:
                        Xmin = x_cor
                    if y_cor > Ymax:
                        Ymax = y_cor
                    if y_cor < Ymin:
                        Ymin = y_cor
                # drawing rectangle around hand
                cv.rectangle(frame, (Xmin - 60, Ymin - 60), (Xmax + 60, Ymax + 60), (15, 196, 241), 3)
                # cropped the hand out of image
                cropped_hand = frame[Ymin - 60:Ymax + 60, Xmin - 60:Xmax + 60]
                # drawing landmarks
                # mp_draw.draw_landmarks(frame, hand_lms, mp_hand.HAND_CONNECTIONS)

        # if hand is available in the image then process it pre-processing did on train dataset, then pass it to classifier
        if len(cropped_hand) != 0 and cropped_hand.shape[1] > 0:
            # converting BGR to grayscale
            cropped_hand = cv.cvtColor(cropped_hand, cv.COLOR_BGR2GRAY)
            # resizing the image so it meets the classifier standard
            cropped_hand = cv.resize(cropped_hand, (32, 32))
            # plt.imshow(cropped_hand, cmap='gray')
            # plt.xticks([])
            # plt.yticks([])
            # plt.show()
            # preparing the hand image for passing it to model
            img_array = keras.utils.img_to_array(cropped_hand)
            img_array = tf.expand_dims(img_array, 0)
            prediction = cnn_model.predict(img_array)
            print('prediction',prediction)
            score = tf.nn.softmax(prediction)
            print('score',score)
            print('labels',test_labels[np.argmax(np.array(score))])
            # print(
            #     "This image most likely belongs to {} with a {:.2f} percent confidence."
            #     .format(test_labels[np.argmax(score)], 100 * np.max(score)))
            gestures = list(test_labels[np.argmax(score)])
            if (gestures[0]==1 or gestures[1]==1):
                volume_control(gestures, frame)

        # show frame
        cv.imshow('Frame', frame)
        # delay of 1ms and by close the window by pressing q
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()