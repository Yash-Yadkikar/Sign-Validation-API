from sklearn import svm
import sign_valid as sign
import joblib
import numpy as np

path = "F:\\Academics\\Groww PS\\Project 2\\input"

image = sign.Sign_Valid(path1)
features = image.process()
features = np.array(features)

clf = joblib.load('SignClassifierSVM.pkl')

clf_prediction = clf.predict(features)
