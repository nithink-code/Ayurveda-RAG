import logging
import datetime
import os

from fastapi import FastAPI
from dotenv import load_dotenv
import inngest
import inngest.fast_api
from inngest.experimental import ai

import data_loader
from vector_db import AyurvedicStorage
import ayurvedic_rag

load_dotenv(override=True)

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "ok", "service": "AyurvedaRAG API — Personalized Treatment Intelligence"}


# ──────────────────────────────────────────────
#  Inngest Client
# ──────────────────────────────────────────────
inngest_client = inngest.Inngest(
    app_id="study-rag",
    logger=logging.getLogger("uvicorn"),
    is_production=not bool(os.getenv("INNGEST_DEV")),
    signing_key=os.getenv("INNGEST_SIGNING_KEY"),
    event_key=os.getenv("INNGEST_EVENT_KEY"),
)


# ══════════════════════════════════════════════
#  Ayurvedic Knowledge Base Seeder
# ══════════════════════════════════════════════
@inngest_client.create_function(
    fn_id="Ayurveda: Seed Knowledge Base",
    trigger=inngest.TriggerEvent(event="ayurveda/seed-kb"),
)
async def ayurveda_seed_kb(ctx: inngest.Context):
    """Seed/re-seed all Ayurvedic knowledge collections in Qdrant."""
    force = ctx.event.data.get("force", False)

    def _seed() -> dict:
        return ayurvedic_rag.seed_knowledge_base(force=force)

    stats = await ctx.step.run("seed-collections", _seed)
    return {"status": "done", "collections": stats}


# ══════════════════════════════════════════════
#  Generate Ayurvedic Treatment Plan
# ══════════════════════════════════════════════
@inngest_client.create_function(
    fn_id="Ayurveda: Generate Treatment Plan",
    trigger=inngest.TriggerEvent(event="ayurveda/generate-plan"),
)
async def ayurveda_generate_plan(ctx: inngest.Context):
    """
    Retrieve condition-specific knowledge and generate a structured treatment plan.
    Event data: { condition: str, user_id: str }
    """
    condition = ctx.event.data.get("condition", "")
    user_id = ctx.event.data.get("user_id", "anonymous")

    if not condition:
        return {"error": "condition is required"}

    def _retrieve() -> dict:
        return ayurvedic_rag.retrieve_for_condition(condition)

    def _generate(retrieved: dict) -> str:
        return ayurvedic_rag.generate_treatment_plan(condition, retrieved)

    retrieved = await ctx.step.run("retrieve-knowledge", _retrieve)
    plan = await ctx.step.run("generate-plan", lambda: _generate(retrieved))

    # Removed 7-day follow-up reminder automatic scheduling

    return {
        "condition": condition,
        "user_id": user_id,
        "plan": plan,
        "retrieved_sections": list(retrieved.keys()),
    }


# ══════════════════════════════════════════════
#  Log Weekly Progress
# ══════════════════════════════════════════════
@inngest_client.create_function(
    fn_id="Ayurveda: Log Progress",
    trigger=inngest.TriggerEvent(event="ayurveda/log-progress"),
)
async def ayurveda_log_progress(ctx: inngest.Context):
    """
    Store a week's progress log and generate a progress report.
    Event data: { user_id, condition, week, energy_level, symptoms_improvement,
                  digestion, sleep_quality, notes }
    """
    data = ctx.event.data
    user_id = data.get("user_id", "anonymous")
    condition = data.get("condition", "")
    week = data.get("week", 1)

    progress_data = {
        "energy_level": data.get("energy_level", ""),
        "symptoms_improvement": data.get("symptoms_improvement", ""),
        "digestion": data.get("digestion", ""),
        "sleep_quality": data.get("sleep_quality", ""),
        "notes": data.get("notes", ""),
    }

    def _log_and_report() -> dict:
        store = AyurvedicStorage()
        embed_text = f"Progress week {week}: {str(progress_data)}"
        vecs = data_loader.embed_texts([embed_text])
        vec = vecs[0] if vecs else [0.0] * 1536

        log_id = store.log_progress(
            user_id=user_id,
            condition=condition,
            week=week,
            progress_data=progress_data,
            vector=vec,
        )

        all_logs = store.get_user_progress(user_id, condition)
        report = ayurvedic_rag.generate_progress_report(user_id, condition, all_logs)

        return {
            "log_id": log_id,
            "week": week,
            "report": report,
            "total_weeks_logged": len(all_logs),
        }

    result = await ctx.step.run("log-and-report", _log_and_report)
    return result


# ══════════════════════════════════════════════
#  Register Ayurvedic functions
# ══════════════════════════════════════════════
inngest.fast_api.serve(
    app,
    inngest_client,
    [
        ayurveda_seed_kb,
        ayurveda_generate_plan,
        ayurveda_log_progress,
    ],
)
