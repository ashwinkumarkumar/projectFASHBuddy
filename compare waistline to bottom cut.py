import pandas as pd
import random
import os

def load_csv(filepath):
    try:
        df = pd.read_csv(filepath)
        print(f"Loaded {filepath} successfully.")
        return df
    except pd.errors.ParserError as e:
        print(f"Error parsing {filepath}: {e}")
    except pd.errors.EmptyDataError as e:
        print(f"No columns to parse from {filepath}: {e}")
    except Exception as e:
        print(f"An error occurred while loading {filepath}: {e}")
    return None

# Load the first CSV file (detection data)
detection_df = load_csv(r'C:\Users\Aswin\OneDrive\Documents\Learning\pose_estimation_data.csv')
if detection_df is None:
    exit()

# Load the second CSV file (waistline preferences)
preferences_df = load_csv(r'C:\Users\Aswin\OneDrive\Documents\Learning\waistline_preference.csv')
if preferences_df is None:
    exit()

# Strip any leading/trailing whitespace from the column names
detection_df.columns = detection_df.columns.str.strip()
preferences_df.columns = preferences_df.columns.str.strip()

# Get the last row of the detection data
last_row = detection_df.iloc[-1]
detected_waist_type = last_row['WaistType']

# Print debug information
print("Detected Waist Type:", detected_waist_type)

# Ensure all strings are compared in lowercase
preferences_df['Waistline'] = preferences_df['Waistline'].str.lower().str.strip()
detected_waist_type = detected_waist_type.lower().strip()

# Filter the preferences data by the detected waist type
matching_preferences = preferences_df[preferences_df['Waistline'].str.contains(detected_waist_type, case=False)]

# Print debug information
print("Matching Preferences:\n", matching_preferences)

# Initialize an empty list to store the results
results = []

# Append only the BottomCut to the results list
for _, pref_row in matching_preferences.iterrows():
    results.append({
        'SerialNumber': last_row['SerialNumber'],
        'BottomCut': pref_row['Bottom Cut']
    })

# Randomly select two bottom cuts for each detected waist type
bottom_cuts = list(set(row['BottomCut'] for row in results))
random_bottom_cuts = random.sample(bottom_cuts, min(2, len(bottom_cuts)))

# Prepare the final result with incremented serial number and both bottom cuts in the same row
final_result = {
    'SerialNumber': last_row['SerialNumber'],
    'BottomCut1': random_bottom_cuts[0] if len(random_bottom_cuts) > 0 else '',
    'BottomCut2': random_bottom_cuts[1] if len(random_bottom_cuts) > 1 else ''
}

# Convert the final result to a DataFrame
final_result_df = pd.DataFrame([final_result])

# Define the output file path
output_file_path = r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\recommendation_results_waistline.csv'

# Check if the output CSV file already exists
if os.path.isfile(output_file_path):
    existing_df = pd.read_csv(output_file_path)
    # Get the next serial number
    if not existing_df.empty:
        next_serial_number = existing_df['SerialNumber'].max() + 1
    else:
        next_serial_number = 1
    
    # Update the serial number in the final result DataFrame
    final_result_df['SerialNumber'] = next_serial_number
    combined_df = pd.concat([existing_df, final_result_df], ignore_index=True).drop_duplicates()
else:
    # If the file does not exist, use the final result DataFrame and start serial number from 1
    final_result_df['SerialNumber'] = 1
    combined_df = final_result_df

# Save the combined DataFrame to the CSV file
combined_df.to_csv(output_file_path, index=False)

print("Recommendations saved to recommendation_results_waistline.csv")

