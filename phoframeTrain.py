import tensorflow as tf
import numpy as np
from scipy import misc
import random
import math
import os

TRAIN_SET_START = 14
TRAIN_SET_END = 120000

TEST_SET_START = 120030
TEST_SET_END = 131030

phoframeFile = open("/media/rob/Ma Book1/CS 230/videoToVoice/3/phoframes.txt","r") 

phoframes = phoframeFile.read().split("\n")

FOLDER_SAVE_NAME = "phoframe41"

if not os.path.exists(FOLDER_SAVE_NAME):
    os.makedirs(FOLDER_SAVE_NAME)

if not os.path.exists(FOLDER_SAVE_NAME+"/samples"):
    os.makedirs(FOLDER_SAVE_NAME+"/samples")

if not os.path.exists(FOLDER_SAVE_NAME+"/models"):
    os.makedirs(FOLDER_SAVE_NAME+"/models")

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def getRandomFrame(isTraining):
    if isTraining:
       f = int(math.floor(random.randrange(TRAIN_SET_START, TRAIN_SET_END)))
       while not isFValid(f):  # Exclude portions of the video with no visible mouth
           f = int(math.floor(random.randrange(TRAIN_SET_START, TRAIN_SET_END)))
       return f
    else:
       f = int(math.floor(random.randrange(TEST_SET_START, TEST_SET_END)))
       while not isFValid(f):  # Exclude portions of the video with no visible mouth
           f = int(math.floor(random.randrange(TEST_SET_START, TEST_SET_END)))
       return f


def isFValid(f):
    for nearF in range(f-14,f+15):
        strIndex = str(nearF)
        while len(strIndex) < 4:
            strIndex = "0"+strIndex
        if not os.path.exists('3/mouthImages/frame'+strIndex+'.jpg'):
            return False
    return True # As of now, i can't remember where the invalid frames are.

def getInVidsAtFrame(f):
    arr = np.zeros([1, INVID_HEIGHT,INVID_WIDTH,INVID_DEPTH])
    for imageIndex in range(0,29):
        strIndex = str(f-14+imageIndex)
        while len(strIndex) < 4:
            strIndex = "0"+strIndex
        newImage = misc.imread('3/mouthImages/frame'+strIndex+'.jpg')

        if newImage.shape[0] > INVID_HEIGHT:
            extraMargin = (newImage.shape[0]-INVID_HEIGHT)//2
            newImage = newImage[extraMargin:extraMargin+INVID_HEIGHT,:,:]
        if newImage.shape[1] > INVID_WIDTH:
            extraMargin = (newImage.shape[1]-INVID_WIDTH)//2
            newImage = newImage[:,extraMargin:extraMargin+INVID_WIDTH,:]

        h = newImage.shape[0]
        w = newImage.shape[1]
        yStart = (INVID_HEIGHT-h)//2
        xStart = (INVID_WIDTH-w)//2
        arr[:,yStart:yStart+h,xStart:xStart+w,imageIndex*3:(imageIndex+1)*3] = newImage
    return np.asarray(arr)/255.0

def getLabelsAtFrame(f):
  return int(phoframes[f])

INVID_WIDTH = 256 # mouth width
INVID_HEIGHT = 256 # mouth height
INVID_DEPTH = 87 # 29 images of R, G, B

PHONEME_CATEGORIES = 41

learning_rate = 0.0002

invids_ = tf.placeholder(tf.float32, (None, INVID_HEIGHT, INVID_WIDTH, INVID_DEPTH), name='invids')
labels_ = tf.placeholder(tf.int32, (None), name='labels')

### Encode the invids
conv1 = tf.layers.conv2d(inputs=invids_, filters=40, kernel_size=(5,5), strides=(2,2), padding='same', activation=tf.nn.relu)
# Now 128x128x40
maxpool1 = tf.layers.max_pooling2d(conv1, pool_size=2, strides=(2,2), padding='same')
# Now 64x64x40
conv2 = tf.layers.conv2d(inputs=maxpool1, filters=70, kernel_size=(5,5), padding='same', activation=tf.nn.relu)
# Now 64x64x70
maxpool2 = tf.layers.max_pooling2d(conv2, pool_size=2, strides=(2,2), padding='same')
# Now 32x32x70
conv3 = tf.layers.conv2d(inputs=maxpool2, filters=100, kernel_size=(5,5), padding='same', activation=tf.nn.relu)
# Now 32x32x100
maxpool3 = tf.layers.max_pooling2d(conv3, pool_size=2, strides=(2,2), padding='same')
# Now 16x16x100
conv4 = tf.layers.conv2d(inputs=maxpool3, filters=130, kernel_size=(5,5), padding='same', activation=tf.nn.relu)
# Now 16x16x130
maxpool4 = tf.layers.max_pooling2d(conv4, pool_size=4, strides=(4,4), padding='same')
# Now 4x4x130 (flatten to 2080)

maxpool4_flat = tf.reshape(maxpool4, [-1,4*4*130])
# Now 2080

W_fc1 = weight_variable([2080, 1000])
b_fc1 = bias_variable([1000])
fc1 = tf.nn.relu(tf.matmul(maxpool4_flat, W_fc1) + b_fc1)

W_fc2 = weight_variable([1000, 300])
b_fc2 = bias_variable([300])
fc2 = tf.nn.relu(tf.matmul(fc1, W_fc2) + b_fc2)

W_fc3 = weight_variable([300, PHONEME_CATEGORIES])
b_fc3 = bias_variable([PHONEME_CATEGORIES])
logits = tf.matmul(fc2, W_fc3) + b_fc3
#Now 40
onehot_labels = tf.one_hot(indices=labels_, depth=PHONEME_CATEGORIES)
loss = tf.losses.sparse_softmax_cross_entropy(labels=labels_, logits=logits)

# Get cost and define the optimizer
cost = tf.reduce_mean(loss)
opt = tf.train.AdamOptimizer(learning_rate).minimize(cost)



print("made it here! :D")
sess = tf.Session()
epochs = 2000000
batch_size = 50

test_batch_size = 10

MODEL_SAVE_EVERY = 50
SAVE_FILE_START_POINT = 0

saver = tf.train.Saver()

sess.run(tf.global_variables_initializer())

if SAVE_FILE_START_POINT >= 1:
    saver.restore(sess,  FOLDER_SAVE_NAME+"/models/model"+str(SAVE_FILE_START_POINT)+".ckpt")

f= open(FOLDER_SAVE_NAME+"/lossOverTime.txt","a")
f.write("Epoch\tTrain Loss\tTest Loss\n")
f.close()

print("about to start...")
for e in range(SAVE_FILE_START_POINT, epochs):

    invids = np.empty([50,INVID_HEIGHT,INVID_WIDTH,INVID_DEPTH])
    labels = np.empty(50)

    for x in range(0,50):
        frameIndex = getRandomFrame(True)
        invids[x] = getInVidsAtFrame(frameIndex)
        labels[x] = getLabelsAtFrame(frameIndex)

    train_loss, _, _logits = sess.run([cost, opt, logits],
       feed_dict={invids_: invids, labels_: labels}) # """inspecs_: inspecs,"""

    


    invids = np.empty([10,INVID_HEIGHT,INVID_WIDTH,INVID_DEPTH])
    labels = np.empty(10)

    for x in range(0,10):
        frameIndex = getRandomFrame(False)
        invids[x] = getInVidsAtFrame(frameIndex)
        labels[x] = getLabelsAtFrame(frameIndex)

    test_loss, _logits = sess.run([cost, logits],
       feed_dict={invids_: invids, labels_: labels}) # """inspecs_: inspecs,"""

    print("Epoch: {}/{}...".format(e, epochs), "Training loss: {:.4f}".format(train_loss), "Test loss: {:.4f}".format(test_loss))
    
    f= open(FOLDER_SAVE_NAME+"/lossOverTime.txt","a+")
    f.write(str(e)+"\t"+str(train_loss)+"\t"+str(test_loss)+"\n")
    f.close()
    
    if (e)%MODEL_SAVE_EVERY == 0:
        save_path = saver.save(sess, FOLDER_SAVE_NAME+"/models/model"+str(e)+".ckpt")
        print("MODEL SAVED, BRO: "+str(save_path))
