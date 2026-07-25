from fastapi import FastAPI

app = FastAPI(title="FlyRank Auth API")

@app.get("/")
def root():
    return {"message": "Server running and connected to Supabase"}