#!/usr/bin/env python3
"""
Redis 세션 관리 기능 테스트 스크립트
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_session_management():
    """세션 관리 기능 테스트"""
    print("=== Redis 세션 관리 테스트 ===\n")
    
    # 1. 로그인 테스트
    print("1. 로그인 테스트")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/api/login", json=login_data)
    print(f"로그인 응답: {response.status_code}")
    print(f"응답 내용: {response.json()}")
    
    if response.status_code != 200:
        print("❌ 로그인 실패")
        return
    
    # 쿠키 저장
    cookies = response.cookies
    print(f"세션 쿠키: {cookies.get('session_token')}")
    print("✅ 로그인 성공\n")
    
    # 2. 세션 정보 조회 테스트
    print("2. 세션 정보 조회 테스트")
    response = requests.get(f"{BASE_URL}/api/session", cookies=cookies)
    print(f"세션 조회 응답: {response.status_code}")
    if response.status_code == 200:
        session_info = response.json()
        print(f"세션 정보: {json.dumps(session_info, indent=2, ensure_ascii=False)}")
        print("✅ 세션 조회 성공\n")
    else:
        print(f"❌ 세션 조회 실패: {response.text}\n")
    
    # 3. 문의 데이터 조회 테스트 (인증 필요)
    print("3. 문의 데이터 조회 테스트 (인증 필요)")
    response = requests.get(f"{BASE_URL}/api/contactus", cookies=cookies)
    print(f"문의 데이터 조회 응답: {response.status_code}")
    if response.status_code == 200:
        contacts = response.json()
        print(f"문의 데이터 수: {len(contacts)}")
        print("✅ 문의 데이터 조회 성공\n")
    else:
        print(f"❌ 문의 데이터 조회 실패: {response.text}\n")
    
    # 4. 세션 연장 테스트
    print("4. 세션 연장 테스트")
    response = requests.post(f"{BASE_URL}/api/session/extend", cookies=cookies)
    print(f"세션 연장 응답: {response.status_code}")
    if response.status_code == 200:
        print(f"세션 연장 결과: {response.json()}")
        print("✅ 세션 연장 성공\n")
    else:
        print(f"❌ 세션 연장 실패: {response.text}\n")
    
    # 5. 로그아웃 테스트
    print("5. 로그아웃 테스트")
    response = requests.post(f"{BASE_URL}/api/logout", cookies=cookies)
    print(f"로그아웃 응답: {response.status_code}")
    if response.status_code == 200:
        print(f"로그아웃 결과: {response.json()}")
        print("✅ 로그아웃 성공\n")
    else:
        print(f"❌ 로그아웃 실패: {response.text}\n")
    
    # 6. 로그아웃 후 세션 접근 테스트
    print("6. 로그아웃 후 세션 접근 테스트")
    response = requests.get(f"{BASE_URL}/api/session", cookies=cookies)
    print(f"세션 접근 응답: {response.status_code}")
    if response.status_code == 401:
        print("✅ 세션 무효화 확인 (예상된 결과)")
    else:
        print(f"❌ 세션 무효화 실패: {response.text}")
    
    print("\n=== 테스트 완료 ===")

def test_redis_connection():
    """Redis 연결 테스트"""
    print("=== Redis 연결 테스트 ===\n")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"API 서버 응답: {response.status_code}")
        if response.status_code == 200:
            print("✅ API 서버 정상 동작")
        else:
            print("❌ API 서버 오류")
    except requests.exceptions.ConnectionError:
        print("❌ API 서버에 연결할 수 없습니다.")
        print("Docker Compose가 실행 중인지 확인하세요.")
        print("실행 명령어: docker-compose up -d")

if __name__ == "__main__":
    print("Redis 세션 관리 테스트를 시작합니다...\n")
    
    # Redis 연결 테스트
    test_redis_connection()
    print()
    
    # 세션 관리 테스트
    test_session_management() 