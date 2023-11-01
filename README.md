Webhook Relay
---

Simple python flask app to relay webhooks calls asynchronously to backend services.

## Dependencies:
* Python3

## Usage

The app receives requests at the path `/webhooks`, anything received in this path will be relayed asynchronously to the  `RELAY_DST_URL`, the original requested will get a `200` response without waiting for the destination to respond.

Any path that comes after `/webhooks` will also be relayed to the destination URl, without the `/webhooks` part. The same is true for any json payload that gets sent in the original request, it will be relayed untouched to the destination URL.

**NOTE: The relay supports redirecting to just one destination URL, if you need to route to more destinations, it's recommended to setup multiple instances of the relay.**


## Development

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
