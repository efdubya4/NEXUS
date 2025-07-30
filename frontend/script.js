// NEXUS AI Frontend JavaScript

class NexusAI {
    constructor() {
        this.currentAgent = 'guardian';
        this.apiBaseUrl = 'http://localhost:5001/api/nexus';
        this.agents = {
            guardian: { name: 'NEXUS Guardian', icon: '🛡️', description: 'Primary interface agent for user interaction and query preprocessing' },
            navigator: { name: 'NEXUS Navigator', icon: '🧭', description: 'Query routing and orchestration specialist' },
            builder: { name: 'NEXUS Builder', icon: '🏗️', description: 'Construction and DIY project specialist' },
            coder: { name: 'NEXUS Coder', icon: '💻', description: 'Programming and software development specialist' },
            gardener: { name: 'NEXUS Gardener', icon: '🌱', description: 'Horticulture and gardening specialist' },
            teacher: { name: 'NEXUS Teacher', icon: '📚', description: 'Education and learning specialist' },
            chef: { name: 'NEXUS Chef', icon: '👨‍🍳', description: 'Culinary arts and cooking specialist' },
            monitor: { name: 'NEXUS Monitor', icon: '📊', description: 'Performance tracking and analytics' },
            learner: { name: 'NEXUS Learner', icon: '🧠', description: 'Continuous improvement and adaptation' }
        };
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupAutoResize();
        this.updateAgentInfo();
        this.checkBackendStatus();
    }

    async checkBackendStatus() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/status`);
            if (response.ok) {
                const data = await response.json();
                console.log('Backend status:', data);
                this.updateSystemStatus('online');
            } else {
                this.updateSystemStatus('offline');
            }
        } catch (error) {
            console.log('Backend not available, using simulated responses');
            this.updateSystemStatus('offline');
        }
    }

    updateSystemStatus(status) {
        const statusIndicator = document.querySelector('.status-indicator');
        const statusText = document.querySelector('.status-text');
        
        if (status === 'online') {
            statusIndicator.className = 'status-indicator online';
            statusText.textContent = 'System Online';
        } else {
            statusIndicator.className = 'status-indicator offline';
            statusText.textContent = 'System Offline (Simulated)';
        }
    }

    bindEvents() {
        // Send button click
        const sendButton = document.getElementById('sendButton');
        const messageInput = document.getElementById('messageInput');
        
        sendButton.addEventListener('click', () => this.sendMessage());
        
        // Enter key handling
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Agent navigation
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', () => {
                const agentId = item.dataset.agent;
                this.switchAgent(agentId);
            });
        });

        // Auto-resize textarea
        messageInput.addEventListener('input', () => {
            this.autoResizeTextarea(messageInput);
        });
    }

    setupAutoResize() {
        const textarea = document.getElementById('messageInput');
        this.autoResizeTextarea(textarea);
    }

    autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    switchAgent(agentId) {
        // Update navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-agent="${agentId}"]`).classList.add('active');

        // Update current agent
        this.currentAgent = agentId;
        const agent = this.agents[agentId];

        // Update header
        document.querySelector('.page-title').textContent = agent.name;
        document.querySelector('.page-subtitle').textContent = agent.description;

        // Update agent indicator
        document.querySelector('.indicator-value').textContent = agent.name;

        // Update agent details sidebar
        this.updateAgentInfo();

        // Add system message about agent switch
        this.addSystemMessage(`${agent.name} is now active. How can I help you?`);
    }

    updateAgentInfo() {
        const agent = this.agents[this.currentAgent];
        
        // Update agent card
        const agentIcon = document.querySelector('.agent-card .agent-icon');
        const agentName = document.querySelector('.agent-card .agent-name');
        const agentDescription = document.querySelector('.agent-card .agent-description');
        
        agentIcon.textContent = agent.icon;
        agentName.textContent = agent.name;
        agentDescription.textContent = agent.description;

        // Update metrics (simulate different performance for different agents)
        this.updateMetrics();
    }

    updateMetrics() {
        const metrics = document.querySelectorAll('.metric-value');
        const responseTime = Math.floor(Math.random() * 100) + 20;
        const accuracy = (Math.random() * 10 + 85).toFixed(1);
        const efficiency = (Math.random() * 10 + 80).toFixed(1);

        metrics[0].textContent = `${responseTime}ms`;
        metrics[1].textContent = `${accuracy}%`;
        metrics[2].textContent = `${efficiency}%`;
    }

    async sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();
        
        if (!message) return;

        // Add user message
        this.addUserMessage(message);
        
        // Clear input
        messageInput.value = '';
        this.autoResizeTextarea(messageInput);

        // Process message through backend or simulate response
        await this.processMessage(message);
    }

    async processMessage(message) {
        try {
            // Try to use backend API
            const response = await fetch(`${this.apiBaseUrl}/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    context: {
                        current_agent: this.currentAgent
                    }
                })
            });

            if (response.ok) {
                const data = await response.json();
                this.handleBackendResponse(data, message);
            } else {
                // Fallback to simulated response
                this.simulateAIResponse(message);
            }
        } catch (error) {
            console.log('Backend not available, using simulated response');
            this.simulateAIResponse(message);
        }
    }

    handleBackendResponse(data, originalMessage) {
        const response = data.response;
        const routing = data.routing;
        const metrics = data.metrics;
        
        let routingInfo = null;
        if (routing && routing.domain !== 'general') {
            routingInfo = `Routed to NEXUS ${routing.domain.charAt(0).toUpperCase() + routing.domain.slice(1)}`;
        }
        
        const responseTime = metrics ? metrics.response_time_ms : Math.floor(Math.random() * 200) + 50;
        
        setTimeout(() => {
            this.addSystemMessage(response, routingInfo, responseTime);
            this.updateMetrics();
        }, 500);
    }

    addUserMessage(message) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-header">
                    <span class="agent-name">You</span>
                    <span class="message-time">${time}</span>
                </div>
                <div class="message-text">${this.escapeHtml(message)}</div>
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    addSystemMessage(message, routingInfo = null, responseTime = null) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message system-message';
        
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const agent = this.agents[this.currentAgent];
        
        let metaHtml = '';
        if (routingInfo || responseTime) {
            metaHtml = `
                <div class="message-meta">
                    ${routingInfo ? `<span class="routing-info">Routing: ${routingInfo}</span>` : ''}
                    ${responseTime ? `<span class="response-time">Response: ${responseTime}ms</span>` : ''}
                </div>
            `;
        }
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-header">
                    <span class="agent-name">${agent.name}</span>
                    <span class="message-time">${time}</span>
                </div>
                <div class="message-text">${this.escapeHtml(message)}</div>
                ${metaHtml}
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    simulateAIResponse(userMessage) {
        const agent = this.agents[this.currentAgent];
        let response = '';
        let routingInfo = null;
        const responseTime = Math.floor(Math.random() * 200) + 50;

        // Simulate different responses based on agent and message content
        if (this.currentAgent === 'guardian') {
            // Guardian routes to appropriate specialist
            if (userMessage.toLowerCase().includes('build') || userMessage.toLowerCase().includes('construction')) {
                routingInfo = 'Routed to NEXUS Builder';
                response = 'I\'ve routed your construction query to NEXUS Builder, our construction specialist. They\'ll provide you with detailed guidance on your project.';
            } else if (userMessage.toLowerCase().includes('code') || userMessage.toLowerCase().includes('programming')) {
                routingInfo = 'Routed to NEXUS Coder';
                response = 'I\'ve routed your programming query to NEXUS Coder, our software development specialist. They\'ll help you with your coding needs.';
            } else if (userMessage.toLowerCase().includes('garden') || userMessage.toLowerCase().includes('plant')) {
                routingInfo = 'Routed to NEXUS Gardener';
                response = 'I\'ve routed your gardening query to NEXUS Gardener, our horticulture specialist. They\'ll provide expert gardening advice.';
            } else {
                response = 'I understand your query. Let me help you with that. How can I assist you further?';
            }
        } else if (this.currentAgent === 'builder') {
            response = 'As your construction specialist, I can help you with building projects, DIY tasks, and construction planning. What specific project are you working on?';
        } else if (this.currentAgent === 'coder') {
            response = 'As your programming specialist, I can help you with code development, debugging, and software architecture. What programming challenge are you facing?';
        } else if (this.currentAgent === 'gardener') {
            response = 'As your gardening specialist, I can help you with plant care, garden design, and horticultural advice. What gardening question do you have?';
        } else {
            response = `As ${agent.name}, I'm here to help you with your specialized needs. How can I assist you today?`;
        }

        // Simulate typing delay
        setTimeout(() => {
            this.addSystemMessage(response, routingInfo, responseTime);
            this.updateMetrics();
        }, 1000);
    }

    scrollToBottom() {
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize NEXUS AI when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.nexusAI = new NexusAI();
});

// Add some interactive features
document.addEventListener('DOMContentLoaded', () => {
    // Add hover effects for better UX
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            if (!item.classList.contains('active')) {
                item.style.backgroundColor = '#f0f0f0';
            }
        });
        
        item.addEventListener('mouseleave', () => {
            if (!item.classList.contains('active')) {
                item.style.backgroundColor = '';
            }
        });
    });

    // Add loading state to send button
    const sendButton = document.getElementById('sendButton');
    const originalButtonContent = sendButton.innerHTML;
    
    // Simulate loading state when sending
    window.nexusAI.originalSendMessage = window.nexusAI.sendMessage;
    window.nexusAI.sendMessage = function() {
        sendButton.innerHTML = '<div class="loading-spinner"></div>';
        sendButton.disabled = true;
        
        setTimeout(() => {
            sendButton.innerHTML = originalButtonContent;
            sendButton.disabled = false;
        }, 1500);
        
        this.originalSendMessage();
    };
}); 