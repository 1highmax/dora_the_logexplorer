def check_usernames_in_file(file_path, total_usernames):
    # Read the text file
    with open(file_path, 'r') as file:
        content = file.read()

    # Count usernames found
    found_count = 0
    for i in range(total_usernames):
        username = f'User{i:03}'
        if username in content:
            found_count += 1

    # Calculate percentage
    percentage_found = (found_count / total_usernames) * 100
    return percentage_found

# Define the path to your log file
log_file_path = 'results.txt'

# Call the function and print the result
percentage = check_usernames_in_file(log_file_path, 100)
print(f"Percentage of usernames found at least once: {percentage:.2f}%")
