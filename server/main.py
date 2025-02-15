import time
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from core.databases import init_chromadb, init_db
from core.logger import setup_logger
from routers import assistant, report_generation, users


@asynccontextmanager
async def on_startup(app: FastAPI):
    await init_db()
    await init_chromadb()
    yield


logger = setup_logger()

app = FastAPI(
    title="Urban LLM Service",
    description="Сервис для ранжирования арх. бюро, общения с ассистентом-урбанистом и составлению отчетов.",
    version="1.0.0",
    license_info={"name": "MIT License", "url": "https://mit-license.org/"},
    lifespan=on_startup,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception as exc:
        await logger.error(f"{request.method} {request.url}: {exc}")
        raise
    process_time = time.time() - start_time
    await logger.info(
        f"{request.method} {request.url} with time [{process_time:.2f} sec] with status_code={response.status_code}"
    )
    return response


app.include_router(assistant.router)
app.include_router(report_generation.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return RedirectResponse("/redoc")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
