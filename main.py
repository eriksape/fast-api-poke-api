from typing import Optional
import requests
import zipfile
from io import BytesIO
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/berries")
def read_item(name: Optional[str] = None, limit: Optional[int] = 10, offset: Optional[int] = 0, output: Optional[str] = 'json'):
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


    if output == 'json':

        return {"data": r.json()['data'], "limit": limit, "offset": offset, "next_offset": limit + offset}

    if output == 'zip':

        mem_file = BytesIO()
        zip_file = zipfile.ZipFile(mem_file, 'w', zipfile.ZIP_DEFLATED)
        current_time = datetime.now().strftime("%G_%m_%d")
        file_name = 'berries_' + str(current_time) + '.json'
        zip_file.writestr(file_name, r.content)

        zip_file.close()

        return StreamingResponse(
            iter([mem_file.getvalue()]),
            media_type="application/x-zip-compressed",
            headers={"Content-Disposition": f"attachment;filename=download.zip"}
        )

    return {"error": "output not supported"}