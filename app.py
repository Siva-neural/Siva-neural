from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

app = Flask(__name__)

# Add rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/api/hello', methods=['GET'])
@limiter.limit("10 per minute")
def hello():
    logging.info("Hello endpoint accessed")
    return jsonify({"message": "Hello, World!, this is a test"})

@app.route('/api/echo', methods=['POST'])
@limiter.limit("20 per minute")
def echo():
    logging.info("Echo endpoint accessed")
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    return jsonify(data)

# Add a new endpoint
@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"})

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logging.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)



