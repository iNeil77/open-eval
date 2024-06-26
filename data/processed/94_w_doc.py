import pandas as pd
from random import randint, uniform, seed

def task_func(categories=None, months=None, random_seed=42):
    """
    Generates a DataFrame with simulated monthly sales data for various product categories, ensuring reproducibility through the use of a random seed.

    Parameters:
        categories (list of str, optional): A list specifying the product categories to include in the report. If not provided, defaults to ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Beauty & Personal Care'].
        months (list of str, optional): A list specifying the months to include in the report. If not provided, defaults to ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'].
        random_seed (int, optional): The seed value for the random number generator to ensure the reproducibility of the sales data. Defaults to 42.

    Returns:
        pandas.DataFrame: A DataFrame with three columns: 'Month', 'Category', and 'Sales'. The 'Sales' values are floating-point numbers in the range [100, 501), generated by the formula: randint(100, 500) + uniform(0, 1), ensuring sales values are diverse yet consistent upon repeated executions with the same seed.

    Raises:
        ValueError: If either 'categories' or 'months' is not provided as a list or if either is an empty list.

    Notes:
        - The function sets the random seed at the beginning of execution to ensure that the generated sales data is the same for any given seed value.
        - The sales data for each category is generated for each month, creating a comprehensive report that spans all specified categories and months.

    Requirements:
    - pandas 
    - random

    Example:
        >>> report = task_func()
        >>> print(report.head())
             Month                Category       Sales
        0  January             Electronics  427.111331
        1  January                Clothing  479.275029
        2  January          Home & Kitchen  214.139538
        3  January                   Books  152.676699
        4  January  Beauty & Personal Care  379.086939
    """
    if categories is None:
        categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Beauty & Personal Care']
    if months is None:
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    if not isinstance(categories, list) or not categories:
        raise ValueError("Invalid 'categories': must be a non-empty list.")
    if not isinstance(months, list) or not months:
        raise ValueError("Invalid 'months': must be a non-empty list.")
    seed(random_seed)  # Setting the seed for reproducibility
    sales_data = []
    for month in months:
        for category in categories:
            sales = randint(100, 500) + uniform(0, 1)
            sales_data.append([month, category, sales])
    sales_df = pd.DataFrame(sales_data, columns=['Month', 'Category', 'Sales'])
    return sales_df

import unittest
import pandas as pd
import os
class TestCases(unittest.TestCase):
    def tearDown(self) -> None:
        if os.path.exists('df_contents.txt'):
            os.remove('df_contents.txt')
    def test_reproducibility(self):
        df1 = task_func(random_seed=42)
        df2 = task_func(random_seed=42)
        pd.testing.assert_frame_equal(df1, df2)
    def test_dataframe_structure(self):
        df = task_func()
        self.assertEqual(list(df.columns), ['Month', 'Category', 'Sales'])
        self.assertEqual(len(df), 60)  # 12 months * 5 categories
    def test_invalid_categories(self):
        with self.assertRaises(ValueError):
            task_func(categories="Not a list")
    def test_invalid_months(self):
        with self.assertRaises(ValueError):
            task_func(months=123)
    def test_custom_categories_and_months(self):
        custom_categories = ['A', 'B', 'C']
        custom_months = ['Jan', 'Feb']
        df = task_func(categories=custom_categories, months=custom_months)
        self.assertEqual(len(df), len(custom_categories) * len(custom_months))
        self.assertTrue(set(df['Category']).issubset(custom_categories))
        self.assertTrue(set(df['Month']).issubset(custom_months))
    def test_values(self):
        df = task_func()
        df_list = df.apply(lambda row: ','.join(row.values.astype(str)), axis=1).tolist()
        with open('df_contents.txt', 'w') as file:
            file.write(str(df_list))
        
        expect = ['January,Electronics,427.11133106816567', 'January,Clothing,479.2750293183691', 'January,Home & Kitchen,214.13953792852516', 'January,Books,152.67669948742292', 'January,Beauty & Personal Care,379.0869388326294', 'February,Electronics,316.0317826794818', 'February,Clothing,147.2186379748036', 'February,Home & Kitchen,358.60201872905', 'February,Books,387.19883765068664', 'February,Beauty & Personal Care,432.70132497359026', 'March,Electronics,314.2204406220407', 'March,Clothing,401.2781907082307', 'March,Home & Kitchen,103.75880736712976', 'March,Books,181.69813939498823', 'March,Beauty & Personal Care,274.27787134167164', 'April,Electronics,210.95721307220677', 'April,Clothing,272.1022102765198', 'April,Home & Kitchen,294.09671637683346', 'April,Books,276.6037260313669', 'April,Beauty & Personal Care,122.72973178669382', 'May,Electronics,374.1248261628532', 'May,Clothing,293.07880019807845', 'May,Home & Kitchen,250.829404664253', 'May,Books,416.8854517479368', 'May,Beauty & Personal Care,285.5773521452568', 'June,Electronics,460.0695551488237', 'June,Clothing,438.22789827565157', 'June,Home & Kitchen,248.98522152066076', 'June,Books,219.86648366675527', 'June,Beauty & Personal Care,294.27797360311007', 'July,Electronics,425.83411042664073', 'July,Clothing,183.37018096711688', 'July,Home & Kitchen,207.6701751743777', 'July,Books,459.9366545877125', 'July,Beauty & Personal Care,431.07140250957855', 'August,Electronics,425.1711386481981', 'August,Clothing,473.2448109251514', 'August,Home & Kitchen,336.37945544175767', 'August,Books,427.68816195843334', 'August,Beauty & Personal Care,212.68461425098988', 'September,Electronics,493.77599991154625', 'September,Clothing,217.8218025940068', 'September,Home & Kitchen,261.4011647870223', 'September,Books,133.21098284358632', 'September,Beauty & Personal Care,390.87636762647264', 'October,Electronics,261.21262654405416', 'October,Clothing,355.39563190106065', 'October,Home & Kitchen,429.4588518525874', 'October,Books,235.1396303195255', 'October,Beauty & Personal Care,481.56136813416316', 'November,Electronics,234.74701381165227', 'November,Clothing,319.8978228836025', 'November,Home & Kitchen,304.3619964437136', 'November,Books,170.50952629367646', 'November,Beauty & Personal Care,146.75578215753373', 'December,Electronics,156.15284131934825', 'December,Clothing,181.79207936436296', 'December,Home & Kitchen,316.596409030732', 'December,Books,297.3816192865065', 'December,Beauty & Personal Care,339.5291143450991']
        self.assertEqual(df_list, expect, "DataFrame contents should match the expected output")
