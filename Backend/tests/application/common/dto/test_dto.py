# tests/application/common/dto/test_dto.py

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.application.common.dto import (
    BaseDTO,
    PagedResult,
    RequestDTO,
    ResponseDTO,
)


class SampleRequest(RequestDTO):
    """
    Test request DTO.
    """

    name: str


class SampleResponse(ResponseDTO):
    """
    Test response DTO.
    """

    name: str


class SampleDTO(BaseDTO):
    """
    Test base DTO.
    """

    name: str


def test_base_dto_accepts_valid_data() -> None:
    dto = SampleDTO(
        name="Pamacore",
    )

    assert dto.name == "Pamacore"


def test_base_dto_strips_whitespace() -> None:
    dto = SampleDTO(
        name="  Pamacore  ",
    )

    assert dto.name == "Pamacore"


def test_base_dto_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        SampleDTO(
            name="Pamacore",
            unknown="value",
        )


def test_request_dto_is_mutable() -> None:
    dto = SampleRequest(
        name="Initial",
    )

    dto.name = "Updated"

    assert dto.name == "Updated"


def test_response_dto_is_immutable() -> None:
    dto = SampleResponse(
        name="Initial",
    )

    with pytest.raises(ValidationError):
        dto.name = "Updated"


def test_paged_result_calculates_total_pages() -> None:
    result = PagedResult[int](
        items=[1, 2, 3],
        page_number=1,
        page_size=10,
        total_items=25,
    )

    assert result.total_pages == 3


def test_paged_result_empty_result() -> None:
    result = PagedResult[int](
        items=[],
        page_number=1,
        page_size=10,
        total_items=0,
    )

    assert result.total_pages == 0


def test_paged_result_rejects_invalid_page_data() -> None:
    with pytest.raises(ValidationError):
        PagedResult[int](
            items=[],
            page_number="first",
            page_size=10,
            total_items=0,
        )
