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

## 인증키

K-CRIS API는 **공공데이터포털(data.go.kr)** 인증키가 필요합니다.

1. [공공데이터포털](https://www.data.go.kr/) 회원가입 후 로그인
2. [「질병관리청_임상연구 DB」](https://www.data.go.kr/data/3033869/openapi.do) 오픈 API 검색 후 활용신청
3. 마이페이지에서 **인증키(일반 인증키)** 발급

## 설치 및 실행 (uvx)

프로젝트 루트에서:

```bash
# 의존성 설치 후 서버 실행 (stdio)
uv run kcris-mcp-server
```

또는 **uvx**로 전역 실행(패키지가 PyPI에 공개된 경우):

```bash
uvx kcris-mcp-server
```

로컬 패키지를 uvx로 실행하려면:

```bash
uvx --from . kcris-mcp-server
```

## MCP 클라이언트 설정 예시

Cursor, Claude Desktop, Cline 등 MCP 클라이언트에 아래처럼 추가합니다.

**stdio (권장)**

```json
{
  "mcpServers": {
    "kcris": {
      "command": "uvx",
      "args": ["--from", "/path/to/kcris-mcp-server", "kcris-mcp-server"],
      "env": {
        "KCRIS_SERVICE_KEY": "발급받은_인증키"
      }
    }
  }
}
```

로컬에서 `uv run` 사용 시:

```json
{
  "mcpServers": {
    "kcris": {
      "command": "uv",
      "args": ["run", "kcris-mcp-server"],
      "cwd": "/path/to/kcris-mcp-server",
      "env": {
        "KCRIS_SERVICE_KEY": "발급받은_인증키"
      }
    }
  }
}
```

---

## Claude Desktop 사용 예시

### 설정 파일 위치

| OS | 경로 |
|----|------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |

Claude Desktop에서 **설정 → Developer → Edit Config** 로 열 수 있습니다.

### 설정 예시 (Claude Desktop)

`command`, `args`, `cwd`의 경로는 본인 환경에 맞게 넣으면 됩니다.

```json
{
  "mcpServers": {
    "kcris": {
      "command": "uvx",
      "args": ["--from", "/path/to/kcris-mcp-server", "kcris-mcp-server"],
      "env": {
        "KCRIS_SERVICE_KEY": "발급받은_인증키"
      }
    }
  }
}
```

또는 `uv run` 사용:

```json
{
  "mcpServers": {
    "kcris": {
      "command": "uv",
      "args": ["run", "kcris-mcp-server"],
      "cwd": "/path/to/kcris-mcp-server",
      "env": {
        "KCRIS_SERVICE_KEY": "발급받은_인증키"
      }
    }
  }
}
```

- 설정 후 Claude Desktop을 완전히 종료했다가 다시 실행하세요.

### Claude에게 해볼 수 있는 질문 예시

| 하고 싶은 것 | 예시 질문 |
|--------------|-----------|
| 조건/키워드로 목록 검색 | "당뇨 임상연구 목록 검색해줘", "심장 관련 모집 중인 임상시험 10개만 보여줘" |
| 특정 연구 상세 보기 | "KCT0002243 이 연구 상세 정보 알려줘", "CRIS등록번호 KCT0001234 참여기관이랑 연구책임기관 알려줘" |
| 페이지 조절 | "당뇨 검색해서 2페이지 결과도 보여줘" |

예시 대화:

- **사용자**: 당뇨 임상연구 목록 10개 검색해줘.
- **Claude**: (K-CRIS 도구로 `kcris_list_studies(srch_word="당뇨", num_of_rows=10, page_no=1)` 호출 후 결과를 정리해서 보여줌)

- **사용자**: KCT0002243 이 연구 상세 정보 알려줘.
- **Claude**: (K-CRIS 도구로 `kcris_get_study(cris_number="KCT0002243")` 호출 후 연구제목, 모집현황, 참여기관, 중재군 등을 요약해서 보여줌)

---

## API 참고

- **서비스 URL**: `http://apis.data.go.kr/1352159/crisinfodataview`
- **목록 조회**: `GET .../list` — `serviceKey`, `resultType=json`, `srchWord`, `numOfRows`(1~50), `pageNo`
- **상세 조회**: `GET .../detail` — `serviceKey`, `resultType=json`, `crisNumber`(CRIS등록번호)

## 라이선스

This project is licensed under the MIT License.
