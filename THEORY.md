# Theoretical Motivation and Scope

## 1. Theoretical Motivation and Scope

This model conceptualizes urban population change as the outcome of a feedback system driven by inequality and migration. Population dynamics do not arise from explicit individual decision-making, but from aggregate responses to socio-economic conditions.

The model operates at a meso-level, positioned between purely macro-scale growth models and fully micro-founded agent decision models. It does not incorporate spatial structure of cities, nor does it simulate strategic or optimizing behavior at the individual level.

The purpose of the model is not numerical prediction, but directional and stability-oriented theoretical analysis of long-run urban dynamics.

---

## 2. Core Growth Assumptions

Population growth is governed by a logistic process with an exogenously specified carrying capacity (`land_capacity`). This reflects environmental and infrastructural constraints that limit indefinite urban expansion.

Urban economic output follows a super-linear scaling relationship with population size. The scaling exponent β is fixed at 1.15, consistent with empirical estimates reported in the original urban scaling literature. This parameter is treated as externally given rather than endogenously derived.

---

## 3. Wealth Dynamics and Inequality

Individual wealth is modeled as a stochastic variable following a log-normal distribution. This choice reflects the empirical regularity that a small fraction of individuals holds a disproportionately large share of total wealth.

Individuals exit the system when their wealth falls below a subsistence threshold determined by an exogenous survival cost. The model does not include debt mechanisms, social insurance, or redistributive safety nets. As a result, exit is absorbing and irreversible.

Inequality is measured using the Gini coefficient computed via a discrete formulation without weighting or grouped approximation. Any sorting operations applied in the source code are used solely for statistical computation and do not represent persistent social classes or fixed stratification.

---

## 4. Morale, Migration, and Feedback Structure

Morale is a composite socio-economic indicator derived from mean wealth and inequality. Its functional form is specified as a power function based on empirical plausibility rather than formal theoretical derivation.

Migration acts as the primary feedback channel linking inequality to population change. Changes in morale mediate migration pressure, which in turn alters population size. Population change then reshapes aggregate production and wealth distribution, completing the feedback loop.

---

## 5. Endogenous Productivity Growth

Educational investment increases total factor productivity (TFP) over time. This relationship is strictly one-directional: productivity growth affects output but does not feed back into educational investment decisions.

TFP dynamics are therefore partially endogenous but not fully coupled to other socio-economic variables within the model.

---

## 6. Exogenous Variables and Abstractions

Land carrying capacity is treated as an exogenous constraint. Wealth is measured in abstract economic units rather than real-world currency values.

Several real-world mechanisms are intentionally excluded, including individual choice modeling, urban spatial structure, inter-city competition, fiscal redistribution, and institutional heterogeneity beyond migration frictions.

---

## 7. Interpretation Boundaries

This model should not be interpreted as a forecasting tool. Its results are intended to illustrate qualitative dynamics, feedback directions, and stability properties rather than to generate empirically calibrated predictions.

Conclusions drawn from the model are valid only within the abstraction boundaries defined above.
