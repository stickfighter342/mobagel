from Model import Model

class User():
    def __init__(self, id: int, username: str, password: str, authentication = False, model = Model()):
        self.id = id
        self.username = username
        self.password = password
        self.authentication = authentication
        self.model = model
        
# Helper functions START

    def set_username(self, username: str):
        self.username = username


    def set_password(self, password: str):
        self.password = password
    

    def set_data_train(self, X_data, y_data):
        return self.model.set_data_train(X_data, y_data)
    

    def set_X_train(self, X_data):
        return self.model.set_X_train(X_data)


    def set_y_train(self, y_data):
        return self.model.set_y_train(y_data)


    def set_X_test(self, X_data):
        return self.model.set_X_train(X_data)


    def set_y_test(self, y_data):
        return self.model.set_y_train(y_data)


# Helper functions END

# ---------------------------------------------------------------

# regression model replacement functions START

    def set_model_lr(self):
        self.model.lr()
    

    def set_model_svm(self):
        self.model.svm()


    def set_model_sgd(self):
        self.model.sgd()

# regression model replacement functions END

# ---------------------------------------------------------------

# model training functions START

    def train(self):
        return self.model.train()

    def predict(self, X_data):
        return self.model.predict(X_data)
    

    

    

        