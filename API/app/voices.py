import os
import pickle
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture 
from sklearn import preprocessing
import numpy as np
import python_speech_features as mfcc

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
    mfcc_feat = mfcc.mfcc(audio, rate, 0.025, 0.01,20,appendEnergy = True, nfft=1200)
    mfcc_feat = preprocessing.scale(mfcc_feat) #Standarization Gaussian with zero mean and unit variance.
    delta = calculate_delta(mfcc_feat)

    #combining both mfcc features and delta
    combined = np.hstack((mfcc_feat,delta)) 
    return combined

def add_user(user_id):
    
    name = user_id
    
    source = "./API/app/voice_database/" + name

    dest =  "./API/app/gmm_models/"
    count = 1

    for path in os.listdir(source):
        path = os.path.join(source, path)

        features = np.asfarray(())
        
        # reading audio files of speaker
        (sr, audio) = read(path)
        
        # extract 40 dimensional MFCC & delta MFCC features
        vector   = extract_features(audio,sr)

        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))
            
        # when features of 3 files of speaker are exist and concatenated, then do model training
        if count == 3:    
            gmm = GaussianMixture(n_components = 16, max_iter = 500, covariance_type='diag',n_init = 3)
            gmm.fit(features)

            # saving the trained gaussian model
            pickle.dump(gmm, open(dest + name + '.gmm', 'wb'))
            print(name + ' added successfully') 
            
            features = np.asfarray(())
            count = 0
        count = count + 1

#The model will be created for every 3 voices in the folder.

def recognize(user_id, voice):
    audio = voice

    modelpath = "./API/app/gmm_models"

    gmm_files = [os.path.join(modelpath, fname) for fname in os.listdir(modelpath) if fname.endswith('.gmm')]
    print (gmm_files)

    models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]

    speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname in gmm_files]
 
    #read test file
    sr,audio = read(voice)
   
    # extract mfcc features
    vector = extract_features(audio,sr)
    log_likelihood = np.zeros(len(models)) 

    #checking with each model one by one
    for i in range(len(models)):
        gmm = models[i]         
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()
        print (scores)
        print (models[i])

    pred = np.argmax(log_likelihood)
    identity = speakers[pred]
    print(pred)
    print(identity)
  
    # if voice not recognized than terminate the process
    if identity == 'unknown':
        return ("Not Recognized! Try again...")

    # if voice is not the same then return unknown
    if identity != ("gmm_models\\" + user_id):
        return ("Unknown voice!")

    return (True)