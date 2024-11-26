# urban-service
>System of recommendations from architectural bureaus based on a multi-agent environment
---
## Installation
1. After downloading the repository, you need to configure the files:
    - `.chromadb`
        ```sh
        CHROMA_SERVER_AUTH_CREDENTIALS="test-token"
        CHROMA_SERVER_AUTH_PROVIDER="chromadb.auth.token_authn.TokenAuthenticationServerProvider"
        CHROMA_AUTH_TOKEN_TRANSPORT_HEADER="Authorization"
        ```
    - `.env`
        ```sh
        OPENAI_API_KEY="sk-proj-..."
        TG_TOKEN="..."
        ```
2. Run the following command:
```sh
docker compose up -d --build
```

## Using
1. Go to the address for the API documentation `http://0.0.0.0:8001/redoc` or `http://0.0.0.0:8001/docs`

2. Use your telegram bot for testing.

## LICENSE
Copyright © 2024 [dsuhoi](https://github.com/dsuhoi).

This project is [MIT](https://github.com/dsuhoi/urban-service/blob/main/LICENSE) licensed.
