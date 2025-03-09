import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime
from io import BytesIO

class ASA24Analyzer:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.data = {}
        self.subjects = set()
        self.load_data()

    def load_data(self):
        """Load all ASA24 CSV files into dataframes"""
        for file in os.listdir(self.data_dir):
            if file.endswith('.csv'):
                name = file.split('_')[-1].replace('.csv', '')
                df = pd.read_csv(os.path.join(self.data_dir, file))
                self.data[name] = df
                if 'UserName' in df.columns:
                    self.subjects.update(df['UserName'].unique())

    def get_nutrient_summary(self, subjects=None):
        """Get summary of daily nutrient intake"""
        if 'Totals' in self.data:
            df = self.data['Totals']
            if subjects:
                df = df[df['UserName'].isin(subjects)]
            
            key_nutrients = {
                'Energy (kcal)': 'KCAL',
                'Protein (g)': 'PROT',
                'Total Fat (g)': 'TFAT',
                'Carbohydrate (g)': 'CARB',
                'Fiber (g)': 'FIBE',
                'Sugar (g)': 'SUGR',
                'Calcium (mg)': 'CALC',
                'Iron (mg)': 'IRON',
                'Vitamin C (mg)': 'VC',
                'Vitamin D (mcg)': 'VITD',
                'Vitamin A (mcg)': 'VARA',
                'Vitamin B12 (mcg)': 'VB12',
                'Folate (mcg)': 'FOLA',
                'Sodium (mg)': 'SODI',
                'Potassium (mg)': 'POTA',
                'Omega-3 Fatty Acids (g)': 'OMEGA3',
                'Choline (mg)': 'CHOLINE',
                'Iodine (mcg)': 'IODINE',
                'Zinc (mg)': 'ZINC',
                'DHA (g)': 'DHA',
                'EPA (g)': 'EPA',
                'ALA (g)': 'ALA',
                'Selenium (mcg)': 'SELENIUM',
                'Magnesium (mg)': 'MAGNESIUM'
            }
            
            summary = df[['UserName', 'RecallNo', 'IntakeStartDateTime'] + list(key_nutrients.values())].copy()
            summary['IntakeStartDateTime'] = pd.to_datetime(summary['IntakeStartDateTime'])
            summary['Visit'] = 'Visit ' + summary['RecallNo'].astype(str)
            
            summary = summary.rename(columns=key_nutrients)
            return summary.set_index(['UserName', 'Visit'])
        return pd.DataFrame()

    def get_food_groups_summary(self, subjects=None):
        """Get summary of food groups intake"""
        if 'Totals' in self.data:
            df = self.data['Totals']
            if subjects:
                df = df[df['UserName'].isin(subjects)]
            
            food_groups = {
                'Total Fruits (cup eq)': 'F_TOTAL',
                'Citrus/Melons/Berries (cup eq)': 'F_CITMLB',
                'Other Fruits (cup eq)': 'F_OTHER',
                'Total Vegetables (cup eq)': 'V_TOTAL',
                'Dark Green Vegetables (cup eq)': 'V_DRKGR',
                'Red/Orange Vegetables (cup eq)': 'V_REDOR_TOTAL',
                'Total Grains (oz eq)': 'G_TOTAL',
                'Whole Grains (oz eq)': 'G_WHOLE',
                'Refined Grains (oz eq)': 'G_REFINED',
                'Total Protein Foods (oz eq)': 'PF_TOTAL',
                'Meat (oz eq)': 'PF_MEAT',
                'Poultry (oz eq)': 'PF_POULT',
                'Seafood (oz eq)': 'PF_SEAFD_HI',
                'Eggs (oz eq)': 'PF_EGGS',
                'Nuts/Seeds (oz eq)': 'PF_NUTSDS',
                'Total Dairy (cup eq)': 'D_TOTAL',
                'Milk (cup eq)': 'D_MILK',
                'Cheese (cup eq)': 'D_CHEESE',
                'Added Sugars (tsp eq)': 'ADD_SUGARS',
                'Oils (g)': 'OILS'
            }
            
            summary = df[['UserName', 'RecallNo', 'IntakeStartDateTime'] + list(food_groups.values())].copy()
            summary['IntakeStartDateTime'] = pd.to_datetime(summary['IntakeStartDateTime'])
            summary['Visit'] = 'Visit ' + summary['RecallNo'].astype(str)
            
            summary = summary.rename(columns=food_groups)
            return summary.set_index(['UserName', 'Visit'])
        return pd.DataFrame()

    def get_supplement_summary(self, subjects=None):
        """Get summary of supplement intake"""
        if 'INS' in self.data:
            df = self.data['INS']
            if subjects:
                df = df[df['UserName'].isin(subjects)]
            
            supplement_info = df[['UserName', 'RecallNo', 'IntakeStartDateTime', 'Suppl_Description', 
                                'SupplAmount', 'SupplUnit']].copy()
            supplement_info['IntakeStartDateTime'] = pd.to_datetime(supplement_info['IntakeStartDateTime'])
            supplement_info['Visit'] = 'Visit ' + supplement_info['RecallNo'].astype(str)
            return supplement_info
        return pd.DataFrame()

    def get_meal_summary(self, subjects=None):
        """Get summary of meals"""
        if 'Items' in self.data:
            df = self.data['Items']
            if subjects:
                df = df[df['UserName'].isin(subjects)]
            
            meal_names = {
                '1': 'Breakfast',
                '2': 'Morning Snack',
                '3': 'Lunch',
                '4': 'Afternoon Snack',
                '5': 'Dinner',
                '6': 'Evening Snack',
                '7': 'Late Evening Snack',
                '8': 'Other Time'
            }
            
            df['Meal'] = df['Occ_Name'].astype(str).map(meal_names)
            meal_summary = df.groupby(['UserName', 'RecallNo', 'Meal']).agg({
                'FoodNum': 'count',
                'KCAL': 'sum',
                'PROT': 'sum',
                'TFAT': 'sum',
                'CARB': 'sum'
            }).round(1)
            
            meal_summary.columns = ['Number of Items', 'Calories', 'Protein (g)', 'Fat (g)', 'Carbs (g)']
            meal_summary = meal_summary.reset_index()
            meal_summary['Visit'] = 'Visit ' + meal_summary['RecallNo'].astype(str)
            return meal_summary.set_index(['UserName', 'Visit', 'Meal'])
        return pd.DataFrame()
        
    def get_detailed_food_items(self, subjects=None):
        """Get detailed food items list"""
        if 'Items' in self.data:
            df = self.data['Items']
            if subjects:
                df = df[df['UserName'].isin(subjects)]
            
            # Create meal name mapping
            meal_names = {
                '1': 'Breakfast',
                '2': 'Morning Snack',
                '3': 'Lunch',
                '4': 'Afternoon Snack',
                '5': 'Dinner',
                '6': 'Evening Snack',
                '7': 'Late Evening Snack',
                '8': 'Other Time'
            }
            
            food_items = df[['UserName', 'RecallNo', 'Occ_Name', 'Food_Description',
                           'FoodAmt', 'KCAL', 'PROT', 'TFAT', 'CARB']].copy()
            food_items['Meal'] = food_items['Occ_Name'].astype(str).map(meal_names)
            food_items['Visit'] = 'Visit ' + food_items['RecallNo'].astype(str)
            return food_items
        return pd.DataFrame()
        
    def calculate_hei_2015(self, subjects=None):
        """Calculate Healthy Eating Index-2015 scores
        
        The HEI-2015 includes 13 components:
        1. Total Fruits (5 points)
        2. Whole Fruits (5 points)
        3. Total Vegetables (5 points)
        4. Greens and Beans (5 points)
        5. Whole Grains (10 points)
        6. Dairy (10 points)
        7. Total Protein Foods (5 points)
        8. Seafood and Plant Proteins (5 points)
        9. Fatty Acids ratio (10 points)
        10. Refined Grains (10 points)
        11. Sodium (10 points)
        12. Added Sugars (10 points)
        13. Saturated Fats (10 points)
        
        Total possible score: 100 points
        """
        if 'Totals' not in self.data:
            return pd.DataFrame()
            
        df = self.data['Totals']
        if subjects:
            df = df[df['UserName'].isin(subjects)]
        
        # Create empty DataFrame for HEI scores
        hei_scores = pd.DataFrame()
        hei_scores['UserName'] = df['UserName']
        hei_scores['Visit'] = 'Visit ' + df['RecallNo'].astype(str)
        
        # Calculate component scores based on density (per 1000 kcal)
        energy_factor = 1000 / df['KCAL']
        
        # 1. Total Fruits (5 points) - ≥0.8 cup eq. per 1,000 kcal
        total_fruits = df['F_TOTAL'] * energy_factor
        hei_scores['Total Fruits'] = (total_fruits / 0.8 * 5).clip(0, 5)
        
        # 2. Whole Fruits (5 points) - ≥0.4 cup eq. per 1,000 kcal
        whole_fruits = (df['F_TOTAL'] - df['F_JUICE']) * energy_factor
        hei_scores['Whole Fruits'] = (whole_fruits / 0.4 * 5).clip(0, 5)
        
        # 3. Total Vegetables (5 points) - ≥1.1 cup eq. per 1,000 kcal
        total_veg = df['V_TOTAL'] * energy_factor
        hei_scores['Total Vegetables'] = (total_veg / 1.1 * 5).clip(0, 5)
        
        # 4. Greens and Beans (5 points) - ≥0.2 cup eq. per 1,000 kcal
        greens_beans = (df['V_DRKGR'] + df['V_LEGUMES']) * energy_factor
        hei_scores['Greens and Beans'] = (greens_beans / 0.2 * 5).clip(0, 5)
        
        # 5. Whole Grains (10 points) - ≥1.5 oz eq. per 1,000 kcal
        whole_grains = df['G_WHOLE'] * energy_factor
        hei_scores['Whole Grains'] = (whole_grains / 1.5 * 10).clip(0, 10)
        
        # 6. Dairy (10 points) - ≥1.3 cup eq. per 1,000 kcal
        dairy = df['D_TOTAL'] * energy_factor
        hei_scores['Dairy'] = (dairy / 1.3 * 10).clip(0, 10)
        
        # 7. Total Protein Foods (5 points) - ≥2.5 oz eq. per 1,000 kcal
        total_protein = df['PF_TOTAL'] * energy_factor
        hei_scores['Total Protein Foods'] = (total_protein / 2.5 * 5).clip(0, 5)
        
        # 8. Seafood and Plant Proteins (5 points) - ≥0.8 oz eq. per 1,000 kcal
        seafood_plant = (df['PF_SEAFD_HI'] + df['PF_NUTSDS']) * energy_factor
        hei_scores['Seafood and Plant Proteins'] = (seafood_plant / 0.8 * 5).clip(0, 5)
        
        # 9. Fatty Acids ((MUFA + PUFA) / SFA) (10 points) - ≥2.5
        # Check if the necessary columns exist
        if 'MUFA' in df.columns and 'PUFA' in df.columns and 'SFA' in df.columns:
            fatty_acids_ratio = (df['MUFA'] + df['PUFA']) / df['SFA']
            hei_scores['Fatty Acids'] = ((fatty_acids_ratio - 1.2) / (2.5 - 1.2) * 10).clip(0, 10)
        else:
            # Use M161 (Oleic acid) + M181 (Linoleic acid) + P183 (Alpha-linolenic acid) for MUFA+PUFA
            # and S040 (Butyric acid) + S060 (Caproic acid) + ... + S180 (Stearic acid) for SFA
            # if available
            if all(col in df.columns for col in ['M161', 'M181', 'P183', 'S040', 'S060', 'S080', 'S100', 'S120', 'S140', 'S160', 'S180']):
                mufa_pufa = df['M161'] + df['M181'] + df['P183']
                sfa = df['S040'] + df['S060'] + df['S080'] + df['S100'] + df['S120'] + df['S140'] + df['S160'] + df['S180']
                fatty_acids_ratio = mufa_pufa / sfa
                hei_scores['Fatty Acids'] = ((fatty_acids_ratio - 1.2) / (2.5 - 1.2) * 10).clip(0, 10)
            else:
                # If we don't have the necessary columns, assign a default score
                hei_scores['Fatty Acids'] = 5  # Default middle score
        
        # 10. Refined Grains (10 points) - ≤1.8 oz eq. per 1,000 kcal
        refined_grains = df['G_REFINED'] * energy_factor
        hei_scores['Refined Grains'] = ((4.3 - refined_grains) / (4.3 - 1.8) * 10).clip(0, 10)
        
        # 11. Sodium (10 points) - ≤1.1 gram per 1,000 kcal
        sodium = df['SODI'] * energy_factor / 1000  # Convert to grams
        hei_scores['Sodium'] = ((2.0 - sodium) / (2.0 - 1.1) * 10).clip(0, 10)
        
        # 12. Added Sugars (10 points) - ≤6.5% of energy
        added_sugars_perc = df['ADD_SUGARS'] * 4 * 100 / df['KCAL']  # Convert to % of energy
        hei_scores['Added Sugars'] = ((26 - added_sugars_perc) / (26 - 6.5) * 10).clip(0, 10)
        
        # 13. Saturated Fats (10 points) - ≤8% of energy
        if 'SFA' in df.columns:
            sat_fat_perc = df['SFA'] * 9 * 100 / df['KCAL']  # Convert to % of energy
        elif 'SFAT' in df.columns:
            sat_fat_perc = df['SFAT'] * 9 * 100 / df['KCAL']  # Convert to % of energy
        else:
            # Use individual saturated fatty acids if available
            if all(col in df.columns for col in ['S040', 'S060', 'S080', 'S100', 'S120', 'S140', 'S160', 'S180']):
                sfa = df['S040'] + df['S060'] + df['S080'] + df['S100'] + df['S120'] + df['S140'] + df['S160'] + df['S180']
                sat_fat_perc = sfa * 9 * 100 / df['KCAL']
            else:
                # Default to a middle value if we can't calculate
                sat_fat_perc = 12  # Middle value between 8 and 16
        
        hei_scores['Saturated Fats'] = ((16 - sat_fat_perc) / (16 - 8) * 10).clip(0, 10)
        
        # Calculate total HEI score
        hei_scores['Total HEI Score'] = hei_scores.drop(['UserName', 'Visit'], axis=1).sum(axis=1)
        
        return hei_scores.set_index(['UserName', 'Visit'])

def show_glossary(page_type="general"):
    """Show relevant abbreviations and terms based on the page type"""
    with st.expander("📚 Click here to see abbreviations and terms"):
        if page_type == "nutrients":
            st.markdown("""
            ### Nutrient Abbreviations
            - **KCAL**: Kilocalories (Energy)
            - **PROT**: Protein
            - **TFAT**: Total Fat
            - **CARB**: Carbohydrates
            - **FIBE**: Dietary Fiber
            - **SUGR**: Total Sugars
            - **CALC**: Calcium
            - **IRON**: Iron
            - **VC**: Vitamin C
            - **VITD**: Vitamin D
            - **VARA**: Vitamin A
            - **VB12**: Vitamin B12
            - **FOLA**: Folate
            - **SODI**: Sodium
            - **POTA**: Potassium
            - **OMEGA3**: Omega-3 Fatty Acids
            - **CHOLINE**: Choline
            - **IODINE**: Iodine
            - **ZINC**: Zinc
            - **DHA**: Docosahexaenoic Acid (Omega-3)
            - **EPA**: Eicosapentaenoic Acid (Omega-3)
            - **ALA**: Alpha-Linolenic Acid (Omega-3)
            - **SELENIUM**: Selenium
            - **MAGNESIUM**: Magnesium
            
            ### Units
            - **g**: grams
            - **mg**: milligrams
            - **mcg**: micrograms
            - **kcal**: kilocalories
            """)
        elif page_type == "food_groups":
            st.markdown("""
            ### Food Group Abbreviations
            - **F_**: Fruit related measures
                - **F_TOTAL**: Total Fruits
                - **F_CITMLB**: Citrus, Melons, and Berries
                - **F_OTHER**: Other Fruits
            - **V_**: Vegetable related measures
                - **V_TOTAL**: Total Vegetables
                - **V_DRKGR**: Dark Green Vegetables
                - **V_REDOR**: Red and Orange Vegetables
            - **G_**: Grain related measures
                - **G_TOTAL**: Total Grains
                - **G_WHOLE**: Whole Grains
                - **G_REFINED**: Refined Grains
            - **PF_**: Protein Foods
                - **PF_TOTAL**: Total Protein Foods
                - **PF_MEAT**: Meat
                - **PF_POULT**: Poultry
                - **PF_SEAFD**: Seafood
                - **PF_EGGS**: Eggs
                - **PF_NUTSDS**: Nuts and Seeds
            - **D_**: Dairy related measures
                - **D_TOTAL**: Total Dairy
                - **D_MILK**: Milk
                - **D_CHEESE**: Cheese
            
            ### Units
            - **cup eq**: Cup Equivalent
            - **oz eq**: Ounce Equivalent
            - **tsp eq**: Teaspoon Equivalent
            - **g**: grams
            """)
        elif page_type == "meals":
            st.markdown("""
            ### Meal Names
            - **Breakfast**: First meal of the day
            - **Morning Snack**: Mid-morning snack
            - **Lunch**: Midday meal
            - **Afternoon Snack**: Mid-afternoon snack
            - **Dinner**: Evening meal
            - **Evening Snack**: After dinner snack
            - **Late Evening Snack**: Late night snack
            - **Other Time**: Meals at other times
            
            ### Nutrient Measures
            - **KCAL**: Kilocalories (Energy)
            - **PROT**: Protein (g)
            - **TFAT**: Total Fat (g)
            - **CARB**: Carbohydrates (g)
            """)
        else:
            st.markdown("""
            ### General Terms
            - **ASA24**: Automated Self-Administered 24-Hour Dietary Assessment Tool
            - **Visit**: The dietary recall visit number
            - **UserName**: Unique identifier for each participant
            - **IntakeStartDateTime**: Start date and time of the dietary recall period
            """)

def convert_df_to_excel(df):
    """Convert dataframe to Excel bytes for download"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=True, sheet_name='Sheet1')
    return output.getvalue()

def main():
    st.set_page_config(
        page_title="ASA24 Data Analyzer Demo",
        page_icon="🥗",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Add custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 0rem 1rem;
        }
        .stButton>button {
            width: 100%;
        }
        .reportview-container .main .block-container {
            padding-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("ASA24 Data Analyzer Demo")
    
    # Demo notice
    st.info("""
    👋 Welcome to the ASA24 Data Analyzer Demo!
    
    This is a demonstration version using sample data. For analyzing your own data:
    1. Download the code from [GitHub Repository](https://github.com/wangyunai/MOMMA-ASA24-22-Data-Analyzer)
    2. Follow the installation instructions in the README
    3. Run locally with your own ASA24 data
    """)

    # Use demo data directory
    demo_data_dir = "demo_data"
    analyzer = ASA24Analyzer(demo_data_dir)

    # Subject selection in sidebar
    st.sidebar.title("Subject Selection")
    available_subjects = sorted(list(analyzer.subjects))
    selected_subjects = st.sidebar.multiselect(
        "Select subjects to analyze",
        available_subjects,
        default=available_subjects
    )

    if not selected_subjects:
        st.warning("Please select at least one subject to analyze.")
        return

    # Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Analysis Type", 
        ["About",
         "Nutrient Summary",
         "Food Groups",
         "Supplements",
         "Meals",
         "Food Items",
         "Healthy Eating Index"])

    if page == "About":
        st.header("About ASA24 Data Analyzer")
        st.write("""
        This tool helps analyze dietary recall data collected using the ASA24 
        (Automated Self-Administered 24-Hour Dietary Assessment Tool).
        
        ### Features
        - 📊 Analyze nutrient intake
        - 🥗 Track food group consumption
        - 💊 Monitor supplement use
        - 🕒 Examine meal patterns
        - 📈 Visualize trends
        - 📥 Export data to Excel
        
        ### How to Use
        1. Select subjects from the sidebar
        2. Choose an analysis type
        3. View data tables and visualizations
        4. Download reports as needed
        
        ### Sample Data
        The demo includes sample data from the MOMMA study, showing:
        - Multiple subjects
        - Multiple recall days
        - Various nutrients and food groups
        - Supplement intake
        - Meal patterns
        """)

    elif page == "Nutrient Summary":
        st.header("Nutrient Summary")
        show_glossary("nutrients")
        df = analyzer.get_nutrient_summary(selected_subjects)
        st.dataframe(df)
        
        excel_data = convert_df_to_excel(df)
        st.download_button(
            label="Download Nutrient Summary as Excel",
            data=excel_data,
            file_name="nutrient_summary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.subheader("Visualize Nutrients")
        nutrients = [col for col in df.columns if col not in ['IntakeStartDateTime']]
        selected_nutrient = st.selectbox("Select nutrient to visualize", nutrients)
        
        fig = px.line(df.reset_index(), x='Visit', y=selected_nutrient, 
                     color='UserName', markers=True,
                     title=f'{selected_nutrient} over Visits')
        fig.update_xaxes(tickmode='array',
                        ticktext=sorted(df.reset_index()['Visit'].unique()),
                        tickvals=sorted(df.reset_index()['Visit'].unique()))
        st.plotly_chart(fig)

    elif page == "Food Groups":
        st.header("Food Groups Summary")
        show_glossary("food_groups")
        df = analyzer.get_food_groups_summary(selected_subjects)
        st.dataframe(df)
        
        excel_data = convert_df_to_excel(df)
        st.download_button(
            label="Download Food Groups Summary as Excel",
            data=excel_data,
            file_name="food_groups_summary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.subheader("Visualize Food Groups")
        food_groups = [col for col in df.columns if col not in ['IntakeStartDateTime']]
        selected_group = st.selectbox("Select food group to visualize", food_groups)
        
        fig = px.line(df.reset_index(), x='Visit', y=selected_group,
                     color='UserName', markers=True,
                     title=f'{selected_group} over Visits')
        fig.update_xaxes(tickmode='array',
                        ticktext=sorted(df.reset_index()['Visit'].unique()),
                        tickvals=sorted(df.reset_index()['Visit'].unique()))
        st.plotly_chart(fig)

    elif page == "Supplements":
        st.header("Supplement Summary")
        show_glossary("general")
        df = analyzer.get_supplement_summary(selected_subjects)
        st.dataframe(df)
        
        excel_data = convert_df_to_excel(df)
        st.download_button(
            label="Download Supplement Summary as Excel",
            data=excel_data,
            file_name="supplement_summary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    elif page == "Meals":
        st.header("Meal Summary")
        show_glossary("meals")
        df = analyzer.get_meal_summary(selected_subjects)
        st.dataframe(df)
        
        excel_data = convert_df_to_excel(df)
        st.download_button(
            label="Download Meal Summary as Excel",
            data=excel_data,
            file_name="meal_summary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.subheader("Visualize Meals")
        metrics = ['Calories', 'Protein (g)', 'Fat (g)', 'Carbs (g)']
        selected_metric = st.selectbox("Select metric to visualize", metrics)
        
        meal_data = df.reset_index()
        fig = px.bar(meal_data, x='Meal', y=selected_metric,
                    color='UserName', barmode='group',
                    facet_col='Visit',
                    title=f'{selected_metric} by Meal and Visit')
        st.plotly_chart(fig)

    elif page == "Food Items":
        st.header("Detailed Food Items")
        show_glossary("general")
        df = analyzer.get_detailed_food_items(selected_subjects)
        st.dataframe(df)
        
        excel_data = convert_df_to_excel(df)
        st.download_button(
            label="Download Food Items as Excel",
            data=excel_data,
            file_name="food_items.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    elif page == "Healthy Eating Index":
        st.header("Healthy Eating Index (HEI-2015)")
        st.markdown("""
        The Healthy Eating Index (HEI) is a measure of diet quality used to assess how well a set of foods aligns with key recommendations of the Dietary Guidelines for Americans.

        The HEI-2015 includes 13 components that reflect the key recommendations:
        - Adequacy components (higher scores indicate higher consumption):
          - Total Fruits (5 points)
          - Whole Fruits (5 points)
          - Total Vegetables (5 points)
          - Greens and Beans (5 points)
          - Whole Grains (10 points)
          - Dairy (10 points)
          - Total Protein Foods (5 points)
          - Seafood and Plant Proteins (5 points)
          - Fatty Acids ratio (10 points)

        - Moderation components (higher scores indicate lower consumption):
          - Refined Grains (10 points)
          - Sodium (10 points)
          - Added Sugars (10 points)
          - Saturated Fats (10 points)

        Total possible score: 100 points
        """)
        
        df = analyzer.calculate_hei_2015(selected_subjects)
        
        # Display HEI scores
        st.subheader("HEI Component Scores")
        st.dataframe(df)
        
        excel_data = convert_df_to_excel(df)
        st.download_button(
            label="Download HEI Scores as Excel",
            data=excel_data,
            file_name="hei_scores.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Visualization options
        st.subheader("Visualize HEI Scores")
        
        # Total HEI Score visualization
        fig_total = px.line(df.reset_index(), x='Visit', y='Total HEI Score',
                          color='UserName', markers=True,
                          title='Total HEI Score over Visits')
        fig_total.update_xaxes(tickmode='array',
                             ticktext=sorted(df.reset_index()['Visit'].unique()),
                             tickvals=sorted(df.reset_index()['Visit'].unique()))
        st.plotly_chart(fig_total)
        
        # Individual components visualization
        components = [col for col in df.columns if col != 'Total HEI Score']
        selected_component = st.selectbox("Select HEI component to visualize", components)
        
        fig_comp = px.line(df.reset_index(), x='Visit', y=selected_component,
                          color='UserName', markers=True,
                          title=f'{selected_component} Score over Visits')
        fig_comp.update_xaxes(tickmode='array',
                            ticktext=sorted(df.reset_index()['Visit'].unique()),
                            tickvals=sorted(df.reset_index()['Visit'].unique()))
        st.plotly_chart(fig_comp)
        
        # Radar chart for latest visit
        st.subheader("HEI Component Scores Radar Chart")
        latest_visits = df.reset_index().groupby('UserName')['Visit'].max()
        latest_data = df.reset_index().merge(latest_visits, on=['UserName', 'Visit'])
        
        fig_radar = px.line_polar(latest_data, r=components,
                                theta=components,
                                line_close=True,
                                color='UserName',
                                title='HEI Component Scores (Latest Visit)')
        st.plotly_chart(fig_radar)

    # Add footer
    st.markdown("""
    ---
    Made with ❤️ by the MOMMA Study Team | [GitHub Repository](https://github.com/wangyunai/MOMMA-ASA24-22-Data-Analyzer)
    """)

if __name__ == "__main__":
    main()