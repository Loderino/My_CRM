import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from CRM.server.frontend.routes import router as frontend_router
from CRM.server.api.routes import router as api_router

async def run_server(host: str = "127.0.0.1", port: int = 8000):
    app = FastAPI()
    
    app.mount(
        "/static", 
        StaticFiles(directory="CRM/server/frontend/static"),
        name="static"
    )
    templates = Jinja2Templates(directory="CRM/server/frontend/templates")
    app.state.templates = templates
    app.include_router(frontend_router)
    app.include_router(api_router, prefix="/api")

    config = uvicorn.Config(
        app=app,
        host=host,
        port=port,
        reload=True,
        loop="asyncio"
    )
    server = uvicorn.Server(config)
    await server.serve() 