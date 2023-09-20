# Estimate Power Output

Cycling is a well researched sports primarily because it provides a highly reproducible and controlled exercise mode. 
It allows researchers to precisely manipulate variables such as intensity (by adjusting resistance or terrain), duration, and frequency. 
The availability of advanced sensors and their portability contribute to control. The sensors are capable of precisely measuring various
physiological parameters such as power output, cadence, heart rate, and speed. 
These attributes make cycling an ideal field of sports conducive to the study of the relationship between power output and other physiological parameters.

The ultimate goal of this project is to estimate power output for various human activities using affordable and portable sensors. 
The study of cycling is a stepping stone towards that goal.

The initial set of bike sensors we utilize are:
- Garmin Edge 1040 Bike Computer with GPS (lat/lon, speed, altitude)
- Garmin HRM-Pro chest strap heart-rate monitor
- Garmin Varia RTL515 bike radar (vehicle count and speed)
- SRAM Quarq Rival AXS power meter (power, cadence)
  

# Contents
1. [EDA](notebooks/eda.ipynb) (Exploratory Data Analysis)
2. Part1: [model evaluation](notebooks/part1_model_evaluation.ipynb)
3. Part2: [analysis of power](notebooks/part2_power_analysis.ipynb): here we attempt to identify the source of the systematic errors by examining the related physics in detail.
4. Part3: [conclusion](notebooks/part3_conclusion.ipynb)
* Note that plotly figures, which are critical to the analyses, aren't rendered in the notebooks on git. Please clone+execute to examine them.
* A simplified [overview ppt](misc/project_overview.pptx) is available.

# Summary of Results

This project was a typical example of domain knowledge trumping machine learning.
Polynomial features derived from theory in physics with a simple linear regressor proved to be the most efficient (in terms of both computation
efficiency and accuracy) predictor of power.

It was impossible to predict the sharp peaks of power. I had to modify the target variable by computing its moving averages over 50 seconds in order to approximate
the peaks. This means in particular that a near real-time system is impossible. There was a sharp accuracy vs. time-delay trade off that needed to be considered.

That power depends on the cube of ground speed was a revelation. Which means the power required to double your speed is more than 2^3=8 times the initial power.
In case the head wind velocity equals the negative of ground speed velocity, the coefficient of the cube of ground speed quadruples compared to the case when there is no head wind.
In this vein reduction of frontal area is critical to the reduction of required power.

In part2 I've demonstrated that velocity was a critical missing feature. On a windy section of the data, I've shown that even a simplisitc prevalent constant wind model could
cut the MAE by more than half for that section.

Linear regression with theory-based features had 19.5 MAE. This loss is about 5% of the overall max of power, and ~19% of the mean of power.

Please see the end of the part3 notebook for further detailed findings.

# Next Steps
- Further tune the gradient boosting regressor with augmented features. Grid search turned out to be too computationally intensive, preventing me from performing further analyses.
  I cannot fathom that a good estimator will not incorporate features such as `cadence` when predicting `power`.
- Collect more data, including if possible wind data and also data from different individuals
- We've modeled the system disregarding history. Features such as heart rate are not Markovian. Thus modeling with RNN is warranted.


# References
We've made use of the [fitdecode library](https://github.com/polyvertex/fitdecode) to parse Garmin's proprietary binary .fit format files. 

Garmin does publish their own [API](https://developer.garmin.com/fit/cookbook/decoding-activity-files/), however their decoded results have a structure of their own that isn't conducive to ingesting into notebooks.

Some Wikipedia references for underlying physics:
- [drag force](https://en.wikipedia.org/wiki/Drag_(physics)#The_drag_equation)
- [rolling resistance](https://en.wikipedia.org/wiki/Rolling_resistance#Rolling_resistance_coefficient)



