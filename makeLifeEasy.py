import pickle
import os


l = pickle.load(open("spawn4", "rb"))
l = [[[8, 0]],[[16, 12]]]

pickle.dump(l, open("spawn4", "wb"))