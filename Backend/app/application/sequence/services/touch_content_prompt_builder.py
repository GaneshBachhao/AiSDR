"""
Touch content prompt builder (EPIC-09.2).

Pure and deterministic -- no AI/network calls, fully unit-testable without
a live Gemini/OpenAI call. Builds the prompt GenerateSequenceContentHandler
sends to AIExecutionService, and derives which "angle" a touch should take
purely from its position: signal-led opener (first) -> proof point(s)
(middle) -> breakup message (last). A single-touch Sequence collapses to
just an opener -- there's nothing to break up from.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.sequence.enums.touch_channel import TouchChannel

_CHANNEL_GUIDANCE = {
    TouchChannel.EMAIL: "a short outbound email (no subject line, just the body)",
    TouchChannel.LINKEDIN: "a short LinkedIn connection note or direct message",
    TouchChannel.CALL_TASK: "brief talking points for a phone call, not a word-for-word script",
}


@dataclass(frozen=True, slots=True)
class LeadEvidenceContext:
    """Whatever real evidence exists for a Lead, gathered once per
    generation run and reused for every touch's prompt.

    Ordered by how commonly each source is actually populated: ``notes``
    and ``evidence_signals`` come from the AI-research promotion path and
    are the most likely to exist; the Discovery/Assessment/Recommendation
    chain is pure manual CRUD with nothing auto-populating it from a Lead,
    so it's realistically empty for a fresh Lead -- included opportunistically
    when it does exist, at zero extra AI cost.
    """

    notes: str | None = None
    evidence_signals: dict[str, bool] | None = None
    discovery_problem_statement: str | None = None
    discovery_business_impact: str | None = None
    assessment_summary: str | None = None
    recommendation_executive_summary: str | None = None

    def has_meaningful_content(self) -> bool:
        """Whether there's anything real to ground generated copy in.

        Mirrors CreateRecommendationHandler._has_meaningful_content()'s
        discipline: refuse to generate from nothing rather than let the
        model invent a company profile out of thin air.
        """
        if self.notes and self.notes.strip():
            return True
        if self.evidence_signals and any(self.evidence_signals.values()):
            return True
        return any(
            [
                self.discovery_problem_statement,
                self.discovery_business_impact,
                self.assessment_summary,
                self.recommendation_executive_summary,
            ]
        )

    def to_prompt_block(self) -> str:
        lines: list[str] = []
        if self.notes and self.notes.strip():
            lines.append(f"- Lead notes: {self.notes.strip()}")
        if self.evidence_signals:
            confirmed = [key for key, value in self.evidence_signals.items() if value]
            if confirmed:
                lines.append(f"- Confirmed signal categories: {', '.join(confirmed)}")
        if self.discovery_problem_statement:
            lines.append(f"- Discovery, problem statement: {self.discovery_problem_statement}")
        if self.discovery_business_impact:
            lines.append(f"- Discovery, business impact: {self.discovery_business_impact}")
        if self.assessment_summary:
            lines.append(f"- Assessment summary: {self.assessment_summary}")
        if self.recommendation_executive_summary:
            lines.append(f"- Recommendation summary: {self.recommendation_executive_summary}")
        return "\n".join(lines) if lines else "(no real evidence captured for this Lead yet)"


def derive_touch_angle(index: int, total: int) -> str:
    """The angle this touch's position should take.

    index 0 -> opener (wins even in a single-touch sequence, since a
    breakup message only makes sense after an opener already happened).
    Last index (when total > 1) -> breakup. Everything between -> a
    numbered proof point, distinct from any prior touch.
    """
    if index == 0:
        return "signal-led opener"
    if index == total - 1:
        return "breakup message"
    return f"proof point #{index}"


def build_touch_prompt(
    index: int,
    total: int,
    channel: TouchChannel,
    evidence: LeadEvidenceContext,
    prior_touches: list[tuple[str, str]],
) -> tuple[str, str]:
    """Build the prompt for one touch. Returns (prompt, angle_label).

    ``prior_touches`` is (angle_label, content) for every touch already
    drafted earlier in this same generation run, listed so the model can
    mechanically avoid repeating an angle or opening line rather than
    just being asked nicely not to.
    """
    angle = derive_touch_angle(index, total)

    if prior_touches:
        prior_block = "\n".join(
            f'- Touch {position + 1} ({prior_angle}): "{content}"'
            for position, (prior_angle, content) in enumerate(prior_touches)
        )
    else:
        prior_block = "(this is the first touch in the sequence)"

    closing_instruction = (
        "This is the final touch -- keep it low-pressure, acknowledge you haven't "
        "heard back, and give them an easy, no-pressure way to say not interested."
        if angle == "breakup message"
        else "End with a soft, low-pressure call to action, not a hard sell."
    )

    prompt = f"""You are drafting touch {index + 1} of {total} in an outbound sales sequence.
Angle for this touch: {angle}.
Channel: {channel.value} -- write {_CHANNEL_GUIDANCE[channel]}.

Real evidence available about this Lead:
{evidence.to_prompt_block()}

Ground the message in the real evidence above. Do not invent additional
specific facts, numbers, or signals beyond what's listed -- if the
evidence is thin, write a general, honestly-hedged message rather than
guessing specifics.

Touches already drafted earlier in this sequence -- do not repeat their
angle, opening line, or specific wording:
{prior_block}

Rules:
- 2-4 short sentences.
- Sound like a real person wrote it, not a template.
- {closing_instruction}

Respond with ONLY the message text -- no subject line, no markdown, no
explanation, no quotation marks around it."""

    return prompt, angle
