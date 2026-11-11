import numpy as np
import matplotlib.pyplot as plt

def evaluate(reference_file: str, candidate_file: str) -> dict:
    """
    Evaluates a candidate team's reconstruction against the reference spike_data.npz.

    Inputs:
        reference_file: path to original spike_data.npz or raw_data.npy
        candidate_file: path to another team's reconstruction npz

    Output:
        dictionary containing validity, metrics, overlay_figure, and final_score.
    """
    # 1. Load Data
    ref_data = np.load(reference_file, allow_pickle=True)
    cand_data = np.load(candidate_file, allow_pickle=True)

    # Robust handling for reference file (supports both .npy arrays and .npz dicts)
    if isinstance(ref_data, np.ndarray):
        ref_raw = ref_data
        ref_t = np.arange(len(ref_raw)) / 10000.0
    elif hasattr(ref_data, 'files'):
        if 'raw_data' in ref_data:
            ref_raw = ref_data['raw_data']
        else:
            ref_raw = ref_data[ref_data.files[0]]

        if 't' in ref_data:
            ref_t = ref_data['t']
        else:
            ref_t = np.arange(len(ref_raw)) / 10000.0
    else:
        ref_raw = np.array(ref_data)
        ref_t = np.arange(len(ref_raw)) / 10000.0

    # 2. Structural Validity Checks on Candidate File
    required_keys = ['t', 'drift', 'spike_signal', 'noise', 'reconstruction', 'spike_indices']

    if not hasattr(cand_data, 'files'):
        return {
            "validity": False,
            "validity_details": "Candidate file is not a valid dictionary-based .npz file.",
            "final_score": 0.0
        }

    missing_keys = [k for k in required_keys if k not in cand_data]
    is_valid = len(missing_keys) == 0
    validity_details = "Passed all structural checks." if is_valid else f"Missing keys: {missing_keys}"

    if not is_valid:
        return {
            "validity": False,
            "validity_details": validity_details,
            "final_score": 0.0
        }

    cand_rec = cand_data['reconstruction']
    cand_t = cand_data['t']

    # 3. Numerical Metrics
    mse = float(np.mean((ref_raw - cand_rec) ** 2))
    rmse = float(np.sqrt(mse))
    mae = float(np.mean(np.abs(ref_raw - cand_rec)))

    # Pearson Correlation Coefficient
    corr_matrix = np.corrcoef(ref_raw, cand_rec)
    pearson_r = float(corr_matrix[0, 1])

    # Coefficient of Determination (R2 Score)
    ss_res = np.sum((ref_raw - cand_rec) ** 2)
    ss_tot = np.sum((ref_raw - np.mean(ref_raw)) ** 2)
    r2_score = float(1.0 - (ss_res / ss_tot))

    # 4. Final Score Calculation (0 - 100 Scale)
    score_corr = max(0.0, pearson_r) * 70.0
    score_r2 = max(0.0, r2_score) * 30.0
    final_score = round(score_corr + score_r2, 2)

    # 5. Overlay Figure (FIXED: set_ylabel instead of ylabel)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(ref_t, ref_raw, label="Reference Raw Signal", color="black", alpha=0.5, linewidth=0.8)
    ax.plot(cand_t, cand_rec, label="Candidate Reconstruction", color="crimson", alpha=0.8, linewidth=1.0)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Voltage (mV)")
    ax.set_title(f"Evaluation Overlay | Pearson R = {pearson_r:.4f} | R² = {r2_score:.4f}")
    ax.legend(loc="upper right")
    plt.tight_layout()

    # 6. Output Dictionary
    return {
        "validity": is_valid,
        "validity_details": validity_details,
        "metrics": {
            # Error metrics measuring magnitude differences (lower is better)
            "MSE": mse,
            "RMSE": rmse,
            "MAE": mae,

            # Correlation coefficient measuring shape/morphology similarity.
            "Pearson_R": pearson_r,

            #Coefficient of determination measuring how much variance of the raw signal is explained by the reconstruction
            "R2_Score": r2_score
        },
        "overlay_figure": fig,
        "final_score": final_score
    }