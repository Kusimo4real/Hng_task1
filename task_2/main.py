from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas, crud, utils, deps
from app.database import engine, SessionLocal
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.post("/auth/register")
def register(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    # return db_user
    if db_user:
        raise HTTPException (
            status_code=400,
            detail={
                "status": "Bad request",
                "message": "Registration unsuccessful",
                "statusCode": 400
            }
        )
    db_user = crud.create_user(db=db, user=user)

    if db_user == None:
        raise HTTPException (
            status_code=400,
            detail={
                "status": "Bad request",
                "message": "Registration unsuccessful",
                "statusCode": 400
            }
        )
    access_token = utils.create_access_token(data={"sub": str(db_user.userId)})
    response_user = schemas.UserBase.from_orm(db_user).model_dump(mode="json")
    return {
        "status": "success",
        "message": "Registration successful",
        "data": {
            "accessToken": access_token,
            "user": response_user
        }
    }

@app.post("/auth/login")
def login(form_data: schemas.UserLogin , db: Session = Depends(deps.get_db)):
    user = crud.get_user_by_email(db, email=form_data.email)
    if not user or not utils.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail={
                "status": "Bad request",
                "message": "Authentication failed",
                "statusCode": 401
            })
    access_token = utils.create_access_token(data={"sub": str(user.userId)})
    return {
        "status": "success",
        "message": "Login successful",
        "data": {
            "accessToken": access_token,
            "user": user
        }
    }


@app.get("/api/users/{id}")
def read_user_me(id: str, current_user: models.User = Depends(deps.get_current_user)):
    if current_user and current_user.userId != id:
        raise HTTPException(status_code=401, detail={
                "status": "Bad request",
                "message": "Invalid request",
                "statusCode": 404
            })
    response_user = schemas.UserBase.from_orm(current_user).model_dump(mode="json")
    return {
        "status": "success",
        "message": "User details",
        "data": {
            **response_user
        }
    }
    return current_user

@app.get("/api/organisations")
def read_organisations(current_user: models.User = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    organisations = crud.get_organisations(db=db, user_id=str(current_user.userId))
    return {"status": "success", "message": "Organisations retrieved successfully", "data": {"organisations": organisations}}

@app.get("/api/organisations/{org_id}")
def read_organisation(org_id: str, current_user: models.User = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    organisation = crud.get_organisation(db=db, org_id=org_id, userId=current_user.userId)
    if not organisation:
        raise HTTPException(status_code=404, detail="Organisation not found")
    return {"status": "success", "message": "Organisation retrieved successfully", "data": organisation}

@app.post("/api/organisations")
def create_organisation(organisation: schemas.OrganisationCreate, current_user: models.User = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    created_organisation = crud.create_organisation(db=db, organisation=organisation, user_id=str(current_user.userId))

    response_org = schemas.Organisation.from_orm(created_organisation).model_dump(mode="json")
   
    return {"status": "success", "message": "Organisation created successfully", "data": response_org}


@app.post("/api/organisations/{org_id}/users")
def add_user_to_organisation(org_id: str, userId: schemas.AddUserOrgan, current_user: models.User = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    organisation = crud.get_organisation(db=db, org_id=org_id)
    if not organisation:
        raise HTTPException(status_code=404, detail="Organisation not found")
    
    user = crud.get_user(db=db, user_id=userId.userId)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    crud.add_user_to_organisation(db=db, user_id=userId.userId, org_id=org_id)
    return {"status": "success", "message": "User added to organisation successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)