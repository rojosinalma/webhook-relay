from dotenv import load_dotenv
import os

load_dotenv()

workers = 1  # You can adjust the number of worker processes
env     = {
    "RELAY_HOST": "0.0.0.0",
    "RELAY_PORT": "50000"
}

bind = f"{os.environ['RELAY_HOST']}:{os.environ['RELAY_PORT']}"
