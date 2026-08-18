# tests/application/common/mappers/test_mapper.py

from __future__ import annotations

from dataclasses import dataclass

from app.application.common.mappers import (
    Mapper,
)


@dataclass
class SampleEntity:
    """
    Test domain object.
    """

    value: str


@dataclass
class SampleDTO:
    """
    Test application DTO.
    """

    value: str


class SampleMapper(
    Mapper[SampleEntity, SampleDTO],
):
    """
    Test mapper implementation.
    """

    def to_dto(
        self,
        source: SampleEntity,
    ) -> SampleDTO:
        return SampleDTO(
            value=source.value,
        )

    def to_entity(
        self,
        target: SampleDTO,
    ) -> SampleEntity:
        return SampleEntity(
            value=target.value,
        )


def test_mapper_converts_entity_to_dto() -> None:
    mapper = SampleMapper()

    entity = SampleEntity(
        value="Pamacore",
    )

    dto = mapper.to_dto(
        entity,
    )

    assert dto.value == "Pamacore"


def test_mapper_converts_dto_to_entity() -> None:
    mapper = SampleMapper()

    dto = SampleDTO(
        value="AI Consulting",
    )

    entity = mapper.to_entity(
        dto,
    )

    assert entity.value == "AI Consulting"
