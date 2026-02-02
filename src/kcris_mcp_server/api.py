"""K-CRIS(질병관리청 임상연구정보) OpenAPI 클라이언트.

API 가이드: KCDC18-CRIS-API01 v1.3 (2024-02-14)
서비스 URL: http://apis.data.go.kr/1352159/crisinfodataview
"""

from __future__ import annotations

import os
from typing import Any

import httpx

BASE_URL = "http://apis.data.go.kr/1352159/crisinfodataview"
DEFAULT_TIMEOUT = 30.0

# 공공데이터포털 에러 코드 (가이드 2. OpenAPI 에러 코드정리)
ERROR_CODES = {
    "00": "NORMAL_SERVICE",
    "01": "APPLICATION_ERROR",
    "03": "NODATA_ERROR",
    "10": "INVALID_REQUEST_PARAMETER_ERROR",
    "12": "NO_OPENAPI_SERVICE_ERROR",
    "20": "SERVICE_ACCESS_DENIED_ERROR",
    "22": "LIMITED_NUMBER_OF_SERVICE_REQUESTS_EXCEEDS_ERROR",
    "30": "SERVICE_KEY_IS_NOT_REGISTERED_ERROR",
    "31": "DEADLINE_HAS_EXPIRED_ERROR",
    "32": "UNREGISTERED_IP_ERROR",
    "99": "UNKNOWN_ERROR",
}


class KcrisApiError(Exception):
    """K-CRIS API 오류."""

    def __init__(self, code: str, message: str, detail: str | None = None) -> None:
        self.code = code
        self.message = message
        self.detail = detail or ERROR_CODES.get(code, "UNKNOWN")
        super().__init__(f"[{self.code}] {self.message} ({self.detail})")


def _get_service_key() -> str:
    key = os.environ.get("KCRIS_SERVICE_KEY") or os.environ.get("DATA_GO_KR_SERVICE_KEY")
    if not key or not key.strip():
        raise KcrisApiError(
            "30",
            "인증키가 설정되지 않았습니다. KCRIS_SERVICE_KEY 또는 DATA_GO_KR_SERVICE_KEY 환경변수를 설정하세요.",
            "공공데이터포털(data.go.kr)에서 인증키를 발급받아 설정하세요.",
        )
    return key.strip()


def list_studies(
    srch_word: str | None = None,
    num_of_rows: int = 10,
    page_no: int = 1,
    service_key: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """임상연구정보 목록 조회.

    Args:
        srch_word: 검색어 (조건/연구제목 등).
        num_of_rows: 페이지당 출력 개수 (1~50, 기본 10).
        page_no: 출력될 페이지 번호 (기본 1).
        service_key: 인증키. 미지정 시 환경변수 사용.
        timeout: 요청 타임아웃(초).

    Returns:
        resultCode, resultMsg, totalCount, pageNo, numOfRows, items 리스트.
    """
    key = service_key or _get_service_key()
    num_of_rows = max(1, min(50, num_of_rows))
    page_no = max(1, page_no)

    params: dict[str, str | int] = {
        "serviceKey": key,
        "resultType": "json",
        "numOfRows": num_of_rows,
        "pageNo": page_no,
    }
    if srch_word and srch_word.strip():
        params["srchWord"] = srch_word.strip()

    with httpx.Client(timeout=timeout) as client:
        resp = client.get(f"{BASE_URL}/list", params=params)
        resp.raise_for_status()
        data = resp.json()

    result_code = data.get("resultCode", "")
    if result_code != "00":
        raise KcrisApiError(
            result_code,
            data.get("resultMsg", "Unknown error"),
            ERROR_CODES.get(result_code),
        )

    # 응답이 items 없이 빈 목록일 수 있음
    items = data.get("items") or []
    if isinstance(items, dict):
        items = [items]

    return {
        "resultCode": data.get("resultCode", "00"),
        "resultMsg": data.get("resultMsg", "NORMAL_SERVICE"),
        "totalCount": int(data.get("totalCount", 0)),
        "pageNo": int(data.get("pageNo", page_no)),
        "numOfRows": int(data.get("numOfRows", num_of_rows)),
        "items": items,
    }


def get_study_detail(
    cris_number: str,
    service_key: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """임상연구정보 상세 조회.

    Args:
        cris_number: CRIS등록번호 (예: KCT0002243).
        service_key: 인증키. 미지정 시 환경변수 사용.
        timeout: 요청 타임아웃(초).

    Returns:
        임상연구 상세 정보 (참여기관, 연구비지원기관, 연구책임기관, 중재군, 주요결과변수 등).
    """
    key = service_key or _get_service_key()
    cris_number = cris_number.strip()
    if not cris_number:
        raise ValueError("CRIS등록번호(cris_number)는 필수입니다.")

    params: dict[str, str] = {
        "serviceKey": key,
        "resultType": "json",
        "crisNumber": cris_number,
    }

    with httpx.Client(timeout=timeout) as client:
        resp = client.get(f"{BASE_URL}/detail", params=params)
        resp.raise_for_status()
        data = resp.json()

    result_code = data.get("resultCode", "")
    if result_code != "00":
        raise KcrisApiError(
            result_code,
            data.get("resultMsg", "Unknown error"),
            ERROR_CODES.get(result_code),
        )

    # detail 응답은 item 단일 객체 (가이드 기준)
    return {k: v for k, v in data.items() if k not in ("resultCode", "resultMsg")}
