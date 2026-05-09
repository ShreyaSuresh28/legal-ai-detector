import os
import json
from google import genai
from dotenv import load_dotenv

# ─────────────────────────────
# LOAD ENV
# ─────────────────────────────
load_dotenv()

# ─────────────────────────────
# CONFIGURE GEMINI
# ─────────────────────────────
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not set")

client = genai.Client(api_key=API_KEY)

# IMPORTANT:
# Do NOT use "models/" prefix
MODEL_NAME = "gemini-2.5-flash"


# ─────────────────────────────
# SAFE JSON PARSER
# ─────────────────────────────
def extract_json(text: str):
    """
    Safely extracts JSON from Gemini response
    even if wrapped in markdown.
    """

    if not text:
        return None

    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    try:
        start = text.find("{")
        end = text.rfind("}") + 1

        if start != -1 and end != -1:
            json_text = text[start:end]
            return json.loads(json_text)

    except Exception as e:
        print("JSON PARSE ERROR:", e)
        return None

    return None


# ─────────────────────────────
# CLASSIFY SINGLE CLAUSE PAIR
# ─────────────────────────────
def classify_pair(pair):

    clause_a = pair.get("clause_a", {})
    clause_b = pair.get("clause_b", {})

    # Handle both dict and string safely
    text_a = (
        clause_a.get("text", "")
        if isinstance(clause_a, dict)
        else str(clause_a)
    )

    text_b = (
        clause_b.get("text", "")
        if isinstance(clause_b, dict)
        else str(clause_b)
    )

    # Empty text handling
    if not text_a.strip() or not text_b.strip():
        return {
            "type": "yellow",
            "explanation": "Clause text missing or extraction failed.",
            "recommendation": "Check PDF extraction or clause segmentation."
        }

    # ─────────────────────────
    # GEMINI PROMPT
    # ─────────────────────────
    prompt = f"""
You are a legal inconsistency detector.

Analyze the two clauses carefully.

Classification Rules:
- RED → direct contradiction/conflict
- YELLOW → ambiguity, incomplete clause, partial mismatch
- GREEN → legally consistent and aligned

Return ONLY valid JSON.

Example:
{{
  "type": "YELLOW",
  "explanation": "The clauses are partially aligned but missing important details.",
  "recommendation": "Manual legal review recommended."
}}

Clause A:
{text_a}

Clause B:
{text_b}
"""

    try:

        # ─────────────────────
        # GEMINI API CALL
        # ─────────────────────
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        # Safe response extraction
        raw_text = (
            response.text
            if hasattr(response, "text")
            else str(response)
        )

        # ─────────────────────
        # DEBUG OUTPUT
        # ─────────────────────
        print("\n========== RAW GEMINI RESPONSE ==========")
        print(raw_text)
        print("=========================================\n")

        # ─────────────────────
        # TRY JSON PARSING
        # ─────────────────────
        data = extract_json(raw_text)

        if data and "type" in data:

            return {
                "type": str(data.get("type", "yellow")).strip().lower(),
                "explanation": str(data.get("explanation", "")),
                "recommendation": str(
                    data.get(
                        "recommendation",
                        "Manual review recommended."
                    )
                )
            }

        # ─────────────────────
        # FALLBACK CLASSIFIER
        # ─────────────────────
        raw = raw_text.lower()

        red_words = [
            "contradiction",
            "conflict",
            "inconsistent",
            "mismatch",
            "opposite"
        ]

        yellow_words = [
            "ambiguous",
            "unclear",
            "partial",
            "moderate",
            "missing",
            "incomplete",
            "needs clarification"
        ]

        green_words = [
            "consistent",
            "aligned",
            "compatible",
            "match",
            "no issue"
        ]

        if any(word in raw for word in red_words):
            t = "red"

        elif any(word in raw for word in yellow_words):
            t = "yellow"

        elif any(word in raw for word in green_words):
            t = "green"

        else:
            t = "yellow"

        return {
            "type": t,
            "explanation": raw_text[:500],
            "recommendation": "Manual legal review recommended."
        }

    except Exception as e:

        print("\n❌ GEMINI ERROR:")
        print(str(e))
        print()

        return {
            "type": "yellow",
            "explanation": f"LLM error: {str(e)}",
            "recommendation": "Check Gemini API configuration or quota."
        }


# ─────────────────────────────
# PHASE 3 MAIN FUNCTION
# ─────────────────────────────
def run_phase3(pairs):

    red_flags = []
    yellow_flags = []
    green_flags = []

    for pair in pairs:

        result = classify_pair(pair)

        flag = {
            "clause_a": pair.get("clause_a"),
            "clause_b": pair.get("clause_b"),
            "similarity_score": pair.get(
                "similarity_score",
                0
            ),
            "issue_type": result["type"].upper(),
            "explanation": result["explanation"],
            "recommendation": result["recommendation"]
        }

        if result["type"] == "red":
            red_flags.append(flag)

        elif result["type"] == "yellow":
            yellow_flags.append(flag)

        else:
            green_flags.append(flag)

    # ─────────────────────────
    # FINAL RESPONSE
    # ─────────────────────────
    return {
        "red_flags": red_flags,
        "yellow_flags": yellow_flags,
        "green_flags": green_flags,
        "summary": (
            f"{len(red_flags)} contradictions, "
            f"{len(yellow_flags)} ambiguities, "
            f"{len(green_flags)} consistent pairs."
        )
    }