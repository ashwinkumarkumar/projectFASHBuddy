import pandas as pd

# List of input CSV file paths
csv_files = [
    r'C:\Users\Aswin\OneDrive\Documents\Learning\recommendation_results.csv',
    r'C:\Users\Aswin\OneDrive\Documents\Learning\recommendation_results_waistline.csv',
    r'C:\Users\Aswin\OneDrive\Documents\Learning\face_shape_recommendations.csv',
    r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\fitnessStatus.csv',
    r'C:\Users\Aswin\OneDrive\Documents\Learning\random_colors.csv'
]

# Initialize an empty list to hold the DataFrames with only the last row
last_rows = []

# Load each CSV file, get the last row, and append it to the list
for file in csv_files:
    df = pd.read_csv(file)
    last_row = df.tail(1)  # Get the last row as a DataFrame
    last_rows.append(last_row)

# Merge all DataFrames on the 'SerialNumber' column
merged_df = last_rows[0]
for df in last_rows[1:]:
    merged_df = pd.merge(merged_df, df, on='SerialNumber', how='inner')

# Drop the 'SerialNumber' column
merged_df.drop(columns=['SerialNumber'], inplace=True)

# Extract the row values as a list of lists
row_values = merged_df.values.tolist()

# Flatten the list of lists into a single list
flattened_values = [item for sublist in row_values for item in sublist]

# Save the flattened values to a new CSV file
output_file_path = r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\pre_prompt.csv'
with open(output_file_path, 'w') as file:
    file.write(','.join(map(str, flattened_values)))

print(f"Merged data saved to {output_file_path}")

# Print the merged data to verify the output
print(flattened_values)
