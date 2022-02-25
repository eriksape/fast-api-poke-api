from typing import Optional
import requests
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/berries")
def read_item(name: Optional[str] = None, limit: Optional[int] = 10, offset: Optional[int] = 0):
    name_filter = ""
    if name:
        name_filter = ',where: {name: {_in: [%s]}}' % (name)

    query = """query samplePokeAPIquery {
                pokemon_v2_berry(limit: %d, offset: %d %s) {
                    id
                    name
                    growth_time
                    max_harvest
                }
            }        
            """ % (limit, offset, name_filter)

    r = requests.post('https://beta.pokeapi.co/graphql/v1beta', json={"query": query})


    return {"data": r.json()['data'], "limit": limit, "offset": offset, "next_offset": limit + offset}


