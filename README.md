# MOMMA ASA24-22 Data Analyzer

A Streamlit-based web application for analyzing ASA24 (Automated Self-Administered 24-Hour Dietary Assessment) data.

## Features

- Multi-subject analysis support
- Interactive data visualization
- Nutrient intake analysis
- Food group analysis
- Meal pattern analysis
- Supplement tracking
- Excel export functionality

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MOMMA-ASA24-22-Data-Analyzer.git
cd MOMMA-ASA24-22-Data-Analyzer
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Create a directory for your ASA24 data files (e.g., `data`)
2. Place your ASA24 CSV files in the data directory
3. Run the Streamlit application:
```bash
streamlit run src/asa24_analyzer.py
```
4. Access the web interface at http://localhost:8501
5. In the sidebar, enter the path to your data directory (e.g., "data" or absolute path)

### Example Directory Structure
```
your-project-directory/
├── data/
│   ├── MOMMA_*_INS.csv
│   ├── MOMMA_*_Items.csv
│   ├── MOMMA_*_Responses.csv
│   ├── MOMMA_*_TNS.csv
│   ├── MOMMA_*_TS.csv
│   └── MOMMA_*_Totals.csv
└── src/
    └── asa24_analyzer.py
```

## Data Analysis Features

1. **Nutrient Summary**
   - View and compare nutrient intake across visits
   - Track neurodevelopment-related nutrients (Omega-3, Choline, etc.)
   - Interactive visualizations
   - Export data to Excel

2. **Food Groups**
   - Analyze food group consumption
   - Compare intake patterns
   - Track dietary diversity
   - Comprehensive food group coverage

3. **Supplements**
   - Monitor supplement intake
   - Track compliance
   - Export supplement records

4. **Meal Analysis**
   - Analyze meal patterns
   - Compare meal composition
   - Visualize eating occasions

5. **Detailed Food Items**
   - View individual food items
   - Track portion sizes
   - Export detailed records

6. **Healthy Eating Index (HEI-2015)**
   - Calculate HEI-2015 scores
   - Track diet quality
   - Visualize component scores
   - Compare scores across visits
   - Export HEI analysis

## File Structure

```
MOMMA-ASA24-22-Data-Analyzer/
├── src/
│   └── asa24_analyzer.py
├── docs/
│   └── user_guide.md
├── tests/
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.