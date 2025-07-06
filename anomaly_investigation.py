import pandas as pd

def analyze_anomalies():
    # Load anomaly report CSV
    anomalies = pd.read_csv('anomaly_report.csv')

    # Convert 'timestamp' to datetime type
    anomalies['timestamp'] = pd.to_datetime(anomalies['timestamp'], errors='coerce')

    # Drop rows where timestamp conversion failed (optional, if needed)
    anomalies = anomalies.dropna(subset=['timestamp'])

    print(f"Total anomalies found: {len(anomalies)}\n")

    print("Anomalies by Test Case:")
    print(anomalies['test_case'].value_counts(), "\n")

    print("Anomalies by Error Code:")
    print(anomalies['error_code'].value_counts(dropna=False), "\n")

    # Group anomalies by date
    anomalies_over_time = anomalies.groupby(anomalies['timestamp'].dt.date).size()
    print("Anomalies over Time:")
    print(anomalies_over_time)

if __name__ == "__main__":
    analyze_anomalies()
