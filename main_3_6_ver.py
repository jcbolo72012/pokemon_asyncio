import asyncio
import httpx
import time

"""
Uncomment for faster use on Linux
For use with python 3.6
"""
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def get_pokemon(client, url):
  resp = await client.get(url)
  pokemon = resp.json()

  return pokemon['name']


async def main_with_tasks():

    async with httpx.AsyncClient() as client:

        tasks = []
        for number in range(1, 151):
            url = f'https://pokeapi.co/api/v2/pokemon/{number}'
            tasks.append(asyncio.ensure_future(get_pokemon(client, url)))

        original_pokemon = await asyncio.gather(*tasks)
        for pokemon in original_pokemon:
            print(pokemon, end = ', ')

uvloop.install()

loop = asyncio.get_event_loop()

print('Awaited with tasks:')
start_time = time.time()
loop.run_until_complete(main_with_tasks())
print("\n--- %s seconds ---" % (time.time() - start_time))