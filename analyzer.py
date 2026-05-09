from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')


def run_phase2(clauses):
    # ─────────────────────────────
    # 1. Normalize input safely
    # ─────────────────────────────
    texts = []

    for c in clauses:
        if isinstance(c, dict):
            texts.append(c.get("text", ""))
        else:
            texts.append(str(c))

    # ─────────────────────────────
    # 2. Generate embeddings
    # ─────────────────────────────
    embeddings = model.encode(texts)

    # ─────────────────────────────
    # 3. Similarity matrix
    # ─────────────────────────────
    sim_matrix = cosine_similarity(embeddings)

    pairs = []

    # ─────────────────────────────
    # 4. Build clause pairs
    # ─────────────────────────────
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            score = float(sim_matrix[i][j])

            pairs.append({
                "clause_a": clauses[i],
                "clause_b": clauses[j],
                "similarity_score": round(score, 3)
            })

    # ─────────────────────────────
    # 5. Sort by similarity
    # ─────────────────────────────
    pairs = sorted(
        pairs,
        key=lambda x: x["similarity_score"],
        reverse=True
    )

    # ─────────────────────────────
    # 6. Filter important pairs
    # ─────────────────────────────
    filtered = [p for p in pairs if p["similarity_score"] > 0.5]

    return {
        "total_pairs_checked": len(pairs),
        "suspicious_pairs": filtered[:10]
    }