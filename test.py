import asyncio
import httpx
import time


async def main_awaited():

    async with httpx.AsyncClient() as client:

        for number in range(1, 151):
            pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{number}'

            resp = await client.get(pokemon_url)
            pokemon = resp.json()
            print(pokemon['name'], end=', ')
    print('/n')

def main_just_httpx():
    client = httpx.Client()

    for number in range(1, 151):
        url = f'https://pokeapi.co/api/v2/pokemon/{number}'
        resp = client.get(url)
        pokemon = resp.json()
        print(pokemon['name'], end=', ')

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




print('Awaited:')
start_time = time.time()
asyncio.run(main_awaited())
print("\n--- %s seconds ---" % (time.time() - start_time))

print('Just httpx:')
start_time = time.time()
main_just_httpx()
print("\n--- %s seconds ---" % (time.time() - start_time))

print('Awaited with tasks:')
start_time = time.time()
asyncio.run(main_with_tasks())
print("\n--- %s seconds ---" % (time.time() - start_time))