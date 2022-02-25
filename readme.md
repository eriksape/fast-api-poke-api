### Install

You can run this project via docker compose

```shell
docker compose up
```

and you can check it

```shell
curl --location --request GET 'http://localhost:8000'
```
and the response will be
```json
{
    "Hello": "World"
}
```

also you can check the postman collection [here](https://raw.githubusercontent.com/eriksape/fast-api-poke-api/main/berries_2022_02_25.json) to see the integration.