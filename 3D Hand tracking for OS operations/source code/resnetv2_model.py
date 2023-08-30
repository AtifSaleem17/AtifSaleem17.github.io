# importing libraries
from keras.applications import InceptionResNetV2
from keras.layers import Flatten, Dense, Dropout
from keras.models import Model
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

def resnetv2_model(dataset):
    # ----------------------------Loading Dataset-------------------
    train_images, train_labels, test_images, test_labels = dataset
    # print(np.array(train_images).shape)
    # print(np.array(test_images).shape)
    # print(np.unique(train_labels))
    # print(np.unique(test_labels))
    # print(train_labels[0])
    # print(test_labels[0])

    # ------------------------------------Model-----------------------------
    model = InceptionResNetV2(include_top=False, input_shape=(75, 75, 3))

    # last layers being added to the model
    flatten = Flatten()(model.layers[-1].output)
    layer1 = Dense(150, activation='relu')(flatten)
    layer1 = Dropout(0.5)(layer1)
    layer2 = Dense(20, activation='relu')(layer1)
    output_layer = Dense(4, activation='softmax')(layer2)
    model = Model(inputs=model.inputs, outputs=output_layer)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    # ------------------------------------Summary-----------------------------------
    model.summary()
    epochs = 10
    # ------------------------------------Training-----------------------------------
    history = model.fit(np.array(train_images), train_labels, epochs=epochs,
                        validation_data=(np.array(test_images), test_labels), batch_size=10)
    model.save('resnet_model.h5')
    # ------------------------------------Plotting-----------------------------------
    plt.plot(range(epochs), history.history['accuracy'], label="Accuracy")
    plt.plot(range(epochs), history.history['val_accuracy'], label="val_accuracy")
    plt.plot(range(epochs), history.history['loss'], label="Loss")
    plt.plot(range(epochs), history.history['val_loss'], label="Val_loss")
    plt.title("ResNet-v2 Performance")
    plt.xlabel("Epochs")
    plt.ylabel("Rate")
    plt.legend(loc='center right')
    plt.savefig('resnet graph.jpg')
    plt.show()
    return model