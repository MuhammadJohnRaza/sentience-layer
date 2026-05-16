"""
Economic Engine Service
Cost-benefit analysis, ROI calculation, and resource optimization.
Uses Antigravity for enterprise financial modeling.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import json

from backend.python.utils.logger import get_logger
from backend.python.antigravity_client import AntigravityClient

logger = get_logger(__name__)


class CostType(Enum):
    DIRECT = "direct"
    INDIRECT = "indirect"
    OPPORTUNITY = "opportunity"
    EXTERNALITY = "externality"


@dataclass
class CostItem:
    name: str
    type: CostType
    amount: float
    currency: str = "USD"
    recurring: bool = False
    probability: float = 1.0


@dataclass
class BenefitItem:
    name: str
    amount: float
    currency: str = "USD"
    probability: float = 1.0
    time_horizon_months: int = 12


@dataclass
class EconomicAnalysis:
    action_id: str
    total_cost: float
    total_benefit: float
    net_present_value: float
    roi_percentage: float
    payback_period_months: Optional[float]
    break_even_probability: float
    risk_adjusted_return: float
    cost_breakdown: List[CostItem]
    benefit_breakdown: List[BenefitItem]
    sensitivity_analysis: Dict[str, Any]


class EconomicEngineService:
    """
    Comprehensive economic modeling with Monte Carlo simulation.
    Integrates with Antigravity for market data and cost benchmarks.
    """

    def __init__(self, antigravity_client: Optional[AntigravityClient] = None):
        self.ag = antigravity_client or AntigravityClient()
        logger.info("EconomicEngineService initialized")

    async def analyze(
        self,
        action: Dict[str, Any],
        market_context: Optional[Dict[str, Any]] = None,
        num_simulations: int = 1000,
        discount_rate: float = 0.08,
    ) -> EconomicAnalysis:
        """
        Agentic economic analysis:
        1. Cost identification → 2. Benefit estimation → 3. NPV calculation →
        4. Monte Carlo simulation → 5. Sensitivity analysis → 6. Risk adjustment
        """
        market_context = market_context or {}
        
        try:
            # Step 1: Identify costs
            costs = await self._identify_costs(action, market_context)
            
            # Step 2: Estimate benefits
            benefits = await self._estimate_benefits(action, market_context)
            
            # Step 3: Calculate NPV
            npv = self._calculate_npv(costs, benefits, discount_rate)
            
            # Step 4: Monte Carlo simulation
            mc_results = self._monte_carlo_simulation(costs, benefits, num_simulations)
            
            # Step 5: Sensitivity analysis
            sensitivity = self._sensitivity_analysis(costs, benefits, discount_rate)
            
            # Step 6: Risk adjustment
            risk_adjusted = self._risk_adjustment(mc_results)
            
            total_cost = sum(c.amount * c.probability for c in costs)
            total_benefit = sum(b.amount * b.probability for b in benefits)
            
            roi = ((total_benefit - total_cost) / total_cost * 100) if total_cost > 0 else 0
            
            return EconomicAnalysis(
                action_id=action.get("id", "unknown"),
                total_cost=total_cost,
                total_benefit=total_benefit,
                net_present_value=npv,
                roi_percentage=roi,
                payback_period_months=self._calculate_payback(costs, benefits),
                break_even_probability=mc_results.get("break_even_prob", 0.5),
                risk_adjusted_return=risk_adjusted,
                cost_breakdown=costs,
                benefit_breakdown=benefits,
                sensitivity_analysis=sensitivity
            )

        except Exception as e:
            logger.error(f"Economic analysis failed: {e}")
            raise EconomicEngineError(f"Analysis failed: {e}") from e

    async def estimate_action_cost(self, action: Dict) -> float:
        """Quick cost estimate for action ranking."""
        try:
            estimate = await self.ag.finance.estimate_cost(action)
            return estimate.get("total", 0.0)
        except Exception:
            # Fallback: heuristic based on steps
            steps = action.get("steps", [])
            return len(steps) * 50.0  # $50 per step heuristic

    async def _identify_costs(
        self, action: Dict, context: Dict
    ) -> List[CostItem]:
        """Identify all cost types."""
        costs = []
        
        # Direct costs
        if "compute_cost" in action:
            costs.append(CostItem(
                name="Compute",
                type=CostType.DIRECT,
                amount=action["compute_cost"],
                probability=1.0
            ))
        
        if "human_hours" in action:
            costs.append(CostItem(
                name="Labor",
                type=CostType.DIRECT,
                amount=action["human_hours"] * 75,  # $75/hr assumption
                probability=1.0
            ))
        
        # Tool costs
        for step in action.get("steps", []):
            if step.get("tool"):
                try:
                    tool_cost = await self.ag.finance.get_tool_cost(step["tool"])
                    costs.append(CostItem(
                        name=f"Tool: {step['tool']}",
                        type=CostType.DIRECT,
                        amount=tool_cost,
                        probability=0.95
                    ))
                except Exception:
                    costs.append(CostItem(
                        name=f"Tool: {step['tool']}",
                        type=CostType.DIRECT,
                        amount=10.0,
                        probability=0.95
                    ))
        
        # Opportunity cost
        costs.append(CostItem(
            name="Opportunity Cost",
            type=CostType.OPPORTUNITY,
            amount=sum(c.amount for c in costs) * 0.1,  # 10% opportunity cost
            probability=1.0
        ))
        
        return costs

    async def _estimate_benefits(
        self, action: Dict, context: Dict
    ) -> List[BenefitItem]:
        """Estimate benefits."""
        benefits = []
        
        # Time savings
        if "time_saved_hours" in action:
            benefits.append(BenefitItem(
                name="Time Savings",
                amount=action["time_saved_hours"] * 75,
                probability=0.9
            ))
        
        # Revenue impact
        if "expected_revenue" in action:
            benefits.append(BenefitItem(
                name="Revenue Impact",
                amount=action["expected_revenue"],
                probability=0.7
            ))
        
        # Risk reduction
        if "risk_reduction_value" in action:
            benefits.append(BenefitItem(
                name="Risk Reduction",
                amount=action["risk_reduction_value"],
                probability=0.8
            ))
        
        # Default benefit if none specified
        if not benefits:
            benefits.append(BenefitItem(
                name="Operational Efficiency",
                amount=500.0,
                probability=0.8
            ))
        
        return benefits

    def _calculate_npv(
        self,
        costs: List[CostItem],
        benefits: List[BenefitItem],
        discount_rate: float
    ) -> float:
        """Calculate Net Present Value."""
        # Simplified: annualized
        total_cost = sum(c.amount for c in costs)
        annual_benefit = sum(b.amount for b in benefits) / 12  # Monthly
        
        # 5-year NPV
        npv = -total_cost
        for month in range(1, 61):
            npv += annual_benefit / ((1 + discount_rate / 12) ** month)
        
        return npv

    def _monte_carlo_simulation(
        self,
        costs: List[CostItem],
        benefits: List[BenefitItem],
        n: int
    ) -> Dict[str, Any]:
        """Run Monte Carlo for probability distribution."""
        import random
        
        outcomes = []
        for _ in range(n):
            total_cost = sum(
                c.amount if random.random() < c.probability else 0
                for c in costs
            )
            total_benefit = sum(
                b.amount if random.random() < b.probability else 0
                for b in benefits
            )
            outcomes.append(total_benefit - total_cost)
        
        outcomes.sort()
        break_even = sum(1 for o in outcomes if o > 0) / n
        
        return {
            "break_even_prob": break_even,
            "mean": sum(outcomes) / n,
            "median": outcomes[n // 2],
            "p10": outcomes[n // 10],
            "p90": outcomes[9 * n // 10]
        }

    def _sensitivity_analysis(
        self,
        costs: List[CostItem],
        benefits: List[BenefitItem],
        discount_rate: float
    ) -> Dict[str, Any]:
        """Analyze sensitivity to key variables."""
        base_npv = self._calculate_npv(costs, benefits, discount_rate)
        
        # Vary discount rate
        npv_low_rate = self._calculate_npv(costs, benefits, discount_rate * 0.5)
        npv_high_rate = self._calculate_npv(costs, benefits, discount_rate * 1.5)
        
        # Vary benefits
        high_benefits = [BenefitItem(**{**b.__dict__, "amount": b.amount * 1.5}) for b in benefits]
        low_benefits = [BenefitItem(**{**b.__dict__, "amount": b.amount * 0.5}) for b in benefits]
        
        return {
            "base_npv": base_npv,
            "discount_rate_sensitivity": {
                "low": npv_low_rate,
                "high": npv_high_rate
            },
            "benefit_sensitivity": {
                "optimistic": self._calculate_npv(costs, high_benefits, discount_rate),
                "pessimistic": self._calculate_npv(costs, low_benefits, discount_rate)
            }
        }

    def _risk_adjustment(self, mc_results: Dict) -> float:
        """Calculate risk-adjusted return."""
        mean = mc_results.get("mean", 0)
        p10 = mc_results.get("p10", 0)
        # Risk-adjusted = mean - 0.5 * downside risk
        downside = max(0, mean - p10)
        return mean - 0.5 * downside

    def _calculate_payback(
        self,
        costs: List[CostItem],
        benefits: List[BenefitItem]
    ) -> Optional[float]:
        """Calculate payback period in months."""
        total_cost = sum(c.amount for c in costs)
        monthly_benefit = sum(b.amount for b in benefits) / 12
        
        if monthly_benefit <= 0:
            return None
        
        return total_cost / monthly_benefit


class EconomicEngineError(Exception):
    pass