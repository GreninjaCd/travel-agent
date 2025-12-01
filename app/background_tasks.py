import asyncio

async def periodic_cleanup():
    while True:
        await asyncio.sleep(60)
