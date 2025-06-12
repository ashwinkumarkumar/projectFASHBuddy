# FASHBuddy
A brief description of the project.

## Description
This project includes various scripts for analyzing body shapes, fitness comparisons, and generating fashion recommendations based on user inputs.

## Features
- Image search using Bing API to find fashion-related images.
- Facial shape detection and recommendations for necklines.
- Shoulder and waistline detection with recommendations for clothing styles.
- Fitness comparison based on user height, weight, and shirt size.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
- To run the Bing image search:
  ```bash
  python bing_image_search.py
  ```
- To analyze facial shape:
  ```bash
  python facial shape detection system.py <image_path>
  ```
- To analyze shoulder and waistline:
  ```bash
  python Shoulder & waistline Detection system.py <image_path>
  ```
- To check fitness:
  ```bash
  python FitnessComparision system.py <height> <weight_kg> <shirt_size>
  ```

## Script Overview
- **bing_image_search.py**: Searches for images based on a query and saves them.
- **facial shape detection system.py**: Detects facial landmarks and classifies face shapes.
- **Shoulder & waistline Detection system.py**: Estimates shoulder and waist lengths and classifies body types.
- **Compare facial shape to necklines.py**: Recommends necklines based on detected face shapes.
- **compare waistline to bottom cut.py**: Recommends bottom cuts based on waist types.
- **FitnessComparision system.py**: Calculates BMI and determines body type.
- **compare shoulder to sleeve.py**: Recommends sleeve types based on shoulder types.
- **pre_prompt.py**: Merges results from various analyses into a single CSV file.

## License
This project is licensed under the MIT License.
