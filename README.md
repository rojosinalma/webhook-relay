Webhook Relay
---

Simple python flask app to relay webhooks calls asynchronously to backend services.

## Dependencies:
* Python3

## Usage

The app receives requests at the path `/<relay_id>/_anything_else_`, anything received in this path will be relayed asynchronously to the  `RELAY_DST_URL`, the original requester will get a `200` response without waiting for the destination to respond.

The path `<relay_id>` is just an arbitrary id that needs to be prepended in order to send a notification and log internally whats being relayed.

Any path that comes after `/<relay_id>` will also be relayed to the destination URl, but without the `/<relay_id>` part. The same is true for the headers and any json payload that gets sent from the original request.

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

Or with `docker-compose`

```bash
docker-compose -f docker-compose.yaml build
docker-compose -f docker-compose.yaml up -d
```

With this you can easily have the app and the api test running without more setup.

## Simulating an internal service
There's also a simple app in `dst_api.py` that receives requests on any path available and responds with `200`, to use it:

```bash
python dst_api.py
```

This will give you a place to test the relay of webhooks, you can set the `RELAY_DST_URL` in your .env to localhost:50001. You can set a different port in the `dst_api.py` script.
If you're using `docker-compose` this has already been configured.

## Development

1. Fork it
2. Change it
3. Make a PR
4. Ping me!
