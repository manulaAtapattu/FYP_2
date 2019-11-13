import scipy.io.wavfile as wav
import mfeatures
from sklearn.mixture import GaussianMixture
import numpy as np

source = "../Data_set/samples/alice/alice_good_morning.wav"
file = ""
# gmms = []

def writeAudio(rate, data, i):
    writeDestn = 'training_data/sample' + str(i) + '.wav'
    wav.write(writeDestn, rate, data)
    return

rate, sig = wav.read(source)
sigLen = len(sig)
sig = sig [int(sigLen*.2):int(sigLen*.8)]
mfcc_feat = mfeatures.extract_features(sig, rate)
gmm = GaussianMixture(n_components=16, covariance_type='diag', n_init=10)
gmm.fit(mfcc_feat)
# gmms.append(gmm)

# writeAudio(rate, sig)
# print('Created partition ...')

source2 = "../Data_set/samples/george/gerorge_hello_everyone.wav"
rate2, sig2 = wav.read(source2)
sigLen2 = len(sig2)
sig2 = sig2 [int(sigLen2*.2):int(sigLen2*.8)]
finalTotal = 0
iterations = 100

for i in range(0,iterations):
    mfcc_feat2 = mfeatures.extract_features(sig2, rate2)
    scores = np.array(gmm.score(mfcc_feat2))
    totalScore =scores.sum()
    finalTotal +=totalScore

avragedTotal = finalTotal/iterations

print('Average Score : ', avragedTotal)