from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes.task_routes import router as task_router
from routes.websocket_routes import router as websocket_router
from database.database import init_db
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform actions during application startup
    print("Starting up the application...")
    init_db()
    yield  # Run the application
    # Perform actions during application shutdown
    print("Shutting down the application...")

app = FastAPI(lifespan=lifespan)
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)
# Include routes
app.include_router(task_router)

# Include the WebSocket routes
app.include_router(websocket_router)
