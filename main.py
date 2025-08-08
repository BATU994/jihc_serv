from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from sqlmodel import Session, select
from models.models import User
from schemas import LoginRequest, TokenResponse, UserCreate
from auth import verify_password, create_access_token,hash_password, TokenData,get_current_user
from database import get_db, init_db,engine
from models.events import NewsPost
from sqlmodel import Session
from uuid import uuid4
from datetime import datetime,timezone
from models.lost_found import LostFoundPost
import os
app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

data = []

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/auth/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    statement = select(User).where(User.email == data.email)
    user = db.exec(statement).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.id})
    return {"access_token": access_token}

@app.post("/users/", response_model=User, status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    hashed = hash_password(user_data.password)

    new_user = User(
        email=user_data.email,
        hashed_password=hashed,
        name=user_data.name,
        group=user_data.group,
        gender=user_data.gender 
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/news/")
def create_post(
    title: str = Form(...),
    content: str = Form(...),
    file: UploadFile = File(None),
    current_user: TokenData = Depends(get_current_user)  # 🔐 ensures JWT
):
    with Session(engine) as session:
        post = NewsPost(
            id=str(uuid4()), 
            title=title,
            content=content,
            created_at=datetime.now(timezone.utc),
            author_id=current_user.user_id
        )

        # Optional: save file to disk or storage
        if file:
            filename = f"uploads/{post.id}_{file.filename}"
            with open(filename, "wb") as f:
                f.write(file.file.read())
            post.attachment_url = filename

        session.add(post)
        session.commit()
        session.refresh(post)

        return {"message": "Post created", "post_id": post.id}


@app.post("/lostfound/")
def create_lostfound_post(
    item_name: str = Form(...),
    type: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    location: str = Form(...),
    image: UploadFile = File(...),
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    image_filename = f"{uuid4().hex}_{image.filename}"
    image_path = os.path.join(UPLOAD_DIR, image_filename)

    with open(image_path, "wb") as f:
        f.write(image.file.read())


    post = LostFoundPost(
        item_name=item_name,
        type=type,
        description=description,
        date=date,
        location=location,
        image_path=image_path,
        user_id=current_user.id
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@app.get("/lostfound/")
def get_lostfound_posts(session: Session = Depends(get_db)):
    return session.exec(select(LostFoundPost)).all()