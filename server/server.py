from flask import Flask, jsonify, request
from flask_cors import CORS
import httpx
import asyncio
from functools import wraps

app = Flask(__name__)
CORS(app)

@app.route('/')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'farmer_insights_api'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=8080)