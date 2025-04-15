import math
import time
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/ping")
def ping():
    # Simula trabajo de CPU
    [math.sqrt(i) for i in range(10000)]
    time.sleep(0.05)  # 50ms de espera artificial
    return {"message": "pong"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
