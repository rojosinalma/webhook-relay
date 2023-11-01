Webhook Relay
---

Simple python flask app to relay webhooks calls asynchronously to backend services.

## Dependencies:
* Python3


## Usage

1. Duplicate the `.env.example` and fill the variables with their proper values.

2. Run the relay
    ```bash
    pip install -r requirements.txt
    python relay.py # For local usage
    gunicorn -c gunicorn_config.py app:app # For production usage
    ```

## Running with Docker
If you want to use the Docker image locally:

```bash
docker build -t webhook-relay:latest -f Dockerfile .
docker run -it webhook-relay:latest
```

## Simulating an internal service
There's also a simple webserver that receives requests on any path available with dst_api_test.py, to use it:

```bash
python dst_api_test.py
```

This will give you a place to test the relay of webhooks, you can set the `RELAY_DST_URL` in your .env to localhost:50001. You can set a different port in the dst_api_test.py script.

## Development

1. Fork it
2. Change it
3. Make a PR
4. Ping me!
