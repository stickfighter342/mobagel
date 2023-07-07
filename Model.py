import jwt
import numpy as np

from sklearn import linear_model, svm


class Model:
    def __init__(self):
        self.X_train = self.y_train = None
        self.X_test = self.y_test = None
        self.model = None

# Helper functions START


    def set_X_train(self, X_data):
        self.X_train = X_data
    

    def set_y_train(self, y_data):
        self.y_train = y_data


    def set_X_test(self, X_data):
        self.X_test = X_data
    
    
    def set_y_test(self, y_data):
        self.y_test = y_data
    

    def set_data_train(self, X_data, y_data):
        self.set_X_train(X_data)
        self.set_y_train(y_data)
        return True
    

    def set_data_test(self, X_data, y_data):
        self.set_X_test(X_data)
        self.set_y_test(y_data)
        return True

# helper functions END

# ---------------------------------------------------------------

# regression model replacement functions START

    def lr(self):
        self.model = linear_model.LinearRegression()
    

    def svm(self):
        self.model = svm.SVR()
    

    def sgd(self):
        self.model = linear_model.SGDRegressor()

# regression model replacement functions END

# ---------------------------------------------------------------

# model training & prediction functions START

    def train(self):
        if type(self.X_train) is np.ndarray:
            self.model.fit(self.X_train, self.y_train)
            return True
        return False


    def predict(self, X_test):
        # replace X_test with data
        # replace y_test with trained results
        return self.model.predict(X_test)

