import pandas as pd
import random
import os

# Function to load CSV file
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

# Load the preferences CSV file
preferences_df = load_csv(r'C:\Users\Aswin\OneDrive\Documents\Learning\skintonePreference.csv')
if preferences_df is None:
    exit()

# Strip any leading/trailing whitespace from the column names
preferences_df.columns = preferences_df.columns.str.strip()

# Normalize the 'Skintone' column to lowercase and strip whitespace
preferences_df['Skintone'] = preferences_df['Skintone'].str.lower().str.strip()

# Function to get random colors for a given skintone
def get_random_colors(skintone):
    skintone = skintone.lower().strip()
    
    # Filter the preferences data by the given skintone
    matching_colors = preferences_df[preferences_df['Skintone'] == skintone]['Colour'].tolist()
    
    # Check if there are at least two colors
    if len(matching_colors) < 2:
        print(f"Not enough colors available for skintone: {skintone}")
        return []

    # Randomly select two colors
    random_colors = random.sample(matching_colors, 2)
    
    return random_colors

def get_next_serial_number(output_file_path):
    if os.path.isfile(output_file_path):
        # Load the existing CSV file to get the highest serial number
        try:
            existing_df = pd.read_csv(output_file_path)
            if not existing_df.empty and 'SerialNumber' in existing_df.columns:
                max_serial_number = existing_df['SerialNumber'].max()
                return max_serial_number + 1
        except pd.errors.EmptyDataError:
            return 1
    return 1

# Example input skintone
input_skintone = 'Dark skintone'
random_colors = get_random_colors(input_skintone)

# Check if random colors were successfully selected
if not random_colors:
    print("No colors available for the given skintone.")
    exit()

# Print the randomly selected colors
print(f"Randomly selected colors for {input_skintone}: {random_colors}")

# Get the next serial number
output_file_path = r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\random_colors.csv'
serial_number = get_next_serial_number(output_file_path)

# Prepare the result with serial number
result = {'SerialNumber': serial_number, 'Color1': random_colors[0], 'Color2': random_colors[1]}
result_df = pd.DataFrame([result])

# Append the result to the CSV file
if os.path.isfile(output_file_path):
    result_df.to_csv(output_file_path, mode='a', header=False, index=False)
else:
    result_df.to_csv(output_file_path, index=False)

print(f"Random colors saved to {output_file_path}")
