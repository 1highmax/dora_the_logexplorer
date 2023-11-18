import re
from collections import Counter

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
    print("Most Common Prefixes:")
    for prefix in most_prefixes:
        print(f"- {prefix}")

import matplotlib.pyplot as plt
from collections import Counter

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import Counter
from dateutil import parser

def to_datetime(log_data):
    # Convert timestamp strings to datetime objects
    datetime_objects = [parser.parse(log['time']) for log in log_data if log['time']]
    # Count occurrences of each datetime
    datetime_counts = Counter(datetime_objects)
    return datetime_objects

from collections import defaultdict
import datetime

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

def find_most_active_timeframes(datetime_counts, interval='hourly',top_n=10):
    aggregated_counts = aggregate_counts(datetime_counts, interval)
    # Sort the timeframes by datetime in ascending order
    sorted_by_time = sorted(aggregated_counts.items(), key=lambda x: x[0])[:top_n]
    return sorted_by_time


def parse_timestamp(timestamp):
    try:
        # Assuming the format is consistent as "Mon DD HH:MM:SS"
        return datetime.strptime(timestamp, '%b %d %H:%M:%S')
    except ValueError:
        # Handle cases where the timestamp format might be incorrect
        return None
    
from dateutil import parser
from datetime import timedelta

def calculate_log_duration_hours(log_data):
    if not log_data:
        return 0

    # Extract datetime objects from log data
    datetime_objects = [parser.parse(log['time']) for log in log_data if log['time']]

    if not datetime_objects:
        return 0

    # Find earliest and latest timestamps
    earliest_time = min(datetime_objects)
    latest_time = max(datetime_objects)

    # Calculate duration
    duration = latest_time - earliest_time
    duration_in_hours = duration.total_seconds() / 3600

    print(f"the log goes from {earliest_time} to {latest_time}, which is {int(duration_in_hours+1)} hours")

    return duration_in_hours

file_name = "data/final_log_final.txt"

log_data = to_dict(file_name)
log_duration_hours = calculate_log_duration_hours(log_data)
print(f"Total log duration: {int(log_duration_hours+1)} hours") # round


datetime_objects = to_datetime(log_data)
datetime_counts = Counter(datetime_objects)
most_active_hours = find_most_active_timeframes(datetime_counts, 'hourly', 20)
print("Most Active Hours:")
for datetime, count in most_active_hours:
    print(f"{datetime}: {count} messages")

# analyze_log_file(file_name)
