/**
 * LLM-Powered Routing Service
 * Uses Google Antigravity / OpenRouter to intelligently route user queries
 * to the appropriate screen and orchestrate agent swarms
 */

import APIService from './api';

class LLMRoutingService {
  constructor() {
    this.routeCache = new Map();
  }

  /**
   * Analyze user input and determine the best route/action
   */
  async analyzeIntent(userInput, currentContext = {}) {
    try {
      // Check cache first
      const cacheKey = `${userInput}-${JSON.stringify(currentContext)}`;
      if (this.routeCache.has(cacheKey)) {
        return this.routeCache.get(cacheKey);
      }

      // Call backend for LLM-powered intent analysis
      const result = await APIService.processQuery(userInput, {
        ...currentContext,
        intent_analysis_only: true,
      });

      if (result.success && result.data) {
        const intent = this.extractIntent(result.data);
        this.routeCache.set(cacheKey, intent);
        return intent;
      }

      // Fallback to rule-based routing
      return this.fallbackRouting(userInput);
    } catch (error) {
      console.error('Intent analysis failed:', error);
      return this.fallbackRouting(userInput);
    }
  }

  /**
   * Extract structured intent from LLM response
   */
  extractIntent(data) {
    const understanding = data.understanding || {};
    const insights = data.insights || [];
    const actions = data.suggested_actions || [];

    // Determine primary intent
    let primaryIntent = 'analyze';
    if (understanding.intent) {
      const intent = understanding.intent.toLowerCase();
      if (intent.includes('simulate') || intent.includes('test')) {
        primaryIntent = 'simulate';
      } else if (intent.includes('execute') || intent.includes('run')) {
        primaryIntent = 'execute';
      } else if (intent.includes('analyze') || intent.includes('understand')) {
        primaryIntent = 'analyze';
      } else if (intent.includes('chat') || intent.includes('discuss')) {
        primaryIntent = 'chat';
      } else if (intent.includes('dashboard') || intent.includes('overview')) {
        primaryIntent = 'dashboard';
      }
    }

    // Determine target screen
    let targetScreen = 'Results';
    if (primaryIntent === 'simulate' && actions.length > 0) {
      targetScreen = 'Simulation';
    } else if (primaryIntent === 'chat') {
      targetScreen = 'Chat';
    } else if (primaryIntent === 'dashboard') {
      targetScreen = 'Dashboard';
    } else if (primaryIntent === 'execute') {
      targetScreen = 'Simulation';
    }

    // Determine required agents
    const requiredAgents = this.determineRequiredAgents(understanding, insights);

    return {
      primaryIntent,
      targetScreen,
      requiredAgents,
      confidence: understanding.confidence || 0.7,
      urgency: understanding.urgency_score || 0.5,
      suggestedActions: actions.slice(0, 3),
      insights: insights.slice(0, 5),
      fullData: data,
    };
  }

  /**
   * Determine which agents should be involved
   */
  determineRequiredAgents(understanding, insights) {
    const agents = new Set(['cognitive_kernel']); // Always include base agent

    // Add agents based on content
    if (understanding.urgency_score > 0.7) {
      agents.add('premonition_agent');
      agents.add('uncertainty_agent');
    }

    // Add agents based on insights
    insights.forEach(insight => {
      if (insight.type === 'pattern') {
        agents.add('causal_inference_agent');
      } else if (insight.type === 'anomaly') {
        agents.add('adversarial_test_agent');
      } else if (insight.type === 'prediction') {
        agents.add('premonition_agent');
      } else if (insight.type === 'risk') {
        agents.add('ethics_agent');
        agents.add('uncertainty_agent');
      }
    });

    // Add economic agent if financial terms detected
    const text = JSON.stringify(understanding).toLowerCase();
    if (text.includes('cost') || text.includes('revenue') || text.includes('price')) {
      agents.add('economic_agent');
    }

    return Array.from(agents);
  }

  /**
   * Fallback rule-based routing when LLM is unavailable
   */
  fallbackRouting(userInput) {
    const input = userInput.toLowerCase();

    // Keyword-based routing
    if (input.includes('simulate') || input.includes('test') || input.includes('what if')) {
      return {
        primaryIntent: 'simulate',
        targetScreen: 'Simulation',
        requiredAgents: ['cognitive_kernel', 'causal_inference_agent'],
        confidence: 0.6,
        urgency: 0.5,
        suggestedActions: [],
        insights: [],
      };
    }

    if (input.includes('chat') || input.includes('talk') || input.includes('discuss')) {
      return {
        primaryIntent: 'chat',
        targetScreen: 'Chat',
        requiredAgents: ['cognitive_kernel'],
        confidence: 0.7,
        urgency: 0.3,
        suggestedActions: [],
        insights: [],
      };
    }

    if (input.includes('dashboard') || input.includes('overview') || input.includes('status')) {
      return {
        primaryIntent: 'dashboard',
        targetScreen: 'Dashboard',
        requiredAgents: ['cognitive_kernel'],
        confidence: 0.8,
        urgency: 0.2,
        suggestedActions: [],
        insights: [],
      };
    }

    // Default to analysis
    return {
      primaryIntent: 'analyze',
      targetScreen: 'Results',
      requiredAgents: ['cognitive_kernel', 'causal_inference_agent'],
      confidence: 0.5,
      urgency: 0.5,
      suggestedActions: [],
      insights: [],
    };
  }

  /**
   * Orchestrate agent swarm based on intent
   */
  async orchestrateSwarm(intent, userInput) {
    const { requiredAgents, urgency } = intent;

    // Determine execution strategy
    const strategy = urgency > 0.7 ? 'parallel' : 'sequential';

    return {
      agents: requiredAgents,
      strategy,
      priority: urgency > 0.7 ? 'high' : 'normal',
      estimatedTime: requiredAgents.length * (strategy === 'parallel' ? 2 : 5),
    };
  }

  /**
   * Smart navigation with context preservation
   */
  async navigateWithContext(navigation, userInput, currentScreen) {
    try {
      const intent = await this.analyzeIntent(userInput, {
        current_screen: currentScreen,
      });

      // Navigate to target screen with full context
      if (intent.fullData) {
        navigation.navigate(intent.targetScreen, {
          data: intent.fullData,
          intent: intent.primaryIntent,
          agents: intent.requiredAgents,
        });
      } else {
        navigation.navigate(intent.targetScreen);
      }

      return intent;
    } catch (error) {
      console.error('Navigation failed:', error);
      return null;
    }
  }

  /**
   * Clear routing cache
   */
  clearCache() {
    this.routeCache.clear();
  }
}

export default new LLMRoutingService();
