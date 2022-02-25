import requests
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/berries")
def read_item():
    query = """query samplePokeAPIquery {
                pokemon_v2_berry {
                    id
                    name
                    growth_time
                    max_harvest
                }
            }        
            """

    r = requests.post('https://beta.pokeapi.co/graphql/v1beta', json={"query": query})

    return {"data": r.json()['data']}


