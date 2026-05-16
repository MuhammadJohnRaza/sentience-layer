import json
import uuid
import math
import random
from typing import Any, Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict, deque


@dataclass
class MarketSegment:
    id: str
    name: str
    size: float
    growth_rate: float
    price_sensitivity: float
    brand_loyalty: float
    demographics: Dict[str, Any]
    needs: List[str]
    willingness_to_pay: Tuple[float, float]


@dataclass
class CompetitorPosition:
    competitor_id: str
    name: str
    market_share: float
    price_point: float
    quality_perception: float
    innovation_score: float
    customer_satisfaction: float
    distribution_strength: float


@dataclass
class DemandForecast:
    period: str
    predicted_demand: float
    confidence_interval: Tuple[float, float]
    seasonality_factor: float
    trend_direction: str


class MarketModel:
    def __init__(self, embedding_engine=None, temporal_simulator=None):
        self.embedding_engine = embedding_engine
        self.temporal_simulator = temporal_simulator
        self.segments: Dict[str, MarketSegment] = {}
        self.competitors: Dict[str, CompetitorPosition] = {}
        self.demand_history: deque = deque(maxlen=1000)
        self.price_elasticities: Dict[str, float] = {}
        self.cross_elasticities: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.network_effects: Dict[str, float] = {}
        self.switching_costs: Dict[str, float] = {}
        self.scenarios: Dict[str, Dict[str, Any]] = {}
        self.forecasts: Dict[str, List[DemandForecast]] = {}

    def add_segment(
        self,
        name: str,
        size: float,
        growth_rate: float = 0.05,
        price_sensitivity: float = 0.5,
        brand_loyalty: float = 0.3,
        demographics: Optional[Dict[str, Any]] = None,
        needs: Optional[List[str]] = None,
        min_wtp: float = 10.0,
        max_wtp: float = 1000.0,
    ) -> str:
        segment_id = str(uuid.uuid4())
        segment = MarketSegment(
            id=segment_id,
            name=name,
            size=size,
            growth_rate=growth_rate,
            price_sensitivity=price_sensitivity,
            brand_loyalty=brand_loyalty,
            demographics=demographics or {},
            needs=needs or [],
            willingness_to_pay=(min_wtp, max_wtp),
        )
        self.segments[segment_id] = segment
        return segment_id

    def add_competitor(
        self,
        name: str,
        market_share: float,
        price_point: float,
        quality_perception: float = 0.5,
        innovation_score: float = 0.5,
        customer_satisfaction: float = 0.5,
        distribution_strength: float = 0.5,
    ) -> str:
        competitor_id = str(uuid.uuid4())
        competitor = CompetitorPosition(
            competitor_id=competitor_id,
            name=name,
            market_share=market_share,
            price_point=price_point,
            quality_perception=quality_perception,
            innovation_score=innovation_score,
            customer_satisfaction=customer_satisfaction,
            distribution_strength=distribution_strength,
        )
        self.competitors[competitor_id] = competitor
        return competitor_id

    def set_price_elasticity(self, segment_id: str, elasticity: float) -> None:
        self.price_elasticities[segment_id] = elasticity

    def set_cross_elasticity(
        self,
        product_a: str,
        product_b: str,
        elasticity: float,
    ) -> None:
        self.cross_elasticities[product_a][product_b] = elasticity

    def calculate_demand(
        self,
        segment_id: str,
        price: float,
        marketing_spend: float = 0.0,
        competitor_prices: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        if segment_id not in self.segments:
            raise ValueError(f"Segment {segment_id} not found")

        segment = self.segments[segment_id]
        base_demand = segment.size

        price_elasticity = self.price_elasticities.get(segment_id, -1.5)
        reference_price = segment.willingness_to_pay[1] * 0.5
        price_ratio = price / reference_price
        price_effect = math.pow(price_ratio, price_elasticity)

        marketing_effect = 1 + math.log1p(marketing_spend / segment.size) * 0.1

        competitor_effect = 1.0
        if competitor_prices:
            for comp_id, comp_price in competitor_prices.items():
                cross_elasticity = self.cross_elasticities.get("self", {}).get(comp_id, 0.5)
                competitor_effect += cross_elasticity * (comp_price / price - 1)

        demand = base_demand * price_effect * marketing_effect * competitor_effect

        return {
            "predicted_demand": demand,
            "price_effect": price_effect,
            "marketing_effect": marketing_effect,
            "competitor_effect": competitor_effect,
            "revenue": demand * price,
        }

    def forecast_demand(
        self,
        segment_id: str,
        periods: int = 12,
        period_type: str = "month",
    ) -> List[DemandForecast]:
        if segment_id not in self.segments:
            raise ValueError(f"Segment {segment_id} not found")

        segment = self.segments[segment_id]
        forecasts = []
        base_demand = segment.size

        for i in range(periods):
            trend = math.pow(1 + segment.growth_rate, i / 12)
            seasonality = 1 + 0.1 * math.sin(2 * math.pi * i / 12)
            noise = random.gauss(0, 0.02)

            predicted = base_demand * trend * seasonality * (1 + noise)
            std_dev = predicted * 0.05

            forecast = DemandForecast(
                period=f"{period_type}_{i+1}",
                predicted_demand=predicted,
                confidence_interval=(predicted - 1.96 * std_dev, predicted + 1.96 * std_dev),
                seasonality_factor=seasonality,
                trend_direction="up" if segment.growth_rate > 0 else "down",
            )
            forecasts.append(forecast)

        self.forecasts[segment_id] = forecasts
        return forecasts

    def simulate_price_war(
        self,
        competitor_id: str,
        price_cut_percentage: float,
        segments: Optional[List[str]] = None,
        rounds: int = 5,
    ) -> List[Dict[str, Any]]:
        if competitor_id not in self.competitors:
            raise ValueError(f"Competitor {competitor_id} not found")

        competitor = self.competitors[competitor_id]
        target_segments = segments or list(self.segments.keys())
        results = []

        for round_num in range(rounds):
            new_price = competitor.price_point * (1 - price_cut_percentage / 100)

            market_shifts = {}
            for seg_id in target_segments:
                if seg_id not in self.segments:
                    continue

                segment = self.segments[seg_id]
                elasticity = self.price_elasticities.get(seg_id, -1.5)

                demand_change = elasticity * (price_cut_percentage / 100)
                share_change = demand_change * (1 - segment.brand_loyalty)

                market_shifts[seg_id] = {
                    "demand_change_pct": demand_change * 100,
                    "share_change_pct": share_change * 100,
                    "revenue_impact": (1 + demand_change) * new_price - competitor.price_point,
                }

            competitor.price_point = new_price
            competitor.market_share = min(
                competitor.market_share * (1 + sum(s["share_change_pct"] for s in market_shifts.values()) / len(market_shifts) / 100),
                1.0,
            )

            results.append({
                "round": round_num + 1,
                "price": new_price,
                "market_share": competitor.market_share,
                "segment_impacts": market_shifts,
            })

            price_cut_percentage *= 0.8

        return results

    def calculate_market_equilibrium(
        self,
        segment_id: str,
        cost_structure: Dict[str, float],
    ) -> Dict[str, Any]:
        if segment_id not in self.segments:
            raise ValueError(f"Segment {segment_id} not found")

        segment = self.segments[segment_id]
        marginal_cost = cost_structure.get("marginal_cost", 50)
        fixed_cost = cost_structure.get("fixed_cost", 10000)

        elasticity = abs(self.price_elasticities.get(segment_id, -1.5))
        optimal_price = marginal_cost * (elasticity / (elasticity - 1)) if elasticity > 1 else marginal_cost * 2

        demand_result = self.calculate_demand(segment_id, optimal_price)
        quantity = demand_result["predicted_demand"]

        profit = (optimal_price - marginal_cost) * quantity - fixed_cost

        return {
            "optimal_price": optimal_price,
            "optimal_quantity": quantity,
            "max_profit": profit,
            "consumer_surplus": 0.5 * (segment.willingness_to_pay[1] - optimal_price) * quantity,
            "producer_surplus": profit,
            "deadweight_loss": 0,
        }

    def network_effect_model(
        self,
        segment_id: str,
        current_users: int,
        virality_coefficient: float,
        churn_rate: float,
        periods: int = 12,
    ) -> List[Dict[str, Any]]:
        users = [current_users]
        results = []

        for period in range(periods):
            current = users[-1]
            new_users = current * virality_coefficient
            churned = current * churn_rate
            next_users = current + new_users - churned

            network_value = next_users * math.log1p(next_users) if next_users > 0 else 0

            results.append({
                "period": period + 1,
                "users": int(next_users),
                "new_users": int(new_users),
                "churned": int(churned),
                "network_value": network_value,
                "virality": virality_coefficient,
            })

            users.append(next_users)
            virality_coefficient *= 0.95

        return results

    def game_theory_payoff(
        self,
        player_a_strategies: List[str],
        player_b_strategies: List[str],
        payoff_matrix: Dict[Tuple[str, str], Tuple[float, float]],
    ) -> Dict[str, Any]:
        nash_equilibria = []
        dominated_strategies_a = set()
        dominated_strategies_b = set()

        for strat_a in player_a_strategies:
            for strat_b in player_b_strategies:
                payoff_a, payoff_b = payoff_matrix.get((strat_a, strat_b), (0, 0))

                is_nash = True
                for other_a in player_a_strategies:
                    if other_a != strat_a:
                        other_payoff, _ = payoff_matrix.get((other_a, strat_b), (0, 0))
                        if other_payoff > payoff_a:
                            is_nash = False
                            break

                if is_nash:
                    for other_b in player_b_strategies:
                        if other_b != strat_b:
                            _, other_payoff = payoff_matrix.get((strat_a, other_b), (0, 0))
                            if other_payoff > payoff_b:
                                is_nash = False
                                break

                if is_nash:
                    nash_equilibria.append({
                        "strategy_a": strat_a,
                        "strategy_b": strat_b,
                        "payoff_a": payoff_a,
                        "payoff_b": payoff_b,
                    })

        return {
            "nash_equilibria": nash_equilibria,
            "dominated_strategies_a": list(dominated_strategies_a),
            "dominated_strategies_b": list(dominated_strategies_b),
            "payoff_matrix": {f"{k[0]}_{k[1]}": v for k, v in payoff_matrix.items()},
        }

    def scenario_planning(
        self,
        name: str,
        assumptions: Dict[str, Any],
        variables: Dict[str, List[float]],
    ) -> Dict[str, Any]:
        scenarios = []
        base_case = {}

        for var_name, values in variables.items():
            base_case[var_name] = sum(values) / len(values)

        optimistic = {k: max(v) for k, v in variables.items()}
        pessimistic = {k: min(v) for k, v in variables.items()}

        for scenario_name, params in [("base", base_case), ("optimistic", optimistic), ("pessimistic", pessimistic)]:
            combined = {**assumptions, **params}
            scenarios.append({
                "name": scenario_name,
                "parameters": params,
                "projected_outcome": self._project_outcome(combined),
            })

        self.scenarios[name] = {
            "assumptions": assumptions,
            "variables": variables,
            "scenarios": scenarios,
        }

        return {
            "scenario_name": name,
            "scenarios": scenarios,
        }

    def _project_outcome(self, params: Dict[str, Any]) -> Dict[str, float]:
        market_size = params.get("market_size", 1000000)
        growth_rate = params.get("growth_rate", 0.05)
        market_share = params.get("market_share", 0.1)
        price = params.get("price", 100)
        margin = params.get("margin", 0.3)

        revenue = market_size * market_share * price
        profit = revenue * margin

        return {
            "revenue": revenue,
            "profit": profit,
            "market_cap": profit * 20,
            "roi": (profit / max(revenue * (1 - margin), 1)) * 100,
        }

    def customer_lifetime_value(
        self,
        acquisition_cost: float,
        annual_revenue: float,
        annual_cost: float,
        discount_rate: float,
        years: int = 5,
        retention_rates: Optional[List[float]] = None,
    ) -> Dict[str, Any]:
        if retention_rates is None:
            retention_rates = [0.9, 0.85, 0.8, 0.75, 0.7]

        clv = -acquisition_cost
        yearly_values = []

        for year in range(years):
            retention = retention_rates[min(year, len(retention_rates) - 1)]
            profit = (annual_revenue - annual_cost) * math.pow(retention, year + 1)
            discounted_profit = profit / math.pow(1 + discount_rate, year + 1)
            clv += discounted_profit

            yearly_values.append({
                "year": year + 1,
                "retention_rate": retention,
                "gross_profit": profit,
                "discounted_profit": discounted_profit,
            })

        return {
            "clv": clv,
            "payback_period": next(
                (y["year"] for y in yearly_values if sum(v["discounted_profit"] for v in yearly_values[:y["year"]]) >= acquisition_cost),
                years,
            ),
            "yearly_breakdown": yearly_values,
            "ltv_cac_ratio": clv / max(acquisition_cost, 1),
        }

    def market_concentration(self) -> Dict[str, float]:
        shares = [c.market_share for c in self.competitors.values()]
        total_share = sum(shares)

        if total_share == 0:
            return {"hhi": 0, "cr4": 0}

        normalized_shares = [s / total_share for s in shares]
        hhi = sum(s ** 2 for s in normalized_shares) * 10000

        sorted_shares = sorted(normalized_shares, reverse=True)
        cr4 = sum(sorted_shares[:4]) * 100

        return {
            "hhi": hhi,
            "cr4": cr4,
            "concentration_level": "high" if hhi > 2500 else "moderate" if hhi > 1500 else "low",
        }

    def diffusion_of_innovation(
        self,
        segment_id: str,
        innovation_type: str = "continuous",
        p: float = 0.03,
        q: float = 0.38,
        periods: int = 20,
    ) -> List[Dict[str, Any]]:
        if segment_id not in self.segments:
            raise ValueError(f"Segment {segment_id} not found")

        market_size = self.segments[segment_id].size
        adopters = [0]
        results = []

        for t in range(1, periods + 1):
            if innovation_type == "continuous":
                new_adopters = (p + q * adopters[-1] / market_size) * (market_size - adopters[-1])
            else:
                new_adopters = p * market_size if t == 1 else q * adopters[-1]

            total = min(adopters[-1] + new_adopters, market_size)
            adopters.append(total)

            results.append({
                "period": t,
                "cumulative_adopters": total,
                "new_adopters": new_adopters,
                "adoption_rate": total / market_size,
            })

        return results

    def get_market_summary(self) -> Dict[str, Any]:
        total_market_size = sum(s.size for s in self.segments.values())
        total_competitor_share = sum(c.market_share for c in self.competitors.values())

        return {
            "total_segments": len(self.segments),
            "total_competitors": len(self.competitors),
            "total_addressable_market": total_market_size,
            "market_concentration": self.market_concentration(),
            "segment_breakdown": [
                {
                    "name": s.name,
                    "size": s.size,
                    "growth_rate": s.growth_rate,
                }
                for s in self.segments.values()
            ],
            "competitive_landscape": [
                {
                    "name": c.name,
                    "market_share": c.market_share,
                    "price_point": c.price_point,
                }
                for c in self.competitors.values()
            ],
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "segments": len(self.segments),
            "competitors": len(self.competitors),
            "forecasts": {k: len(v) for k, v in self.forecasts.items()},
            "scenarios": list(self.scenarios.keys()),
            "market_summary": self.get_market_summary(),
        }