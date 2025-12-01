from fastapi import FastAPI, Depends, HTTPException, Request, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, func, select
from sqlalchemy.orm import declarative_base
import os
from datetime import datetime
from session_manager import session_manager

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

class ContactUs(Base):
    __tablename__ = "contactus"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    mail = Column(String(100))
    telno = Column(String(50))
    referrer = Column(String(100))
    title = Column(String(200))
    contents = Column(Text)
    confirm = Column(Boolean)
    created_at = Column(TIMESTAMP, server_default=func.now())

class ContactUsCreate(BaseModel):
    name: str
    mail: EmailStr
    telno: str = ""
    referrer: str = ""
    title: str
    contents: str
    confirm: bool

class ContactUsResponse(BaseModel):
    id: int
    name: str
    mail: str
    telno: str
    referrer: str
    title: str
    contents: str
    confirm: bool
    created_at: str

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        # created_at을 문자열로 변환
        if hasattr(obj, 'created_at') and obj.created_at:
            obj.created_at = obj.created_at.isoformat()
        return super().from_orm(obj)

# 세션 관련 모델
class LoginRequest(BaseModel):
    username: str
    password: str

class SessionResponse(BaseModel):
    session_id: str
    user_data: dict
    created_at: str
    last_accessed: str

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용하도록 수정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_db():
    async with SessionLocal() as session:
        yield session

async def get_current_session(session_token: str = Cookie(None, alias="session_token")):
    """현재 세션 조회"""
    if not session_token:
        raise HTTPException(status_code=401, detail="Session token required")
    
    session_id = session_manager.decode_session_token(session_token)
    if not session_id:
        raise HTTPException(status_code=401, detail="Invalid session token")
    
    session = await session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Session expired")
    
    return session

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await session_manager.disconnect()

@app.get("/")
async def root():
    return {"message": "BGROUND API is running"}

# 세션 관리 API
@app.post("/api/login")
async def login(request: LoginRequest, response: Response):
    """사용자 로그인 및 세션 생성"""
    # 간단한 인증 로직 (실제로는 데이터베이스에서 사용자 확인)
    if request.username == "admin" and request.password == "admin123":
        user_data = {
            "username": request.username,
            "role": "admin",
            "login_time": datetime.utcnow().isoformat()
        }
        
        session_id = await session_manager.create_session(user_data)
        session_token = session_manager.create_session_token(session_id)
        
        # 쿠키에 세션 토큰 설정
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            secure=False,  # HTTPS 사용 시 True로 변경
            samesite="lax",
            max_age=3600  # 1시간
        )
        
        return {"success": True, "message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/logout")
async def logout(response: Response, session: dict = Depends(get_current_session)):
    """사용자 로그아웃 및 세션 삭제"""
    session_token = session_manager.create_session_token(session.get("session_id", ""))
    await session_manager.delete_session(session.get("session_id", ""))
    
    # 쿠키 삭제
    response.delete_cookie(key="session_token")
    
    return {"success": True, "message": "Logout successful"}

@app.get("/api/session", response_model=SessionResponse)
async def get_session_info(session: dict = Depends(get_current_session)):
    """현재 세션 정보 조회"""
    return SessionResponse(
        session_id=session.get("session_id", ""),
        user_data=session.get("user_data", {}),
        created_at=session.get("created_at", ""),
        last_accessed=session.get("last_accessed", "")
    )

@app.post("/api/session/extend")
async def extend_session(session: dict = Depends(get_current_session)):
    """세션 만료 시간 연장"""
    session_id = session.get("session_id", "")
    success = await session_manager.extend_session(session_id)
    
    if success:
        return {"success": True, "message": "Session extended"}
    else:
        raise HTTPException(status_code=400, detail="Failed to extend session")

@app.get("/api/contactus", response_model=list[ContactUsResponse])
async def get_contactus(db: AsyncSession = Depends(get_db), session: dict = Depends(get_current_session)):
    """문의하기 데이터 전체 조회 (인증 필요)"""
    result = await db.execute(select(ContactUs).order_by(ContactUs.created_at.desc()))
    contacts = result.scalars().all()
    
    # 각 contact 객체의 created_at을 문자열로 변환
    response_contacts = []
    for contact in contacts:
        contact_dict = {
            "id": contact.id,
            "name": contact.name,
            "mail": contact.mail,
            "telno": contact.telno,
            "referrer": contact.referrer,
            "title": contact.title,
            "contents": contact.contents,
            "confirm": contact.confirm,
            "created_at": contact.created_at.isoformat() if contact.created_at else None
        }
        response_contacts.append(ContactUsResponse(**contact_dict))
    
    return response_contacts

@app.get("/api/contactus/{contact_id}", response_model=ContactUsResponse)
async def get_contactus_by_id(contact_id: int, db: AsyncSession = Depends(get_db), session: dict = Depends(get_current_session)):
    """특정 문의하기 데이터 조회 (인증 필요)"""
    result = await db.execute(select(ContactUs).where(ContactUs.id == contact_id))
    contact = result.scalar_one_or_none()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    contact_dict = {
        "id": contact.id,
        "name": contact.name,
        "mail": contact.mail,
        "telno": contact.telno,
        "referrer": contact.referrer,
        "title": contact.title,
        "contents": contact.contents,
        "confirm": contact.confirm,
        "created_at": contact.created_at.isoformat() if contact.created_at else None
    }
    return ContactUsResponse(**contact_dict)

@app.post("/api/contactus")
async def create_contactus(data: ContactUsCreate, db: AsyncSession = Depends(get_db)):
    """문의하기 데이터 생성 (인증 불필요)"""
    contact = ContactUs(**data.dict())
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return {"success": True, "id": contact.id}
