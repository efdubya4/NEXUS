"""
NEXUS API Server
Flask-based API to connect NEXUS Guardian backend with frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging
import yaml
from nexus_guardian import NexusGuardian, LLMClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load config
def load_config():
    with open('NEXUS/nexus-config.yaml', 'r') as f:
        return yaml.safe_load(f)

config = load_config()
llm_cfg = config.get('llm', {})
llm_provider = llm_cfg.get('provider', 'openai')
llm_model = llm_cfg.get('model', 'gpt-3.5-turbo')
llm_temperature = llm_cfg.get('temperature', 0.7)
llm_max_tokens = llm_cfg.get('max_tokens', 512)

llm_client = None
if llm_provider in ['openai', 'anthropic']:
    llm_client = LLMClient(
        provider=llm_provider,
        model=llm_model,
        temperature=llm_temperature,
        max_tokens=llm_max_tokens
    )

# Initialize NEXUS Guardian with LLM support
guardian = NexusGuardian(llm_client=llm_client)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

@app.route('/api/nexus/query', methods=['POST'])
def process_query():
    """
    Process user query through NEXUS Guardian
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        user_context = data.get('context', {})
        
        if not user_message:
            return jsonify({
                'error': 'No message provided',
                'status': 'error'
            }), 400
        
        # Process query through Guardian
        result = guardian.process_query(user_message, user_context)
        
        # Extract response for frontend
        response_text = result['payload']['response_text']
        routing_info = result['payload']['routing_decision']
        performance_metrics = result['payload']['performance_metrics']
        
        return jsonify({
            'status': 'success',
            'response': response_text,
            'routing': routing_info,
            'metrics': performance_metrics,
            'aicl_message': result
        })
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/nexus/status', methods=['GET'])
def get_status():
    """
    Get NEXUS system status
    """
    try:
        metrics = guardian.get_performance_metrics()
        
        return jsonify({
            'status': 'online',
            'agent': guardian.get_agent_info(),
            'metrics': metrics,
            'system_health': {
                'guardian': 'online',
                'router': 'online',
                'aicl_protocol': 'online'
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/nexus/metrics', methods=['GET'])
def get_metrics():
    """
    Get detailed performance metrics
    """
    try:
        metrics = guardian.get_performance_metrics()
        
        return jsonify({
            'status': 'success',
            'metrics': metrics
        })
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/nexus/agents', methods=['GET'])
def get_agents():
    """
    Get available agents information (Guardian only)
    """
    try:
        agents = {
            'guardian': guardian.get_agent_info(),
        }
        return jsonify({
            'status': 'success',
            'agents': agents
        })
    except Exception as e:
        logger.error(f"Error getting agents: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/nexus/test', methods=['POST'])
def test_query():
    """
    Test endpoint for development
    """
    try:
        data = request.get_json()
        test_message = data.get('message', 'How do I build a deck?')
        
        # Process test query
        result = guardian.process_query(test_message)
        
        return jsonify({
            'status': 'success',
            'test_message': test_message,
            'result': result
        })
        
    except Exception as e:
        logger.error(f"Error in test query: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Simple health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'service': 'NEXUS API',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    logger.info("Starting NEXUS API Server...")
    logger.info("NEXUS Guardian initialized successfully")
    logger.info("Available endpoints:")
    logger.info("  POST /api/nexus/query - Process user queries")
    logger.info("  GET  /api/nexus/status - Get system status")
    logger.info("  GET  /api/nexus/metrics - Get performance metrics")
    logger.info("  GET  /api/nexus/agents - Get available agents")
    logger.info("  POST /api/nexus/test - Test endpoint")
    logger.info("  GET  /health - Health check")
    
    app.run(host='0.0.0.0', port=5001, debug=True) 