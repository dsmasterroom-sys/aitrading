#!/usr/bin/env python3
"""
Google Sheets에서 API 키 읽어와서 .env 파일 업데이트

사용법:
    python scripts/sync_env_from_sheet.py
"""

import os
import sys
import json
from pathlib import Path

# Google Sheets API
try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    print("❌ gspread 패키지가 필요합니다:")
    print("   pip install gspread google-auth")
    sys.exit(1)

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).parent.parent
WORKSPACE_ROOT = Path("/Users/master/.openclaw/workspace")

# Google Sheets 설정
SHEET_ID = "189aWQEXCdiGuCQ8NObrfuHlEtr5pEK8clJWG1ef4w4A"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]


def get_google_sheets_client():
    """Google Sheets 클라이언트 생성"""
    
    # Credential 파일 경로
    token_file = WORKSPACE_ROOT / "token_pipeline.json"
    
    if not token_file.exists():
        print(f"❌ Token 파일이 없습니다: {token_file}")
        sys.exit(1)
    
    try:
        # OAuth Token 방식 (token_pipeline.json)
        from google.oauth2.credentials import Credentials as OAuthCredentials
        
        with open(token_file, 'r') as f:
            token_data = json.load(f)
        
        # OAuth Credentials 생성
        creds = OAuthCredentials(
            token=token_data.get('token'),
            refresh_token=token_data.get('refresh_token'),
            token_uri=token_data.get('token_uri'),
            client_id=token_data.get('client_id'),
            client_secret=token_data.get('client_secret'),
            scopes=token_data.get('scopes')
        )
        
        client = gspread.authorize(creds)
        print(f"✅ Google Sheets 인증 완료 (OAuth Token)")
        return client
    
    except Exception as e:
        print(f"❌ Google Sheets 인증 실패: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def read_api_keys_from_sheet(client):
    """Google Sheets에서 API 키 읽기"""
    
    print(f"📊 Google Sheets 읽는 중...")
    print(f"   Sheet ID: {SHEET_ID}")
    
    try:
        # 시트 열기
        sheet = client.open_by_key(SHEET_ID)
        
        # 첫 번째 워크시트 (또는 특정 시트명)
        worksheet = sheet.get_worksheet(0)
        
        # 모든 데이터 읽기
        all_values = worksheet.get_all_values()
        
        if not all_values:
            print("❌ 시트가 비어있습니다")
            return {}
        
        print(f"✅ {len(all_values)}개 행 읽기 완료")
        
        # 헤더 확인
        headers = all_values[0]
        print(f"   헤더: {headers}")
        
        # API 키 추출 (헤더에 따라 다름)
        # 예상 구조: Key | Value 또는 Service | Key | Value
        
        api_keys = {}
        
        for i, row in enumerate(all_values[1:], 2):  # 헤더 제외
            if len(row) < 2:
                continue
            
            # 예: [Service, Key, Value] 또는 [Key, Value]
            if len(row) >= 3:
                # Service | Key | Value 형식
                service = row[0].strip()
                key = row[1].strip()
                value = row[2].strip()
                
                if key and value:
                    api_keys[key] = value
                    print(f"   [{i}] {service}: {key} = {value[:20]}...")
            
            elif len(row) >= 2:
                # Key | Value 형식
                key = row[0].strip()
                value = row[1].strip()
                
                if key and value:
                    api_keys[key] = value
                    print(f"   [{i}] {key} = {value[:20]}...")
        
        print(f"\n✅ 총 {len(api_keys)}개 API 키 발견")
        return api_keys
    
    except Exception as e:
        print(f"❌ 시트 읽기 실패: {e}")
        import traceback
        traceback.print_exc()
        return {}


def update_env_file(api_keys):
    """
    .env 파일 업데이트
    
    Instagram 자동화 관련 키만 선택적으로 업데이트
    """
    
    env_file = PROJECT_ROOT / ".env"
    
    # Instagram 관련 키 매핑
    KEY_MAPPING = {
        "INSTAGRAM_ACCESS_TOKEN": "INSTAGRAM_ACCESS_TOKEN",
        "INSTAGRAM_ACCOUNT_ID": "INSTAGRAM_ACCOUNT_ID",
        "INSTAGRAM_USER_ID": "INSTAGRAM_ACCOUNT_ID",  # 별칭
        "META_APP_ID": "META_APP_ID",
        "META_APP_SECRET": "META_APP_SECRET",
        "IMGUR_CLIENT_ID": "IMGUR_CLIENT_ID",
        "NANOGEN_API_KEY": "NANOGEN_API_KEY",
        "NANOGEN_API_URL": "NANOGEN_API_URL",
    }
    
    # 기존 .env 읽기
    env_content = {}
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    env_content[key.strip()] = value.strip()
    
    print(f"\n📝 .env 파일 업데이트 중...")
    updated_keys = []
    
    # API 키 업데이트
    for sheet_key, env_key in KEY_MAPPING.items():
        if sheet_key in api_keys:
            env_content[env_key] = api_keys[sheet_key]
            updated_keys.append(env_key)
            print(f"   ✅ {env_key} 업데이트")
    
    # .env 파일 쓰기
    with open(env_file, 'w') as f:
        f.write("# Instagram Automation - Auto-synced from Google Sheets\n")
        f.write(f"# Last updated: {__import__('datetime').datetime.now().isoformat()}\n\n")
        
        for key, value in sorted(env_content.items()):
            f.write(f"{key}={value}\n")
    
    print(f"\n✅ .env 파일 저장 완료: {env_file}")
    print(f"   업데이트된 키: {len(updated_keys)}개")
    print(f"   {', '.join(updated_keys)}")
    
    return updated_keys


def main():
    print("=" * 70)
    print("🔑 Google Sheets → .env 동기화")
    print("=" * 70)
    print()
    
    # 1. Google Sheets 클라이언트
    client = get_google_sheets_client()
    
    # 2. API 키 읽기
    api_keys = read_api_keys_from_sheet(client)
    
    if not api_keys:
        print("\n❌ API 키를 찾을 수 없습니다")
        return 1
    
    # 3. .env 파일 업데이트
    updated_keys = update_env_file(api_keys)
    
    if not updated_keys:
        print("\n⚠️  업데이트된 키가 없습니다")
        return 1
    
    print()
    print("=" * 70)
    print("✅ 동기화 완료!")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
