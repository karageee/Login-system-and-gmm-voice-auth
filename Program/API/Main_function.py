from types import MethodType
import numpy as np
import json
import glob
import os
import sys
import pickle
import time
from numpy import genfromtxt
import pyaudio
import wave
from scipy.io.wavfile import read
from sklearn import mixture
import warnings
warnings.filterwarnings("ignore")

from sklearn import preprocessing
from python_speech_features import mfcc

#Calculate and returns the delta of given feature vector matrix
def calculate_delta(array):
    rows,cols = array.shape
    deltas = np.zeros((rows,20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i-j < 0:
                first = 0
            else:
                first = i-j
            if i+j > rows -1:
                second = rows -1
            else:
                second = i+j
            index.append((second,first))
            j+=1
        deltas[i] = ( array[index[0][0]]-array[index[0][1]] + (2 * (array[index[1][0]]-array[index[1][1]])) ) / 10
    return deltas

#convert audio to mfcc features
def extract_features(audio,rate):    
    mfcc_feat = mfcc.mfcc(audio,rate, 0.025, 0.01,20,appendEnergy = True, nfft=1103)
    mfcc_feat = preprocessing.scale(mfcc_feat)
    delta = calculate_delta(mfcc_feat)

    #combining both mfcc features and delta
    combined = np.hstack((mfcc_feat,delta)) 
    return combined



from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/add_user', methods=['POST'])
def add():
    name = request.args.get('user_id')
    source = "./voice_database/" + name #change to user ID
  
    os.mkdir(source)

    dest =  "./gmm_models/"
    count = 1

    for path in os.listdir(source):
        path = os.path.join(source, path)

        features = np.array([])
      
        # reading audio files of speaker
        (sr, audio) = read(path)
      
        # extract 40 dimensional MFCC & delta MFCC features
        vector   = extract_features(audio,sr)

        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))
          
        # when features of 3 files of speaker are concatenated, then do model training
        if count == 3:    
            gmm = mixture.GaussianMixture(n_components = 16, n_iter = 200, covariance_type='diag',n_init = 3)
            gmm.fit(features)

            # saving the trained gaussian model
            pickle.dump(gmm, open(dest + name + '.gmm', 'wb'))
            print(name + ' added successfully') 
          
            features = np.asarray(())
            count = 0
        count = count + 1

@app.route('/Verfication')
def recognize():
   # Voice Authentication
   FILENAME = "./test.wav"

   audio = pyaudio.PyAudio()

   modelpath = "./gmm_models/"

   gmm_files = [os.path.join(modelpath,fname) for fname in 
               os.listdir(modelpath) if fname.endswith('.gmm')]

   models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]

   speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
               in gmm_files]
 
   #read test file
   sr,audio = read(FILENAME)
   
   # extract mfcc features
   vector = extract_features(audio,sr)
   log_likelihood = np.zeros(len(models)) 

   #checking with each model one by one
   for i in range(len(models)):
       gmm = models[i]         
       scores = np.array(gmm.score(vector))
       log_likelihood[i] = scores.sum()

   pred = np.argmax(log_likelihood)
   identity = speakers[pred]
  
   # if voice not recognized than terminate the process
   if identity == 'unknown':
           print("Not Recognized! Try again...")
           return
   
   print( "Recognized as - ", identity)