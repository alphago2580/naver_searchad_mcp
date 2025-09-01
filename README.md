# Naver SearchAd MCP

> Naver SearchAd 키워드 통계, 입찰가 추정 툴을 Claude Desktop 에서 바로 호출할 수 있는 MCP 서버 / DXT 확장.

## 🚀 일반 사용자: 가장 쉬운 설치 (임베디드 DXT)

Python 설치 필요 없음 (Windows).

1. 최신 `naver-searchad-embedded-lite-<version>.dxt` 파일 다운로드
2. Claude Desktop 열기 → Extensions 패널(또는 파일 드래그)로 .dxt 추가
3. 확장 추가 UI에서 API Key / Secret / Customer ID 입력
4. Tools 목록에서 `health` 실행 → `{ "status": "ok" }` 나오면 완료

문제 시 Claude 로그에서 `[naver-searchad]` 메시지 참고.

## 🔑 API 자격증명 설정

필요 값:

* NAVER_API_KEY
* NAVER_SECRET_KEY
* NAVER_CUSTOMER_ID

DXT 설치 시 UI 필드에 직접 입력 (암호화 저장은 Claude 정책 따름). 개발/소스 실행 시에는 환경변수 또는 `.env` 지원.

## 🛠 제공 Tools

| 이름 | 설명 |
|------|------|
| health | 상태 확인 및 기본 파라미터 확인 |
| get_keyword_stats | 최대 BATCH 단위로 키워드 통계 조회 (캐시 옵션) |
| estimate_average_position_bids | 평균 노출 위치별 예상 입찰가 추정 |

## 🧪 빠른 사용 예 (Claude 대화 중)

```text
/tool health
/tool get_keyword_stats {"keywords":["나이키","운동화"],"show_detail":true}
```

## 👩‍💻 개발자 / 고급 사용자

### A. 소스/호스트 Python 방식

```bash
git clone https://github.com/alphago2580/naver_searchad_mcp.git
cd naver_searchad_mcp
pip install -e .
export NAVER_API_KEY=... NAVER_SECRET_KEY=... NAVER_CUSTOMER_ID=...
python -m naver_searchad_mcp --help
```

Claude config (수동 등록) 예시:

```json
"naver-searchad": {
	"command": "python",
	"args": ["-m", "naver_searchad_mcp"],
	"env": {"NAVER_API_KEY": "...", "NAVER_SECRET_KEY": "...", "NAVER_CUSTOMER_ID": "..."}
}
```

### B. Docker

```bash
docker build -t naver-searchad-mcp .
docker run --rm -e NAVER_API_KEY=KEY -e NAVER_SECRET_KEY=SEC -e NAVER_CUSTOMER_ID=CID naver-searchad-mcp
```

## 📦 임베디드 DXT 빌드 (Windows)

개발자가 직접 재생성할 때:

```powershell
cd dxt_extension
pwsh .\prepare_embedded_python.ps1 -PyVersion 3.11.9   # 임베디드 런타임 (필요 시 최초 1회)
pwsh .\build_vendor.ps1                               # vendor 라이브러리 (fastmcp/requests 등)
dxt pack . naver-searchad-embedded-lite-<ver>.dxt
```

주요 파일:

```text
dxt_extension/
	manifest.json               # DXT 메타 + platform_overrides.win32
	server/main.py              # 경로 탐지 + FastMCP 구동
	naver_searchad_mcp/         # 번들 패키지 (필요 최소 코드)
	server/lib/                 # vendor 사이트 패키지
	runtime/win32/python/       # 임베디드 Python (재생성 가능)
```

## 🧹 저장소 구조 & 정리

커밋 대상 유지 권장:

* `naver_searchad_mcp/` (핵심 코드)
* `dxt_extension/manifest.json`, `server/main.py`, `prepare_embedded_python.ps1`, `build_vendor.ps1`
* vendor 라이브러리(재현성 위해 커밋 가능) 또는 스크립트로 재생성 선택

커밋 제외(.gitignore 추가됨):

* `*.dxt` 산출물
* `dxt_extension/runtime/` (임베디드 재생성 가능)
* `_inspect/`, `.bundle_venv/`

## 🔍 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| ModuleNotFoundError (임베디드) | `_pth` 경로/ sys.path 삽입 실패 | 최신 DXT 재설치 (버전 증가) |
| Tools 미표시 | Claude 재시작 필요 또는 Key 누락 | Claude 완전 종료 후 재시작 |
| 401/403 | 잘못된 API Key | 키 재확인 / 재발급 |
| 지연/타임아웃 | API rate 제한 | 키워드 배치 줄이기 |

## 🔐 보안/키 관리

* `.env` / `api_keys.txt` 는 커밋 금지
* 필요 최소 권한 키 사용
* 의심 시 즉시 키 회전

## 🧾 버전

* 패키지: `0.2.5`
* DXT manifest 동일 버전 태깅 (캐시 무효화 목적)

## 📄 라이선스

Proprietary (내부/허가된 사용 범위로 제한). 필요 시 LICENSE 조정.

---

피드백 / 버그 제보 환영: Issue 등록 또는 PR.
> ⚡ .dxt 추가

