from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes.clean import router as clean_router

app = FastAPI(
    title="DataSanity AI",
    description="Intelligent CSV Data Cleaning for Medicine Datasets",
    version="2.0.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route
app.include_router(clean_router)

# Templates
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@app.get("/test")
async def test():
    return JSONResponse({
        "status": "ok",
        "message": "DataSanity AI v2.0 is running!",
        "features": [
            "Smart column detection",
            "Quality scoring",
            "Excel reports",
            "Expiry warnings"
        ]
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )