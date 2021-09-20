#Create by HashTable159
#Edit this function before used
from tensorflow.keras.models import load_model

class Obj_Func:
    def __init__(self):
        self.model = load_model("XFLR5_model")

    def function(self, x):
        predict = self.model.predict([x])
        return 1/predict[0][0]*predict[0][1]

    def result(self, x):
        predict = self.model.predict([x])
        return predict[0][0], predict[0][1], predict[0][2]