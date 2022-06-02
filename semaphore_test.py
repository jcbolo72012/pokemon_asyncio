import asyncio
import httpx


"""
Baseline code from : https://tutorialedge.net/python/concurrency/python-asyncio-semaphores-tutorial/

"""
async def myPokeWorker(semaphore, client, url):
    await semaphore.acquire()
    print('Successfully acquired the semaphore')
    await asyncio.sleep(2)
    resp = await client.get(url)
    pokemon = resp.json()

    print('Releasing Semaphore')
    semaphore.release()
    return pokemon['name']

async def main():

    mySemaphore = asyncio.Semaphore(value = 100)
    async with httpx.AsyncClient() as client:

        tasks = []
        for number in range(1, 151):
            url = f'https://pokeapi.co/api/v2/pokemon/{number}'
            tasks.append(asyncio.ensure_future(myPokeWorker(mySemaphore, client, url)))

        original_pokemon = await asyncio.gather(*tasks)
        for pokemon in original_pokemon:
            print(pokemon, end = ', ')
    print('Finished All Workers')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
print("Our Loop Has Completed")
loop.close()