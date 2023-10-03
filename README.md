# Arbitrage Optimization



## About

This project provides my solution of the arbitrage optimization problem. Theory and solution of the problem are provided in Jupyter notebook **arbitrage_optimization.ipynd**. Additionally, there is a **data/** directory storing NYISO data for August 2022, **utils.py** with utilities for the solution and **expressions.py** with expressions used in the optimization formulation.

## Installation and dependencies

The implementation is written in python and requires Jupyter (or an IDE supporting notebooks) to inspect/run the solution. On top of the python standard library, following packages were used: \
**numpy==1.25.0** \
**pandas==2.0.3** \
**Pyomo==6.6.1** 

To be able to perform the optimization, one also needs to install appropriate MILP solver supported by pyomo. This example uses **GLPK** solver.

## Conclusion

Some insights and conclusions from the model:
- as the problem uses largely idealized conditions, obtaining the solution is not expensive  (< 1s)
- the solution generally followed intuitive expectation, with charging occuring in the periods with cheaper prices and discharging occuring in the periods with higher prices
- however, on this day, the cheapest LBMP period occurred between 6 and 9 am, where we would normally expect morning peak
- the model is able to yield net gain
- as expected, fluctuations in the LBMP over the day lead to higher gain, and the days with higher variance in the energy prices achieve higher profit
- whenever the battery charges/discharges, it does so at full power
- the battery ends the cycle at (maximum) depth of discharge
- in this idealized setting, the model never ends up in a loss (should the conditions be unfavorable, it would simply not trade at all and end up with 0)
