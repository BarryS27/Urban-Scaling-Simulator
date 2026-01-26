import os
import csv
from model import CityEngine

def run_simulation(round_name, intellect, population, wealth, cost, tax_baseline, edu_baseline, years):
    edu_rates = [round(edu_baseline * factor, 3) for factor in [0.5, 0.75, 1.0, 1.25, 1.5]]
    tax_rates = [round(tax_baseline * factor, 3) for factor in [0.5, 0.75, 1.0, 1.25, 1.5]]
    
    os.makedirs("data", exist_ok=True)
    filepath = f'../data/results_{round_name}.csv'

    config = {
        "intellect": intellect,
        "population": population,
        "wealth": wealth,
        "cost": cost
    }

    print(f"--- Simulation {round_name} started. ({years} years) ---")
    
    with open(filepath, 'w', newline = '') as f:
        fieldnames = ['year','population','gini','morale','yield','edu_rate','tax_rate']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
    
        for i in edu_rates:
            for j in tax_rates:
                sample = CityEngine(name=f"Sample_{i}_{j}", config=config)
                last_valid_result = {}
                
                for year in range(1, years + 1):
                    response = sample.run_fiscal_year(i,j)
                    if response['population'] == 0 or response == 0:
                        break
                    last_valid_result = response
    
                last_valid_result['edu_rate'] = i
                last_valid_result['tax_rate'] = j
                writer.writerow(last_valid_result)
    
    print(f"Simulation complete. {round_name} data saved to {filepath}")
    return filepath

if __name__ == "__main__":
    round_name = input("")
    intellect = float(input(""))
    population = int(input(""))
    wealth = float(input(""))
    cost = float(input(""))
    tax_baseline = float(input(""))
    edu_baseline = float(input(""))
    years = int(input(""))
    run_simulation(round_name, intellect, population, wealth, cost, tax_baseline, edu_baseline, years)
