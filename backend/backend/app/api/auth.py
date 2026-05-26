"""Authentication API"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt

from config.database import get_db
from config.settings import settings
from models.user import User
from schemas.auth import Token, TokenData, UserCreate, UserResponse, UserUpdate

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None or not user.is_active:
        raise credentials_exception
    
    return user


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register new user"""
    # Check if user exists
    existing = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Create user
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=pwd_context.hash(user_data.password),
        nickname=user_data.nickname or user_data.username
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get access token"""
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    user.last_login_at = datetime.utcnow()
    db.commit()
    
    # Create token
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user info with detailed stats"""
    from datetime import datetime
    from utils.logger import ActivityLogger, log_global_activity
    
    # Log profile access
    logger = ActivityLogger(current_user.id, current_user.username)
    logger.log("view_profile")
    log_global_activity(current_user.id, current_user.username, "view_profile")
    
    # Update last login if needed
    if current_user.last_login_at is None:
        current_user.last_login_at = datetime.utcnow()
        db.commit()
    
    # Return user with full stats
    return current_user


@router.get("/me/activity")
def get_user_activity(
    days: int = 7,
    current_user: User = Depends(get_current_user)
):
    """Get user activity log"""
    from utils.logger import ActivityLogger
    
    logger = ActivityLogger(current_user.id, current_user.username)
    summary = logger.get_activity_summary(days=days)
    
    return {
        "username": current_user.username,
        "days": days,
        "summary": summary
    }


@router.put("/me")
def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    from utils.logger import ActivityLogger, log_global_activity
    
    # Update fields
    if user_update.nickname is not None:
        current_user.nickname = user_update.nickname
    if user_update.avatar_url is not None:
        current_user.avatar_url = user_update.avatar_url
    if user_update.phone is not None:
        current_user.phone = user_update.phone
    
    db.commit()
    db.refresh(current_user)
    
    # Log update
    logger = ActivityLogger(current_user.id, current_user.username)
    logger.log("update_profile", {"fields": user_update.model_dump()})
    log_global_activity(current_user.id, current_user.username, "update_profile")
    
    return current_user


@router.get("/me/orders")
def get_user_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's course orders"""
    from models.course import CourseOrder
    from sqlalchemy.orm import joinedload
    
    orders = db.query(CourseOrder).options(
        joinedload(CourseOrder.course)
    ).filter(
        CourseOrder.user_id == current_user.id
    ).order_by(CourseOrder.created_at.desc()).all()
    
    return orders


@router.get("/me/certificates")
def get_user_certificates(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's certificates"""
    from models.certificate import UserCertificate
    from sqlalchemy.orm import joinedload
    
    user_certs = db.query(UserCertificate).options(
        joinedload(UserCertificate.certificate)
    ).filter(
        UserCertificate.user_id == current_user.id
    ).order_by(UserCertificate.obtained_at.desc()).all()
    
    return user_certs
