import math
import random

class CityEngine:
    """
    A quantitative simulation engine that models urban socio-economic evolution.
    Integrates urban scaling laws, logistic population growth, and endogenous 
    growth theories to simulate wealth distribution and migration.
    """
    def __init__(self, name, intellect=4.5):
        # Basic identification and state variables
        self.name = name
        self.intellect = intellect                              # Total Factor Productivity (TFP)
        self.year = 0

        # System Constants
        self.beta = 1.15                                        # Super-linear scaling exponent for urban output
        self.land_capacity = 10000                              # Carrying capacity (K) of the environment
        self.base_growth = 0.008                                # Intrinsic growth rate (r)
        self.corruption = 0.05                                  # Friction coefficient in economic yield (Reserved for expansion)
        self.cost = 10.0                                        # Per capita annual survival cost

        # Population initialization: 1000 individuals with 50.0 units of wealth each
        self.wealth_dist = [50.0] * 1000
        self.gini_data = []                                     # Historical tracking of Gini Coefficient
        self.population_data = []                               # Historical tracking of population size
    
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
            # Sort wealth to simulate that the impoverished are most vulnerable to displacement
            self.wealth_dist.sort()
            num_to_remove = abs(diff)
            # Remove the n individuals with the lowest wealth
            self.wealth_dist = self.wealth_dist[num_to_remove:]
    
    def run_fiscal_year(self, edu_rate, tax_rate):
        """
        Executes a full cycle of the city's socio-economic activity.
        1. Production -> 2. Distribution -> 3. Survival -> 4. Technical Progress -> 5. Migration
        """
        if self.population == 0:
            return 0

        self.year += 1

        # 1. Economic Production: Yield follows urban scaling law Y = A * N^beta
        gross_yield = self.intellect * math.pow(self.population, self.beta)
        net_to_people = gross_yield * (1 - tax_rate)
        avg_share = net_to_people / self.population

        # 2. Micro-distribution and Survival Attrition
        new_wealth = []
        for w in self.wealth_dist:
            # Apply a random luck/productivity shock
            shock = random.lognormvariate(0,0.3)
            w += avg_share * shock
            w -= self.cost                                      # Deduct annual survival cost
            if w > 0:
                new_wealth.append(w)                            # Only survivors continue to the next year
        
        self.wealth_dist = new_wealth

        # 3. Post-attrition safety check
        if self.population == 0:
            return {
                "year": self.year,
                "population": 0,
                "gini": None,
                "morale": 0,
                "yield": int(gross_yield)
            }

        # 4. Socio-metric calculation
        gini = self.get_gini(self.wealth_dist)
        mean_wealth = sum(self.wealth_dist) / self.population
        # Morale is derived from per capita wealth adjusted by the fairness of distribution
        morale = mean_wealth * math.pow(1 - gini, 0.6)

        self.gini_data.append(gini)
        self.population_data.append(self.population)

        # 5. Endogenous Growth: Education investment drives Intellect (TFP)
        self.intellect *= math.exp(edu_rate * 0.15)

        # 6. Macroscopic Population Dynamics
        # Migration is driven by morale relative to a benchmark
        migration = 0.02 * math.log(morale / 25) if morale > 0 else -0.1
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
