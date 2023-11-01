from flask import Flask, request, jsonify
import ipdb

app = Flask(__name__)

@app.route('/<path:any>', methods=['POST'])
def webhook(any):
  return jsonify(success=True), 200

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=50001)
