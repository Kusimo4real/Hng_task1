from sqlalchemy.orm import Session
from . import models, schemas
from .utils import get_password_hash
from uuid import uuid4
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.userId == user_id).first()

def create_organisation(db: Session, organisation: schemas.OrganisationCreate, user_id: str):
    db_organisation = models.Organisation(
        name=organisation.name,
        description=organisation.description,
        orgId= str(uuid4())
    )
    db.add(db_organisation)
    db.commit()
    db.refresh(db_organisation)

    user = db.query(models.User).filter(models.User.userId == user_id).first()
    user.organisations.append(db_organisation)
    
    return db_organisation

def create_user(db: Session, user: schemas.UserCreate):
    user_dict = user.model_dump(mode="json")  
    user_dict['password'] = get_password_hash(user_dict.get('password'))
    user_dict["userId"] = str(uuid4())

    db_user = models.User(**user_dict)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    organisation = create_organisation(db=db, organisation=schemas.OrganisationCreate(name=f"{user.firstName}'s Organisation"), user_id=str(db_user.userId))
    return db_user



# def create_user(db: Session, user: schemas.UserCreate):
#     try:
#         user_dict = user.model_dump(mode="json")  
#         user_dict['password'] = get_password_hash(user_dict.get('password'))

#         db_user = models.User(**user_dict)
#         db_org = models.Organisation(name=user_dict.get('firstName') + ' ' + "Organisation", users=db_user, description="")
#         db.add(db_user)
#         db.add(db_org)
#         db.commit()
#         db.refresh(db_user)
#         db.refresh(db_org)
#         return db_user
#     except Exception as e:
#         print(e)
#         return None




def get_organisations(db: Session, user_id: str):
    user = db.query(models.User).filter(models.User.userId == user_id).first()
    return user.organisations

def get_organisation(db: Session, org_id: str, userId: str = None):
    if not userId:
        return db.query(models.Organisation).filter(models.Organisation.orgId == org_id).first()
    return db.query(models.Organisation).filter(models.Organisation.orgId == org_id, models.User.userId == userId).first()

def add_user_to_organisation(db: Session, user_id: str, org_id: str):
    user = db.query(models.User).filter(models.User.userId == user_id).first()
    organisation = db.query(models.Organisation).filter(models.Organisation.orgId == org_id).first()
    organisation.users.append(user)
    db.commit()
    return organisation
