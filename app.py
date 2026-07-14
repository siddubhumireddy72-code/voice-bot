"""Main Flask Application for Voice Bot"""
import os
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config
from database.db import init_db
import logging

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config[os.getenv('FLASK_ENV', 'development')])

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize database
with app.app_context():
    init_db()


@app.route('/')
def index():
    """Dashboard home page"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')


@app.route('/calls')
def calls():
    """Call logs page"""
    return render_template('calls.html')


@app.route('/settings')
def settings():
    """Settings page"""
    return render_template('settings.html')


# API Endpoints
@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Voice Bot is running'
    }), 200


@app.route('/api/calls', methods=['GET'])
def get_calls():
    """Get all calls"""
    from database.models import Call
    try:
        calls = Call.query.all()
        return jsonify({
            'status': 'success',
            'calls': [call.to_dict() for call in calls]
        }), 200
    except Exception as e:
        logger.error(f"Error fetching calls: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/calls/<int:call_id>', methods=['GET'])
def get_call(call_id):
    """Get specific call details"""
    from database.models import Call
    try:
        call = Call.query.get(call_id)
        if not call:
            return jsonify({
                'status': 'error',
                'message': 'Call not found'
            }), 404
        return jsonify({
            'status': 'success',
            'call': call.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Error fetching call: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/webhook/call', methods=['POST'])
def incoming_call():
    """Webhook for incoming calls from Asterisk"""
    try:
        data = request.get_json()
        logger.info(f"Incoming call received: {data}")
        
        from call_handler.call_manager import CallManager
        call_manager = CallManager()
        result = call_manager.handle_incoming_call(data)
        
        return jsonify({
            'status': 'success',
            'message': 'Call received and processing',
            'result': result
        }), 200
    except Exception as e:
        logger.error(f"Error handling incoming call: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/process_speech', methods=['POST'])
def process_speech():
    """Process speech input"""
    try:
        data = request.get_json()
        user_input = data.get('text')
        call_id = data.get('call_id')
        
        if not user_input:
            return jsonify({
                'status': 'error',
                'message': 'No text provided'
            }), 400
        
        from ai_engine.openai_client import OpenAIClient
        ai_client = OpenAIClient()
        response = ai_client.get_response(user_input)
        
        return jsonify({
            'status': 'success',
            'response': response,
            'call_id': call_id
        }), 200
    except Exception as e:
        logger.error(f"Error processing speech: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get call statistics"""
    from database.models import Call
    try:
        total_calls = Call.query.count()
        answered_calls = Call.query.filter_by(status='answered').count()
        missed_calls = Call.query.filter_by(status='missed').count()
        
        return jsonify({
            'status': 'success',
            'stats': {
                'total_calls': total_calls,
                'answered_calls': answered_calls,
                'missed_calls': missed_calls
            }
        }), 200
    except Exception as e:
        logger.error(f"Error fetching stats: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({
        'status': 'error',
        'message': 'Resource not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    logger.error(f"Internal error: {str(error)}")
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    app.run(
        host=app.config['SERVER_HOST'],
        port=app.config['SERVER_PORT'],
        debug=app.config['DEBUG']
    )
