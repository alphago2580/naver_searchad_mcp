# Naver SearchAd MCP 

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

## Claude Desktop 연동 (MCP 서버 설정)

Claude Desktop(Anthropic)에서 이 패키지를 MCP 서버로 불러와 대화 중 Naver 광고 데이터를 조회할 수 있습니다.

### 1. 설치

이미 설치했다면 생략 가능합니다.

```bash
pip install naver-searchad-mcp  # 또는 소스 루트에서: pip install .
```

### 2. 환경 변수 설정 (택 1)

1. OS 환경 변수 직접 설정

PowerShell 예시:

```powershell
$env:NAVER_API_KEY = "YOUR_KEY"
$env:NAVER_SECRET_KEY = "YOUR_SECRET"
$env:NAVER_CUSTOMER_ID = "YOUR_CID"
```

1. .env 파일 사용 (권장)

프로젝트 루트에 `.env` 파일 생성:

```env
NAVER_API_KEY=YOUR_KEY
NAVER_SECRET_KEY=YOUR_SECRET
NAVER_CUSTOMER_ID=YOUR_CID
```

(.env 사용 시 아래 config에서 env 블록을 생략해도 되고, 명시적으로 넣어도 됩니다.)

### 3. Claude Desktop 설정 파일 위치

| OS | 경로 |
| --- | --- |
| Windows | `%APPDATA%\\Claude\\claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Linux (베타) | `~/.config/Claude/claude_desktop_config.json` |

파일이 없으면 Claude Desktop을 한 번 실행 후 종료하면 생성됩니다.

### 4. config 예시 추가

`claude_desktop_config.json` 의 `mcpServers` 객체 안에 항목을 추가합니다. (다른 서버가 이미 있다면 JSON 쉼표 주의)

```jsonc
{
	// ... 기존 설정 ...
	"mcpServers": {
		// ... 다른 서버 ...
		"naver-searchad": {
			"command": "naver-searchad-mcp", // 또는 "python"
			"args": [
				// python을 사용하는 경우: "-m", "naver_searchad_mcp"
			],
			"env": {
				"NAVER_API_KEY": "YOUR_KEY",
				"NAVER_SECRET_KEY": "YOUR_SECRET",
				"NAVER_CUSTOMER_ID": "YOUR_CID"
			}
		}
	}
}
```

python -m 형태를 쓰고 싶다면:

```jsonc
"naver-searchad": {
	"command": "python",
	"args": ["-m", "naver_searchad_mcp"],
	"env": {
		"NAVER_API_KEY": "YOUR_KEY",
		"NAVER_SECRET_KEY": "YOUR_SECRET",
		"NAVER_CUSTOMER_ID": "YOUR_CID"
	}
}
```

### 5. Claude 재시작 & 동작 확인

1. Claude Desktop 완전히 종료 후 다시 실행
2. 신규 대화 열기 → 우측/상단 Tools 패널(또는 / 입력)에서 서버가 로드되었는지 확인
3. `health` 툴 실행 → 정상 응답이면 연결 OK
4. `get_keyword_stats` 실행 시 필요한 파라미터를 Claude가 물으면 값 제공

### 6. 빠른 점검 체크리스트

- 패키지 설치: `pip show naver-searchad-mcp` 로 확인
- 실행 파일 인식: 터미널에서 `naver-searchad-mcp --help` 동작 여부
- JSON 구문 오류: config 저장 후 중괄호/쉼표 확인 (JSON Lint 권장)
- 권한: Windows에서 보안 소프트웨어가 python 실행 차단하지 않는지

### 7. 로깅 / 디버깅

Claude UI에서 서버가 안 뜨는 경우:

```powershell
naver-searchad-mcp --api-key "YOUR_KEY" --secret-key "YOUR_SECRET" --customer-id "YOUR_CID" --debug
```
직접 실행하여 에러 스택을 먼저 해결 후 config로 다시 연결.

### 8. 안전한 키 관리 팁

- 공개 저장소에 `.env` 커밋 금지 (`.gitignore` 확인)
- 키 로테이션 주기적으로 수행 (유출 의심 시 즉시 교체)
- 최소 권한 CID 사용

### 9. FAQ

Q. 툴 목록에 안 보입니다.
- A: config JSON에 `mcpServers` 루트 키가 존재하는지, JSON 파싱 오류가 없는지, 재시작했는지 확인.

Q. 인증 오류(401/403)가 납니다.
- A: 키/시크릿/CID 오타, 혹은 네이버 광고 API 권한 여부 재확인.

Q. Windows에서 한글 경로 때문에 실행 실패.
- A: Python 설치 경로에 공백/한글이 포함된 경우 `"command": "python"` 대신 절대경로 (`C:\\Python312\\python.exe`) 명시 권장.
