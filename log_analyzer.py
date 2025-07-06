import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

# Load & parse logs
def load_logs(file_path):
    df = pd.read_csv(file_path, parse_dates=['timestamp'])
    return df

# Feature engineering
def extract_features(df):
    df['status_binary'] = df['status'].apply(lambda x: 1 if x == 'FAIL' else 0)
    features = df[['duration', 'status_binary']]
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    return features_scaled, df

# Threshold-based anomaly detection
def detect_threshold_anomalies(df, duration_threshold=10):
    df['threshold_anomaly'] = df['duration'] > duration_threshold
    return df

# Clustering-based anomaly detection with DBSCAN
def detect_cluster_anomalies(features_scaled, df):
    model = DBSCAN(eps=0.5, min_samples=3)
    clusters = model.fit_predict(features_scaled)
    df['cluster'] = clusters
    df['cluster_anomaly'] = df['cluster'] == -1
    return df

# Combine anomalies from threshold and clustering
def combine_anomalies(df):
    df['anomaly'] = df['threshold_anomaly'] | df['cluster_anomaly']
    return df

# Visualization of anomalies
def plot_anomalies(df):
    plt.figure(figsize=(12, 6))
    colors = df['anomaly'].map({True: 'red', False: 'green'})
    plt.scatter(df.index, df['duration'], c=colors)
    plt.xlabel('Test Run Index')
    plt.ylabel('Duration (seconds)')
    plt.title('Test Runs Duration with Anomalies Highlighted (Red)')
    plt.show()

# Summary report
def save_report(df, output_file='anomaly_report.csv'):
    df.to_csv(output_file, index=False)
    print(f"Anomaly report saved to {output_file}")

# Main function to run the analysis pipeline
def main(log_file='synthetic_test_logs.csv'):
    print("Loading logs...")
    df = load_logs(log_file)

    print("Extracting features...")
    features_scaled, df = extract_features(df)

    print("Detecting threshold anomalies...")
    df = detect_threshold_anomalies(df)

    print("Detecting cluster anomalies...")
    df = detect_cluster_anomalies(features_scaled, df)

    print("Combining anomalies...")
    df = combine_anomalies(df)

    print("Plotting anomalies...")
    plot_anomalies(df)

    print("Saving anomaly report...")
    save_report(df)

if __name__ == '__main__':
    main()
