from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import threading
import requests
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def async_request(url, headers, data):
  # Errors in thread need to be tried separately because they don't propagate to the main stack
  try:
    if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'  # Set a default Content-Type, if it's not included in the original request our request fails (Flask requires content type to be present by default)

    res = requests.post(url, headers=headers, json=data)
    res.raise_for_status()  # Raise an exception if the request was not successful (status code >= 400)
  except requests.exceptions.RequestException as e:
    logging.error(f"Failed to make a request to {url}: {e}") # Catch request errors separately
  except Exception as e:
      logging.error(f"An error occurred in async_request: {e}") # Catch any other errors

@app.route('/webhooks/<path:subpath>', methods=['POST'])
def webhook(subpath):
  try:
    dst_url = os.environ.get("RELAY_DST_URL")
    headers = request.headers
    data    = request.get_json()
    url     = f"{dst_url}/{subpath}"

    thread  = threading.Thread(target=async_request, args=(url, headers, data))
    thread.start()

    return jsonify(success=True), 200
  except Exception as e:
    logging.error(f"An error occurred in the main thread: {e}")

if __name__ == '__main__':
  app.run(host=os.environ.get("RELAY_HOST", "0.0.0.0"), port=os.environ.get("RELAY_PORT", 50000))
