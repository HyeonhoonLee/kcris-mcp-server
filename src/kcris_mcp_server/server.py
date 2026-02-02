"""K-CRIS MCP 서버: 도구 등록 및 실행."""

from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from kcris_mcp_server.api import KcrisApiError, get_study_detail, list_studies

mcp = FastMCP(
    "K-CRIS MCP Server",
    json_response=True,
)


@mcp.tool()
def kcris_list_studies(
    srch_word: str | None = None,
    num_of_rows: int = 10,
    page_no: int = 1,
) -> str:
    """K-CRIS(한국 임상연구정보)에서 임상연구 목록을 검색합니다.

    질병관리청 임상연구 DB OpenAPI를 사용하여 검색어, 페이지당 개수, 페이지 번호에 맞는
    CRIS등록번호, 연구제목(국문/영문), 연구종류, 모집현황, 연구비지원기관, 연구책임기관 등을 반환합니다.

    Args:
        srch_word: 검색어 (조건, 연구제목, 키워드 등). 생략 시 전체 목록 조회.
        num_of_rows: 페이지당 출력 개수 (1~50, 기본 10).
        page_no: 출력할 페이지 번호 (기본 1).

    Returns:
        JSON 문자열: resultCode, resultMsg, totalCount, pageNo, numOfRows, items(목록).
    """
    num_of_rows = max(1, min(50, num_of_rows))
    page_no = max(1, page_no)
    try:
        result = list_studies(
            srch_word=srch_word,
            num_of_rows=num_of_rows,
            page_no=page_no,
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    except KcrisApiError as e:
        return json.dumps(
            {
                "error": True,
                "code": e.code,
                "message": e.message,
                "detail": e.detail,
            },
            ensure_ascii=False,
            indent=2,
        )


@mcp.tool()
def kcris_get_study(cris_number: str) -> str:
    """CRIS등록번호로 임상연구 상세 정보를 조회합니다.

    K-CRIS(한국 임상연구정보)에서 CRIS등록번호(예: KCT0002243)에 해당하는
    임상연구 상세, 참여기관, 연구비지원기관, 연구책임기관, 중재군, 주요결과변수 등을 반환합니다.

    Args:
        cris_number: CRIS등록번호 (예: KCT0002243).

    Returns:
        JSON 문자열: 연구제목, 모집현황, 참여기관, 연구비지원기관, 연구책임기관, 중재군, 주요결과변수 등.
    """
    cris_number = (cris_number or "").strip()
    if not cris_number:
        return json.dumps(
            {"error": True, "message": "CRIS등록번호(cris_number)는 필수입니다."},
            ensure_ascii=False,
            indent=2,
        )
    try:
        result: dict[str, Any] = get_study_detail(cris_number=cris_number)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except KcrisApiError as e:
        return json.dumps(
            {
                "error": True,
                "code": e.code,
                "message": e.message,
                "detail": e.detail,
            },
            ensure_ascii=False,
            indent=2,
        )
