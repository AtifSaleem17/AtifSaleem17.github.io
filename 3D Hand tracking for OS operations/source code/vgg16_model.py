# importing libraries
from keras.applications import VGG16
from keras.layers import Flatten, Dense
from keras.models import Model
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

def vgg16_model(dataset):
    # ----------------------------Loading Dataset-------------------
    train_images, train_labels, test_images, test_labels = dataset
    # ------------------------------------Model-----------------------------
    model = VGG16(include_top=False, input_shape=(32, 32, 3))
    # extending last layers into the model
    flatten = Flatten()(model.layers[-1].output)
    layer1 = Dense(150, activation='relu')(flatten)
    layer2 = Dense(15, activation='relu')(layer1)
    output_layer = Dense(4, activation='softmax')(layer2)
    model = Model(inputs=model.inputs, outputs=output_layer)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # ------------------------------------Summary-----------------------------------
    model.summary()
    epochs = 10
    # ------------------------------------Training-----------------------------------
    history = model.fit(np.array(train_images), train_labels, epochs=epochs,
                        validation_data=(np.array(test_images), test_labels), batch_size=10)
    # ----------------------------------- Saving model ---------------------------
    model.save('vgg_model.h5')
    # ------------------------------------Plotting-----------------------------------
    plt.plot(range(epochs), history.history['accuracy'], label="Accuracy")
    plt.plot(range(epochs), history.history['val_accuracy'], label="val_accuracy")
    plt.plot(range(epochs), history.history['loss'], label="Loss")
    plt.plot(range(epochs), history.history['val_loss'], label="Val_loss")
    plt.title("VGG-16 Performance")
    plt.xlabel("Epochs")
    plt.ylabel("Rate")
    plt.legend(loc='center right')
    plt.show()
    return model