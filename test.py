import random

# Define the path to your log file
log_file_path = '/Users/marian/Desktop/Hackatum/loganalysis/max/dora_the_logexplorer/data/test_log1_modified.txt'

# Generate 100 unique names
random_names = [f'User{i:03}' for i in range(50)]

# Read the existing log file
with open(log_file_path, 'r') as file:
    lines = file.readlines()

# Generate 100 new log entries with unique names
new_entries = [f'crucial attack from {name} system shutting down\n' for name in random_names]

# Insert new log entries at random positions
for entry in new_entries:
    insert_position = random.randint(0, len(lines))
    lines.insert(insert_position, entry)

# Write the modified content back to the file
with open(log_file_path, 'w') as file:
    file.writelines(lines)

print("Log file updated successfully.")
