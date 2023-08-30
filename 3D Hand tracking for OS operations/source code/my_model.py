import numpy as np
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.models import Sequential
import matplotlib.pyplot as plt


def my_model(dataset):
    # ----------------------------Loading Dataset-------------------
    train_images, train_labels, test_images, test_labels = dataset
    # print(np.unique(train_labels))
    # print(test_labels[0])
    # ------------------------------------Model-----------------------------
    model = Sequential()
    # first layer
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 1), padding='same'))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D((2, 2), padding='same'))
    model.add(Dropout(0.5))
    # second layer
    model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D((2, 2), padding='same'))
    model.add(Dropout(0.5))
    # third layer
    model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D((2, 2), padding='same'))
    model.add(Dropout(0.5))
    # fourth layer
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    # output layer
    model.add(Dense(4, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # ------------------------------------Summary-----------------------------------
    model.summary()
    epochs = 20
    # ------------------------------------Training-----------------------------------
    history = model.fit(np.array(train_images), train_labels, epochs=epochs, batch_size=10,
                        validation_data=(np.array(test_images), test_labels))
    # ----------------------------------- Saving model ---------------------------
    model.save('cnn_model3.h5')
    # ------------------------------------Plotting-----------------------------------
    plt.plot(range(epochs), history.history['accuracy'], label="Accuracy")
    plt.plot(range(epochs), history.history['val_accuracy'], label="val_accuracy")
    plt.plot(range(epochs), history.history['loss'], label="Loss")
    plt.plot(range(epochs), history.history['val_loss'], label="Val_loss")
    plt.title("CNN-Model Performance")
    plt.xlabel("Epochs")
    plt.ylabel("Rate")
    plt.legend(loc='upper right')
    plt.savefig('Cnn graph.jpg')
    plt.show()
    return model
