from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Session
from app.models.user import User, RoleEnum, StateUser
from app.core.security import get_password_hash

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

def create_user(
    db: Session,
    *,
    name: str,
    lastname: str,
    cellphone: str,
    direction: str,
    username: str,
    password: str,
    rol: RoleEnum,
    country: str,
    email: str,
    state: StateUser,
    creation_date,
    last_activity_date = None,
    number_followers: int = 0
) -> User:
    try:
        user = User(
            name=name,
            lastname=lastname,
            cellphone=cellphone,
            direction=direction,
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            rol=rol,
            country=country,
            state=state,
            creation_date=creation_date,
            last_activity_date=last_activity_date,
            number_followers=number_followers
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        print(f"Error al crear usuario: {e}")
        raise

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()
    return user
