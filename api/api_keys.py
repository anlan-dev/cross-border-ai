"""API Key management for user-configurable external API access."""

from __future__ import annotations

import os
import json
import hashlib
import secrets
from datetime import datetime
from typing import Optional
from pathlib import Path

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel

router = APIRouter(prefix="/api/keys", tags=["API Keys"])

# ── Storage ─────────────────────────────────────────────

KEYS_FILE = Path(__file__).parent / "data" / "api_keys.json"

def _ensure_dir():
    KEYS_FILE.parent.mkdir(parents=True, exist_ok=True)

def _load_keys() -> dict:
    _ensure_dir()
    if KEYS_FILE.exists():
        return json.loads(KEYS_FILE.read_text(encoding="utf-8"))
    return {}

def _save_keys(data: dict):
    _ensure_dir()
    KEYS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ── Models ──────────────────────────────────────────────

class APIKeyCreate(BaseModel):
    name: str
    provider: str  # openai, anthropic, google, custom
    api_key: str
    base_url: Optional[str] = None
    model: Optional[str] = None

class APIKeyUpdate(BaseModel):
    name: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None
    is_active: Optional[bool] = None

class APIKeyResponse(BaseModel):
    id: str
    name: str
    provider: str
    masked_key: str
    base_url: Optional[str]
    model: Optional[str]
    is_active: bool
    created_at: str
    last_used: Optional[str]


# ── Helpers ─────────────────────────────────────────────

def _mask_key(key: str) -> str:
    if len(key) <= 8:
        return "****"
    return key[:4] + "****" + key[-4:]

def _generate_id() -> str:
    return secrets.token_hex(8)


# ── Endpoints ───────────────────────────────────────────

@router.get("/list")
async def list_keys():
    """List all configured API keys (masked)."""
    keys = _load_keys()
    result = []
    for kid, kdata in keys.items():
        result.append({
            "id": kid,
            "name": kdata.get("name", ""),
            "provider": kdata.get("provider", ""),
            "masked_key": _mask_key(kdata.get("api_key", "")),
            "base_url": kdata.get("base_url"),
            "model": kdata.get("model"),
            "is_active": kdata.get("is_active", True),
            "created_at": kdata.get("created_at", ""),
            "last_used": kdata.get("last_used"),
        })
    return {"keys": result}


@router.post("/create")
async def create_key(req: APIKeyCreate):
    """Create a new API key configuration."""
    keys = _load_keys()
    kid = _generate_id()
    keys[kid] = {
        "name": req.name,
        "provider": req.provider,
        "api_key": req.api_key,
        "base_url": req.base_url,
        "model": req.model,
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "last_used": None,
    }
    _save_keys(keys)
    return {"id": kid, "masked_key": _mask_key(req.api_key), "status": "created"}


@router.put("/{key_id}")
async def update_key(key_id: str, req: APIKeyUpdate):
    """Update an existing API key configuration."""
    keys = _load_keys()
    if key_id not in keys:
        raise HTTPException(status_code=404, detail="API key not found")
    
    kdata = keys[key_id]
    if req.name is not None:
        kdata["name"] = req.name
    if req.api_key is not None:
        kdata["api_key"] = req.api_key
    if req.base_url is not None:
        kdata["base_url"] = req.base_url
    if req.model is not None:
        kdata["model"] = req.model
    if req.is_active is not None:
        kdata["is_active"] = req.is_active
    
    _save_keys(keys)
    return {"status": "updated"}


@router.delete("/{key_id}")
async def delete_key(key_id: str):
    """Delete an API key configuration."""
    keys = _load_keys()
    if key_id not in keys:
        raise HTTPException(status_code=404, detail="API key not found")
    del keys[key_id]
    _save_keys(keys)
    return {"status": "deleted"}


@router.post("/{key_id}/test")
async def test_key(key_id: str):
    """Test if an API key is valid by making a lightweight call."""
    keys = _load_keys()
    if key_id not in keys:
        raise HTTPException(status_code=404, detail="API key not found")
    
    kdata = keys[key_id]
    provider = kdata.get("provider", "")
    api_key = kdata.get("api_key", "")
    base_url = kdata.get("base_url")
    model = kdata.get("model", "")
    
    try:
        if provider == "openai":
            import httpx
            url = (base_url or "https://api.openai.com/v1") + "/models"
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url, headers={"Authorization": f"Bearer {api_key}"})
                if resp.status_code == 200:
                    # Update last_used
                    kdata["last_used"] = datetime.now().isoformat()
                    _save_keys(keys)
                    return {"status": "valid", "message": "API key is valid"}
                return {"status": "invalid", "message": f"HTTP {resp.status_code}"}
        elif provider == "anthropic":
            import httpx
            url = (base_url or "https://api.anthropic.com/v1") + "/messages"
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(url, 
                    headers={
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={
                        "model": model or "claude-3-haiku-20240307",
                        "max_tokens": 10,
                        "messages": [{"role": "user", "content": "hi"}]
                    }
                )
                if resp.status_code == 200:
                    kdata["last_used"] = datetime.now().isoformat()
                    _save_keys(keys)
                    return {"status": "valid", "message": "API key is valid"}
                return {"status": "invalid", "message": f"HTTP {resp.status_code}: {resp.text[:200]}"}
        elif provider == "google":
            import httpx
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    kdata["last_used"] = datetime.now().isoformat()
                    _save_keys(keys)
                    return {"status": "valid", "message": "API key is valid"}
                return {"status": "invalid", "message": f"HTTP {resp.status_code}"}
        else:
            # Custom provider - just check if key is non-empty
            if api_key and len(api_key) > 4:
                return {"status": "assumed_valid", "message": "Custom API key saved (cannot auto-verify)"}
            return {"status": "invalid", "message": "API key is too short"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/providers")
async def list_providers():
    """List supported API providers."""
    return {
        "providers": [
            {"id": "openai", "name": "OpenAI", "default_model": "gpt-4o-mini", "default_base_url": "https://api.openai.com/v1"},
            {"id": "anthropic", "name": "Anthropic (Claude)", "default_model": "claude-3-haiku-20240307", "default_base_url": "https://api.anthropic.com/v1"},
            {"id": "google", "name": "Google (Gemini)", "default_model": "gemini-1.5-flash", "default_base_url": "https://generativelanguage.googleapis.com/v1beta"},
            {"id": "deepseek", "name": "DeepSeek", "default_model": "deepseek-chat", "default_base_url": "https://api.deepseek.com/v1"},
            {"id": "custom", "name": "自定义 (OpenAI兼容)", "default_model": "", "default_base_url": ""},
        ]
    }
