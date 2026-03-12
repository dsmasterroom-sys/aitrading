# 이미지 스토리지 설정 가이드

Instagram Graph API는 **공개 URL**이 필요합니다. 3가지 옵션이 있습니다.

---

## 옵션 1: Cloudflare R2 (권장 ⭐)

**장점**:
- ✅ 월 10GB 무료
- ✅ 무료 Egress (전송량 무제한)
- ✅ S3 호환 API
- ✅ 빠름

**설정 (5분)**:

### Step 1: R2 버킷 생성
1. https://dash.cloudflare.com 로그인
2. 좌측 메뉴 "R2" 클릭
3. "Create bucket" 클릭
4. Bucket name: `gena-feed-images`
5. Location: Automatic
6. "Create bucket" 클릭

### Step 2: Public Access 설정
1. 생성된 버킷 클릭
2. "Settings" 탭 → "Public Access" 섹션
3. "Allow Access" 클릭
4. 공개 URL 확인 (예: `https://gena-feed-images.ACCOUNT_ID.r2.dev`)

### Step 3: API Token 생성
1. R2 메인 → 우측 상단 "Manage R2 API Tokens"
2. "Create API Token" 클릭
3. Token name: `gena-feed-upload`
4. Permissions: "Object Read & Write"
5. TTL: Forever
6. "Create API Token" 클릭
7. **Access Key ID** 및 **Secret Access Key** 복사

### Step 4: .env 설정
```env
CLOUDFLARE_ACCOUNT_ID=YOUR_ACCOUNT_ID
R2_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
R2_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
R2_BUCKET_NAME=gena-feed-images
R2_PUBLIC_URL=https://gena-feed-images.ACCOUNT_ID.r2.dev
```

### Step 5: 테스트
```bash
pip install boto3

python scripts/upload_to_storage.py test.png --provider r2
```

---

## 옵션 2: AWS S3

**장점**:
- ✅ 안정적
- ✅ 월 5GB 무료 (12개월)

**단점**:
- ⚠️ Egress 비용 (GB당 $0.09)
- ⚠️ 신용카드 필요

**설정 (10분)**:

### Step 1: S3 버킷 생성
1. https://s3.console.aws.amazon.com 로그인
2. "Create bucket" 클릭
3. Bucket name: `gena-feed-images`
4. Region: `us-east-1` (또는 가까운 리전)
5. **Block Public Access**: 모두 해제 (공개 버킷)
6. "Create bucket" 클릭

### Step 2: 버킷 정책 설정
1. 생성된 버킷 → "Permissions" 탭
2. "Bucket Policy" → "Edit" 클릭
3. 다음 정책 입력:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicRead",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::gena-feed-images/*"
    }
  ]
}
```

### Step 3: IAM 사용자 생성
1. https://console.aws.amazon.com/iam
2. "Users" → "Add users"
3. User name: `gena-feed-uploader`
4. "Access key - Programmatic access" 선택
5. Permissions: "Attach existing policies directly" → `AmazonS3FullAccess` 선택
6. "Create user" 클릭
7. **Access Key ID** 및 **Secret Access Key** 복사

### Step 4: .env 설정
```env
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
S3_BUCKET_NAME=gena-feed-images
AWS_REGION=us-east-1
```

### Step 5: 테스트
```bash
pip install boto3

python scripts/upload_to_storage.py test.png --provider s3
```

---

## 옵션 3: Imgur

**장점**:
- ✅ 무료
- ✅ 간단

**단점**:
- ⚠️ API 제한 (일 1250 requests)
- ⚠️ 안정성 낮음

**설정**: (현재 로그인 이슈로 보류)

---

## 🎯 추천

### 개발/테스트
- **Cloudflare R2** (무료 10GB, Egress 무료)

### 프로덕션
- **Cloudflare R2** (여전히 최고)
- 또는 **AWS S3** + **CloudFront** (CDN)

---

## 📝 사용법

### 1. 단일 파일 업로드
```bash
python scripts/upload_to_storage.py image.png --provider r2
```

### 2. 여러 파일 업로드
```bash
python scripts/upload_to_storage.py slides/*.png --provider r2
```

### 3. URL 리스트 저장
```bash
python scripts/upload_to_storage.py slides/*.png --provider r2 --output urls.txt
```

### 4. Instagram 발행
```bash
# 업로드
python scripts/upload_to_storage.py slides/*.png --provider r2 --output urls.txt

# 발행
python scripts/instagram_api.py publish-carousel \
  --images $(cat urls.txt | tr '\n' ' ') \
  --caption "봄 패션 트렌드 🌸 #봄패션"
```

---

## 🔧 자동화 통합

`scheduler` 에이전트가 자동으로:
1. 이미지 생성 (designer)
2. R2/S3 업로드 (upload_to_storage.py)
3. Instagram 발행 (instagram_api.py)

---

**최종 업데이트**: 2026-03-06  
**작성**: 자비스
