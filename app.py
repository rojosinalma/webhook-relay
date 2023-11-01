from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import threading
import requests

import ipdb # Dev debugger

load_dotenv()

app = Flask(__name__)

def async_request(url):
  # This is the function that will run in a separate thread
  requests.post(url)

@app.route('/webhooks/<path:subpath>', methods=['POST'])
def webhook(subpath):
  dst_url = os.environ.get("RELAY_DST_URL")
  data    = request.get_json()
  url     = f"{dst_url}/{subpath}"

  thread  = threading.Thread(target=async_request, args=(url,))
  thread.start()
  # ipdb.set_trace()
  # requests.post(url)

  return jsonify(success=True), 200

if __name__ == '__main__':
  env = {
      "RELAY_HOST": "0.0.0.0",
      "RELAY_PORT": "8000"
  }

  app.run(host=os.environ['RELAY_HOST'], port=os.environ['RELAY_PORT'])
