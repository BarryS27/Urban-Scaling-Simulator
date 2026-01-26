import math
import random

class CityEngine:
    """
    A quantitative simulation engine that models urban socio-economic evolution.
    Integrates urban scaling laws, logistic population growth, and endogenous 
    growth theories to simulate wealth distribution and migration.
    """
    def __init__(self, name, config=None):
        # Basic identification and state variables
        self.name = name
        default_config = {
            "intellect": 4.5,
            "population": 1000,
            "wealth": 50.0,
            "cost": 10.0
        }
        if config:
            default_config.update(config)
        
        self.intellect = default_config["intellect"]            # Total Factor Productivity (TFP)
        self.year = 0

        # System Constants
        self.beta = 1.15                                        # Super-linear scaling exponent for urban output
        self.land_capacity = 10000                              # Carrying capacity (K) of the environment
        self.base_growth = 0.008                                # Intrinsic growth rate (r)
        self.corruption = 0.05                                  # Friction coefficient in economic yield (Reserved for expansion)
        self.cost = default_config["cost"]                      # Per capita annual survival cost

        # Population initialization: 1000 individuals with 50.0 units of wealth each
        self.wealth_dist = [default_config["wealth"]] * default_config["population"]
        self.gini_data = []                                     # Historical tracking of Gini Coefficient
        self.population_data = []                               # Historical tracking of population size

        # Migration-related institutional parameters
        self.eta_base = 0.02                                    # Baseline migration sensitivity
        self.infrastructure = 0.6                               # Transport / infrastructure index [0,1]
        self.policy_barrier = 0.4                               # Institutional friction (e.g. hukou, visas)
        self.info_flow = 0.7                                    # Information transparency [0,1]
        
        # Elasticities
        self.alpha_I = 1.0
        self.alpha_P = 1.5
        self.alpha_F = 0.8
    
    @property
    def population(self):
        """Returns the current number of individuals in the system."""
        return len(self.wealth_dist)

    # Get Gini Coefficient
    def get_gini(self, wealth):
        """
        Calculates the Gini Coefficient using the discrete mean absolute difference formula.
        G = (2 * sum(i * w_i)) / (n * sum(w_i)) - (n + 1) / n
        Result ranges from 0 (perfect equality) to 1 (perfect inequality).
        """
        if not wealth:
            return 0
        
        sorted_w = sorted(wealth)
        n = len(sorted_w)
        total = sum(sorted_w)
        cum_wealth = 0

        # Avoid division by zero if the total wealth of the society is zero
        if total == 0:
            return 0
        
        # Calculate the cumulative weighted wealth
        cum_wealth = sum(i * w for i, w in enumerate(sorted_w, start=1))

        # Standard Gini formula for discrete distributions
        gini = (2 * cum_wealth) / (n * total) - (n + 1) / n
        return gini

    def get_migration_sensitivity(self):
        """
        Computes dynamic migration sensitivity (eta) based on
        infrastructure, policy barriers, and information flow.
        """
        infra_effect = 1 + self.alpha_I * self.infrastructure
        policy_effect = math.exp(-self.alpha_P * self.policy_barrier)
        info_effect = 1 + self.alpha_F * self.info_flow
    
        return self.eta_base * infra_effect * policy_effect * info_effect
    
    def handle_population_shift(self, projected_population):
        """
        Adjusts the microscopic agent list to match macroscopic population projections.
        Simulates migration and natural demographic shifts.
        """
        if not self.population:
            return 0

        # Calculate the gap between projected and current agent count
        diff = projected_population - self.population

        # Case 1: Inward Migration / Births
        if diff > 0:
            avg_wealth = sum(self.wealth_dist) / self.population
            newcomers = []
            for _ in range(diff):
                # Newcomers enter with a wealth shock based on log-normal distribution
                immigrant_wealth = avg_wealth * random.lognormvariate(0, 0.3)
                newcomers.append(max(5.0, immigrant_wealth))    # Ensure a minimum survival buffer
            self.wealth_dist.extend(newcomers)

        # Case 2: Outward Migration / Social Attrition
        elif diff < 0:
            num_to_remove = abs(diff)
            if num_to_remove >= self.population:
                self.wealth_dist = []
            else:
                # Vulnerability score = random factor / (wealth + 0.1)
                scored_population = [(w, random.random() / (w + 0.1)) for w in self.wealth_dist]
                scored_population.sort(key=lambda x: x[1], reverse=True)
                self.wealth_dist = [item[0] for item in scored_population[num_to_remove:]]
    
    def run_fiscal_year(self, edu_rate, tax_rate):
        """
        Executes a full cycle of the city's socio-economic activity.
        1. Production -> 2. Distribution -> 3. Survival -> 4. Technical Progress -> 5. Migration
        """
        if self.population == 0:
            return 0

        self.year += 1

        # 1. Only survivors form the "Effective Labor Force".
        survivors = []
        for w in self.wealth_dist:
            w -= self.cost                                      # Survival cost is paid at the start of the year
            if w > 0:
                survivors.append(w)
        self.wealth_dist = survivors

        # Post-attrition safety check
        if self.population == 0:
            return {
                "year": self.year,
                "population": 0,
                "gini": None,
                "morale": 0,
                "yield": 0                                      # Changed from gross_yield to 0, since no one produced anything
            }

        # 2. Production & Distribution by the Effective Labor Force
        gross_yield = self.intellect * math.pow(self.population, self.beta)
        net_to_people = gross_yield * (1 - tax_rate)
        avg_share = net_to_people / self.population

        # Distribute wealth to survivors
        for i in range(self.population):
            shock = random.lognormvariate(0, 0.3)
            self.wealth_dist[i] += avg_share * shock

        # 4. Socio-metric calculation
        gini = self.get_gini(self.wealth_dist)
        mean_wealth = sum(self.wealth_dist) / self.population
        # Morale is derived from per capita wealth adjusted by the fairness of distribution
        morale = mean_wealth * math.pow(1 - gini, 0.6)

        self.gini_data.append(gini)
        self.population_data.append(self.population)

        # 5. Endogenous Growth: Education investment drives Intellect (TFP)
        # Marginal returns on TFP
        growth_factor = (edu_rate * 0.15) / math.sqrt(self.intellect)
        self.intellect *= (1 + growth_factor)

        # 6. Macroscopic Population Dynamics
        # Migration is driven by morale relative to a benchmark
        eta = self.get_migration_sensitivity()
        benchmark_morale = 25
        
        raw_migration = eta * math.log(max(morale, 1e-9) / benchmark_morale)
        MAX_OUTFLOW_RATE = math.log(0.7)                          # ln(0.7) ≈ -0.356 (represents max 30% drop)
        migration = max(MAX_OUTFLOW_RATE, raw_migration)

        # Logistic growth accounts for environmental carrying capacity
        logistic_growth = self.base_growth * (1 - self.population / self.land_capacity)

        # Calculate target population for the next cycle
        projected_population = int(self.population * math.exp(logistic_growth + migration))

        # Synchronize macroscopic math with microscopic agent list
        self.handle_population_shift(projected_population)
        
        return {
            "year": self.year,
            "population": self.population,
            "gini": round(gini, 3),
            "morale": round(morale, 2),
            "yield": int(gross_yield)
        }

    def get_report(self):
        """Print final data"""
        return {
            "name": self.name,
            "final_tfp": self.intellect,
            "history_gini": self.gini_data,
            "history_pop": self.population_data
        }
