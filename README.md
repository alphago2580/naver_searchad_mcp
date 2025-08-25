# Naver SearchAd MCP (Standalone)

이 디렉토리는 상위 폴더의 레거시 코드와 분리된 독립 실행 MCP 서버 패키지입니다.

## 설치

```bash
pip install .
naver-searchad-mcp --api-key YOUR_KEY --secret-key YOUR_SECRET --customer-id YOUR_CID
```

## 모듈 실행

```bash
python -m naver_searchad_mcp --api-key YOUR_KEY --secret-key YOUR_SECRET --customer-id YOUR_CID
```

환경변수 사용:

```bash
export NAVER_API_KEY=...
export NAVER_SECRET_KEY=...
export NAVER_CUSTOMER_ID=...
python -m naver_searchad_mcp
```

.env 파일 사용 (.env.example 복사):

```bash
cp .env.example .env  # Windows PowerShell: copy .env.example .env
# .env 편집 후
python -m naver_searchad_mcp
```

## Tools

- get_keyword_stats
- estimate_average_position_bids
- health

## Docker

```bash
docker build -t naver-searchad-mcp .
docker run --rm -e NAVER_API_KEY=KEY -e NAVER_SECRET_KEY=SEC -e NAVER_CUSTOMER_ID=CID naver-searchad-mcp
```
