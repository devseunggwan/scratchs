#!/bin/bash

# S3에서 특정 경로의 모든 파일을 로컬로 다운로드하는 스크립트
# 사용법: ./download.sh <s3-path> <local-path>

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 사용법 출력 함수
usage() {
    echo "사용법: $0 <s3-path> <local-path>"
    echo ""
    echo "예시:"
    echo "  $0 s3://my-bucket/path/to/files ./downloads"
    echo "  $0 s3://my-bucket/prefix/ /Users/username/data"
    echo ""
    echo "옵션:"
    echo "  --profile <profile-name>  AWS 프로파일 지정"
    echo "  --dryrun                  실제 다운로드 없이 시뮬레이션만 수행"
    echo "  --exclude <pattern>       특정 패턴의 파일 제외"
    echo "  --include <pattern>       특정 패턴의 파일만 포함"
    exit 1
}

# AWS CLI 설치 확인
if ! command -v aws &> /dev/null; then
    echo -e "${RED}Error: AWS CLI가 설치되어 있지 않습니다.${NC}"
    echo "설치 방법: brew install awscli"
    exit 1
fi

# 인자 파싱
S3_PATH=""
LOCAL_PATH=""
AWS_PROFILE=""
DRYRUN=""
EXCLUDE=""
INCLUDE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --profile)
            AWS_PROFILE="--profile $2"
            shift 2
            ;;
        --dryrun)
            DRYRUN="--dryrun"
            shift
            ;;
        --exclude)
            EXCLUDE="--exclude $2"
            shift 2
            ;;
        --include)
            INCLUDE="--include $2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            if [ -z "$S3_PATH" ]; then
                S3_PATH="$1"
            elif [ -z "$LOCAL_PATH" ]; then
                LOCAL_PATH="$1"
            else
                echo -e "${RED}Error: 너무 많은 인자가 전달되었습니다.${NC}"
                usage
            fi
            shift
            ;;
    esac
done

# 필수 인자 확인
if [ -z "$S3_PATH" ] || [ -z "$LOCAL_PATH" ]; then
    echo -e "${RED}Error: S3 경로와 로컬 경로가 모두 필요합니다.${NC}"
    usage
fi

# S3 경로 형식 확인
if [[ ! "$S3_PATH" =~ ^s3:// ]]; then
    echo -e "${RED}Error: S3 경로는 s3://로 시작해야 합니다.${NC}"
    exit 1
fi

# 로컬 디렉토리 생성
if [ ! -d "$LOCAL_PATH" ]; then
    echo -e "${YELLOW}로컬 디렉토리가 존재하지 않아 생성합니다: $LOCAL_PATH${NC}"
    mkdir -p "$LOCAL_PATH"
fi

# S3 경로 존재 확인
echo -e "${YELLOW}S3 경로 확인 중...${NC}"
if ! aws s3 ls "$S3_PATH" $AWS_PROFILE &> /dev/null; then
    echo -e "${RED}Error: S3 경로에 접근할 수 없거나 존재하지 않습니다: $S3_PATH${NC}"
    echo "권한 또는 경로를 확인해주세요."
    exit 1
fi

# 다운로드 시작
echo -e "${GREEN}다운로드 시작...${NC}"
echo "S3 경로: $S3_PATH"
echo "로컬 경로: $LOCAL_PATH"

if [ -n "$DRYRUN" ]; then
    echo -e "${YELLOW}[DRY RUN 모드] 실제 다운로드는 수행되지 않습니다.${NC}"
fi

# AWS S3 sync 명령어 실행
aws s3 sync "$S3_PATH" "$LOCAL_PATH" \
    $AWS_PROFILE \
    $DRYRUN \
    $EXCLUDE \
    $INCLUDE \
    --no-progress

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 다운로드가 성공적으로 완료되었습니다!${NC}"
    
    # 다운로드된 파일 수 카운트
    if [ -z "$DRYRUN" ]; then
        FILE_COUNT=$(find "$LOCAL_PATH" -type f | wc -l | tr -d ' ')
        echo "다운로드된 파일 수: $FILE_COUNT"
        
        # 디렉토리 크기 출력
        if command -v du &> /dev/null; then
            SIZE=$(du -sh "$LOCAL_PATH" | cut -f1)
            echo "전체 크기: $SIZE"
        fi
    fi
else
    echo -e "${RED}✗ 다운로드 중 오류가 발생했습니다.${NC}"
    exit 1
fi

