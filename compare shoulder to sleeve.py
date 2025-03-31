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

# Load the second CSV file (preferences)
preferences_df = load_csv(r'C:\Users\Aswin\OneDrive\Documents\Learning\shoulderTypeVsSleeveType.csv')
if preferences_df is None:
    exit()

# Strip any leading/trailing whitespace from the column names
detection_df.columns = detection_df.columns.str.strip()
preferences_df.columns = preferences_df.columns.str.strip()

# Get the last row of the detection data
last_row = detection_df.iloc[-1]
detected_shoulder_type = last_row['ShoulderType']

# Print debug information
print("Detected Shoulder Type:", detected_shoulder_type)

# Ensure all strings are compared in lowercase
preferences_df['ShoulderType'] = preferences_df['ShoulderType'].str.lower().str.strip()
detected_shoulder_type = detected_shoulder_type.lower().strip()

# Filter the preferences data by the detected shoulder type
matching_preferences = preferences_df[preferences_df['ShoulderType'].str.contains(detected_shoulder_type, case=False)]

# Print debug information
print("Matching Preferences:\n", matching_preferences)

# Initialize an empty list to store the results
results = []

# Append only the SleeveType to the results list
for _, pref_row in matching_preferences.iterrows():
    results.append({
        'SerialNumber': last_row['SerialNumber'],
        'SleeveType': pref_row['Sleeve type']
    })

# Randomly select two sleeve types for each detected shoulder type
sleeve_types = list(set(row['SleeveType'] for row in results))
random_sleeve_types = random.sample(sleeve_types, min(2, len(sleeve_types)))

# Prepare the final result with incremented serial number and both sleeve types in the same row
final_result = {
    'SerialNumber': last_row['SerialNumber'],
    'SleeveType1': random_sleeve_types[0] if len(random_sleeve_types) > 0 else '',
    'SleeveType2': random_sleeve_types[1] if len(random_sleeve_types) > 1 else ''
}

# Convert the final result to a DataFrame
final_result_df = pd.DataFrame([final_result])

# Define the output file path
output_file_path = r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\face_shape_recommendations.csv'

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

print("Recommendations saved to recommendation_results.csv")
