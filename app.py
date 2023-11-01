from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import threading
import requests
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def async_request(url):
  try:
    res = requests.post(url)
    res.raise_for_status()  # Raise an exception if the request was not successful (status code >= 400)
  except requests.exceptions.RequestException as e:
    logging.error(f"Failed to make a request to {url}: {e}")

@app.route('/webhooks/<path:subpath>', methods=['POST'])
def webhook(subpath):
  dst_url = os.environ.get("RELAY_DST_URL")
  data    = request.get_json()
  url     = f"{dst_url}/{subpath}"

  thread  = threading.Thread(target=async_request, args=(url,))
  thread.start()

  return jsonify(success=True), 200

if __name__ == '__main__':
  env = {
      "RELAY_HOST": "0.0.0.0",
      "RELAY_PORT": "50000"
  }

  app.run(host=os.environ['RELAY_HOST'], port=os.environ['RELAY_PORT'])
