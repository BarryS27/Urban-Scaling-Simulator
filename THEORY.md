# Theoretical Motivation and Scope

## 1. Theoretical Motivation and Scope

This model conceptualizes urban population change as the outcome of a feedback system driven by inequality and migration. Population dynamics emerge from aggregate socio-economic conditions rather than explicit individual decision-making.

The model operates at a meso-level, positioned between macro growth models and fully micro-founded agent decision frameworks. It excludes individual optimization and urban spatial structure.

The model is intended for directional and stability-oriented theoretical analysis rather than numerical prediction.

**Code reference:**  
Overall system dynamics are implemented in the `CityEngine` class, primarily within the `run_fiscal_year()` method.

---

## 2. Population Growth and Carrying Capacity

Population growth follows a logistic process constrained by an exogenous carrying capacity (`land_capacity`). This reflects environmental and infrastructural limits on urban expansion.

Migration pressure modifies the baseline growth path, allowing population to expand or contract endogenously around the logistic trend.

**Code reference:**  
- Logistic growth term:  
  `logistic_growth = base_growth * (1 - population / land_capacity)`  
  implemented in `run_fiscal_year()`
- Population update via exponential growth and migration:  
  `projected_population = int(population * exp(logistic_growth + migration))`
- Micro–macro synchronization handled in `handle_population_shift()`

---

## 3. Production Scaling and Aggregate Output

Urban economic output scales super-linearly with population size. The scaling exponent β is fixed at 1.15, consistent with empirical estimates from urban scaling literature, and is treated as exogenous.

Total factor productivity (TFP) multiplicatively shifts aggregate output.

**Code reference:**  
- Super-linear production function:  
  `gross_yield = intellect * population ** beta`  
  implemented in `run_fiscal_year()`
- Scaling exponent specified as `self.beta = 1.15` in `__init__()`

---

## 4. Wealth Dynamics and Inequality

Individual wealth evolves stochastically. Income shocks follow a log-normal distribution, capturing empirical wealth skewness where a small fraction of agents holds a large share of total wealth.

Individuals exit the system when wealth falls below subsistence requirements determined by a fixed survival cost. The model excludes debt, borrowing, and social insurance mechanisms.

Inequality is measured using the discrete Gini coefficient. Sorting operations used in computation do not represent persistent social classes.

**Code reference:**  
- Log-normal income shocks:  
  `random.lognormvariate(0, 0.3)` in `run_fiscal_year()`
- Survival cost and exit:  
  wealth reduction via `self.cost`, filtering in `run_fiscal_year()`
- Gini computation:  
  implemented in `get_gini()`
- Sorting used only for statistical calculation inside `get_gini()`

---

## 5. Morale as a Mediating Variable

Morale is a composite indicator derived from mean wealth and inequality. Its functional form is specified as a power function based on empirical plausibility rather than formal derivation.

Morale mediates the relationship between inequality and migration pressure.

**Code reference:**  
- Morale calculation:  
  `morale = mean_wealth * (1 - gini) ** 0.6`  
  implemented in `run_fiscal_year()`

---

## 6. Migration and Feedback Structure

Migration is the primary feedback channel linking socio-economic conditions to population change. Migration sensitivity depends on infrastructure quality, policy barriers, and information flow.

Changes in morale alter migration pressure, which in turn affects population size and reshapes wealth distribution through scale effects.

**Code reference:**  
- Migration sensitivity:  
  implemented in `get_migration_sensitivity()`
- Migration pressure calculation:  
  `raw_migration = eta * log(morale / benchmark_morale)`
- Population adjustment via migration:  
  implemented through `handle_population_shift()`

---

## 7. Endogenous Productivity Growth

Educational investment increases TFP over time. This relationship is one-directional: productivity affects output but does not feed back into education decisions.

**Code reference:**  
- TFP update rule:  
  `self.intellect *= (1 + growth_factor)`  
  implemented in `run_fiscal_year()`

---

## 8. Exogenous Variables and Interpretation Boundaries

Land carrying capacity, wealth units, and several institutional features are treated as exogenous. Wealth units are abstract and do not correspond to real-world currency values.

The model excludes spatial structure, inter-city competition, fiscal redistribution, and endogenous institutional change.

**Code reference:**  
- Exogenous parameters initialized in `__init__()`

---

## 9. Model Interpretation

This model is not designed for forecasting. Its results should be interpreted as qualitative dynamics illustrating feedback mechanisms and stability properties within the specified abstraction boundaries.
