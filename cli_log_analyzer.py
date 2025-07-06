import argparse
from log_analyzer import load_logs, extract_features, detect_threshold_anomalies, detect_cluster_anomalies, combine_anomalies, save_report, plot_anomalies

def main():
    parser = argparse.ArgumentParser(description='Log Anomaly Detection Tool')
    parser.add_argument('--log', default='synthetic_test_logs.csv', help='Input log CSV file')
    parser.add_argument('--duration-threshold', type=float, default=10.0, help='Duration threshold')
    parser.add_argument('--eps', type=float, default=0.5, help='DBSCAN eps')
    parser.add_argument('--min-samples', type=int, default=3, help='DBSCAN min samples')
    parser.add_argument('--output', default='anomaly_report.csv', help='Output CSV file for anomaly report')
    args = parser.parse_args()

    df = load_logs(args.log)
    features_scaled, df = extract_features(df)
    df = detect_threshold_anomalies(df, duration_threshold=args.duration_threshold)
    df = detect_cluster_anomalies(features_scaled, df, eps=args.eps, min_samples=args.min_samples)
    df = combine_anomalies(df)
    save_report(df, output_file=args.output)
    plot_anomalies(df)

if __name__ == '__main__':
    main()
