#!/usr/bin/env python3
"""
이미지를 클라우드 스토리지에 업로드 (S3 / Cloudflare R2)

사용법:
    # S3
    python scripts/upload_to_storage.py image.png --provider s3
    
    # Cloudflare R2
    python scripts/upload_to_storage.py image.png --provider r2
    
    # 여러 파일
    python scripts/upload_to_storage.py slides/*.png --provider r2
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# boto3 (AWS SDK)
try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    print("❌ boto3가 필요합니다: pip install boto3")
    sys.exit(1)


def upload_to_s3(file_path, bucket_name, object_name=None, region='us-east-1'):
    """
    AWS S3에 파일 업로드
    
    Args:
        file_path: 로컬 파일 경로
        bucket_name: S3 버킷 이름
        object_name: S3 객체 이름 (생략 시 파일명 사용)
        region: AWS 리전
    
    Returns:
        str: 공개 URL
    """
    if object_name is None:
        object_name = Path(file_path).name
    
    # S3 클라이언트
    s3_client = boto3.client(
        's3',
        region_name=region,
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    
    try:
        # 업로드
        s3_client.upload_file(
            file_path,
            bucket_name,
            object_name,
            ExtraArgs={'ACL': 'public-read'}  # 공개 읽기
        )
        
        # 공개 URL 생성
        url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_name}"
        return url
    
    except ClientError as e:
        print(f"❌ S3 업로드 실패: {e}")
        return None


def upload_to_r2(file_path, bucket_name, object_name=None, account_id=None, public_url=None):
    """
    Cloudflare R2에 파일 업로드
    
    Args:
        file_path: 로컬 파일 경로
        bucket_name: R2 버킷 이름
        object_name: 객체 이름 (생략 시 파일명 사용)
        account_id: Cloudflare 계정 ID
        public_url: 커스텀 도메인 (예: https://images.yourdomain.com)
    
    Returns:
        str: 공개 URL
    """
    if object_name is None:
        object_name = Path(file_path).name
    
    account_id = account_id or os.getenv('CLOUDFLARE_ACCOUNT_ID')
    if not account_id:
        print("❌ CLOUDFLARE_ACCOUNT_ID가 설정되지 않았습니다")
        return None
    
    # R2는 S3 호환 API 사용
    endpoint_url = f"https://{account_id}.r2.cloudflarestorage.com"
    
    s3_client = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY')
    )
    
    try:
        # 업로드
        s3_client.upload_file(
            file_path,
            bucket_name,
            object_name
        )
        
        # 공개 URL 생성
        if public_url:
            # 커스텀 도메인 사용
            url = f"{public_url.rstrip('/')}/{object_name}"
        else:
            # R2 기본 URL (Public Bucket 설정 필요)
            url = f"https://{bucket_name}.{account_id}.r2.dev/{object_name}"
        
        return url
    
    except ClientError as e:
        print(f"❌ R2 업로드 실패: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='클라우드 스토리지 이미지 업로드')
    parser.add_argument('files', nargs='+', help='업로드할 파일 경로')
    parser.add_argument('--provider', choices=['s3', 'r2'], default='r2', help='스토리지 제공자')
    parser.add_argument('--bucket', help='버킷 이름 (생략 시 환경변수 사용)')
    parser.add_argument('--output', '-o', help='URL 리스트를 저장할 파일')
    
    args = parser.parse_args()
    
    # 버킷 이름
    if args.bucket:
        bucket_name = args.bucket
    else:
        if args.provider == 's3':
            bucket_name = os.getenv('S3_BUCKET_NAME', 'gena-feed-images')
        else:
            bucket_name = os.getenv('R2_BUCKET_NAME', 'gena-feed-images')
    
    print("=" * 70)
    print(f"📤 {args.provider.upper()} 업로드")
    print("=" * 70)
    print(f"  버킷: {bucket_name}")
    print(f"  파일 수: {len(args.files)}")
    print()
    
    # 업로드
    urls = []
    
    for i, file_path in enumerate(args.files, 1):
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"[{i}/{len(args.files)}] ⚠️  파일 없음: {file_path}")
            continue
        
        print(f"[{i}/{len(args.files)}] 업로드 중: {file_path.name}")
        
        # 업로드
        if args.provider == 's3':
            url = upload_to_s3(str(file_path), bucket_name)
        else:
            url = upload_to_r2(str(file_path), bucket_name)
        
        if url:
            urls.append(url)
            print(f"  ✅ {url}")
        else:
            print(f"  ❌ 업로드 실패")
    
    print()
    print("=" * 70)
    print(f"✅ 완료: {len(urls)}/{len(args.files)}개 업로드 성공")
    print("=" * 70)
    
    # URL 리스트 저장
    if args.output and urls:
        output_path = Path(args.output)
        output_path.write_text('\n'.join(urls))
        print(f"💾 URL 저장: {output_path}")
    
    # 결과 출력
    if urls:
        print()
        print("📋 업로드된 URL:")
        for url in urls:
            print(f"  {url}")
    
    return 0 if len(urls) == len(args.files) else 1


if __name__ == "__main__":
    sys.exit(main())
