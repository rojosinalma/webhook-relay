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

def send_discord_notification(message):
    discord_webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if discord_webhook_url is None:
        logging.error("DISCORD_WEBHOOK_URL environment variable is not set")
        return

    payload  = { "content": message }
    response = requests.post(discord_webhook_url, json=payload)
    logging.info("Discord notification sent successfully")

def async_request(url, headers, data):
  try:
    res = requests.post(url, headers=headers, json=data, verify=False)
    res.raise_for_status()  # Raise an exception if the request was not successful (status code >= 400)
    logging.info(f"Successfully relayed request to {url}")

    message = "Request successfully relayed to " + url
    send_discord_notification(message)

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

    if not dst_url:
      raise ValueError("RELAY_DST_URL environment variable is not set")

    if 'Content-Type' in headers:
      data = request.get_json() # We skip if there's no content type because otherwise flask complains

    thread  = threading.Thread(target=async_request, args=(url, headers, data))
    thread.start()

    return jsonify(success=True), 200
  except Exception as e:
    logging.error(f"An error occurred in the main thread: {e}")
    return jsonify(success=False), 500

@app.route('/status')
def status():
  return '', 200

if __name__ == '__main__':
  app.run(host=os.environ.get("RELAY_HOST", "0.0.0.0"), port=os.environ.get("RELAY_PORT", 50000))
