import pandas as pd
import numpy as np
import random

def generate_synthetic_logs(num_entries=200):
    np.random.seed(42)
    timestamps = pd.date_range(start='2025-07-01', periods=num_entries, freq='T')
    test_cases = [f'TestCase{random.randint(1, 10)}' for _ in range(num_entries)]
    statuses = np.random.choice(['PASS', 'FAIL'], size=num_entries, p=[0.85, 0.15])
    durations = np.random.normal(loc=5, scale=2, size=num_entries).clip(0.5, 15)
    
    # Inject some anomalies: longer durations and more fails randomly
    for i in range(0, num_entries, 40):
        durations[i] = random.uniform(12, 20)  # Anomalously long duration
        statuses[i] = 'FAIL'
    
    error_codes = []
    for status in statuses:
        if status == 'FAIL':
            error_codes.append(random.choice(['E100', 'E101', 'E104', 'E200']))
        else:
            error_codes.append('')

    df = pd.DataFrame({
        'timestamp': timestamps,
        'test_case': test_cases,
        'status': statuses,
        'duration': durations,
        'error_code': error_codes
    })
    return df

# Save to CSV for use
df_logs = generate_synthetic_logs()
df_logs.to_csv('synthetic_test_logs.csv', index=False)
print("Synthetic logs saved to synthetic_test_logs.csv")
