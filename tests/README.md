# Tests for MOMMA-ASA24-22-Data-Analyzer

This directory contains tests for the MOMMA-ASA24-22-Data-Analyzer project.

## Test Structure

- `test_asa24_analyzer.py`: Tests for the `ASA24Analyzer` class in `src/asa24_analyzer.py`
- `test_data/`: Directory containing test data files

## Running Tests

To run the tests, use the following command from the project root directory:

```bash
python -m pytest tests/
```

To run tests with coverage information:

```bash
python -m pytest --cov=src tests/
```

## Test Coverage

The tests currently cover the core data processing functionality of the `ASA24Analyzer` class:

- `load_data`: Loading data from CSV files
- `get_nutrient_summary`: Getting nutrient summary data
- `get_food_groups_summary`: Getting food group summary data
- `get_supplement_summary`: Getting supplement data
- `get_meal_summary`: Getting meal summary data
- `get_detailed_food_items`: Getting detailed food item data

## Test Data

The `test_data` directory contains CSV files with sample data for testing:

- `test_Totals.csv`: Sample data for nutrient and food group summaries
- `test_Items.csv`: Sample data for meal and food item details
- `test_INS.csv`: Sample data for supplement information

## Future Improvements

Future test improvements could include:

1. Testing the `calculate_hei_2015` method for Healthy Eating Index calculations
2. Testing the UI-related functions like `show_glossary` and `main`
3. Testing the utility function `convert_df_to_excel`
4. Adding more edge cases and error handling tests