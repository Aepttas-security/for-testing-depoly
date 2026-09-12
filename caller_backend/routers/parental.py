# caller_backend/routers/parental.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
import logging
from database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Parental Control"])

# State tracking for child profiles, screentime, filters, and pairing
mock_children = [
    {
        "child_id": "1",
        "parent_id": 1,
        "name": "Leo",
        "age": 10,
        "device": "Samsung Galaxy S22",
        "battery": "87%",
        "is_active_online": True,
        "linking_code": "583921"
    }
]

mock_screentime = {
    "1": {
        "child_id": "1",
        "daily_limit_minutes": 120,
        "current_usage_minutes": 45,
        "is_locked_remotely": False
    }
}

mock_apps = {
    "1": [
        {"app_id": "com.instagram.android", "app_name": "Instagram", "category": "Social", "is_blocked": False},
        {"app_id": "com.zhiliaoapp.musically", "app_name": "TikTok", "category": "Social", "is_blocked": True},
        {"app_id": "com.roblox.client", "app_name": "Roblox", "category": "Games", "is_blocked": False},
        {"app_id": "com.google.android.youtube", "app_name": "YouTube", "category": "Media", "is_blocked": False}
    ]
}

mock_filters = {
    "1": {
        "status": "success",
        "child_id": "1",
        "blocked_categories": {
            "Adult": True,
            "Gambling": True,
            "SocialMedia": False,
            "Gaming": False,
            "Violence": True
        }
    }
}

mock_blacklist = {
    "1": ["badsite.com", "gambling-online.net"]
}

mock_sos = {
    "1": None
}

mock_geofences = {
    "1": [
        {"id": "geo-1", "name": "Home SafeZone", "latitude": 12.9352, "longitude": 77.6245, "radius_meters": 200, "is_active": True},
        {"id": "geo-2", "name": "School Zone", "latitude": 12.9400, "longitude": 77.6300, "radius_meters": 300, "is_active": True}
    ]
}

# ============================================
# 👶 CHILD MANAGEMENT
# ============================================
@router.get("/api/child")
@router.get("/api/parental/child")
def get_children():
    return mock_children

@router.post("/api/child")
@router.post("/api/parental/child")
def create_child(payload: Dict[str, Any]):
    new_id = str(len(mock_children) + 1)
    child = {
        "child_id": new_id,
        "parent_id": payload.get("parent_id", 1),
        "name": payload.get("name", "Child"),
        "age": payload.get("age", 10),
        "device": payload.get("device", "Android Phone"),
        "battery": "90%",
        "is_active_online": True,
        "linking_code": str(uuid.uuid4().int)[:6]
    }
    mock_children.append(child)
    mock_screentime[new_id] = {
        "child_id": new_id,
        "daily_limit_minutes": 120,
        "current_usage_minutes": 0,
        "is_locked_remotely": False
    }
    return child

@router.post("/api/child/{child_id}/generate-code")
@router.post("/api/parental/child/{child_id}/generate-code")
def generate_code(child_id: str):
    code = "729481"
    for c in mock_children:
        if c["child_id"] == child_id:
            c["linking_code"] = code
    return {"status": "success", "code": code}

@router.post("/api/child/{child_id}/permissions-sync")
@router.post("/api/parental/child/{child_id}/permissions-sync")
def sync_permissions(child_id: str, payload: Dict[str, Any]):
    return {"status": "success"}

@router.post("/api/child/{child_id}/unlink")
@router.post("/api/parental/child/{child_id}/unlink")
def unlink_child(child_id: str):
    return {"status": "success", "message": "Device unlinked successfully"}

@router.post("/api/child/{child_id}/request-unlink")
@router.post("/api/parental/child/{child_id}/request-unlink")
def request_unlink(child_id: str):
    return {"status": "success", "code": "482019"}

@router.get("/api/child/{child_id}/active-unlink-code")
@router.get("/api/parental/child/{child_id}/active-unlink-code")
def active_unlink_code(child_id: str):
    return {"status": "success", "code": "482019"}

@router.post("/api/child/{child_id}/verify-unlink")
@router.post("/api/parental/child/{child_id}/verify-unlink")
def verify_unlink(child_id: str, payload: Dict[str, Any]):
    return {"status": "success"}

# ============================================
# 🔗 PAIRING
# ============================================
@router.post("/api/pairing/generate-parent-code")
@router.post("/api/parental/pairing/generate-parent-code")
def generate_parent_code(payload: Dict[str, Any]):
    return {"status": "success", "pairing_code": "847291"}

@router.get("/api/pairing/status-by-code/{code}")
@router.get("/api/parental/pairing/status-by-code/{code}")
def status_by_code(code: str):
    return {
        "status": "linked",
        "child_id": "1",
        "parent_id": 1,
        "name": "Leo"
    }

@router.post("/api/pairing/link-device")
@router.post("/api/parental/pairing/link-device")
def link_device(payload: Dict[str, Any]):
    return {
        "status": "success",
        "child_id": "1",
        "parent_id": 1
    }

@router.get("/api/pairing/check-parent-linked/{parent_id}")
@router.get("/api/parental/pairing/check-parent-linked/{parent_id}")
def check_parent_linked(parent_id: int):
    return {"status": "linked", "is_linked": True, "child_id": "1"}

@router.post("/api/pairing/logout-attempt")
@router.post("/api/parental/pairing/logout-attempt")
def logout_attempt(payload: Dict[str, Any]):
    return {"status": "success"}

@router.get("/api/pairing/check-logout-attempt/{parent_id}")
@router.get("/api/parental/pairing/check-logout-attempt/{parent_id}")
def check_logout_attempt(parent_id: int):
    return {"has_attempt": False}

# ============================================
# ⌛ SCREENTIME
# ============================================
@router.get("/api/screentime/{child_id}/dashboard")
@router.get("/api/parental/screentime/{child_id}/dashboard")
def get_screentime(child_id: str):
    st = mock_screentime.get(child_id, {
        "child_id": child_id,
        "daily_limit_minutes": 120,
        "current_usage_minutes": 45,
        "is_locked_remotely": False
    })
    return st

@router.post("/api/screentime/{child_id}/remote-lock")
@router.post("/api/parental/screentime/{child_id}/remote-lock")
def remote_lock(child_id: str, payload: Dict[str, Any]):
    if child_id in mock_screentime:
        mock_screentime[child_id]["is_locked_remotely"] = payload.get("is_locked", True)
    return {"status": "success", "is_locked": payload.get("is_locked", True)}

@router.post("/api/screentime/{child_id}/daily-limit")
@router.post("/api/parental/screentime/{child_id}/daily-limit")
def daily_limit(child_id: str, payload: Dict[str, Any]):
    if child_id in mock_screentime:
        mock_screentime[child_id]["daily_limit_minutes"] = payload.get("daily_limit_minutes", 120)
    return {"status": "success", "daily_limit_minutes": payload.get("daily_limit_minutes", 120)}

# ============================================
# 📱 APPS & RESTRICTIONS
# ============================================
@router.get("/api/apps/{child_id}")
@router.get("/api/parental/apps/{child_id}")
def get_apps(child_id: str):
    return mock_apps.get(child_id, mock_apps["1"])

@router.post("/api/apps/{child_id}/toggle/{app_id}")
@router.post("/api/parental/apps/{child_id}/toggle/{app_id}")
def toggle_app(child_id: str, app_id: str, payload: Dict[str, Any]):
    apps = mock_apps.get(child_id, mock_apps["1"])
    for a in apps:
        if a["app_id"] == app_id:
            a["is_blocked"] = payload.get("is_blocked", not a["is_blocked"])
    return {"status": "success"}

# ============================================
# 🌐 WEB FILTERING
# ============================================
@router.get("/api/filters/{child_id}/rules")
@router.get("/api/parental/filters/{child_id}/rules")
def get_filters(child_id: str):
    return mock_filters.get(child_id, mock_filters["1"])

@router.post("/api/filters/{child_id}/category")
@router.post("/api/parental/filters/{child_id}/category")
def toggle_category(child_id: str, payload: Dict[str, Any]):
    cat = payload.get("category")
    val = payload.get("is_blocked", True)
    if child_id in mock_filters and cat:
        mock_filters[child_id]["blocked_categories"][cat] = val
    return {"status": "success"}

@router.post("/api/filters/{child_id}/blacklist")
@router.post("/api/parental/filters/{child_id}/blacklist")
def add_blacklist(child_id: str, payload: Dict[str, Any]):
    url = payload.get("url")
    if child_id not in mock_blacklist:
        mock_blacklist[child_id] = []
    if url and url not in mock_blacklist[child_id]:
        mock_blacklist[child_id].append(url)
    return {"status": "success"}

@router.delete("/api/filters/{child_id}/blacklist/{url}")
@router.delete("/api/parental/filters/{child_id}/blacklist/{url}")
def remove_blacklist(child_id: str, url: str):
    if child_id in mock_blacklist:
        mock_blacklist[child_id] = [u for u in mock_blacklist[child_id] if u != url]
    return {"status": "success"}

# ============================================
# 📍 LOCATION & GEOFENCES
# ============================================
@router.get("/api/location/{child_id}/live")
@router.get("/api/parental/location/{child_id}/live")
def get_child_live_location(child_id: str):
    return {
        "status": "success",
        "latitude": 12.9352,
        "longitude": 77.6245,
        "accuracy": 10.0,
        "updated_at": datetime.now().isoformat()
    }

@router.post("/api/location/{child_id}/live")
@router.post("/api/parental/location/{child_id}/live")
def update_child_live_location(child_id: str, payload: Dict[str, Any]):
    return {"status": "success"}

@router.get("/api/location/{child_id}/geofences")
@router.get("/api/parental/location/{child_id}/geofences")
def get_geofences(child_id: str):
    return mock_geofences.get(child_id, mock_geofences["1"])

@router.post("/api/location/{child_id}/geofences")
@router.post("/api/parental/location/{child_id}/geofences")
def save_geofences(child_id: str, payload: Dict[str, Any]):
    return {"status": "success"}

# ============================================
# 🚨 SOS & EMERGENCY
# ============================================
@router.get("/api/sos/preferences/{child_id}")
@router.get("/api/parental/sos/preferences/{child_id}")
def get_sos_preferences(child_id: str):
    return {
        "auto_dial_enabled": True,
        "emergency_contact": "+1 (800) 555-0199",
        "broadcast_location": True
    }

@router.post("/api/sos/trigger")
@router.post("/api/parental/sos/trigger")
def trigger_sos(payload: Dict[str, Any]):
    child_id = str(payload.get("child_id", "1"))
    mock_sos[child_id] = {
        "child_id": child_id,
        "latitude": payload.get("latitude", 12.9352),
        "longitude": payload.get("longitude", 77.6245),
        "triggered_at": datetime.now().isoformat(),
        "is_active": True
    }
    return {"status": "success", "alert_id": "sos-alert-1"}

@router.get("/api/sos/active/{child_id}")
@router.get("/api/parental/sos/active/{child_id}")
def active_sos(child_id: str):
    return mock_sos.get(child_id) or {"is_active": False}

@router.post("/api/sos/resolve/{child_id}")
@router.post("/api/parental/sos/resolve/{child_id}")
def resolve_sos(child_id: str):
    mock_sos[child_id] = None
    return {"status": "success", "message": "SOS alert marked resolved"}

# ============================================
# 📊 REPORTS & AUTH PIN
# ============================================
@router.get("/api/reports/{child_id}/summary")
@router.get("/api/parental/reports/{child_id}/summary")
def get_reports_summary(child_id: str):
    return {
        "child_id": child_id,
        "total_screen_time_hours": 3.5,
        "blocked_web_attempts": 2,
        "flagged_apps_count": 1,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

@router.post("/api/auth/verify-parent-pin")
@router.post("/api/parental/auth/verify-parent-pin")
def verify_parent_pin(payload: Dict[str, Any]):
    pin = payload.get("pin", "")
    if pin == "1234" or len(pin) == 4:
        return {"status": "success", "valid": True}
    return {"status": "error", "valid": False}
