# Reverse-Engineering Project — Team 02

## 1. Inferred Model & Parameters
- **Drift Offset:** 0.0035 mV
- **Drift Amplitude:** 0.6482 mV
- **Drift Frequency:** 0.0910 Hz
- **Drift Phase:** 0.2804 rad
- **Spike Amplitude:** 5.0279 mV
- **Spike Decay Constant (tau):** 2.9773 ms
- **Noise Std Dev (sigma):** 0.2987 mV
- **Firing Rate:** 4.20 Hz

## 2. Assumptions
- The baseline drift is modeled as a low-frequency pure sinusoid: $A \sin(2\pi f t + \phi) + \text{offset}$.
- Spikes exhibit an immediate step voltage increase followed by a first-order exponential decay ($V_0 e^{-t/\tau}$).
- Background noise is zero-mean additive white Gaussian noise (AWGN) estimated from quiet periods.
- Reconstructed signal contains structured components only ($drift + spikes$), omitting noise realization.

## 3. Detection & Reconstruction Method
1. **Spike Detection:** Rising-edge thresholding at $\text{Mean} + 5\sigma$.
2. **Quiet Baseline Masking:** Masking a 15 ms post-onset window for each detected spike.
3. **Drift Estimation:** Ordinary Least Squares (OLS) grid search across frequencies ($0.02 - 0.5$ Hz) on quiet baseline samples.
4. **Decay Dynamics:** Log-linear fitting on average spike profile to estimate $\tau$.

## Team and source
Amanda Cardoso de Sousa, Seonil Jeong, Gebreab Tewelday (Group 2).
Adapted from the team notebook in a15cardoso/python_ws, commit e597c24818b4e4eea3292199c825f5fa54d58dac.
Corrected group ID and excluded generated noise from reconstruction.

## Run and submit
Open task_reverse_engineering.ipynb in Google Colab, upload spike_data.npz, and run all cells. Submit team_02_reconstruction.npz, README.md, and evaluate_team.py.
The included evaluation_result.json records the local test (89.00/100) using the team evaluator, not an official grade.
