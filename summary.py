import re
from collections import Counter
import matplotlib.pyplot as plt
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import Counter
from dateutil import parser
from collections import defaultdict
import datetime
from datetime import datetime
from dateutil import parser
from datetime import timedelta


summary_file = "summary.txt"
with open(summary_file, 'w') as file:
    pass
def write_to_file(content):
    with open(summary_file, 'a') as file:  # 'a' for append mode
        file.write(content + '\n')

def extract_log_data(line):
    # Regular expression to match the time, prefix, and message
    pattern = r'(\b\w{3}\s\d{2}\s\d{2}:\d{2}:\d{2}\b)\s+(.*?)\s*:\s*(.*)'
    match = re.match(pattern, line)
    if match:
        time, prefix, message = match.groups()
        return time, prefix, message
    else:
        return None, None, None

def to_dict(file_path):
    log_data = []
    with open(file_path, 'r') as file:
        for line in file:
            time, prefix, message = extract_log_data(line)
            log_data.append({'time': time, 'prefix': prefix, 'message': message})
    return log_data

def most_common_prefixes(log_data, n):
    prefixes = Counter()
    for log in log_data:
        if log['prefix']:
            prefixes[log['prefix']] += 1
    return prefixes.most_common(n)


def analyze_log_file(file_path):
    log_data = to_dict(file_path)
    most_prefixes = most_common_prefixes(log_data,30)
    write_to_file("Most Common Prefixes:")
    for prefix in most_prefixes:
        write_to_file(f"- {prefix}")



def aggregate_counts(datetime_counts, interval='hourly'):
    aggregated_counts = defaultdict(int)
    for datetime_object, count in datetime_counts.items():
        if interval == 'hourly':
            # Round down to the nearest hour
            rounded_datetime = datetime_object.replace(minute=0, second=0, microsecond=0)
        elif interval == 'daily':
            # Round down to the nearest day
            rounded_datetime = datetime_object.replace(hour=0, minute=0, second=0, microsecond=0)
        # Add counts to the rounded datetime
        aggregated_counts[rounded_datetime] += count
    return aggregated_counts

def find_most_active_timeframes(datetime_counts, interval='hourly', top_n=10):
    aggregated_counts = aggregate_counts(datetime_counts, interval)
    # Sort the timeframes by number of hits in descending order
    sorted_by_hits = sorted(aggregated_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return sorted_by_hits


def find_least_active_timeframes(datetime_counts, interval='hourly',top_n=10):
    aggregated_counts = aggregate_counts(datetime_counts, interval)
    # Sort the timeframes by number of hits in ascending order
    sorted_by_hits = sorted(aggregated_counts.items(), key=lambda x: x[1])[:top_n]
    return sorted_by_hits


def parse_timestamp(timestamp):
    current_year = datetime.now().year
    timestamp_with_year = f"{current_year} {timestamp}"
    try:
        # Adjust the format to include the year
        return datetime.strptime(timestamp_with_year, '%Y %b %d %H:%M:%S')
    except ValueError:
        # Handle cases where the timestamp format might be incorrect
        return None
def to_datetime(log_data):
    # Convert timestamp strings to datetime objects
    datetime_objects = [parse_timestamp(log['time']) for log in log_data if log['time']]
    # Count occurrences of each datetime
    datetime_counts = Counter(datetime_objects)
    return datetime_objects


def calculate_log_duration_hours(log_data):
    if not log_data:
        return 0

    # Extract datetime objects from log data
    datetime_objects = [parse_timestamp(log['time']) for log in log_data if log['time']]


    if not datetime_objects:
        return 0

    # Find earliest and latest timestamps
    earliest_time = min(datetime_objects)
    latest_time = max(datetime_objects)

    # Calculate duration
    duration = latest_time - earliest_time
    duration_in_hours = duration.total_seconds() / 3600

    write_to_file(f"the log goes from {earliest_time} to {latest_time}, which is {int(duration_in_hours+1)} hours")

    return duration_in_hours


def summarize_file(file_name):
    # file_name = "data/final_log_final.txt"

    log_data = to_dict(file_name)
    log_duration_hours = calculate_log_duration_hours(log_data)
    write_to_file(f"Total log duration: {int(log_duration_hours+1)} hours") # round


    datetime_objects = to_datetime(log_data)
    datetime_counts = Counter(datetime_objects)
    most_active_hours = find_most_active_timeframes(datetime_counts, 'hourly', 5)
    write_to_file("Most Active Hours:")
    for datetime, count in most_active_hours:
        write_to_file(f"{datetime}: {count} messages")

    least_active_hours = find_least_active_timeframes(datetime_counts, 'hourly', 5)
    write_to_file("Least Active Hours:")
    for datetime, count in least_active_hours:
        write_to_file(f"{datetime}: {count} messages")

    analyze_log_file(file_name)

    with open(summary_file, 'r') as file:
        return file.read()