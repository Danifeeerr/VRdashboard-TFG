from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError,NoResultFound
import os
from typing import List
from datetime import datetime, timedelta
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
import jwt
from jwt.exceptions import PyJWTError

from models.users import Users, UsersInsert, UserLogin
from models.training import Training, TrainingInsert
from models.assignation import Assignation, AssignationInsert, AssignationUpdate
from models.attempt import Attempt, NewAttempt

load_dotenv() # Load environment variables from .env file

DATABASE_URL = os.getenv("dburl") 


engine = create_engine(DATABASE_URL) # Create a database engine using the URL from the environment variable

app = FastAPI()

hasher = PasswordHasher()

# JWT token data
SECRET_KEY = os.getenv("skey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


@app.get("/")
async def root():
    return {"message": "This is an API for the database management system. Please refer to the documentation for available endpoints."}

 ###########################################################
 ##########################USERS############################
 ###########################################################

@app.get("/users", response_model=List[Users], tags=["Users"])
def get_users():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM users")).mappings().all()
        if not res:
            raise HTTPException(status_code=404, detail="Users not found")
        
        return res


@app.get("/user", response_model=Users, tags=["Users"])
def get_user_by_token(token: str):
    id = token_to_user_id(token)
    with engine.connect() as conn:
        res = conn.execute(
            text("SELECT * FROM users where id= :id"), 
            {"id": id}
        ).mappings().first()

        if res is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return res

@app.get("/user/{id}", response_model=Users, tags=["Users"]) #Només ho pot fer l'administrador
def get_user_by_id(id):
    with engine.connect() as conn:
        res = conn.execute(
            text("SELECT * FROM users where id= :id"), 
            {"id": id}
        ).mappings().first()

        if res is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return res

@app.post("/users/new", response_model=Users, tags=["Users"])
def create_new_user(u: UsersInsert):
    passHash = hasher.hash(u.password_hash)
    with engine.connect() as conn:
        try:
            user = conn.execute(
                text("INSERT INTO users (username, password_hash, admin) VALUES (:username, :pass, :admin) RETURNING *"),
                {"username": u.username.lower(), 
                 "pass": passHash, 
                 "admin": u.admin}
            ).mappings().one()

            conn.commit()
            return user
        
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Username already exists")
        
    

@app.post("/users/update", response_model=Users, tags=["Users"])
def update_user(u: Users):
    with engine.connect() as conn:
        try:
            if u.password_hash:
                passHash = hasher.hash(u.password_hash)
                user = conn.execute(
                    text("UPDATE users SET username = :username, password_hash = :pass, admin = :admin WHERE id = :id RETURNING *"),
                    {"username": u.username.lower(), "pass": passHash, "admin": u.admin, "id": u.id}
                ).mappings().one()
            else:
                user = conn.execute(
                    text("UPDATE users SET username = :username, admin = :admin WHERE id = :id RETURNING *"),
                    {"username": u.username.lower(), "admin": u.admin, "id": u.id}
                ).mappings().one()

            conn.commit()
            return user

        except NoResultFound:
            raise HTTPException(status_code=404, detail="User not found")
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Username already exists")

@app.delete("/users/delete/{id}", tags=["Users"]) # Només ho pot fer l'administrador
def delete_user(id: int):
    with engine.connect() as conn:
        res = conn.execute(
            text("DELETE FROM users where id = :id RETURNING *"),
            {"id": id}
        ).mappings().first()
        conn.commit()

        if res is None:
            raise HTTPException(status_code=404, detail="User not found")
    
        return res

    
 ###########################################################
 ##########################TRAINING#########################
 ###########################################################


@app.get("/training", response_model=List[Training], tags=["Trainings"])
def get_trainings():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM training")).mappings().all()
        if not res:
            raise HTTPException(status_code=404, detail="Trainings not found")
        
        return res

@app.get("/training/{id}", response_model=Training, tags=["Trainings"])
def get_training_by_id(id: int):
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM training WHERE id = :id"),
        {"id": id}
        ).mappings().first()

        if res is None:
            raise HTTPException(status_code=404, detail="Training not found")
    
        return res

@app.post("/training/new", response_model=Training, tags=["Trainings"])
def create_new_training(t: TrainingInsert):
    with engine.connect() as conn:
        try:
            training = conn.execute(
                text("INSERT INTO training (name, hours, error_limit) VALUES (:name, :hours, :e_l) RETURNING *"),
                {"name": t.name, 
                 "hours": t.hours, 
                 "e_l": t.error_limit}
            ).mappings().one()

            conn.commit()
            return training
        
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Training name already exists")
        
@app.post("/training/update", response_model=Training, tags=["Trainings"])
def update_user(t: Training):
    with engine.connect() as conn:
        try:
            training = conn.execute(
                text("UPDATE training SET name = :name, hours = :hours, error_limit = :e_l WHERE id = :id RETURNING *"),
                {"name": t.name,
                 "hours": t.hours,
                 "e_l": t.error_limit,
                 "id": t.id}
            ).mappings().one()

            conn.commit()

            return training
        
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Training not found")             
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Training name already exists")
        
@app.delete("/training/delete/{id}", tags=["Trainings"])
def delete_training(id: int):
    with engine.connect() as conn:
        res = conn.execute(
            text("DELETE FROM training where id = :id RETURNING *"),
            {"id": id}
        ).mappings().first()
        conn.commit()

        if res is None:
            raise HTTPException(status_code=404, detail="Training not found")
    
        return res


 ###########################################################
 ######################ASSIGNATIONS#########################
 ###########################################################


@app.get("/assignation", response_model=List[Assignation], tags=["Assignations"])
def get_assignation():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM assignation")).mappings().all()
        if not res:
            raise HTTPException(status_code=404, detail="Assignations not found")
        return res

@app.get("/assignation/{userid}", response_model=List[Assignation], tags=["Assignations"]) #Només la pot fer l'administrador
def get_assignation_by_id(userid: int):
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM assignation WHERE userid = :userid"),
        {"userid": userid}
        ).mappings().all()

        if not res:
            raise HTTPException(status_code=404, detail="Assignations not found")
    
        return res

@app.get("/assignation", response_model=List[Assignation], tags=["Assignations"])
def get_assignation_by_token(token: str):
    id = token_to_user_id(token)
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM assignation WHERE userid = :userid"),
        {"userid": id}
        ).mappings().all()

        if not res:
            raise HTTPException(status_code=404, detail="Assignations not found")
    
        return res

@app.post("/assignation/new", response_model=Assignation, tags=["Assignations"]) #Només la pot fer l'administrador
def create_new_assignation(a: AssignationInsert):
    with engine.connect() as conn:
        try:
            assignation = conn.execute(
                text("INSERT INTO assignation (userid, trainingid, date) VALUES (:userid, :trainingid, :date) RETURNING *"),
                {"userid": a.userid, 
                 "trainingid": a.trainingid, 
                 "date": a.date}
            ).mappings().one()

            conn.commit()
            return assignation
        
        except IntegrityError:
            raise HTTPException(status_code=409, detail="The user may already have an assignation to this training or the user or the training does not exist")
        

@app.post("/assignation/update", response_model=Assignation, tags=["Assignations"])
def update_assignation(a: AssignationUpdate):
    id = token_to_user_id(a.userid)
    with engine.connect() as conn:
        try:
            assignation = conn.execute(
                text("UPDATE assignation SET completed = :completed WHERE userid = :userid and trainingid = :trainingid RETURNING *"),
                {"completed": a.completed,
                 "userid": id,
                 "trainingid": a.trainingid}
            ).mappings().one()

            conn.commit()

            return assignation
        
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Assignation not found")            

@app.delete("/assignation/delete", tags=["Assignations"]) # Només la pot fer l'administrador
def delete_assignation(userid: int, trainingid: int):
    with engine.connect() as conn:
        res = conn.execute(
            text("DELETE FROM assignation where userid = :userid and trainingid = :trainingid RETURNING *"),
            {"userid": userid,
             "trainingid": trainingid}
        ).mappings().first()
        conn.commit()

        if res is None:
            raise HTTPException(status_code=404, detail="Assignation not found")
    
        return res
 


 ###########################################################
 #########################ATTEMPTS##########################
 ###########################################################

@app.get("/attempt", response_model=List[Attempt], tags=["Attempts"])
def get_attempts_by_userid_and_trainingid(userid: int, trainingid: int):
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM attempt WHERE userid = :userid and trainingid = :trainingid"),
        {"userid": userid,
         "trainingid": trainingid}
        ).mappings().all()

        if not res:
            raise HTTPException(status_code=404, detail="Attempts not found")
    
        return res
    
@app.get("/attempt/user", response_model=List[Attempt], tags=["Attempts"])
def get_attempts_by_userid(userid: int):
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM attempt WHERE userid = :userid"),
        {"userid": userid}
        ).mappings().all()

        if not res:
            raise HTTPException(status_code=404, detail="Attempts not found")
    
        return res
    
@app.get("/attempt/timestamp", response_model=Attempt, tags=["Attempts"])
def get_attempts_by_userid_and_timestamp(userid: int, timestamp: datetime):
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM attempt WHERE userid = :userid and timestamp = :timestamp"),
        {"userid": userid,
         "timestamp": timestamp}
        ).mappings().first()

        if not res:
            raise HTTPException(status_code=404, detail="Attempts not found")
    
        return res
    
@app.post("/attempt/new", tags=["Attempts"])
def create_new_attempt(a: NewAttempt):
    userid = token_to_user_id(a.userid)
    with engine.connect() as conn:
        try:
            attempt = conn.execute(
                text("INSERT INTO attempt (userid, trainingid, time_spent, number_errors, timestamp) VALUES (:userid, :trainingid, :time_spent" \
                ", :number_errors, :timestamp) RETURNING *"),
                {"userid": userid, 
                 "trainingid": a.trainingid, 
                 "time_spent": a.time_spent,
                 "number_errors": a.number_errors,
                 "timestamp": a.timestamp}
            ).mappings().one()
            conn.commit()

            return {"success": True}
        
        except IntegrityError:
            raise HTTPException(status_code=404, detail="No user or training found")
        
@app.delete("/attempt/delete", tags=["Attempts"])
def delete_attempt(userid: int, trainingid: int, timestamp: datetime):
    with engine.connect() as conn:
        res = conn.execute(
            text("DELETE FROM attempt where userid = :userid and trainingid = :trainingid and timestamp = :timestamp RETURNING *"),
            {"userid": userid,
             "trainingid": trainingid,
             "timestamp": timestamp}
        ).mappings().first()
        conn.commit()

        if res is None:
            raise HTTPException(status_code=404, detail="Assignation not found")
    
        return res
 

###########################################################
#########################SESSION###########################
###########################################################


def token_to_user_id(token: str) -> int:

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return int(user_id)
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

@app.post("/login", tags=["User"])
def get_user(u: UserLogin):
    with engine.connect() as conn:
        user = conn.execute(
            text("SELECT id, password_hash from users where username = :username"),
            {"username": u.username.lower()}
        ).mappings().first()
        if not user:
            raise HTTPException(status_code=401, detail="No username found")
        try:
            if hasher.verify(user["password_hash"], u.password):
                payload = {
                    "sub": str(user["id"]),
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                }

                token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

                return {
                    "access_token": token,
                    "token_type": "bearer"
                }
        except VerifyMismatchError:
            raise HTTPException(status_code=401, detail="Incorrect password")


