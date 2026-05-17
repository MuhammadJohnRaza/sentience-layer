/** * Global Types
for Sentience Layer v4.0 */
export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  preferences: UserPreferences;
}
export interface UserPreferences {
  communicationStyle: "concise" | "detailed" | "technical" | "casual";
  theme: "light" | "dark" | "system";
  notifications: boolean;
}
export interface Message {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: string;
  metadata?: {
    intent?: string;
    confidence?: number;
    sources?: string[];
    actions?: Action[];
  };
}
export interface Action {
  id: string;
  title: string;
  description: string;
  status: "pending" | "running" | "completed" | "failed" | "rolled_back";
  steps: ActionStep[];
  confidence: number;
  impactScore: number;
  createdAt: string;
}
export interface ActionStep {
  id: string;
  description: string;
  tool?: string;
  status: "pending" | "running" | "completed" | "failed";
  output?: string;
  error?: string;
  durationMs?: number;
}
export interface Insight {
  id: string;
  type: "pattern" | "anomaly" | "prediction" | "recommendation" | "risk";
  title: string;
  description: string;
  confidence: number;
  severity: "low" | "medium" | "high" | "critical";
  evidence: Evidence[];
  createdAt: string;
}
export interface Evidence {
  source: string;
  excerpt: string;
  confidence: number;
}
export interface AgentTrace {
  id: string;
  agentName: string;
  agentType: string;
  status: "idle" | "running" | "success" | "error";
  startTime: string;
  endTime?: string;
  reasoning: ReasoningStep[];
  decision: Decision;
  metadata?: Record<string, any>;
}
export interface ReasoningStep {
  step: number;
  thought: string;
  action: string;
  observation: string;
  confidence: number;
}
export interface Decision {
  chosen: string;
  alternatives: string[];
  confidence: number;
  framework: string;
}
export interface SimulationResult {
  id: string;
  actionId: string;
  successProbability: number;
  expectedValue: number;
  worstCase: string;
  bestCase: string;
  stepOutcomes: StepOutcome[];
  downstreamEffects: DownstreamEffect[];
}
export interface StepOutcome {
  stepId: string;
  status: string;
  stateDiff: Record<string, any>;
}
export interface DownstreamEffect {
  hop: number;
  description: string;
  probability: number;
}
export interface MemoryNode {
  id: string;
  content: string;
  type: "episodic" | "semantic" | "procedural";
  timestamp: string;
  connections: string[];
  strength: number;
}
export interface DreamReport {
  id: string;
  insightsDiscovered: string[];
  schemasCreated: string[];
  timestamp: string;
}
export interface Premonition {
  id: string;
  eventType: string;
  description: string;
  predictedTime: string;
  confidence: number;
  severity: string;
  indicators: any[];
  recommendedActions: string[];
}
export interface CausalNode {
  id: string;
  label: string;
  type: string;
  x?: number;
  y?: number;
}
export interface CausalEdge {
  source: string;
  target: string;
  effectSize: number;
  confidence: number;
}
export interface EconomicAnalysis {
  actionId: string;
  totalCost: number;
  totalBenefit: number;
  netPresentValue: number;
  roiPercentage: number;
  paybackPeriodMonths?: number;
  riskAdjustedReturn: number;
}
export interface DashboardMetric {
  label: string;
  value: number | string;
  change: number;
  trend: "up" | "down" | "neutral";
  icon: string;
}
export interface WebSocketMessage {
  type: "agent_update" | "insight" | "action_status" | "system" | "chat";
  payload: any;
  timestamp: string;
}
