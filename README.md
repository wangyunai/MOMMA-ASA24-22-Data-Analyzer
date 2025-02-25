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

1. Place your ASA24 data files in a directory
2. Run the Streamlit application:
```bash
streamlit run src/asa24_analyzer.py
```

3. Access the web interface at http://localhost:8501

## Data Analysis Features

1. **Nutrient Summary**
   - View and compare nutrient intake across visits
   - Interactive visualizations
   - Export data to Excel

2. **Food Groups**
   - Analyze food group consumption
   - Compare intake patterns
   - Track dietary diversity

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