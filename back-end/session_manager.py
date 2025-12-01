import os
import json
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import aioredis
from itsdangerous import URLSafeSerializer

class RedisSessionManager:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis = None
        self.serializer = URLSafeSerializer(os.getenv("SECRET_KEY", "your-secret-key-here"))
        self.session_timeout = int(os.getenv("SESSION_TIMEOUT", "3600"))  # 1시간 기본값
    
    async def connect(self):
        """Redis 연결"""
        if not self.redis:
            self.redis = await aioredis.from_url(self.redis_url, encoding="utf-8", decode_responses=True)
    
    async def disconnect(self):
        """Redis 연결 해제"""
        if self.redis:
            await self.redis.close()
            self.redis = None
    
    def generate_session_id(self) -> str:
        """새로운 세션 ID 생성"""
        return str(uuid.uuid4())
    
    async def create_session(self, user_data: Dict[str, Any]) -> str:
        """새로운 세션 생성"""
        await self.connect()
        session_id = self.generate_session_id()
        
        session_data = {
            "user_data": user_data,
            "created_at": datetime.utcnow().isoformat(),
            "last_accessed": datetime.utcnow().isoformat()
        }
        
        # 세션 데이터를 Redis에 저장
        await self.redis.setex(
            f"session:{session_id}",
            self.session_timeout,
            json.dumps(session_data)
        )
        
        return session_id
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """세션 데이터 조회"""
        await self.connect()
        
        session_data = await self.redis.get(f"session:{session_id}")
        if not session_data:
            return None
        
        # 세션 데이터 파싱
        session = json.loads(session_data)
        
        # 세션 ID 추가
        session["session_id"] = session_id
        
        # 마지막 접근 시간 업데이트
        session["last_accessed"] = datetime.utcnow().isoformat()
        await self.redis.setex(
            f"session:{session_id}",
            self.session_timeout,
            json.dumps(session)
        )
        
        return session
    
    async def update_session(self, session_id: str, user_data: Dict[str, Any]) -> bool:
        """세션 데이터 업데이트"""
        await self.connect()
        
        session_data = await self.redis.get(f"session:{session_id}")
        if not session_data:
            return False
        
        session = json.loads(session_data)
        session["user_data"] = user_data
        session["last_accessed"] = datetime.utcnow().isoformat()
        
        await self.redis.setex(
            f"session:{session_id}",
            self.session_timeout,
            json.dumps(session)
        )
        
        return True
    
    async def delete_session(self, session_id: str) -> bool:
        """세션 삭제"""
        await self.connect()
        result = await self.redis.delete(f"session:{session_id}")
        return result > 0
    
    async def extend_session(self, session_id: str) -> bool:
        """세션 만료 시간 연장"""
        await self.connect()
        
        session_data = await self.redis.get(f"session:{session_id}")
        if not session_data:
            return False
        
        session = json.loads(session_data)
        session["last_accessed"] = datetime.utcnow().isoformat()
        
        await self.redis.setex(
            f"session:{session_id}",
            self.session_timeout,
            json.dumps(session)
        )
        
        return True
    
    def create_session_token(self, session_id: str) -> str:
        """세션 ID를 토큰으로 암호화"""
        return self.serializer.dumps(session_id)
    
    def decode_session_token(self, token: str) -> Optional[str]:
        """토큰을 세션 ID로 복호화"""
        try:
            return self.serializer.loads(token)
        except:
            return None

# 전역 세션 매니저 인스턴스
session_manager = RedisSessionManager() 