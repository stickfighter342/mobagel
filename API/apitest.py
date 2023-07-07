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
users = Users("localhost", "root", "stickfighter342", "users")

# User account related functions START

# Token creation
def create_access_token(user: User):
    now = datetime.utcnow()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = now + expires_delta
    to_encode = {"userid": user.id}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt


def check_user_exists(userid: str):
    user = users.get_user_from_id(userid)
    if not user:
        raise HTTPException(status_code = 401, detail = "User does not exist")
    return user

# Authenticate user
def authenticate_user(username: str, password: str):
    user = users.get_user_from_username(username)
    if not user:
        return None
    if not users.verify_password(user, password):
        return None
    return user

# return user from token or throw exception
def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        userid = payload.get("userid")
        user = users.get_user_from_id(userid)
        # if user doesn't exist or token unauthorized/invalid
        if not user:
            raise HTTPException(status_code = 401, detail = "Invalid token")
        return user


    # if decoding the payload raises an error
    except PyJWTError:
        raise HTTPException(status_code = 401, detail = "Invalid token")


@app.post("/clear-cookies")
async def clear_cookies(request: Request, response: Response):
    for i in request.cookies:
        response.delete_cookie(key = i)


# Create new user
@app.post("/signup")
async def create_user(request: Request, response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    cookie = request.cookies

    if cookie:
        raise HTTPException(status_code = 400, detail = 'User already exists')    
    
    # add user
    user = users.add_user(username, password)

    # return token
    access_token = create_access_token(user)

    response.set_cookie(key = 'token', value = access_token, expires = 3600)

    return {"message": "Successfully signed up!"}

# Endpoint for token creation
@app.put("/login")
async def login(response: Response, request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    cookie = request.cookies

    user = None
    if not cookie:
        # authenticate user
        user = authenticate_user(username, password)
        # if user doesn't pass authentication
        if not user:
            raise HTTPException(status_code = 401, detail = "Invalid username or password")
    
    else:
        token = cookie.get('token')
        user = validate_token(token)
        if not users.verify_password(user, password):
            raise HTTPException(status_code = 401, detail = "Invalid username or password")
    
    access_token = create_access_token(user)
    response.set_cookie(key = 'token', value = access_token, expires = 3600)

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
    users.update_user_to_sql(user)
    return {'user': user.username, 'message': 'Training data (X) added successfully'}


@app.put("/set-X-test")
async def set_X_test(X_data: UploadFile, request: Request):
    token = request.cookies.get('token')
    user = validate_token(token)
    X_data = await X_data.read()
    user.set_X_test(convert(X_data))
    users.update_user_to_sql(user)
    return {'user': user.username, 'message': 'Training data (y) added successfully'}


@app.put("/set-y-train")
async def set_y_train(y_data: UploadFile, request: Request):
    token = request.cookies.get('token')
    user = validate_token(token)
    y_data = await y_data.read()
    user.set_y_train(convert(y_data))
    users.update_user_to_sql(user)
    return {'user': user.username, 'message': 'Training data (y) added successfully'}


@app.put("/set-y-train")
async def set_y_test(y_data: UploadFile, request: Request):
    token = request.cookies.get('token')
    user = validate_token(token)
    y_data = await y_data.read()
    user.set_y_test(convert(y_data))
    users.update_user_to_sql(user)
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
    users.update_user_to_sql(user)


@app.put("/svm")
async def svm(request: Request):
    token = request.cookies.get('token')
    user = validate_token(token)
    user.set_model_svm()
    users.update_user_to_sql(user)


@app.put("/sgd")
async def sgd(request: Request):
    token = request.cookies.get('token')
    user = validate_token(token)
    user.set_model_sgd()
    users.update_user_to_sql(user)

# Model setup related functions END

# ---------------------------------------------------------------

# Model training functions START

@app.post("/train")
async def train(request: Request):
    token = request.cookies.get('token')
    user = validate_token(token)
    if not user.train():
        raise HTTPException(status_code = 404, detail = "Invalid training parameters. Please add training data (X, y).")
    users.update_user_to_sql(user)


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
