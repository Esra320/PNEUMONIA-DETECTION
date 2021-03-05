# -*- coding: utf-8 -*-
"""cnn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GviYnT8j-lWwhvLgZ9K94rgMc_bE08Lx

# Veri setinin alınıp modele uygun hale getirilmesi
"""

import numpy as np
import os
from tensorflow.keras.preprocessing.image import img_to_array, load_img
DIRECTORY = r"/content/drive/MyDrive/Proje/"                # Google Drive'a yüklediğimiz veri setinin dizin yolu
CATEGORIES = ["NORMAL", "PNEUMONIA"]         # Veri setinde NORMAL ve PNEUMONIA klasörlerindeki resimlerin alınılması ve etiketlenmesi

data = []
labels = []
for category in CATEGORIES:
    path = os.path.join(DIRECTORY, category)
    for img in os.listdir(path):
      img_path = os.path.join(path, img)
      image = img_to_array(load_img(img_path, color_mode="grayscale" , target_size=(224, 224)))/255
      data.append(image)
      labels.append(category)

"""## Etiketlerin Normal : [1,0], Pneumonia: [0,1] şekilde düzenlenmesi
## Görüntülerin numpy dizisine dönüştürülmesi
## Veri seti %80 Eğitim, %20 Test olacak şekilde bölündü.
"""

from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split

lb = LabelBinarizer()
labels = lb.fit_transform(labels)
labels = to_categorical(labels)

veri = np.array(data, dtype="float32")
etiket = np.array(labels)

(trainX, testX, trainY, testY) = train_test_split(veri, etiket,
	test_size=0.20, stratify=labels, random_state=42)

"""# MODELİN OLUŞTURULMASI
## İlk olarak gerekli kütüphenelerin import edilmesi
"""

import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

batchSize = 40                  # Tek seferde 40 veri alacağız.
classes = 2                     # Normal ve Pneumonia şeklinde 2 sınıf
epoch = 15                      # 15 epoch'ta tekrarda eğitimi tamamlayağız
dataSize = trainX.shape         # Eğitim için verinin boyutları alındı.
imgRow, imgCol, channel = dataSize[1], dataSize[2], dataSize[3]

model = Sequential()

# 3x3 boyutunda 32 adet filtreden oluşan ReLU aktivasyonlu CONV katmanı eklendi. 
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(imgRow,imgCol,1)))

# 3x3 boyutunda 64 adet filtreden oluşan ReLU aktivasyonlu CONV katmanı eklendi. 
model.add(Conv2D(64, (3, 3), activation='relu'))

# 2x2 boyutlu çerçeveden oluşan MAXPOOL katmanı eklendi. 
model.add(MaxPooling2D(pool_size=(2, 2)))

# her seferinde nöronların %25'i atıldı (drop)
model.add(Dropout(0.25))

# Tam bağlantılı (fully connected) katmanına geçiş olacağı için düzleştirme yapıldı. 
model.add(Flatten())

# 128 nörondan oluşan ReLU aktivasyonu FC katmanı eklendi 
model.add(Dense(128, activation='relu'))

# Her seferinde %50'i atıldı (drop)
model.add(Dropout(0.5))

# Çıkış katmanına sınıf sayısı kadar Softmax aktivasyonlu nöron eklendi
model.add(Dense(classes, activation='softmax'))

from keras.callbacks import TensorBoard
import time
time = time.strftime("%Y_%m_%d_%H_%M_%S")

kerasboard = TensorBoard(log_dir="/tmp/tensorboard/{}".format(time),
                        batch_size=batchSize,
                        histogram_freq=1,
                        write_grads=False)



# Adadelta optimizasyon yöntemini ve cross entropy yitim (loss) fonksiyonunu kullananıldı.
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

# eğitim işlemini gerçekleştirildi
CNN_AdadeltaModel = model.fit(trainX, trainY,
          batch_size=batchSize,
          epochs=epoch,
          verbose=1,
          validation_data=(testX, testY),
          callbacks=[kerasboard])

print("tensorboard --logdir="+kerasboard.log_dir)

# Commented out IPython magic to ensure Python compatibility.
import tensorflow as tf
# %load_ext tensorboard
# %tensorboard --/tmp/tensorboard/2021_01_09_14_02_45

plt.figure(1, figsize = (10, 10))  
plt.subplot(211)  
plt.plot(CNN_AdamModel.history['accuracy'])  
plt.plot(CNN_AdamModel.history['val_accuracy'])  
plt.title('Model Accuracy')  
plt.ylabel('Accuracy')  
plt.xlabel('Epoch')  
plt.legend(['train', 'validation'], loc='upper left')   

# plotting model loss 
plt.subplot(212)  
plt.plot(CNN_AdamModel.history['loss'])  
plt.plot(CNN_AdamModel.history['val_loss'])  
plt.title('Model Loss')  
plt.ylabel('Loss')  
plt.xlabel('Epoch')  
plt.legend(['train', 'validation'], loc='upper left')  
plt.show()

# Test işlemini gerçekleştirip sonuçlar ekrana yazıldı.
score = model.evaluate(testX, testY, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

test_image=testX[360]
test_label=testY[360]
test_label

model.summary()

gecmis = model.history

print (gecmis)

model = Sequential()

# 3x3 boyutunda 32 adet filtreden oluşan ReLU aktivasyonlu CONV katmanı eklendi. 
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu',
                 input_shape=(imgRow,imgCol,1)))

# 3x3 boyutunda 64 adet filtreden oluşan ReLU aktivasyonlu CONV katmanı eklendi. 
model.add(Conv2D(64, (3, 3), activation='relu'))

# 2x2 boyutlu çerçeveden oluşan MAXPOOL katmanı eklendi. 
model.add(MaxPooling2D(pool_size=(2, 2)))

# her seferinde nöronların %25'i atıldı (drop)
model.add(Dropout(0.25))

# Tam bağlantılı (fully connected) katmanına geçiş olacağı için düzleştirme yapıldı. 
model.add(Flatten())

# 128 nörondan oluşan ReLU aktivasyonu FC katmanı eklendi 
model.add(Dense(128, activation='relu'))

# Her seferinde %50'i atıldı (drop)
model.add(Dropout(0.5))

# Çıkış katmanına sınıf sayısı kadar Softmax aktivasyonlu nöron eklendi
model.add(Dense(classes, activation='softmax'))

# Adam optimizasyon yöntemini ve cross entropy yitim (loss) fonksiyonunu kullananıldı.
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy'])
# eğitim işlemini gerçekleştirildi
CNN_AdamModel = model.fit(trainX, trainY,
          batch_size=batchSize,
          epochs=epoch,
          verbose=1,
          validation_data=(testX, testY))

plt.figure(1, figsize = (10, 10))  
plt.subplot(211)  
plt.plot(CNN_AdamModel.history['accuracy'])  
plt.plot(CNN_AdamModel.history['val_accuracy'])  
plt.title('Model Accuracy')  
plt.ylabel('Accuracy')  
plt.xlabel('Epoch')  
plt.legend(['train', 'validation'], loc='upper left')   

# plotting model loss 
plt.subplot(212)  
plt.plot(CNN_AdamModel.history['loss'])  
plt.plot(CNN_AdamModel.history['val_loss'])  
plt.title('Model Loss')  
plt.ylabel('Loss')  
plt.xlabel('Epoch')  
plt.legend(['train', 'validation'], loc='upper left')  
plt.show()

model.summary()

model = Sequential()

# 3x3 boyutunda 32 adet filtreden oluşan ReLU aktivasyonlu CONV katmanı eklendi. 
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(imgRow,imgCol,1)))

# 3x3 boyutunda 64 adet filtreden oluşan ReLU aktivasyonlu CONV katmanı eklendi. 
model.add(Conv2D(64, (3, 3), activation='relu'))

# 2x2 boyutlu çerçeveden oluşan MAXPOOL katmanı eklendi. 
model.add(MaxPooling2D(pool_size=(2, 2)))

# her seferinde nöronların %25'i atıldı (drop)
model.add(Dropout(0.25))
model.add(Conv2D(128, (3,3),activation='relu'))
model.add(Conv2D(256, (3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
# Tam bağlantılı (fully connected) katmanına geçiş olacağı için düzleştirme yapıldı. 
model.add(Flatten())

# 128 nörondan oluşan ReLU aktivasyonu FC katmanı eklendi 
model.add(Dense(128, activation='relu'))

# Her seferinde %50'i atıldı (drop)
model.add(Dropout(0.5))

# Çıkış katmanına sınıf sayısı kadar Softmax aktivasyonlu nöron eklendi
model.add(Dense(classes, activation='softmax'))

# Adadelta optimizasyon yöntemini ve cross entropy yitim (loss) fonksiyonunu kullananıldı.
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

# eğitim işlemini gerçekleştirildi
CNN_AdadeltaModel = model.fit(trainX, trainY,
          batch_size=batchSize,
          epochs=epoch,
          verbose=1,
          validation_data=(testX, testY))

plt.figure(1, figsize = (10, 10))  
plt.subplot(211)  
plt.plot(CNN_AdamModel.history['accuracy'])  
plt.plot(CNN_AdamModel.history['val_accuracy'])  
plt.title('Model Accuracy')  
plt.ylabel('Accuracy')  
plt.xlabel('Epoch')  
plt.legend(['train', 'validation'], loc='upper left')   

# plotting model loss 
plt.subplot(212)  
plt.plot(CNN_AdamModel.history['loss'])  
plt.plot(CNN_AdamModel.history['val_loss'])  
plt.title('Model Loss')  
plt.ylabel('Loss')  
plt.xlabel('Epoch')  
plt.legend(['train', 'validation'], loc='upper left')  
plt.show()

# Test işlemini gerçekleştirip sonuçlar ekrana yazıldı.
score = model.evaluate(testX, testY, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

model.summary()

model = Sequential()

# 3x3 boyutunda 32 adet filtreden oluşan ReLU aktivasyonlu CONV katmanı eklendi. 
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(imgRow,imgCol,1)))

# 3x3 boyutunda 64 adet filtreden oluşan ReLU aktivasyonlu CONV katmanı eklendi. 
model.add(Conv2D(64, (3, 3), activation='relu'))

# 2x2 boyutlu çerçeveden oluşan MAXPOOL katmanı eklendi. 
model.add(MaxPooling2D(pool_size=(2, 2)))

# her seferinde nöronların %25'i atıldı (drop)
model.add(Dropout(0.25))
model.add(Conv2D(128, (3,3),activation='relu'))
model.add(Conv2D(256, (3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
# Tam bağlantılı (fully connected) katmanına geçiş olacağı için düzleştirme yapıldı. 
model.add(Flatten())

# 128 nörondan oluşan ReLU aktivasyonu FC katmanı eklendi 
model.add(Dense(128, activation='relu'))

# Her seferinde %50'i atıldı (drop)
model.add(Dropout(0.5))

# Çıkış katmanına sınıf sayısı kadar Softmax aktivasyonlu nöron eklendi
model.add(Dense(classes, activation='softmax'))

# Adam optimizasyon yöntemini ve cross entropy yitim (loss) fonksiyonunu kullananıldı.
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy'])
# eğitim işlemini gerçekleştirildi
CNN_AdamModel = model.fit(trainX, trainY,
          batch_size=batchSize,
          epochs=epoch,
          verbose=1,
          validation_data=(testX, testY))

plt.figure(1, figsize = (10, 10))  
plt.subplot(211)  
plt.plot(CNN_AdamModel.history['accuracy'])  
plt.plot(CNN_AdamModel.history['val_accuracy'])  
plt.title('Model Accuracy')  
plt.ylabel('Accuracy')  
plt.xlabel('Epoch')  
plt.legend(['train', 'validation'], loc='upper left')   

# plotting model loss 
plt.subplot(212)  
plt.plot(CNN_AdamModel.history['loss'])  
plt.plot(CNN_AdamModel.history['val_loss'])  
plt.title('Model Loss')  
plt.ylabel('Loss')  
plt.xlabel('Epoch')  
plt.legend(['train', 'validation'], loc='upper left')  
plt.show()

# Test işlemini gerçekleştirip sonuçlar ekrana yazıldı.
score = model.evaluate(testX, testY, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

model.summary()

