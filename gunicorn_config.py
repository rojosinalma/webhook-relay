from dotenv import load_dotenv
import os

load_dotenv()

workers   = 1  # You can adjust the number of worker processes
accesslog = '-' # Access log to STDOUT
timeout   = int(os.environ.get("RELAY_TIMEOUT", 5))

bind = f'{os.environ.get("RELAY_HOST", "0.0.0.0")}:{os.environ.get("RELAY_PORT", 50000)}'
