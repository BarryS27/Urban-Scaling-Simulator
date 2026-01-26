import os
import csv
from model import CityEngine

simulate_round = input("Simulate Index: ")

tax_baseline = float(input("Enter baseline tax rate (e.g., 0.15): "))
edu_baseline = float(input("Enter baseline edu rate (e.g., 0.05): "))

edu_rates = [round(edu_baseline * factor, 3) for factor in [0.5, 0.75, 1.0, 1.25, 1.5]]
tax_rates = [round(tax_baseline * factor, 3) for factor in [0.5, 0.75, 1.0, 1.25, 1.5]]

os.makedirs("../data", exist_ok=True)

with open(f'../data/results_{simulate_round}.csv', 'w', newline = '') as f:
    fieldnames = ['year','population','gini','morale','yield','edu_rate','tax_rate']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for i in edu_rates:
        for j in tax_rates:
            sample = CityEngine(name=f"Sample_{i}_{j}")
            last_valid_result = {}
            
            for year in range(1, 801):
                response = sample.run_fiscal_year(i,j)
                last_valid_result = response

                if response['population'] == 0:
                    break

            last_valid_result['edu_rate'] = i
            last_valid_result['tax_rate'] = j
            writer.writerow(last_valid_result)

print(f"Simulation complete. {simulate_round} data saved to ../data/results.csv")
