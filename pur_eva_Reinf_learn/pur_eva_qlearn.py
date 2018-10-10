#!/usr/bin/env python

import rl_env_pur_eva as env
import numpy as np
import time
import skimage as skimage
import random
import numpy as np
import cv2
import time
import tensorflow as tf

from collections import deque
from skimage import transform, color, exposure
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD , Adam


ACTIONS = 359 # number of valid actions
GAMMA = 0.95 # decay rate of past observations
OBSERVATION = 50. # timesteps to observe before training
EXPLORE = 80. # frames over which to anneal epsilon
FINAL_EPSILON = 0.0005 # final value of epsilon
INITIAL_EPSILON = 0.1 # starting value of epsilon
REPLAY_MEMORY = 50000 # number of previous transitions to remember
BATCH = 30 # size of minibatch
FRAME_PER_ACTION = 1
LEARNING_RATE = 1e-4

img_rows , img_cols = 100, 100
img_channels = 4 

def buildmodel():
    print("Now we build the model")
    model = Sequential()
    model.add(Convolution2D(64, 8, 8, subsample=(4, 4), border_mode='same',input_shape=(img_rows,img_cols,img_channels)))  #80*80*4
    model.add(Activation('relu'))
    model.add(Convolution2D(128, 4, 4, subsample=(2, 2), border_mode='same'))
    model.add(Activation('relu'))
    model.add(Convolution2D(128, 3, 3, subsample=(1, 1), border_mode='same'))
    model.add(Activation('relu'))
    model.add(Flatten())
    model.add(Dense(6144))
    model.add(Activation('relu'))
    model.add(Dense(360))
   
    adam = Adam(lr=LEARNING_RATE)
    model.compile(loss='mse',optimizer=adam)
    print("We finish building the model")
    return model

def trainNetwork(model):
    game = env.pur_eva()
    D = deque()
    do_nothing = np.zeros(ACTIONS)
    do_nothing[0] = 1
    x_t, r_0, terminal = game.game_state(do_nothing[0])
    x_t = skimage.color.rgb2gray(x_t)
    x_t = skimage.transform.resize(x_t,(100,100))
    x_t = skimage.exposure.rescale_intensity(x_t,out_range=(0,255))
    x_t = x_t / 255.0
    s_t = np.stack((x_t, x_t, x_t, x_t), axis=2)
    s_t = s_t.reshape(1, s_t.shape[0], s_t.shape[1], s_t.shape[2])  #1*80*80*4
    t = 0
    OBSERVE = OBSERVATION
    epsilon = INITIAL_EPSILON
    while (True):
        loss = 0
        Q_sa = 0
        action_index = 0
        r_t = 0
        a_t = np.zeros([ACTIONS])
        #choose an action epsilon greedy
        if t % FRAME_PER_ACTION == 0:
            if random.random() <= epsilon:
                print("----------Random Action----------")
                action_index = random.randrange(ACTIONS)
                a_t[action_index] = action_index
            else:
                q = model.predict(s_t)       #input a stack of 4 images, get the prediction
                max_Q = np.argmax(q)
                action_index = max_Q
                a_t[action_index] = action_index

        #We reduced the epsilon gradually
        if epsilon > FINAL_EPSILON and t > OBSERVE:
            epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE

        #run the selected action and observed next state and reward
        x_t1_colored, r_t, terminal = game.game_state(a_t[action_index])
        x_t1 = skimage.color.rgb2gray(x_t1_colored)
        x_t1 = skimage.transform.resize(x_t1,(100,100))
        x_t1 = skimage.exposure.rescale_intensity(x_t1, out_range=(0, 255))
        x_t1 = x_t1 / 255.0
        x_t1 = x_t1.reshape(1, x_t1.shape[0], x_t1.shape[1], 1) #1x80x80x1
        s_t1 = np.append(x_t1, s_t[:, :, :, :3], axis=3)

        # store the transition in D
        D.append((s_t, action_index, r_t, s_t1, terminal))
        if len(D) > REPLAY_MEMORY:
            D.popleft()

        #only train if done observing
        if t > OBSERVE :
            #sample a minibatch to train on
            minibatch = random.sample(D, BATCH)
            #Now we do the experience replay
            state_t, action_t, reward_t, state_t1, terminal = zip(*minibatch)
            state_t = np.concatenate(state_t)
            state_t1 = np.concatenate(state_t1)
            targets = model.predict(state_t)
            Q_sa = model.predict(state_t1)
            targets[range(BATCH), action_t] = reward_t + GAMMA*np.max(Q_sa, axis=1)*np.invert(terminal)
            loss += model.train_on_batch(state_t, targets)

        s_t = s_t1
        t = t + 1
        # save progress every 10000 iterations
        if t % 200 == 0:
            print("Now we save model")
            model.save_weights("model.h5", overwrite=True)
            print(targets)

        state = ""
        if t <= OBSERVE:
            state = "observe"
        elif t > OBSERVE and t <= OBSERVE + EXPLORE:
            state = "explore"
        else:
            state = "train"

        print("TIMESTEP", t, "/ STATE", state, \
            "/ EPSILON", epsilon, "/ ACTION", action_index, "/ REWARD", r_t, \
            "/ Q_MAX " , np.max(Q_sa), "/ Loss ", loss)

    print("Episode finished!")
    print("************************")


def playGame():
    model = buildmodel()
    trainNetwork(model)

def main():
    playGame()

if __name__ == "__main__":
    sess = tf.Session()
    from keras import backend as K
    K.set_session(sess)
    main()   
    