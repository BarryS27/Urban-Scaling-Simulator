import math
import random

class SociologyEngine:
    def __init__(self, name, souls=50, vault=2500, intellect=4.5):
        self.name = name
        self.souls = souls          # 
        self.vault = vault          # 
        self.intellect = intellect  # 
        self.year = 0
        
        self.beta = 1.15            # 
        self.land_capacity = 10000  # 
        self.base_growth = 0.008    # 
        self.gini = 0.35            # 
        self.corruption = 0.05      # 

    def run_fiscal_year(self, edu_rate, tax_rate):
        self.year += 1
        
        # 
        gross_yield = self.intellect * math.pow(self.souls, self.beta)
        
        # 
        maintenance = 100 * math.exp(0.01 * self.year) * math.pow(self.souls, 0.85)
        survival_cost = self.souls * 8
        total_drain = (maintenance + survival_cost) * (1 + self.corruption)
        
        # 
        per_capita_net = (gross_yield * (1 - tax_rate)) / self.souls
        morale = per_capita_net * math.pow(1 - self.gini, 0.6)
        
        # 
        g = edu_rate * 0.15
        self.intellect *= math.exp(g)
        
        self.vault += (gross_yield * tax_rate) - total_drain
        
        # 
        migration = 0.02 * math.log(morale / 25) if morale > 0 else -0.1
        logistic_growth = self.base_growth * (1 - self.souls / self.land_capacity)
        self.souls *= math.exp(logistic_growth + migration)
        
        return {
            "year": self.year,
            "souls": int(self.souls),
            "vault": int(self.vault),
            "morale": round(morale, 2),
            "yield": int(gross_yield)
        }