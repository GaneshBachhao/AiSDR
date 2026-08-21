"""Tests for touch_content_prompt_builder (EPIC-09.2).

Fully synthetic -- no AI/network calls anywhere in this file.
"""

from __future__ import annotations

from app.application.sequence.services.touch_content_prompt_builder import (
    LeadEvidenceContext,
    build_touch_prompt,
    derive_touch_angle,
)
from app.domain.sequence.enums.touch_channel import TouchChannel


def test_derive_touch_angle_opener_proof_point_breakup_for_a_three_touch_sequence() -> None:
    assert derive_touch_angle(0, 3) == "signal-led opener"
    assert derive_touch_angle(1, 3) == "proof point #1"
    assert derive_touch_angle(2, 3) == "breakup message"


def test_derive_touch_angle_single_touch_collapses_to_opener() -> None:
    assert derive_touch_angle(0, 1) == "signal-led opener"


def test_derive_touch_angle_two_touch_is_opener_then_breakup() -> None:
    assert derive_touch_angle(0, 2) == "signal-led opener"
    assert derive_touch_angle(1, 2) == "breakup message"


def test_derive_touch_angle_four_touch_numbers_each_proof_point_distinctly() -> None:
    assert derive_touch_angle(1, 4) == "proof point #1"
    assert derive_touch_angle(2, 4) == "proof point #2"


class TestLeadEvidenceContext:
    def test_has_meaningful_content_false_when_everything_empty(self) -> None:
        evidence = LeadEvidenceContext()
        assert evidence.has_meaningful_content() is False

    def test_has_meaningful_content_true_for_notes(self) -> None:
        evidence = LeadEvidenceContext(notes="Hiring cloud engineers, expanding fast.")
        assert evidence.has_meaningful_content() is True

    def test_has_meaningful_content_false_for_blank_notes(self) -> None:
        evidence = LeadEvidenceContext(notes="   ")
        assert evidence.has_meaningful_content() is False

    def test_has_meaningful_content_false_when_all_signals_are_false(self) -> None:
        evidence = LeadEvidenceContext(
            evidence_signals={"hiring": False, "growth": False, "technology": False}
        )
        assert evidence.has_meaningful_content() is False

    def test_has_meaningful_content_true_when_a_signal_is_true(self) -> None:
        evidence = LeadEvidenceContext(evidence_signals={"hiring": True, "growth": False})
        assert evidence.has_meaningful_content() is True

    def test_has_meaningful_content_true_for_discovery_or_assessment_or_recommendation_prose(
        self,
    ) -> None:
        assert LeadEvidenceContext(discovery_problem_statement="x").has_meaningful_content() is True
        assert LeadEvidenceContext(discovery_business_impact="x").has_meaningful_content() is True
        assert LeadEvidenceContext(assessment_summary="x").has_meaningful_content() is True
        assert LeadEvidenceContext(recommendation_executive_summary="x").has_meaningful_content() is True

    def test_to_prompt_block_lists_only_populated_fields(self) -> None:
        evidence = LeadEvidenceContext(
            notes="Expanding into new markets.",
            evidence_signals={"hiring": True, "growth": False},
        )
        block = evidence.to_prompt_block()
        assert "Expanding into new markets." in block
        assert "hiring" in block
        assert "growth" not in block  # only confirmed (True) signals are listed

    def test_to_prompt_block_honest_placeholder_when_nothing_captured(self) -> None:
        evidence = LeadEvidenceContext()
        assert evidence.to_prompt_block() == "(no real evidence captured for this Lead yet)"


def test_build_touch_prompt_first_touch_has_no_prior_touches_listed() -> None:
    evidence = LeadEvidenceContext(notes="Real signal here.")

    prompt, angle = build_touch_prompt(0, 3, TouchChannel.EMAIL, evidence, [])

    assert angle == "signal-led opener"
    assert "first touch in the sequence" in prompt
    assert "Real signal here." in prompt


def test_build_touch_prompt_later_touch_lists_prior_touches_to_avoid_repetition() -> None:
    evidence = LeadEvidenceContext(notes="Real signal here.")
    prior = [("signal-led opener", "Hi, noticed you're hiring engineers...")]

    prompt, angle = build_touch_prompt(1, 3, TouchChannel.LINKEDIN, evidence, prior)

    assert angle == "proof point #1"
    assert "Hi, noticed you're hiring engineers..." in prompt
    assert "do not repeat" in prompt.lower()


def test_build_touch_prompt_breakup_touch_gets_the_low_pressure_closing_instruction() -> None:
    evidence = LeadEvidenceContext(notes="Real signal here.")

    prompt, angle = build_touch_prompt(2, 3, TouchChannel.EMAIL, evidence, [])

    assert angle == "breakup message"
    assert "final touch" in prompt.lower()


def test_build_touch_prompt_never_fabricate_instruction_always_present() -> None:
    evidence = LeadEvidenceContext(notes="Real signal here.")

    prompt, _ = build_touch_prompt(0, 1, TouchChannel.CALL_TASK, evidence, [])

    assert "do not invent" in prompt.lower()


def test_build_touch_prompt_channel_guidance_varies_by_channel() -> None:
    evidence = LeadEvidenceContext(notes="Real signal here.")

    email_prompt, _ = build_touch_prompt(0, 1, TouchChannel.EMAIL, evidence, [])
    call_prompt, _ = build_touch_prompt(0, 1, TouchChannel.CALL_TASK, evidence, [])

    assert "email" in email_prompt.lower()
    assert "phone call" in call_prompt.lower()
