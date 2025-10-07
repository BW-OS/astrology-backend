from fastapi import FastAPI, Query, HTTPException
import os, time
import httpx
from kerykeion import AstrologicalSubject
from lunar_python import Solar


app = FastAPI(title="Astrology Backend")

# ---------- Western ----------
@app.get("/western")
def western(lat: float = Query(...), lng: float = Query(...)):
    person = AstrologicalSubject(
        "User", 1990, 1, 1, 12, 0,
        lng=lng, lat=lat, tz_str="America/New_York"
    )
    return {"sun_sign": person.sun.get("sign", "Unknown")}

# ---------- BaZi ----------
@app.get("/bazi")
def bazi(y: int, m: int, d: int, hh: int = 12, mm: int = 0, ss: int = 0, gender: int = 1):
    solar = Solar.fromYmdHms(y, m, d, hh, mm, ss)
    lunar = solar.getLunar()
    ec = lunar.getEightChar()
    bazi_str = ec.toString()

    yun = ec.getYun(gender)  # 1=male, 0=female
    start = {"years": yun.getStartYear(), "months": yun.getStartMonth(), "days": yun.getStartDay()}

    da_yun = yun.getDaYun(3)
    da_yun_pretty = [
        f"{dy.getGanZhi()} (starts age {dy.getStartAge()}, year {dy.getStartYear()})"
        for dy in da_yun
    ]
    return {"bazi": bazi_str, "yun_start_offset": start, "first_3_dayun": da_yun_pretty}

# ---------- VedAstro proxy (paste Builder URLs) ----------
VEDASTRO_KEY = (os.getenv("VEDASTRO_API_KEY") or "").strip() or None

async def call_with_backoff(url: str, max_retries: int = 3):
    headers = {}
    if VEDASTRO_KEY:
        headers["x-api-key"] = VEDASTRO_KEY  # harmless if endpoint ignores it
    delay = 1.5
    async with httpx.AsyncClient(timeout=30) as client:
        for attempt in range(max_retries + 1):
            r = await client.get(url, headers=headers)
            if r.status_code == 200:
                try:
                    return r.json()
                except Exception:
                    return {"raw": r.text}
            if r.status_code == 429 and attempt < max_retries:
                time.sleep(delay); delay *= 2; continue
            raise HTTPException(status_code=r.status_code, detail=r.text)

@app.get("/vedastro/all-planet-data")
async def vedastro_all_planet_data(url: str = Query(..., description="Paste URL from VedAstro API Builder")):
    return await call_with_backoff(url)

@app.get("/vedastro/dasa-range")
async def vedastro_dasa_range(url: str = Query(..., description="Paste URL from VedAstro API Builder")):
    return await call_with_backoff(url)

# ---------- Health check ----------
@app.get("/health")
async def health_check():
    return {"ok": True}

# ---------- Web UI routes ----------
from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/natal", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    name: str = Form(...),
    year: int = Form(...),
    month: int = Form(...),
    day: int = Form(...),
    hour: int = Form(12),
    minute: int = Form(0),
    second: int = Form(0),
    gender: int = Form(1),
):
    # For demonstration, just echo back the form data
    result = {
        "message": "Form submitted successfully",
        "data": {
            "name": name,
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "second": second,
            "gender": gender,
        },
    }
    return templates.TemplateResponse("result.html", {"request": request, "result": result, "name": name, "year": year, "month": month, "day": day, "hour": hour, "minute": minute, "second": second, "gender": gender})

from fastapi.responses import JSONResponse

@app.post("/natal/json")
async def submit_form_json(
    name: str = Form(...),
    year: int = Form(...),
    month: int = Form(...),
    day: int = Form(...),
    hour: int = Form(12),
    minute: int = Form(0),
    second: int = Form(0),
    gender: int = Form(1),
):
    # For demonstration, just echo back the form data as JSON
    result = {
        "message": "Form submitted successfully",
        "data": {
            "name": name,
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "second": second,
            "gender": gender,
        },
    }
    return JSONResponse(content=result)
