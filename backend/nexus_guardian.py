"""
NEXUS Guardian: Primary Interface Agent
Cost-efficient implementation using local processing and intelligent routing
"""

import json
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import re
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, provider: str, model: str, temperature: float, max_tokens: int):
        self.provider = provider
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.openai_api_key = os.environ.get('OPENAI_API_KEY')
        self.anthropic_api_key = os.environ.get('ANTHROPIC_API_KEY')
        self.client = None
        if provider == 'openai':
            pass  # Import in query method
        elif provider == 'anthropic':
            pass  # Import in query method
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def query(self, prompt: str) -> str:
        if self.provider == 'openai':
            import openai  # type: ignore
            openai.api_key = self.openai_api_key
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response['choices'][0]['message']['content']
        elif self.provider == 'anthropic':
            import anthropic  # type: ignore
            client = anthropic.Anthropic(api_key=self.anthropic_api_key)
            response = client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

class NexusGuardian:
    """
    NEXUS Guardian - Primary interface agent for user interaction and query preprocessing
    Uses cost-efficient local processing with intelligent routing to specialists
    """
    
    def __init__(self, llm_client: Any = None):
        self.agent_id = "nexus_guardian"
        self.agent_name = "NEXUS Guardian"
        self.capabilities = ["user_interaction", "context_clarification", "intent_classification", "routing"]
        
        # Domain classification patterns (cost-efficient local processing)
        self.domain_patterns = {
            "construction": [
                r"\b(build|construction|deck|house|renovation|diy|tools?|hammer|saw|drill|wood|metal|concrete|foundation|roof|wall|floor|plumbing|electrical)\b",
                r"\b(project|plan|blueprint|permit|inspection|contractor|builder|carpenter|plumber|electrician)\b"
            ],
            "programming": [
                r"\b(code|programming|software|development|python|javascript|java|c\+\+|html|css|react|node|api|database|sql|git|debug|algorithm|function|class|variable)\b",
                r"\b(programmer|developer|coder|engineer|bug|error|compile|deploy|test|framework|library)\b"
            ],
            "gardening": [
                r"\b(garden|plant|flower|tree|soil|fertilizer|water|sun|shade|seeds?|sprout|grow|harvest|prune|weed|pest|disease|organic|compost)\b",
                r"\b(gardener|horticulture|landscape|lawn|yard|greenhouse|pot|container|indoor|outdoor)\b"
            ],
            "cooking": [
                r"\b(cook|recipe|food|meal|ingredient|spice|herb|bake|grill|fry|boil|steam|roast|chef|kitchen|utensil|pan|pot|oven|stove)\b",
                r"\b(cuisine|diet|nutrition|healthy|organic|fresh|frozen|prep|serve|presentation)\b"
            ],
            "education": [
                r"\b(learn|teach|education|study|school|university|course|lesson|tutorial|exam|test|homework|assignment|research|book|textbook|lecture|professor|student)\b",
                r"\b(subject|topic|concept|theory|practice|skill|knowledge|degree|certificate|academic)\b"
            ]
        }
        
        # Response templates for cost efficiency
        self.response_templates = {
            "construction": [
                "I've identified your query as construction-related. Let me route you to NEXUS Builder, our construction specialist who can provide detailed guidance on {topic}.",
                "This appears to be a construction project. NEXUS Builder will help you with {topic} and provide step-by-step instructions.",
                "For construction and DIY projects like {topic}, NEXUS Builder is your best resource for expert advice."
            ],
            "programming": [
                "I've detected programming content in your query. NEXUS Coder, our software development specialist, will help you with {topic}.",
                "This looks like a programming challenge. NEXUS Coder can assist you with {topic} and provide code examples.",
                "For software development questions about {topic}, NEXUS Coder has the expertise you need."
            ],
            "gardening": [
                "I've identified this as a gardening question. NEXUS Gardener, our horticulture specialist, will help you with {topic}.",
                "This appears to be about plants and gardening. NEXUS Gardener can provide expert advice on {topic}.",
                "For gardening and plant care questions like {topic}, NEXUS Gardener is your go-to specialist."
            ],
            "cooking": [
                "I've detected cooking-related content. NEXUS Chef, our culinary specialist, will help you with {topic}.",
                "This looks like a cooking question. NEXUS Chef can provide recipes and techniques for {topic}.",
                "For culinary questions about {topic}, NEXUS Chef has the expertise you need."
            ],
            "education": [
                "I've identified this as an educational query. NEXUS Teacher, our education specialist, will help you with {topic}.",
                "This appears to be a learning question. NEXUS Teacher can provide educational guidance on {topic}.",
                "For educational content about {topic}, NEXUS Teacher is your best resource."
            ],
            "general": [
                "I understand your query. How can I assist you further?",
                "I'm here to help. What would you like to know more about?",
                "I can help you with that. Is there anything specific you'd like to explore?"
            ]
        }
        
        # Performance tracking
        self.performance_metrics = {
            "total_queries": 0,
            "successful_routes": 0,
            "average_response_time": 0,
            "domain_accuracy": {}
        }
        
        self.llm_client = llm_client
        
        logger.info(f"NEXUS Guardian initialized with {len(self.domain_patterns)} domain patterns")

    def process_query(self, user_message: str, user_context: Optional[Dict] = None) -> Dict:
        """
        Process user query with cost-efficient local processing
        """
        start_time = time.time()
        
        try:
            if self.llm_client:
                # Use LLM for response
                response = self.llm_client.query(user_message)
                domain = "llm"
                confidence = 1.0
                topics = []
            else:
                # Extract key topics from user message
                topics = self._extract_topics(user_message)
                # Classify domain using local pattern matching
                domain, confidence = self._classify_domain(user_message, topics)
                # Generate response based on classification
                response = self._generate_response(user_message, domain, confidence, topics)
            
            # Calculate response time
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Update performance metrics
            self._update_metrics(domain, confidence, response_time)
            
            # Create AICL message format
            aicl_message = self._create_aicl_message(user_message, response, domain, confidence, response_time)
            
            logger.info(f"Guardian processed query in {response_time:.2f}ms, domain: {domain}, confidence: {confidence:.2f}")
            
            return aicl_message
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return self._create_error_response(user_message, str(e))

    def _extract_topics(self, message: str) -> List[str]:
        """
        Extract key topics from user message using simple NLP techniques
        """
        # Convert to lowercase for pattern matching
        message_lower = message.lower()
        
        # Extract potential topics (words that might indicate domain)
        words = re.findall(r'\b\w+\b', message_lower)
        
        # Filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'}
        
        topics = [word for word in words if word not in stop_words and len(word) > 2]
        
        return topics[:5]  # Return top 5 topics

    def _classify_domain(self, message: str, topics: List[str]) -> Tuple[str, float]:
        """
        Classify message domain using local pattern matching (cost-efficient)
        """
        message_lower = message.lower()
        domain_scores = {}
        
        # Score each domain based on pattern matches
        for domain, patterns in self.domain_patterns.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, message_lower)
                score += len(matches) * 0.5  # Weight for pattern matches
            
            # Bonus for topic relevance
            for topic in topics:
                if topic in message_lower:
                    score += 0.3
            
            domain_scores[domain] = score
        
        # Find domain with highest score
        if domain_scores:
            best_domain = max(domain_scores.items(), key=lambda x: x[1])[0]
            max_score = domain_scores[best_domain]
            
            # Calculate confidence (normalize score)
            confidence = min(max_score / 3.0, 1.0)  # Cap at 1.0
            
            # If no clear domain, return general
            if confidence < 0.3:
                return "general", 0.5
            
            return best_domain, confidence
        
        return "general", 0.5

    def _generate_response(self, message: str, domain: str, confidence: float, topics: List[str]) -> str:
        """
        Generate response based on domain classification
        """
        if domain == "general":
            # Use general response template
            template = self.response_templates["general"][0]
            return template
        
        # Use domain-specific template
        templates = self.response_templates.get(domain, self.response_templates["general"])
        template = templates[0]  # Use first template for consistency
        
        # Extract main topic for template
        main_topic = topics[0] if topics else "your project"
        
        # Fill template
        response = template.format(topic=main_topic)
        
        # Add confidence indicator if high confidence
        if confidence > 0.7:
            response += f" (Confidence: {confidence:.1%})"
        
        return response

    def _create_aicl_message(self, user_message: str, response: str, domain: str, confidence: float, response_time: float) -> Dict:
        """
        Create AICL protocol message
        """
        message_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        return {
            "aicl_version": "1.0",
            "message_id": message_id,
            "timestamp": timestamp,
            "sender": {
                "agent_id": self.agent_id,
                "agent_type": "interface",
                "capabilities": self.capabilities
            },
            "recipient": {
                "agent_id": f"nexus_{domain}" if domain != "general" else "user",
                "agent_type": "specialist" if domain != "general" else "user",
                "domain": domain
            },
            "message_type": "response",
            "session_id": str(uuid.uuid4()),
            "context": {
                "user_message": user_message,
                "domain_classification": domain,
                "confidence_score": confidence,
                "extracted_topics": self._extract_topics(user_message),
                "processing_time_ms": response_time
            },
            "payload": {
                "response_text": response,
                "routing_decision": {
                    "target_agent": f"nexus_{domain}" if domain != "general" else None,
                    "confidence": confidence,
                    "domain": domain
                },
                "performance_metrics": {
                    "response_time_ms": response_time,
                    "processing_efficiency": "high",
                    "cost_optimization": "local_processing"
                }
            },
            "metadata": {
                "expected_response_time": "50-200ms",
                "quality_requirements": {
                    "accuracy_threshold": 0.7,
                    "response_time_threshold": 200
                },
                "fallback_agents": ["nexus_navigator", "nexus_guardian"]
            }
        }

    def _create_error_response(self, user_message: str, error: str) -> Dict:
        """
        Create error response in AICL format
        """
        return {
            "aicl_version": "1.0",
            "message_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "sender": {
                "agent_id": self.agent_id,
                "agent_type": "interface",
                "capabilities": self.capabilities
            },
            "recipient": {
                "agent_id": "user",
                "agent_type": "user",
                "domain": "error"
            },
            "message_type": "error",
            "session_id": str(uuid.uuid4()),
            "context": {
                "user_message": user_message,
                "error": error
            },
            "payload": {
                "response_text": "I apologize, but I encountered an error processing your request. Please try again.",
                "error_details": error
            },
            "metadata": {
                "error_type": "processing_error",
                "retry_recommended": True
            }
        }

    def _update_metrics(self, domain: str, confidence: float, response_time: float):
        """
        Update performance metrics
        """
        self.performance_metrics["total_queries"] += 1
        
        if confidence > 0.5:
            self.performance_metrics["successful_routes"] += 1
        
        # Update average response time
        current_avg = self.performance_metrics["average_response_time"]
        total_queries = self.performance_metrics["total_queries"]
        self.performance_metrics["average_response_time"] = (
            (current_avg * (total_queries - 1) + response_time) / total_queries
        )
        
        # Update domain accuracy
        if domain not in self.performance_metrics["domain_accuracy"]:
            self.performance_metrics["domain_accuracy"][domain] = {
                "total": 0,
                "successful": 0,
                "avg_confidence": 0
            }
        
        domain_stats = self.performance_metrics["domain_accuracy"][domain]
        domain_stats["total"] += 1
        if confidence > 0.7:
            domain_stats["successful"] += 1
        
        # Update average confidence
        current_avg_conf = domain_stats["avg_confidence"]
        domain_stats["avg_confidence"] = (
            (current_avg_conf * (domain_stats["total"] - 1) + confidence) / domain_stats["total"]
        )

    def get_performance_metrics(self) -> Dict:
        """
        Get current performance metrics
        """
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "metrics": self.performance_metrics,
            "efficiency_score": self._calculate_efficiency_score(),
            "cost_optimization": "local_processing",
            "response_time_avg_ms": self.performance_metrics["average_response_time"]
        }

    def _calculate_efficiency_score(self) -> float:
        """
        Calculate overall efficiency score
        """
        total_queries = self.performance_metrics["total_queries"]
        if total_queries == 0:
            return 0.0
        
        successful_rate = self.performance_metrics["successful_routes"] / total_queries
        avg_response_time = self.performance_metrics["average_response_time"]
        
        # Efficiency score based on success rate and response time
        # Higher score for faster responses and better success rates
        time_score = max(0, 1 - (avg_response_time / 200))  # Penalize slow responses
        efficiency_score = (successful_rate * 0.7 + time_score * 0.3) * 100
        
        return min(efficiency_score, 100.0)  # Cap at 100%

    def get_agent_info(self) -> Dict:
        """
        Get agent information for frontend
        """
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "description": "Primary interface agent for user interaction and query preprocessing",
            "capabilities": self.capabilities,
            "cost_efficiency": "high",
            "processing_method": "local_pattern_matching",
            "supported_domains": list(self.domain_patterns.keys()) + ["general"]
        } 