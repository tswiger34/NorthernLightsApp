from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import auth, noaa_data, alerts

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router)
app.include_router(noaa_data.router)
app.include_router(alerts.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Solar Weather API!"}
