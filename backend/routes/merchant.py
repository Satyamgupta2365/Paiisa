"""
Merchant Routes — Cash Flow Predictor + Bank Statement Analyzer (Gemini AI)
Supports: PDF, Excel (.xlsx/.xls), CSV, TXT
Auto-saves every uploaded file + analysis result to local disk + SQLite history
Primary: Google Gemini 2.0 Flash | Fallback: Groq llama-3.3-70b-versatile
"""
import json
import os
import shutil
from pathlib import Path
from datetime import datetime

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from database.db import get_db
from database.models import Transaction, StatementHistory
from models.schemas import CashFlowResponse, StatementAnalysisRequest, StatementAnalysisResponse
from services.cashflow_service import cashflow_service
from services.gemini_service import gemini_service
from services.groq_merchant_analysis import analyze_bank_statement as groq_analyze, _mock_analysis
from services.file_extractor import extract_text_from_file

router = APIRouter(prefix="/api/v1/merchant", tags=["merchant"])

# ── Upload storage directory ───────────────────────────────────────────────────
UPLOADS_DIR = Path(__file__).parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)


# ── Helpers ────────────────────────────────────────────────────────────────────

async def _save_history(
    db: AsyncSession,
    company_name: str,
    result: dict,
    filename: str | None = None,
    saved_path: str | None = None,
    file_format: str | None = None,
):
    """Persist analysis result to the statement_history table."""
    record = StatementHistory(
        company_name=company_name,
        original_filename=filename,
        file_format=file_format,
        saved_file_path=saved_path,
        analysis_json=json.dumps(result),
        health_score=result.get("health_score", 0),
        net_cashflow=result.get("summary", {}).get("net_cashflow", 0.0),
        credit_verdict=result.get("credit_verdict", "UNKNOWN"),
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


def _save_file_to_disk(content: bytes, filename: str, company_name: str) -> str:
    """Save the uploaded file to uploads/ and return relative path."""
    safe_company = "".join(c if c.isalnum() or c in "_ -" else "_" for c in company_name)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    ext = Path(filename).suffix.lower()
    save_name = f"{ts}_{safe_company}{ext}"
    save_path = UPLOADS_DIR / save_name
    with open(save_path, "wb") as f:
        f.write(content)
    return save_name  # relative name for DB


# ── Pillar 3: Cash Flow Predictor ──────────────────────────────────────────────

@router.get("/cashflow/{user_id}", response_model=CashFlowResponse)
async def get_cashflow(user_id: UUID, db: AsyncSession = Depends(get_db)):
    if str(user_id) == "23050620-0500-0000-0000-000000000000":
        return cashflow_service._satyam_response()
        
    result = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == user_id)
        .order_by(Transaction.created_at.desc())
        .limit(90)
    )
    transactions = result.scalars().all()
    return cashflow_service.predict(transactions)


@router.get("/cashflow/demo/mock", response_model=CashFlowResponse)
async def get_cashflow_mock():
    return cashflow_service._mock_response()


# ── Bank Statement Analyzer: Text Paste ───────────────────────────────────────

async def _analyze_with_gemini_or_groq(statement_text: str, company_name: str) -> dict:
    """Try Gemini first, fall back to Groq, then to mock data."""
    # Primary: Gemini 2.0 Flash
    if gemini_service.is_available:
        result = await gemini_service.analyze_bank_statement(statement_text, company_name)
        if result and "summary" in result:
            return result
    # Fallback: Groq llama-3.3-70b
    result = groq_analyze(statement_text=statement_text, company_name=company_name)
    return result


@router.post("/analyze-statement", response_model=StatementAnalysisResponse)
async def analyze_statement(req: StatementAnalysisRequest, db: AsyncSession = Depends(get_db)):
    """
    Paste raw bank statement text → Gemini AI full analysis.
    Falls back to Groq llama-3.3-70b if Gemini is unavailable.
    Result is automatically saved to history.
    """
    result = await _analyze_with_gemini_or_groq(
        statement_text=req.statement_text,
        company_name=req.company_name,
    )
    await _save_history(db, req.company_name, result, file_format="text")
    return StatementAnalysisResponse(**result)


# ── Bank Statement Analyzer: File Upload (PDF / Excel / CSV / TXT) ─────────────

@router.post("/analyze-statement/upload", response_model=StatementAnalysisResponse)
async def analyze_statement_file(
    file: UploadFile = File(...),
    company_name: str = Form("My Business"),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload bank statement in ANY format: PDF, Excel (.xlsx/.xls), CSV, TXT.
    File is saved permanently to disk. Analysis is saved to history.
    Primary: Gemini 2.0 Flash | Fallback: Groq llama-3.3-70b-versatile
    """
    content = await file.read()
    filename = file.filename or "statement.txt"
    ext = Path(filename).suffix.lower().lstrip(".")

    # 1. Extract text from file (handles PDF / Excel / CSV / TXT)
    statement_text = extract_text_from_file(content, filename)

    # 2. Save original file to disk
    saved_path = _save_file_to_disk(content, filename, company_name)

    # 3. Run Gemini AI analysis (falls back to Groq)
    result = await _analyze_with_gemini_or_groq(statement_text=statement_text, company_name=company_name)

    # 4. Save to DB history
    await _save_history(db, company_name, result, filename=filename, saved_path=saved_path, file_format=ext)

    return StatementAnalysisResponse(**result)


# ── Demo Endpoint ──────────────────────────────────────────────────────────────

@router.post("/analyze-statement/demo", response_model=StatementAnalysisResponse)
async def analyze_statement_demo(
    company_name: str = "My Business",
    db: AsyncSession = Depends(get_db),
):
    """Demo — instant rich mock analysis for any user-entered company name."""
    result = _mock_analysis(company_name)
    await _save_history(db, company_name, result, file_format="demo")
    return StatementAnalysisResponse(**result)


# ── History: List All Saved Analyses ──────────────────────────────────────────

@router.get("/statement-history")
async def get_statement_history(db: AsyncSession = Depends(get_db)):
    """
    Returns all past bank statement analyses, newest first.
    Each record shows company name, file, health score, verdict, and date.
    """
    result = await db.execute(
        select(StatementHistory).order_by(StatementHistory.created_at.desc()).limit(50)
    )
    rows = result.scalars().all()
    return [
        {
            "id": str(r.id),
            "company_name": r.company_name,
            "original_filename": r.original_filename,
            "file_format": r.file_format,
            "health_score": r.health_score,
            "net_cashflow": r.net_cashflow,
            "credit_verdict": r.credit_verdict,
            "created_at": r.created_at.isoformat(),
        }
        for r in rows
    ]


# ── History: Get Full Analysis by ID ──────────────────────────────────────────

@router.get("/statement-history/{record_id}", response_model=StatementAnalysisResponse)
async def get_statement_by_id(record_id: UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve the full AI analysis JSON for a specific history record."""
    result = await db.execute(
        select(StatementHistory).where(StatementHistory.id == record_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Analysis record not found")
    data = json.loads(record.analysis_json)
    return StatementAnalysisResponse(**data)
