import argparse
import re
from collections import Counter
from datetime import datetime


def read_log_file(file_path):
    """Reads the log file line by line to handle large files efficiently."""
    try:
        with open(file_path, 'r') as file:
            for line in file:
                yield line.strip()  # Using a generator to process large files
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []


def parse_log_line(line):
    """Parses a log line using regex to extract timestamp, level, and message."""
    pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) (INFO|WARNING|ERROR|CRITICAL) (.+)$'
    match = re.match(pattern, line)
    if match:
        timestamp_str, level, message = match.groups()
        return {"timestamp": timestamp_str, "level": level, "message": message}
    return None


def filter_logs_by_level(logs, severity_level):
    """Filters logs by severity level."""
    return [log for log in logs if log["level"] == severity_level]


def parse_logs(raw_lines):
    """Parse raw log lines and return a list of valid entries."""
    parsed_entries = []
    for line in raw_lines:
        entry = parse_log_line(line)
        if entry:
            parsed_entries.append(entry)
        else:
            print(f"Warning: Skipping invalid log entry: {line}")
    return parsed_entries


def count_log_level(parsed_logs):
    """Counts occurrences of each log level (INFO, WARNING, ERROR, CRITICAL)."""
    levels = [log["level"] for log in parsed_logs]
    return Counter(levels)


def find_most_recent_error(parsed_logs):
    """Finds the most recent ERROR log."""
    error_logs = [log for log in parsed_logs if log["level"] == "ERROR"]
    if not error_logs:
        return None
    return max(error_logs, key=lambda log: datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S,%f"))


def write_summary_report(parsed_logs, level_counts, most_recent_error, output_file):
    """Writes a summary report to the output file."""
    total_logs = len(parsed_logs)
    with open(output_file, "w") as f:
        f.write("Log Summary Report\n")
        f.write("----------------------\n")
        f.write(f"Total Logs Processed: {total_logs}\n")
        f.write(f"INFO: {level_counts.get('INFO', 0)}\n")
        f.write(f"WARNING: {level_counts.get('WARNING', 0)}\n")
        f.write(f"ERROR: {level_counts.get('ERROR', 0)}\n")
        f.write(f"CRITICAL: {level_counts.get('CRITICAL', 0)}\n")

        if most_recent_error:
            time = most_recent_error["timestamp"]
            msg = most_recent_error["message"]
            f.write(f"Most Recent ERROR: {time} - {msg}\n")
        else:
            f.write("Most Recent ERROR: None\n")

    print(f"Summary report successfully written to {output_file}\n")


def main():
    parser = argparse.ArgumentParser(description="DevOps Log Analyzer: Parses logs and generates a summary.")
    parser.add_argument("logfile", help="Path to log file.")
    parser.add_argument("--level", help="Filter logs by severity level (INFO, WARNING, ERROR, CRITICAL)",
                        choices=["INFO", "WARNING", "ERROR", "CRITICAL"])
    parser.add_argument("--output", help="Output file for the summary report", default="log_summary.txt")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode to print parsed logs")

    args = parser.parse_args()

    raw_lines = read_log_file(args.logfile)
    parsed_logs = parse_logs(raw_lines)

    if args.level:
        parsed_logs = filter_logs_by_level(parsed_logs, args.level)

    level_counts = count_log_level(parsed_logs)
    most_recent_err = find_most_recent_error(parsed_logs)

    write_summary_report(parsed_logs, level_counts, most_recent_err, args.output)

    if args.debug:
        print("Debug Mode: Parsed Logs")
        for log in parsed_logs:
            print(log)


if __name__ == "__main__":
    main()
