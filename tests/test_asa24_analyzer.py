import os
import unittest
import pandas as pd
import tempfile
from src.asa24_analyzer import ASA24Analyzer

class TestASA24Analyzer(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
        self.analyzer = ASA24Analyzer(self.test_data_dir)

    def test_load_data(self):
        # Test that data is loaded correctly
        self.assertIn('Totals', self.analyzer.data)
        self.assertEqual(len(self.analyzer.data['Totals']), 3)
        self.assertEqual(len(self.analyzer.subjects), 2)
        self.assertTrue('test_user1' in self.analyzer.subjects)
        self.assertTrue('test_user2' in self.analyzer.subjects)

    def test_get_nutrient_summary(self):
        # Test getting nutrient summary for all subjects
        summary = self.analyzer.get_nutrient_summary()
        self.assertEqual(len(summary), 3)  # 3 total records
        self.assertIn(('test_user1', 'Visit 1'), summary.index)
        self.assertIn(('test_user2', 'Visit 1'), summary.index)

        # Print columns for debugging
        print("Columns in summary:", summary.columns.tolist())
        
        # Test nutrient values for a specific record
        test_user1_visit1 = summary.loc[('test_user1', 'Visit 1')]
        self.assertEqual(test_user1_visit1['KCAL'], 2000)  # Use original column name
        self.assertEqual(test_user1_visit1['PROT'], 75)    # Use original column name
        self.assertEqual(test_user1_visit1['TFAT'], 65)    # Use original column name
        
        # Test Omega-3 fatty acids and other nutrients
        self.assertEqual(test_user1_visit1['OMEGA3'], 1.6)  # Omega-3 Fatty Acids
        self.assertEqual(test_user1_visit1['DHA'], 0.5)     # DHA
        self.assertEqual(test_user1_visit1['EPA'], 0.5)     # EPA
        self.assertEqual(test_user1_visit1['ALA'], 1.6)     # ALA

        # Test filtering by subjects
        filtered_summary = self.analyzer.get_nutrient_summary(subjects=['test_user1'])
        self.assertEqual(len(filtered_summary), 2)  # Only test_user1's records
        self.assertNotIn(('test_user2', 'Visit 1'), filtered_summary.index)

    def test_get_nutrient_summary_empty_data(self):
        # Create a temporary empty directory
        with tempfile.TemporaryDirectory() as temp_dir:
            empty_analyzer = ASA24Analyzer(temp_dir)
            summary = empty_analyzer.get_nutrient_summary()
            self.assertTrue(summary.empty)
            
    def test_get_food_groups_summary(self):
        # Test getting food groups summary for all subjects
        summary = self.analyzer.get_food_groups_summary()
        self.assertEqual(len(summary), 3)  # 3 total records
        self.assertIn(('test_user1', 'Visit 1'), summary.index)
        self.assertIn(('test_user2', 'Visit 1'), summary.index)
        
        # Test filtering by subjects
        filtered_summary = self.analyzer.get_food_groups_summary(subjects=['test_user1'])
        self.assertEqual(len(filtered_summary), 2)  # Only test_user1's records
        self.assertNotIn(('test_user2', 'Visit 1'), filtered_summary.index)
        
    def test_get_meal_summary(self):
        # Test getting meal summary
        summary = self.analyzer.get_meal_summary()
        
        # Check that we have the expected number of meal entries
        # 3 meals for test_user1 visit 1, 3 meals for test_user1 visit 2, 3 meals for test_user2 visit 1
        self.assertEqual(len(summary), 9)
        
        # Check that specific meals exist
        self.assertIn(('test_user1', 'Visit 1', 'Breakfast'), summary.index)
        self.assertIn(('test_user1', 'Visit 1', 'Lunch'), summary.index)
        self.assertIn(('test_user1', 'Visit 1', 'Dinner'), summary.index)
        
        # Check meal statistics
        breakfast = summary.loc[('test_user1', 'Visit 1', 'Breakfast')]
        self.assertEqual(breakfast['Number of Items'], 2)
        self.assertEqual(breakfast['Calories'], 255)
        
        # Test filtering by subjects
        filtered_summary = self.analyzer.get_meal_summary(subjects=['test_user1'])
        self.assertEqual(len(filtered_summary), 6)  # 6 meals for test_user1 (3 per visit)
        self.assertNotIn(('test_user2', 'Visit 1', 'Breakfast'), filtered_summary.index)
        
    def test_get_detailed_food_items(self):
        # Test getting detailed food items
        food_items = self.analyzer.get_detailed_food_items()
        
        # Check that we have all food items
        self.assertEqual(len(food_items), 15)  # Total number of food items in test data
        
        # Check that food items have the expected columns
        expected_columns = ['UserName', 'RecallNo', 'Occ_Name', 'Food_Description', 
                           'FoodAmt', 'KCAL', 'PROT', 'TFAT', 'CARB', 'Meal', 'Visit']
        for col in expected_columns:
            self.assertIn(col, food_items.columns)
        
        # Check specific food item details
        oatmeal = food_items[(food_items['UserName'] == 'test_user1') & 
                             (food_items['Food_Description'] == 'Oatmeal')].iloc[0]
        self.assertEqual(oatmeal['KCAL'], 150)
        self.assertEqual(oatmeal['Meal'], 'Breakfast')
        
        # Test filtering by subjects
        filtered_items = self.analyzer.get_detailed_food_items(subjects=['test_user1'])
        self.assertEqual(len(filtered_items), 10)  # Only test_user1's food items
        self.assertTrue(all(filtered_items['UserName'] == 'test_user1'))
        
    def test_get_supplement_summary(self):
        # Test getting supplement summary
        supplements = self.analyzer.get_supplement_summary()
        
        # Check that we have all supplement records
        self.assertEqual(len(supplements), 6)  # Total number of supplement records in test data
        
        # Check that supplement data has the expected columns
        expected_columns = ['UserName', 'RecallNo', 'IntakeStartDateTime', 'Suppl_Description', 
                           'SupplAmount', 'SupplUnit', 'Visit']
        for col in expected_columns:
            self.assertIn(col, supplements.columns)
        
        # Check specific supplement details
        vitamin_d = supplements[(supplements['UserName'] == 'test_user1') & 
                               (supplements['Suppl_Description'] == 'Vitamin D')].iloc[0]
        self.assertEqual(vitamin_d['SupplAmount'], 1000)
        self.assertEqual(vitamin_d['SupplUnit'], 'IU')
        self.assertEqual(vitamin_d['Visit'], 'Visit 1')
        
        # Test filtering by subjects
        filtered_supplements = self.analyzer.get_supplement_summary(subjects=['test_user1'])
        self.assertEqual(len(filtered_supplements), 4)  # Only test_user1's supplements
        self.assertTrue(all(filtered_supplements['UserName'] == 'test_user1'))

if __name__ == '__main__':
    unittest.main()