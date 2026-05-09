import re

def segment_clauses(text: str):
    # 🔴 safety check
    if not text or not isinstance(text, str):
        return []

    # 🔹 normalize text
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    # 🔹 better clause splitting (handles legal docs)
    parts = re.split(r'\.(?=\s+[A-Z])', text)

    clauses = []

    for i, part in enumerate(parts):
        if not part:
            continue

        part = str(part).strip()

        if len(part) < 20:  # remove junk like "Ltd", "Clause 2"
            continue

        clauses.append({
            "title": f"Clause {i+1}",
            "text": part
        })

    return clauses