from fastapi import FastAPI

from typing import Optional
from pydantic import BaseModel


from api.routes.router import api_router
from core.config import (API_PREFIX, APP_NAME, APP_VERSION,IS_DEBUG)
from core.event_handlers import (start_app_handler, stop_app_handler)




def get_app() -> FastAPI:
    app = FastAPI(title=APP_NAME, version=APP_VERSION, debug=IS_DEBUG)
    app.include_router(api_router, prefix=API_PREFIX)

    # app.add_event_handler("startup", start_app_handler(app))
    # app.add_event_handler("shutdown", stop_app_handler(app))
    
    return app



app = get_app()


# for health checks
@app.get("/")
def root():
    return {"status": 200}
