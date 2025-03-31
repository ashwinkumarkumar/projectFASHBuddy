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

# Load the detection CSV file
detection_df = load_csv(r'C:\Users\Aswin\OneDrive\Documents\Learning\face_shape_results.csv')
if detection_df is None:
    exit()

# Load the preference CSV file
preferences_df = load_csv(r'C:\Users\Aswin\OneDrive\Documents\Learning\facial_shape_preference.csv')
if preferences_df is None:
    exit()

# Strip any leading/trailing whitespace from the column names
detection_df.columns = detection_df.columns.str.strip()
preferences_df.columns = preferences_df.columns.str.strip()

# Get the last row of the detection data
last_row = detection_df.iloc[-1]
detected_face_shape = last_row['FaceShape']

# Print debug information
print("Detected Face Shape:", detected_face_shape)

# Ensure all strings are compared in lowercase
preferences_df['FaceShape'] = preferences_df['FaceShape'].str.lower().str.strip()
detected_face_shape = detected_face_shape.lower().strip()

# Filter the preferences data by the detected face shape
matching_preferences = preferences_df[preferences_df['FaceShape'].str.contains(detected_face_shape, case=False)]

# Print debug information
print("Matching Preferences:\n", matching_preferences)

# Initialize an empty list to store the results
results = []

# Append the results to the list
for _, pref_row in matching_preferences.iterrows():
    results.append({
        'SerialNumber': last_row['SerialNumber'],
        'Necklines': pref_row['Necklines']
    })

# Randomly select two unique necklines from the results
unique_necklines = list(set(row['Necklines'] for row in results))
random_necklines = random.sample(unique_necklines, min(2, len(unique_necklines)))

# Prepare the final result with incremented serial number and both necklines in the same row
final_result = {
    'SerialNumber': last_row['SerialNumber'],
    'Necklines': ', '.join(random_necklines)
}

# Convert the final result to a DataFrame
final_result_df = pd.DataFrame([final_result])

# Define the output file path
output_file_path = r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\face_shape_recommendations.csv'

# Check if the output CSV file already exists
if os.path.isfile(output_file_path) and os.path.getsize(output_file_path) > 0:
    try:
        existing_df = pd.read_csv(output_file_path)
        # Get the next serial number
        if not existing_df.empty:
            next_serial_number = existing_df['SerialNumber'].max() + 1
        else:
            next_serial_number = 1
        
        # Update the serial number in the final result DataFrame
        final_result_df['SerialNumber'] = next_serial_number
        combined_df = pd.concat([existing_df, final_result_df], ignore_index=True).drop_duplicates()
    except pd.errors.EmptyDataError:
        combined_df = final_result_df
else:
    # If the file does not exist or is empty, use the final result DataFrame and start serial number from 1
    final_result_df['SerialNumber'] = 1
    combined_df = final_result_df

# Save the combined DataFrame to the CSV file
combined_df.to_csv(output_file_path, index=False)

print("Recommendations saved to face_shape_recommendations.csv")

