import jwt
import uvicorn
import numpy as np

from fastapi import FastAPI, UploadFile, Query, Response, Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta


from Users import Users
from User import User


SECRET_KEY = "stickfighter342"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
AUTH_SCHEME = OAuth2PasswordBearer(tokenUrl="/token")


app = FastAPI()
users = Users()

# User account related functions START

# Token creation
def create_access_token(user: User):
    now = datetime.utcnow()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = now + expires_delta
    to_encode = {"username": user.username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt


def check_user_exists(username: str):
    user = users.get_user(username)
    if not user:
        raise HTTPException(status_code = 401, detail = "User does not exist")
    return user

# Authenticate user
def authenticate_user(username: str, password: str):
    user = users.get_user(username)
    if not user:
        return False
    if not users.verify_password(user, password):
        return False
    return user

# return user from token or throw exception
def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        username = payload.get("username")
        time = payload.get("exp")
        user = users.get_user(username)

        # if user doesn't exist or token unauthorized/invalid
        if not user:
            raise HTTPException(status_code = 401, detail = "Invalid token")
        
        # if token has expired
        
        elif datetime.utcnow() > datetime.utcfromtimestamp(time):
            raise HTTPException(status_code = 403, details = "Expired token")
        
        return check_user_exists(username)

    # if decoding the payload raises an error
    except PyJWTError:
        raise HTTPException(status_code = 401, detail = "Invalid token")

# Create new user
@app.post("/signup")
async def create_user(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    # if user exists
    if users.get_user(username):
        raise HTTPException(status_code = 400, detail = 'User already exists')
    
    # add user
    user = users.add_user(username, password)

    # return token
    access_token = create_access_token(user)

    response.set_cookie(key = 'token', value = access_token)

    return {"message": "Successfully signed up!"}

# Endpoint for token creation
@app.get("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    # authenticate user
    user = authenticate_user(username, password)

    # if user doesn't pass authentication
    if not user:
        raise HTTPException(status_code = 401, detail = "Invalid username or password")

    access_token = create_access_token(user)
    response.set_cookie(key = 'token', value = access_token)

    return {"message": "Login successful!"}

# User account related functions END

# ---------------------------------------------------------------

# File / Data setup related functions START

def convert(data):
    file = data.decode("utf-8-sig").splitlines()
    data = np.genfromtxt(file, delimiter = ',')
    return data


@app.put("/set-X-train")
async def set_X_train(X_data: UploadFile, request: Request):
    token = request.cookies.get('token')
    user = validate_token(token)
    X_data = await X_data.read()
    user.set_X_train(convert(X_data))
    return {'user': user.username, 'message': 'Training data (X) added successfully'}


@app.put("/set-X-test")
async def set_X_test(X_data: UploadFile, request: Request):
    token = request.cookies.get('token')
    user = validate_token(token)
    X_data = await X_data.read()
    user.set_X_test(convert(X_data))
    return {'user': user.username, 'message': 'Training data (y) added successfully'}


@app.put("/set-y-train")
async def set_y_train(y_data: UploadFile, request: Request):
    token = request.cookies.get('token')
    user = validate_token(token)
    y_data = await y_data.read()
    user.set_y_train(convert(y_data))
    return {'user': user.username, 'message': 'Training data (y) added successfully'}


@app.put("/set-y-train")
async def set_y_test(y_data: UploadFile, request: Request):
    token = request.cookies.get('token')
    user = validate_token(token)
    y_data = await y_data.read()
    user.set_y_test(convert(y_data))
    return {'user': user.username, 'message': 'Training data (y) added successfully'}


@app.put("/set-train-data")
async def set_train(X_data: UploadFile, y_data: UploadFile, request: Request):
    token = request.cookies.get('token')
    set_X_train(X_data, token)
    set_y_train(y_data, token)

# File / Data setup related functions END

# ---------------------------------------------------------------

# Model setup related functions START

@app.put("/lr")
async def lr(request: Request):
    token = request.cookies.get('token')
    user = validate_token(token)
    user.set_model_lr()


@app.put("/svm")
async def svm(request: Request):
    token = request.cookies.get('token')
    user = validate_token(token)
    user.set_model_svm()


@app.put("/sgd")
async def sgd(request: Request):
    token = request.cookies.get('token')
    user = validate_token(token)
    user.set_model_sgd()

# Model setup related functions END

# ---------------------------------------------------------------

# Model training functions START

@app.post("/train")
async def train(request: Request):
    token = request.cookies.get('token')
    user = validate_token(token)
    if not user.train():
        raise HTTPException(status_code = 404, detail = "Invalid training parameters. Please add training data (X, y).")


@app.get("/predict")
async def predict(X_data: UploadFile, request: Request):
    token = request.cookies.get('token')
    user = validate_token(token)
    X_data = await X_data.read()
    X = convert(X_data)
    val = user.predict(X)
    dictionary = {}
    for i, x in enumerate(val):
        dictionary['Prediction %d' % (i + 1)] = x
    return dictionary


# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
