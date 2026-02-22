"""
Ayurvedic RAG Engine
Optimized for speed using parallel retrieval.
"""

import os
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from openai import OpenAI
import data_loader
from vector_db import AyurvedicStorage
from ayurvedic_kb import (
    ALL_KNOWLEDGE, SUPPORTED_CONDITIONS
)

load_dotenv(override=True)

# ──────────────────────────────────────────────
#  OpenRouter / OpenAI client
# ──────────────────────────────────────────────
_or_key = os.getenv("OPENROUTER_API_KEY")
if _or_key:
    _llm = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=_or_key)
    _model = "openai/gpt-4o-mini"
else:
    _llm = OpenAI()
    _model = "gpt-4o-mini"


# ──────────────────────────────────────────────
#  Knowledge Base Seeding
# ──────────────────────────────────────────────
def seed_knowledge_base(force: bool = False) -> dict:
    store = AyurvedicStorage()
    collection_map = {
        "conditions": "conditions",
        "herbs": "herbs",
        "diet_guidelines": "diet_guidelines",
        "yoga_practices": "yoga_practices",
        "precautions": "precautions",
        "lifestyle": "lifestyle",
    }

    stats = {}
    for kb_key, coll_name in collection_map.items():
        entries = ALL_KNOWLEDGE[kb_key]
        if not force and store.is_seeded(coll_name):
            stats[coll_name] = f"already seeded ({len(entries)} entries)"
            continue

        texts = [e["text"] for e in entries]
        vectors = data_loader.embed_texts(texts)
        if not vectors:
            continue

        store.upsert_knowledge(coll_name, entries, vectors)
        stats[coll_name] = f"seeded {len(entries)}"

    return stats


# ──────────────────────────────────────────────
#  Parallel Condition-based retrieval
# ──────────────────────────────────────────────
def retrieve_for_condition(condition: str) -> dict:
    """
    Retrieves knowledge from multiple collections in parallel for speed.
    """
    store = AyurvedicStorage()
    query_text = f"Ayurvedic treatment for {condition}"
    query_vec = data_loader.embed_texts([query_text])
    if not query_vec:
        return {}
    qv = query_vec[0]

    collections_to_query = [
        ("conditions", 1, "overview"),
        ("herbs", 4, "herbs"),
        ("diet_guidelines", 1, "diet"),
        ("yoga_practices", 1, "yoga"),
        ("precautions", 1, "precautions"),
        ("lifestyle", 1, "lifestyle"),
    ]

    def _query_task(config):
        coll, top_k, key = config
        try:
            res = store.search_by_condition(coll, qv, condition, top_k=top_k)
            return key, res
        except Exception:
            return key, []

    # Execute all Qdrant queries in parallel threads
    results = {}
    with ThreadPoolExecutor(max_workers=6) as executor:
        for key, data in executor.map(_query_task, collections_to_query):
            results[key] = data
            
    return results


# ──────────────────────────────────────────────
#  Structured plan generation
# ──────────────────────────────────────────────
PLAN_SYSTEM_PROMPT = """You are a highly experienced Ayurvedic physician.
Generate concise, structured, professional treatment plans."""

PLAN_USER_TEMPLATE = """
CONDITION: {condition}
DOSHA: {dosha}

== KNOWLEDGE ==
OVERVIEW: {overview}
HERBS: {herbs}
DIET: {diet}
YOGA: {yoga}
LIFESTYLE: {lifestyle}
PRECAUTIONS: {precautions}

Generate a treatment plan using these sections:
1. **Overview**
2. **Dosha Involvement**
3. **Herbal Remedies** (Include disclaimer)
4. **Diet Plan**
5. **Yoga & Pranayama**
6. **Lifestyle Advice**
7. **Precautions**
8. **When to Consult a Doctor**
"""

def generate_treatment_plan(condition: str, retrieved: dict) -> str:
    def _join(items: list[dict]) -> str:
        texts = [item.get("text", "") for item in items if item.get("text")]
        return "\n".join(texts) if texts else "None"

    dosha = SUPPORTED_CONDITIONS.get(condition, ["Unknown"])[0]

    prompt = PLAN_USER_TEMPLATE.format(
        condition=condition,
        dosha=dosha,
        overview=_join(retrieved.get("overview", [])),
        herbs=_join(retrieved.get("herbs", [])),
        diet=_join(retrieved.get("diet", [])),
        yoga=_join(retrieved.get("yoga", [])),
        lifestyle=_join(retrieved.get("lifestyle", [])),
        precautions=_join(retrieved.get("precautions", [])),
    )

    response = _llm.chat.completions.create(
        model=_model,
        max_tokens=2000,
        temperature=0.2, # Lower temperature for faster/more consistent results
        messages=[
            {"role": "system", "content": PLAN_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()


# ──────────────────────────────────────────────
#  Progress report generation
# ──────────────────────────────────────────────
def generate_progress_report(user_id: str, condition: str, logs: list[dict]) -> str:
    if not logs:
        return "No data."

    log_text = ""
    for log in logs:
        week = log.get("week", "?")
        log_text += f"\nWeek {week}: " + ", ".join([f"{k}: {v}" for k, v in log.items() if k not in ("user_id", "condition", "week", "timestamp")])

    response = _llm.chat.completions.create(
        model=_model,
        max_tokens=1000,
        temperature=0.3,
        messages=[
            {"role": "system", "content": "You are an Ayurvedic wellness coach."},
            {"role": "user", "content": f"Analyze logs for {condition} ({user_id}):\n{log_text}\n\nProvide a brief trend analysis and recommendations."},
        ],
    )
    return response.choices[0].message.content.strip()
