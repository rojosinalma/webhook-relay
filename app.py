from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import threading
import requests
import logging
import urllib3

load_dotenv()
logging.basicConfig(level=logging.INFO)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Disable insecure request warnings

app = Flask(__name__)

def async_request(url, headers, data):
  try:
    res = requests.post(url, headers=headers, json=data, verify=False)
    res.raise_for_status()  # Raise an exception if the request was not successful (status code >= 400)
    logging.info(f"Successfully relayed request to {url}")
  except requests.exceptions.RequestException as e:
    logging.error(f"Failed to make a request to {url}: {e}")
  except Exception as e:
    logging.error(f"An error occurred in async_request: {e}")

@app.route('/webhooks/<path:subpath>', methods=['POST'])
def webhook(subpath):
  try:
    dst_url = os.environ.get("RELAY_DST_URL")
    headers = request.headers
    url     = f"{dst_url}/{subpath}"
    data    = '{}'

    if 'Content-Type' in headers:
      data = request.get_json() # We skip this because otherwise flask complains about not having a content type

    thread  = threading.Thread(target=async_request, args=(url, headers, data))
    thread.start()

    return jsonify(success=True), 200
  except Exception as e:
    logging.error(f"An error occurred in the main thread: {e}")

if __name__ == '__main__':
  app.run(host=os.environ.get("RELAY_HOST", "0.0.0.0"), port=os.environ.get("RELAY_PORT", 50000))
