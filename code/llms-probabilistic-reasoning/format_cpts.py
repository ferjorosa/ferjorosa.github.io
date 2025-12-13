"""Formatting utilities for CPTs."""

from __future__ import annotations

from collections.abc import Sequence

from pgmpy.factors.discrete import TabularCPD

def format_discrete_cpds(cpts: list[TabularCPD]) -> str:
    """Format a list of TabularCPD objects into a single string."""
    cpd_strings = []
    for cpd in cpts:
        cpd_strings.append(cpd_to_ascii_table(cpd))
    return "\n\n".join(cpd_strings)

def _format_table(rows: list[list[str]]) -> str:
    widths: list[int] = []
    for row in rows:
        for i, cell in enumerate(row):
            if i >= len(widths):
                widths.append(len(cell))
            else:
                widths[i] = max(widths[i], len(cell))

    def horiz() -> str:
        parts = ["+" + "-" * (w + 2) for w in widths]
        return "".join(parts) + "+"

    def fmt_row(row: list[str]) -> str:
        cells = [f" {cell.ljust(w)} " for cell, w in zip(row, widths, strict=False)]
        return "|" + "|".join(cells) + "|"

    out: list[str] = []
    out.append(horiz())
    for r in rows:
        out.append(fmt_row(r))
        out.append(horiz())
    return "\n".join(out)


def _parent_assignments(
    parents: Sequence[str],
    state_names: dict[str, Sequence[str]],
) -> list[tuple[str, ...]]:
    from itertools import product

    domains = [state_names[p] for p in parents]
    return list(product(*domains)) if parents else []


def cpd_to_ascii_table(cpd: TabularCPD) -> str:
    """
    Convert a TabularCPD to an ASCII table representation.

    Args:
        cpd: The conditional probability distribution to format.

    Returns:
        A formatted ASCII table string representing the CPD.
    """
    var = cpd.variable
    var_states = list(cpd.state_names[cpd.variable])
    parents = (
        list(cpd.variables[1:])
        if hasattr(cpd, "variables")
        else list(cpd.evidence or [])
    )

    rows: list[list[str]] = []

    if not parents:
        rows.append(["Node(Value)", "Probability"])  # header
        for s_idx, s in enumerate(var_states):
            prob = float(cpd.values[s_idx])
            rows.append([f"{var}({s})", f"{prob:.4f}"])
        return _format_table(rows)

    parent_assigns = _parent_assignments(parents, cpd.state_names)

    # Header rows listing parent assignments as columns
    for p in parents:
        header = [p]
        for assign in parent_assigns:
            val = assign[parents.index(p)]
            header.append(f"{p}({val})")
        rows.append(header)

    # Build index maps for parent state -> integer index
    parent_state_to_idx = {
        p: {name: idx for idx, name in enumerate(cpd.state_names[p])} for p in parents
    }

    # Now child rows: fetch probability using multi-index over parent axes
    for s_idx, s in enumerate(var_states):
        row = [f"{var}({s})"]
        for assign in parent_assigns:
            # Convert state labels in assign to index tuple aligned with parents order
            idx_tuple = tuple(
                parent_state_to_idx[p][assign[parents.index(p)]] for p in parents
            )
            # Access value with full index over all axes:
            # (var_state, parent1, parent2, ...)
            prob = float(cpd.values[(s_idx,) + idx_tuple])
            row.append(f"{prob:.4f}")
        rows.append(row)

    return _format_table(rows)