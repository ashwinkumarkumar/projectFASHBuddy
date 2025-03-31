import pandas as pd

# Paths to the CSV files
csv_files = [
    r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\fitnessStatus.csv',
    r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\random_colors.csv',
    r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\face_shape_recommendations.csv',
    r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\recommendation_results.csv',
    r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\recommendation_results_waistline.csv'
]

# Path to the output CSV file
output_file = r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\last_rows_combined_output.csv'

# Create an empty list to store the last row elements
last_row_elements = []

# Iterate through each CSV file
for file_path in csv_files:
    df = pd.read_csv(file_path)
    if not df.empty:
        # Get the last row
        last_row = df.iloc[[-1]]
        # Exclude the 'SerialNumber' column if it exists
        if 'SerialNumber' in last_row.columns:
            last_row = last_row.drop(columns=['SerialNumber'])
        # Convert the last row to a list and extend it to the combined list
        last_row_elements.extend(last_row.values.flatten().tolist())

# Create a DataFrame with a single row
output_df = pd.DataFrame([last_row_elements])

# Save the output DataFrame to the output CSV file without headers
output_df.to_csv(output_file, index=False, header=False)

print(f"Last rows combined and saved to {output_file}")
