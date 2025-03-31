import os
import subprocess
import csv

# Define the paths to the existing scripts
shoulder_waist_script = r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\Shoulder & waistline Detection system.py'
facial_shape_script = r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\facial shape detection system.py'
fitness_check_script = r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\fitnessComparision system.py'

# Define the paths to the additional processing scripts
skintone_script = r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\skintoneColorComparision system.py'
waistline_bottom_script = r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\compare waistline to bottom cut.py'
shoulder_sleeve_script = r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\compare shoulder to sleeve.py'
facial_neckline_script = r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\Compare facial shape to necklines.py'

# Define the path to the pre-prompt script
pre_prompt_script = r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\save_last_row.py'

# Define the path to the Bing image search script
bing_image_search_script = r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\bing_image_search.py'

# Define image path
image_folder = r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\input_images'
image_path = os.path.join(image_folder, 'input_image.jpg')  # Ensure the image is named 'input_image.jpg'

# Define the path to the output CSV file
output_csv_path = r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\last_rows_combined_output.csv'

# Function to execute a script with the given arguments
def run_script(script_path, *args):
    result = subprocess.run(["python", script_path] + list(args), capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {script_path}: {result.stderr}")
        return False
    else:
        print(f"Output from {script_path}: {result.stdout}")
        return True

# Ensure the image exists
if not os.path.exists(image_path):
    print(f"Error: Image not found at {image_path}")
else:
    # Prompt the user for additional information in the terminal
    height = input("Enter your height (in feet): ")
    weight_kg = input("Enter your weight (in kilograms): ")
    shirt_size = input("Enter your shirt size (e.g., XS, S, M, L, XL, XXL, XXXL): ")
    gender = input("Enter your gender (male/female/other): ")
    skintone = input("Enter your skintone (light/medium/olive/tan/dark): ")
    occasion = input("Enter the occasion: ")

    # Run the shoulder and waistline detection script
    if not run_script(shoulder_waist_script, image_path):
        exit()

    # Run the facial shape detection script
    if not run_script(facial_shape_script, image_path):
        exit()
    
    # Run the fitness check script
    if not run_script(fitness_check_script, height, weight_kg, shirt_size):
        exit()

    # Run the additional processing scripts
    if not run_script(skintone_script):
        exit()
    if not run_script(waistline_bottom_script):
        exit()
    if not run_script(shoulder_sleeve_script):
        exit()
    if not run_script(facial_neckline_script):
        exit()

    # Run the pre-prompt script
    if run_script(pre_prompt_script):
        # Read the output CSV file and append the occasion and gender to the last row
        with open(output_csv_path, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
        
        # Append gender and occasion to the last row
        if rows:
            gender_dress = f"{gender} dress"
            last_row = rows[-1]
            updated_row = [gender_dress, occasion] + last_row[2:]  # Adding gender + "dress" and occasion to the first and second columns
            
            # Replace the last row with updated_row
            rows[-1] = updated_row
        
        # Write back to the CSV file
        with open(output_csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        
        print(f"Occasion and gender added to {output_csv_path}")

        # Run the Bing image search script
        run_script(bing_image_search_script)
        
        print("Bing image search completed.")

    else:
        print("Error in running the pre-prompt script.")

    print("Image processed successfully by all scripts, and fitness data saved.")
