import asyncio


async def start_strongman(name, power):
    print(f"Strongman {name} began the competition.")
    for ball_number in range(1, 6):
        await asyncio.sleep(1 / power)
        print(f"Strongman {name} lifted {ball_number}.")
    print(f"Strongman {name} finished competition.")


async def start_tournament():
    task1 = asyncio.create_task(start_strongman('Pasha', 3))
    task2 = asyncio.create_task(start_strongman('Denis', 4))
    task3 = asyncio.create_task(start_strongman('Apollon', 5))
    await task1
    await task2
    await task3

if __name__ == "__main__":
    asyncio.run(start_tournament())
