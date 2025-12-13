"""Formatting utilities for queries."""

def format_probability_query(
    target: dict[str, str],
    evidence: dict[str, str] | None = None,
) -> str:
    """Generate formatted query string like P(Rain=true | Cloudy=true)."""
    target_str = ", ".join([f"{k}={v}" for k, v in target.items()])
    if evidence:
        evidence_str = ", ".join([f"{k}={v}" for k, v in evidence.items()])
        return f"P({target_str} | {evidence_str})"
    return f"P({target_str})"