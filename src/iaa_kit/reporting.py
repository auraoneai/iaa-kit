def report(scores: dict) -> str:
    lines = ["# Inter-Annotator Agreement Report", "", "Synthetic examples only; no paid or customer data is included.", ""]
    for key, value in scores.items(): lines.append(f"- {key}: {value}")
    return "\n".join(lines) + "\n"
