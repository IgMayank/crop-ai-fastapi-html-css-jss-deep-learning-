from fastapi import FastAPI, File , UploadFile , Form , HTTPException
from fastapi.middleware.cors import CORSMiddleware

from databse.database import engine
from databse.database import Base
from databse.models import Prediction , user
from databse.database import SessionLocker 
from authh.hashing import hash_password

from pydantic import EmailStr


from authh.hashing import verify_pswd
from authh.token import create_access_token

from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from fastapi import Depends
from authh.token import verify_token

from fastapi import WebSocket,WebSocketDisconnect


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers=["*"]
)
Base.metadata.create_all(bind=engine)


oauth2_scheme =OAuth2PasswordBearer(tokenUrl="login")

@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):

    await websocket.accept()
    try:
        while True :
            data = await websocket.receive_text()

            await websocket.send_text("Uploading Image...")
            await websocket.send_text("Running AI Model...")
            await websocket.send_text("Analyzing Disease...")
            await websocket.send_text("Prediction Complete...")
    except WebSocketDisconnect:
        print("client disconnected")





from PIL import Image
from predict import predict_image

@app.get("/")
def home():
    return {"message":"dont know wht to write "}



def get_current_user(token : str=Depends(oauth2_scheme)):
    username  = verify_token(token)

    if username is None:
        return None
    
    db = SessionLocker()

    current_user = (
        db.query(user).filter(user.username == username).first()

    )
    db.close()

    return current_user

@app.post("/predict")
async def predict(file:UploadFile = File(...),current_user = Depends(get_current_user)):
    image = Image.open(file.file).convert("RGB")

    result = predict_image(image)

    db = SessionLocker()
    print(current_user)
    print(type(current_user))

    prediction = Prediction(
        user_id = current_user.id,
        image_name = file.filename,
        crop = result["crop"],
        disease = result["disease"],
        confidence = result["confidence"]

    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    db.close()

    

    return result


@app.get("/history")
def get_history():
    db =SessionLocker()

    prediction = db.query(Prediction).all()

    db.close()

    return prediction



@app.delete("/history/{prediction_id}")
def delete_pred(prediction_id:int):
    
    db = SessionLocker()

    prediction= (
        db.query(Prediction).filter(Prediction.id == prediction_id).first()
    )
    if prediction:
        db.delete(prediction)
        db.commit()

    db.close()

    return{"message":"deleted successfully"}


@app.post("/register")
def register(username:str=Form(...) , email:EmailStr=Form(...),password:str=Form(...)):
    db = SessionLocker()

    

    if len(username) <3:
        raise HTTPException(status_code=400 , detail="Username must be above 3 characters " )
    
    if len(password) <8 :
        raise HTTPException(status_code=400 , detail="password must be atleast 8 characters bruh ")
    
    existing_user = (db.query(user).filter(user.username == username).first())

    if existing_user:
        raise HTTPException(status_code=400,detail="username already exists gng ")
    
    existing_email = (db.query(user).filter(user.email == email).first())

    if existing_email:
        raise HTTPException(status_code=400, detail="email already exists dawgg ")

    User = user(
        username = username,
        email = email,
        password = hash_password(password)
    )
    access_token = create_access_token(data={"sub":User.username})

    db.add(User)

    db.commit()
    db.close()

    return{"message":"user created successfully",
           "access_token":access_token}

@app.post("/login")
def login(request : OAuth2PasswordRequestForm = Depends()):

    db = SessionLocker()

    db_user = (
        db.query(user).filter(user.username == request.username).first()
        
    )
    if db_user is None:
        raise HTTPException(status_code=400 ,detail="user not found ")
    
    if not verify_pswd(
        request.password,
        db_user.password
    ):
        raise HTTPException(status_code=401,detail="invalid password")
    
    access_token = create_access_token(data={"sub":db_user.username})

    return{
        "access_token" : access_token,
        "token_type":"bearer"
    }
    




@app.get("/me")
def me(current_user:str=Depends(get_current_user)):
    return{"username":current_user}



@app.get("/my-history")
def my_history(current_user = Depends(get_current_user)):

    db = SessionLocker()

    predictions = (
        db.query(Prediction).filter(Prediction.user_id == current_user.id).all()
    )
    db.close()

    return predictions



@app.get("/dashboard")
def dashboard(current_user = Depends(get_current_user)):

    db = SessionLocker()

    predictions = (
        db.query(Prediction).filter(Prediction.id == current_user.id).all()
    )

    total_predictions = len(predictions)

    healthy = len([
        p for p in predictions
        if p.disease.lower() == "healthy"
    ])
    diseased = total_predictions - healthy
    db.close()

    return{"username" : current_user.username,
        "total predictions" : total_predictions,
           "healthy":healthy,
           "diseased":diseased}

