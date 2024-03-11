from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    print(f"LOG from MESSAGES: GET")
    return {"message": "NOT IMPLEMENTED"}
