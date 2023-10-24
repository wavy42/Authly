"""
main.py
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> str:
    return "Hello World!"


# debug/dev only
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
