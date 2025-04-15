import asyncio
import httpx
import time

TARGET_URL = "http://localhost/ping"
CONCURRENCY = 1500
DURATION_SECONDS = 5


stop_flag = False

async def bombard(client):
    while not stop_flag:
        try:
            response = await client.get(TARGET_URL, timeout=5.0)
            print(f"{response.status_code}")
        except httpx.RequestError as e:
            print("Request error:", e)

async def run_load_test():
    global stop_flag
    async with httpx.AsyncClient() as client:
        tasks = [asyncio.create_task(bombard(client)) for _ in range(CONCURRENCY)]
        await asyncio.sleep(DURATION_SECONDS)
        stop_flag = True
        await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    print(f"Sending requests to {TARGET_URL} with {CONCURRENCY} workers for {DURATION_SECONDS} seconds...")
    start = time.time()
    try:
        asyncio.run(run_load_test())
    except KeyboardInterrupt:
        print("Test interrupted by user.")
    finally:
        print(f"Finished in {time.time() - start:.2f} seconds.")
