Python 3.11.5 (tags/v3.11.5:cce6ba9, Aug 24 2023, 14:38:34) [MSC v.1936 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "a3573a47-3689-4668-b62f-5c8451b2b4e9",
   "metadata": {
    "tags": []
   },
   "source": [
    "# 0. Install and Import Dependencies"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ddfbccbe-41ae-4c23-98b1-a13868e2b499",
   "metadata": {
    "scrolled": true,
    "tags": []
   },
   "outputs": [],
   "source": [
    "!pip list"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "02f907ea-f669-46c7-adcf-7f257e663448",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "!pip install opencv-python matplotlib imageio gdown tensorflow"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b24af50c-20b8-409d-ad78-30a933fdd669",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "import os\n",
    "import cv2\n",
    "import tensorflow as tf\n",
    "import numpy as np\n",
    "from typing import List\n",
    "from matplotlib import pyplot as plt\n",
    "import imageio"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1e3db0b0-e559-4ad6-91fd-e7414b7d75e6",
   "metadata": {},
   "outputs": [],
   "source": [
    "tf.config.list_physical_devices('GPU')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "378d045a-3003-4f93-b7d2-a25a97774a68",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "physical_devices = tf.config.list_physical_devices('GPU')\n",
    "try:\n",
    "    tf.config.experimental.set_memory_growth(physical_devices[0], True)\n",
    "except:\n",
    "    pass"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "7a19e88e-c7b9-45c1-ae1e-f2109329c71b",
   "metadata": {
    "tags": []
   },
   "source": [
    "# 1. Build Data Loading Functions"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8fb99c90-e05a-437f-839d-6e772f8c1dd5",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "import gdown"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c019e4c6-2af3-4160-99ea-5c8cb009f1a7",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "url = 'https://drive.google.com/uc?id=1YlvpDLix3S-U8fd-gqRwPcWXAXm8JwjL'\n",
    "output = 'data.zip'\n",
    "gdown.download(url, output, quiet=False)\n",
    "gdown.extractall('data.zip')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8548cc59-6dfc-4acc-abc3-3e65212db02e",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "def load_video(path:str) -> List[float]: \n",
    "\n",
    "    cap = cv2.VideoCapture(path)\n",
    "    frames = []\n",
    "    for _ in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))): \n",
    "        ret, frame = cap.read()\n",
    "        frame = tf.image.rgb_to_grayscale(frame)\n",
    "        frames.append(frame[190:236,80:220,:])\n",
    "    cap.release()\n",
    "    \n",
    "    mean = tf.math.reduce_mean(frames)\n",
    "    std = tf.math.reduce_std(tf.cast(frames, tf.float32))\n",
    "    return tf.cast((frames - mean), tf.float32) / std"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ec735e0b-ec98-4eb0-8f49-c35527d6670a",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "vocab = [x for x in \"abcdefghijklmnopqrstuvwxyz'?!123456789 \"]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "be04e972-d7a5-4a72-82d8-a6bdde1f3ce6",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "char_to_num = tf.keras.layers.StringLookup(vocabulary=vocab, oov_token=\"\")\n",
    "num_to_char = tf.keras.layers.StringLookup(\n",
    "    vocabulary=char_to_num.get_vocabulary(), oov_token=\"\", invert=True\n",
    ")\n",
    "\n",
    "print(\n",
    "    f\"The vocabulary is: {char_to_num.get_vocabulary()} \"\n",
    "    f\"(size ={char_to_num.vocabulary_size()})\"\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "559f7420-6802-45fa-9ca0-b1ff209b461c",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "char_to_num.get_vocabulary()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "797ff78b-b48f-4e14-bb62-8cd0ebf9501a",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "char_to_num(['n','i','c','k'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8cd7f4f4-ae77-4509-a4f4-c723787ebad1",
   "metadata": {},
   "outputs": [],
   "source": [
    "num_to_char([14,  9,  3, 11])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9491bab5-6a3c-4f79-879a-8f9fbe73ae2e",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "def load_alignments(path:str) -> List[str]: \n",
    "    with open(path, 'r') as f: \n",
    "        lines = f.readlines() \n",
    "    tokens = []\n",
    "    for line in lines:\n",
    "        line = line.split()\n",
    "        if line[2] != 'sil': \n",
    "            tokens = [*tokens,' ',line[2]]\n",
    "    return char_to_num(tf.reshape(tf.strings.unicode_split(tokens, input_encoding='UTF-8'), (-1)))[1:]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "dd01ca9f-77fb-4643-a2aa-47dd82c5d66b",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "def load_data(path: str): \n",
    "    path = bytes.decode(path.numpy())\n",
    "    #file_name = path.split('/')[-1].split('.')[0]\n",
    "    # File name splitting for windows\n",
    "    file_name = path.split('\\\\')[-1].split('.')[0]\n",
    "    video_path = os.path.join('data','s1',f'{file_name}.mpg')\n",
    "    alignment_path = os.path.join('data','alignments','s1',f'{file_name}.align')\n",
    "    frames = load_video(video_path) \n",
    "    alignments = load_alignments(alignment_path)\n",
    "    \n",
    "    return frames, alignments"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8cb7cc58-31ae-4904-a805-1177a82717d2",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "test_path = '.\\\\data\\\\s1\\\\bbal6n.mpg'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "76aa964f-0c84-490d-897a-d00e3966e2c9",
   "metadata": {},
   "outputs": [],
   "source": [
    "tf.convert_to_tensor(test_path).numpy().decode('utf-8').split('\\\\')[-1].split('.')[0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "eb602c71-8560-4f9e-b26b-08202febb937",
   "metadata": {
    "scrolled": true,
    "tags": []
   },
   "outputs": [],
   "source": [
    "frames, alignments = load_data(tf.convert_to_tensor(test_path))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0e3184a1-6b02-4b4f-84a8-a0a65f951ea2",
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.imshow(frames[40])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d7ec0833-d54b-4073-84cf-92d011c60ec1",
   "metadata": {},
   "outputs": [],
   "source": [
    "alignments"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fe1ad370-b287-4b46-85a2-7c45b0bd9b10",
   "metadata": {},
   "outputs": [],
   "source": [
    "tf.strings.reduce_join([bytes.decode(x) for x in num_to_char(alignments.numpy()).numpy()])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6871031a-b0ba-4c76-a852-f6329b0f2606",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "def mappable_function(path:str) ->List[str]:\n",
    "    result = tf.py_function(load_data, [path], (tf.float32, tf.int64))\n",
    "    return result"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c40a7eb4-0c3e-4eab-9291-5611cb68ce08",
   "metadata": {
    "tags": []
   },
   "source": [
    "# 2. Create Data Pipeline"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7686355d-45aa-4c85-ad9c-053e6a9b4d81",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "from matplotlib import pyplot as plt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f066fea2-91b1-42ed-a67d-00566a1a53ff",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "data = tf.data.Dataset.list_files('./data/s1/*.mpg')\n",
    "data = data.shuffle(500, reshuffle_each_iteration=False)\n",
    "data = data.map(mappable_function)\n",
    "data = data.padded_batch(2, padded_shapes=([75,None,None,None],[40]))\n",
    "data = data.prefetch(tf.data.AUTOTUNE)\n",
    "# Added for split \n",
    "train = data.take(450)\n",
    "test = data.skip(450)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6b1365bd-7742-41d1-95d4-247021751c3a",
   "metadata": {},
   "outputs": [],
   "source": [
    "len(test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5281bde8-fdc8-4da1-bd55-5a7929a9e80c",
   "metadata": {},
   "outputs": [],
   "source": [
    "frames, alignments = data.as_numpy_iterator().next()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "cbebe683-6afd-47fd-bba4-c83b4b13bb32",
   "metadata": {},
   "outputs": [],
   "source": [
    "len(frames)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5cf2d676-93a9-434c-b3c7-bdcc2577b2e7",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "sample = data.as_numpy_iterator()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "efa6cd46-7079-46c0-b45b-832f339f6cb0",
   "metadata": {
    "scrolled": true,
    "tags": []
   },
   "outputs": [],
   "source": [
    "val = sample.next(); val[0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "acf5eb4f-a0da-4a9a-bf24-af13e9cc2fbe",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "imageio.mimsave('./animation.gif', val[0][0], fps=10)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "id": "c33a87a2-d5e0-4ec9-b174-73ebf41bf03a",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.image.AxesImage at 0x10c2ead8d30>"
      ]
     },
     "execution_count": 34,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 640x480 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# 0:videos, 0: 1st video out of the batch,  0: return the first frame in the video \n",
    "plt.imshow(val[0][0][35])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "id": "84593332-133c-4205-b7a6-8e235d5e2b3b",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<tf.Tensor: shape=(), dtype=string, numpy=b'lay blue by e two please'>"
      ]
     },
     "execution_count": 35,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "tf.strings.reduce_join([num_to_char(word) for word in val[1][0]])"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "0f47733c-83bc-465c-b118-b198b492ad37",
   "metadata": {
    "tags": []
   },
   "source": [
    "# 3. Design the Deep Neural Network"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "id": "d8e9a497-191b-4842-afbd-26f5e13c43ba",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "from tensorflow.keras.models import Sequential \n",
    "from tensorflow.keras.layers import Conv3D, LSTM, Dense, Dropout, Bidirectional, MaxPool3D, Activation, Reshape, SpatialDropout3D, BatchNormalization, TimeDistributed, Flatten\n",
    "from tensorflow.keras.optimizers import Adam\n",
    "from tensorflow.keras.callbacks import ModelCheckpoint, LearningRateScheduler"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "id": "3f753ed2-70b9-4236-8c1c-08ca065dc8bf",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(75, 46, 140, 1)"
      ]
     },
     "execution_count": 37,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data.as_numpy_iterator().next()[0][0].shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "id": "f9171056-a352-491a-9ed9-92b28ced268e",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "model = Sequential()\n",
    "model.add(Conv3D(128, 3, input_shape=(75,46,140,1), padding='same'))\n",
    "model.add(Activation('relu'))\n",
    "model.add(MaxPool3D((1,2,2)))\n",
    "\n",
    "model.add(Conv3D(256, 3, padding='same'))\n",
    "model.add(Activation('relu'))\n",
    "model.add(MaxPool3D((1,2,2)))\n",
    "\n",
    "model.add(Conv3D(75, 3, padding='same'))\n",
    "model.add(Activation('relu'))\n",
    "model.add(MaxPool3D((1,2,2)))\n",
    "\n",
    "model.add(TimeDistributed(Flatten()))\n",
    "\n",
    "model.add(Bidirectional(LSTM(128, kernel_initializer='Orthogonal', return_sequences=True)))\n",
    "model.add(Dropout(.5))\n",
    "\n",
    "model.add(Bidirectional(LSTM(128, kernel_initializer='Orthogonal', return_sequences=True)))\n",
    "model.add(Dropout(.5))\n",
    "\n",
    "model.add(Dense(char_to_num.vocabulary_size()+1, kernel_initializer='he_normal', activation='softmax'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "id": "78851825-2bcd-42a9-b7f2-28bb5a6bf43a",
   "metadata": {
    "collapsed": true,
    "jupyter": {
     "outputs_hidden": true
    },
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Model: \"sequential\"\n",
      "_________________________________________________________________\n",
      " Layer (type)                Output Shape              Param #   \n",
      "=================================================================\n",
      " conv3d (Conv3D)             (None, 75, 46, 140, 128)  3584      \n",
      "                                                                 \n",
      " activation (Activation)     (None, 75, 46, 140, 128)  0         \n",
      "                                                                 \n",
      " max_pooling3d (MaxPooling3D  (None, 75, 23, 70, 128)  0         \n",
      " )                                                               \n",
      "                                                                 \n",
      " conv3d_1 (Conv3D)           (None, 75, 23, 70, 256)   884992    \n",
      "                                                                 \n",
      " activation_1 (Activation)   (None, 75, 23, 70, 256)   0         \n",
      "                                                                 \n",
      " max_pooling3d_1 (MaxPooling  (None, 75, 11, 35, 256)  0         \n",
      " 3D)                                                             \n",
      "                                                                 \n",
      " conv3d_2 (Conv3D)           (None, 75, 11, 35, 75)    518475    \n",
      "                                                                 \n",
      " activation_2 (Activation)   (None, 75, 11, 35, 75)    0         \n",
      "                                                                 \n",
      " max_pooling3d_2 (MaxPooling  (None, 75, 5, 17, 75)    0         \n",
      " 3D)                                                             \n",
      "                                                                 \n",
      " time_distributed (TimeDistr  (None, 75, 6375)         0         \n",
      " ibuted)                                                         \n",
      "                                                                 \n",
      " bidirectional (Bidirectiona  (None, 75, 256)          6660096   \n",
      " l)                                                              \n",
      "                                                                 \n",
      " dropout (Dropout)           (None, 75, 256)           0         \n",
      "                                                                 \n",
      " bidirectional_1 (Bidirectio  (None, 75, 256)          394240    \n",
      " nal)                                                            \n",
      "                                                                 \n",
      " dropout_1 (Dropout)         (None, 75, 256)           0         \n",
      "                                                                 \n",
      " dense (Dense)               (None, 75, 41)            10537     \n",
      "                                                                 \n",
      "=================================================================\n",
      "Total params: 8,471,924\n",
      "Trainable params: 8,471,924\n",
      "Non-trainable params: 0\n",
      "_________________________________________________________________\n"
     ]
    }
   ],
   "source": [
    "model.summary()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f4b4798c-a65a-4c47-9e2a-3b09dc98d320",
   "metadata": {},
   "outputs": [],
   "source": [
    "5*17*75"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "id": "e5c2eae0-c359-41a4-97a0-75c44dccb7d1",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "1/1 [==============================] - 3s 3s/step\n"
     ]
    }
   ],
   "source": [
    "yhat = model.predict(val[0])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "id": "ffdc7319-0d69-4f7e-a6d4-ce72deb81c0b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<tf.Tensor: shape=(), dtype=string, numpy=b'444iiiiiiiiiiiiiimmmmmmmmmmmmmmmmmmmmmmiiiiiiiiiiimmmmmmmmiiiiiiiiiiixxxxxx'>"
      ]
     },
     "execution_count": 41,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "tf.strings.reduce_join([num_to_char(x) for x in tf.argmax(yhat[0],axis=1)])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "id": "6ed47531-8317-4255-9a12-b757642258e6",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<tf.Tensor: shape=(), dtype=string, numpy=b'444iiiiiiiiiiiiiimmmmmmmmmmmmmmmmmmmmmmiiiiiiiiiiimmmmmmmmiiiiiiiiiiixxxxxx'>"
      ]
     },
     "execution_count": 42,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "tf.strings.reduce_join([num_to_char(tf.argmax(x)) for x in yhat[0]])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "id": "7c37b9b9-5298-4038-9c33-5031d1b457f0",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(None, 75, 46, 140, 1)"
      ]
     },
     "execution_count": 43,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "model.input_shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "id": "98b316a4-5322-4782-8e36-4b3c1a696d85",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(None, 75, 41)"
      ]
     },
     "execution_count": 44,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "model.output_shape"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "2ec02176-5c26-46c3-aff7-8352e6563c7d",
   "metadata": {
    "tags": []
   },
   "source": [
    "# 4. Setup Training Options and Train"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "id": "ab015fd0-7fb4-4d5d-9fa2-30a05dbd515a",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "def scheduler(epoch, lr):\n",
    "    if epoch < 30:\n",
    "        return lr\n",
    "    else:\n",
    "        return lr * tf.math.exp(-0.1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "id": "c564d5c9-db54-4e88-b311-9aeab7fb3e69",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "def CTCLoss(y_true, y_pred):\n",
    "    batch_len = tf.cast(tf.shape(y_true)[0], dtype=\"int64\")\n",
    "    input_length = tf.cast(tf.shape(y_pred)[1], dtype=\"int64\")\n",
    "    label_length = tf.cast(tf.shape(y_true)[1], dtype=\"int64\")\n",
    "\n",
    "    input_length = input_length * tf.ones(shape=(batch_len, 1), dtype=\"int64\")\n",
    "    label_length = label_length * tf.ones(shape=(batch_len, 1), dtype=\"int64\")\n",
    "\n",
    "    loss = tf.keras.backend.ctc_batch_cost(y_true, y_pred, input_length, label_length)\n",
    "    return loss"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 47,
   "id": "a26dc3fc-a19c-4378-bd8c-e2b597a1d15c",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "class ProduceExample(tf.keras.callbacks.Callback): \n",
    "    def __init__(self, dataset) -> None: \n",
    "        self.dataset = dataset.as_numpy_iterator()\n",
    "    \n",
    "    def on_epoch_end(self, epoch, logs=None) -> None:\n",
    "        data = self.dataset.next()\n",
    "        yhat = self.model.predict(data[0])\n",
    "        decoded = tf.keras.backend.ctc_decode(yhat, [75,75], greedy=False)[0][0].numpy()\n",
    "        for x in range(len(yhat)):           \n",
    "            print('Original:', tf.strings.reduce_join(num_to_char(data[1][x])).numpy().decode('utf-8'))\n",
    "            print('Prediction:', tf.strings.reduce_join(num_to_char(decoded[x])).numpy().decode('utf-8'))\n",
    "            print('~'*100)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 48,
   "id": "04be90d8-2482-46f9-b513-d5f4f8001c7e",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "model.compile(optimizer=Adam(learning_rate=0.0001), loss=CTCLoss)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 49,
   "id": "eab49367-3f1e-4464-ae76-dbd07549d97e",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "checkpoint_callback = ModelCheckpoint(os.path.join('models','checkpoint'), monitor='loss', save_weights_only=True) "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 50,
   "id": "e085a632-d464-46ef-8777-959cad4adb2c",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "schedule_callback = LearningRateScheduler(scheduler)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 51,
   "id": "48eca991-90ab-4592-8a79-b50e9ca015b6",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "example_callback = ProduceExample(test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 52,
   "id": "8ffba483-aa61-4bbe-a15f-a73e1ddf097c",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Epoch 1/100\n",
      "  2/450 [..............................] - ETA: 3:03 - loss: 213.9969 "
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\n",
      "KeyboardInterrupt\n",
      "\n"
     ]
    }
   ],
   "source": [
    "model.fit(train, validation_data=test, epochs=100, callbacks=[checkpoint_callback, schedule_callback, example_callback])"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "fa8ee94b-89f7-4733-8a0c-a86f86ff590a",
   "metadata": {
    "tags": []
   },
   "source": [
    "# 5. Make a Prediction "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "01fa7204-ce0e-49a8-8dbd-14fe5dfead40",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "url = 'https://drive.google.com/uc?id=1vWscXs4Vt0a_1IH1-ct2TCgXAZT-N3_Y'\n",
    "output = 'checkpoints.zip'\n",
    "gdown.download(url, output, quiet=False)\n",
    "gdown.extractall('checkpoints.zip', 'models')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 53,
   "id": "247f664d-3c87-4e96-946e-930dad0e1c2c",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<tensorflow.python.checkpoint.checkpoint.CheckpointLoadStatus at 0x10cfb56c6a0>"
      ]
     },
     "execution_count": 53,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "model.load_weights('models/checkpoint')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 54,
   "id": "7f8d689f-b7bb-443c-9b88-e40c1d800828",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "test_data = test.as_numpy_iterator()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "id": "38546dc2-bee9-4837-864b-8a884df40ad7",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "sample = test_data.next()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 57,
   "id": "a43621f0-229d-4c0d-9554-9c3a3da9c61a",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "1/1 [==============================] - 1s 973ms/step\n"
     ]
    }
   ],
   "source": [
    "yhat = model.predict(sample[0])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 58,
   "id": "ea462999-f87e-4a7e-a057-5be7b6d8f7d5",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ REAL TEXT\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "[<tf.Tensor: shape=(), dtype=string, numpy=b'place white at x six please'>,\n",
       " <tf.Tensor: shape=(), dtype=string, numpy=b'lay blue in x four now'>]"
      ]
     },
     "execution_count": 58,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "print('~'*100, 'REAL TEXT')\n",
    "[tf.strings.reduce_join([num_to_char(word) for word in sentence]) for sentence in sample[1]]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 59,
   "id": "82bd4c10-dd6e-411e-834b-2a3b43fd12c5",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "decoded = tf.keras.backend.ctc_decode(yhat, input_length=[75,75], greedy=True)[0][0].numpy()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 60,
   "id": "5d68ac46-c90b-4eab-a709-f19aee569ff5",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PREDICTIONS\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "[<tf.Tensor: shape=(), dtype=string, numpy=b'place white at x six please'>,\n",
       " <tf.Tensor: shape=(), dtype=string, numpy=b'lay blue in x four now'>]"
      ]
     },
     "execution_count": 60,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "print('~'*100, 'PREDICTIONS')\n",
    "[tf.strings.reduce_join([num_to_char(word) for word in sentence]) for sentence in decoded]"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "64622f98-e99b-4fed-a2cc-f0da82eb5431",
   "metadata": {},
   "source": [
    "# Test on a Video"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 61,
   "id": "a8b0c4d0-2031-4331-b91d-d87b1ae6f6e2",
   "metadata": {},
   "outputs": [],
   "source": [
    "sample = load_data(tf.convert_to_tensor('.\\\\data\\\\s1\\\\bras9a.mpg'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 62,
   "id": "0cca60e4-47a9-4683-8a75-48f4684f723d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ REAL TEXT\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "[<tf.Tensor: shape=(), dtype=string, numpy=b'bin red at s nine again'>]"
      ]
     },
     "execution_count": 62,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "print('~'*100, 'REAL TEXT')\n",
    "[tf.strings.reduce_join([num_to_char(word) for word in sentence]) for sentence in [sample[1]]]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 63,
   "id": "8cc5037c-1e32-435c-b0cc-01e1fb3b863c",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "1/1 [==============================] - 1s 720ms/step\n"
     ]
    }
   ],
...    "source": [
...     "yhat = model.predict(tf.expand_dims(sample[0], axis=0))"
...    ]
...   },
...   {
...    "cell_type": "code",
...    "execution_count": 64,
...    "id": "22c4f77d-715d-409f-bc5e-3ebe48704e8f",
...    "metadata": {},
...    "outputs": [],
...    "source": [
...     "decoded = tf.keras.backend.ctc_decode(yhat, input_length=[75], greedy=True)[0][0].numpy()"
...    ]
...   },
...   {
...    "cell_type": "code",
...    "execution_count": 65,
...    "id": "e4d12ecc-b634-499e-a4bc-db9f010835fb",
...    "metadata": {},
...    "outputs": [
...     {
...      "name": "stdout",
...      "output_type": "stream",
...      "text": [
...       "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PREDICTIONS\n"
...      ]
...     },
...     {
...      "data": {
...       "text/plain": [
...        "[<tf.Tensor: shape=(), dtype=string, numpy=b'bin red at s nine again'>]"
...       ]
...      },
...      "execution_count": 65,
...      "metadata": {},
...      "output_type": "execute_result"
...     }
...    ],
   "source": [
    "print('~'*100, 'PREDICTIONS')\n",
    "[tf.strings.reduce_join([num_to_char(word) for word in sentence]) for sentence in decoded]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "551dfea2-de6b-4400-b71a-a17631529e3f",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fa95863d-3832-47bf-8a77-ebaa38054ace",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "lips",
   "language": "python",
   "name": "lips"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
