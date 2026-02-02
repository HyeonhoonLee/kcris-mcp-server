# K-CRIS MCP Server

공공데이터포털의 [질병관리청 임상연구 DB](https://www.data.go.kr/data/3033869/openapi.do) OpenAPI를 연동하는 **MCP(Model Context Protocol) 서버**입니다.  
임상연구정보서비스(Clinical Research information Service, CRIS)에 대한 자세한 정보는 [임상연구정보서비스(CRIS) 소개](https://cris.nih.go.kr/cris/info/introduce.do)를 참고하세요.

## 기능

| 도구 | 설명 |
|------|------|
| `kcris_list_studies` | 검색어·페이지에 맞는 임상연구 **목록** 조회 (CRIS등록번호, 연구제목, 연구종류 등) |
| `kcris_get_study` | CRIS등록번호(예: KCT0002243)로 임상연구 **상세** 조회 (임상연구정보, 참여기관정보, 연구비지원기관정보, 연구책임기관정보, 중재군정보, 주요결과변수정보 등) |

## 요구사항

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (권장) 또는 pip

## 설치

### 1. Git clone & 프로젝트로 이동

```bash
git clone https://github.com/your-username/kcris-mcp-server.git
cd kcris-mcp-server
```

### 2. Python 의존성 설치

```bash
pip install -r requirements.txt
```

또는 `uv`를 사용하는 경우:

```bash
uv pip install -r requirements.txt
```

로컬 패키지를 실행하려면 설치가 필요합니다:

```bash
pip install -e .
# 또는 uv 사용 시
uv pip install -e .
```

### 3. 환경 변수 설정

```bash
cp .env.example .env
```

`.env` 파일을 편집하여 다음 변수를 설정하세요:

- `DATA_GO_KR_SERVICE_KEY': 공공데이터포털에서 발급한 인증키 ([공공데이터포털](https://www.data.go.kr/) → [질병관리청_임상연구 DB](https://www.data.go.kr/data/3033869/openapi.do) 활용신청 후 마이페이지에서 **개인 API인증키(일반 인증키)** 복사)

## 사용법

### 서버 실행 (로컬)

의존성 설치 후:

```bash
uv run kcris-mcp-server
```

또는 패키지를 설치한 경우:

```bash
python -m kcris_mcp_server
```

### Claude Desktop 이용 방법

Claude Desktop 설정 파일에 다음을 추가하세요.

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Claude Desktop에서 **설정 → Developer → Edit Config** 로 열 수 있습니다.

#### 방법 1: Python 직접 사용

```json
{
  "mcpServers": {
    "kcris": {
      "command": "python",
      "args": ["-m", "kcris_mcp_server"],
      "cwd": "/path/to/kcris-mcp-server",
      "env": {
        "DATA_GO_KR_SERVICE_KEY": "your-service-key-here"
      }
    }
  }
}
```

> 의존성 설치(`pip install -r requirements.txt`) 및 패키지 설치(`pip install -e .`)를 먼저 완료한 뒤 사용하세요.

#### 방법 2: uv 사용 (권장)

```json
{
  "mcpServers": {
    "kcris": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/kcris-mcp-server",
        "run",
        "kcris-mcp-server"
      ],
      "env": {
        "DATA_GO_KR_SERVICE_KEY": "your-service-key-here"
      }
    }
  }
}
```

> **참고**: Claude Desktop(GUI)에서는 `uv`가 PATH에 없을 수 있습니다. 이때는 `command`에 `uv`의 **전체 경로**를 넣으세요 (예: `/Users/username/.local/bin/uv`). 터미널에서 `which uv`로 확인할 수 있습니다.

#### 방법 3: uvx 사용 (로컬 프로젝트)

```json
{
  "mcpServers": {
    "kcris": {
      "command": "/path/to/uvx",
      "args": ["--from", "/path/to/kcris-mcp-server", "kcris-mcp-server"],
      "env": {
        "KCRIS_SERVICE_KEY": "your-service-key-here"
      }
    }
  }
}
```

- 설정 후 Claude Desktop을 완전히 종료했다가 다시 실행하세요.

### 질문 및 응답 예시

| 하고 싶은 것 | 예시 질문 |
|--------------|-----------|
| 조건/키워드로 목록 검색 | "당뇨 임상연구 목록 검색해줘", "심장 관련 모집 중인 임상시험 10개만 보여줘" |
| 특정 연구 상세 보기 | "KCT0002243 이 연구 상세 정보 알려줘", "CRIS등록번호 KCT0001234 참여기관이랑 연구책임기관 알려줘" |
| 페이지 조절 | "당뇨 검색해서 2페이지 결과도 보여줘" |

예시 대화:

- **User**: 당뇨 임상연구 목록 10개 검색해줘.
- **Response**: (K-CRIS 도구로 `kcris_list_studies(srch_word="당뇨", num_of_rows=10, page_no=1)` 호출 후 결과를 정리해서 보여줌)

- **User**: KCT0002243 이 연구 상세 정보 알려줘.
- **Response**: (K-CRIS 도구로 `kcris_get_study(cris_number="KCT0002243")` 호출 후 연구제목, 모집현황, 참여기관, 중재군 등을 요약해서 보여줌)

---

## API 참고

- **서비스 URL**: `http://apis.data.go.kr/1352159/crisinfodataview`
- **목록 조회**: `GET .../list` — `serviceKey`, `resultType=json`, `srchWord`, `numOfRows`(1~50), `pageNo`
- **상세 조회**: `GET .../detail` — `serviceKey`, `resultType=json`, `crisNumber`(CRIS등록번호)

## 라이선스

This project is licensed under the MIT License.
