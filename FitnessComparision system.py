import sys
import pandas as pd
import os

def calculate_bmi(height, weight_kg):
    height_in = height * 12  # Convert height from feet to inches
    bmi = (weight_kg / (height_in ** 2)) * 703 * 0.453592  # Convert pounds to kilograms
    return bmi

def determine_body_type(height, weight_kg, shirt_size):
    height_ranges = {
        (5.0, 5.2): ["XS", "S", "M"],
        (5.3, 5.5): ["S", "M", "L"],
        (5.6, 5.8): ["M", "L", "XL"],
        (5.9, 6.1): ["L", "XL", "XXL"],
        (6.2, 6.5): ["XL", "XXL", "XXXL"]
    }
    
    bmi = calculate_bmi(height, weight_kg)
    if bmi < 18.5:
        bmi_result = "Thin"
    elif 18.5 <= bmi < 25:
        bmi_result = "Fit"
    else:
        bmi_result = "Fat"
    
    height_ft = int(height)
    height_in = (height - height_ft) * 12
    height_inches = height_ft + height_in / 12
    
    for (min_height, max_height), sizes in height_ranges.items():
        if min_height <= height_inches <= max_height:
            if shirt_size in ["XS", "S", "M"]:
                height_weight_result = "Thin"
            elif shirt_size in sizes:
                height_weight_result = "Fit"
            else:
                height_weight_result = "Fat"
            break
    else:
        height_weight_result = "Unknown"
    
    if height_weight_result == "Thin" and bmi_result == "Fat":
        final_result = bmi_result
    elif height_weight_result == "Fat" and bmi_result == "Thin":
        final_result = bmi_result
    else:
        final_result = height_weight_result
    
    return final_result

def get_next_serial_number(output_csv_path):
    if os.path.isfile(output_csv_path):
        existing_df = pd.read_csv(output_csv_path)
        if not existing_df.empty and 'SerialNumber' in existing_df.columns:
            max_serial_number = existing_df['SerialNumber'].max()
            return max_serial_number + 1
        else:
            return 1
    return 1

def save_fitness_data(height, weight_kg, shirt_size, output_csv_path):
    serial_number = get_next_serial_number(output_csv_path)
    fitness = determine_body_type(height, weight_kg, shirt_size)
    if fitness == "Fit":
        result = {'SerialNumber': serial_number, 'Fitness': ''}
    else:
        result = {'SerialNumber': serial_number, 'Fitness': fitness}
    
    result_df = pd.DataFrame([result])
    
    if os.path.isfile(output_csv_path):
        result_df.to_csv(output_csv_path, mode='a', header=False, index=False)
    else:
        result_df.to_csv(output_csv_path, index=False)
    
    print(f"Result saved to {output_csv_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python fitness_check.py <height> <weight_kg> <shirt_size>")
        sys.exit(1)
    
    height = float(sys.argv[1])
    weight_kg = float(sys.argv[2])
    shirt_size = sys.argv[3]
    output_csv_path = 'fitnessStatus.csv'
    
    save_fitness_data(height, weight_kg, shirt_size, output_csv_path)

