import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from month_issue_analysis import MonthIssueAnalysis

class TestMonthIssueAnalysis(unittest.TestCase):

    @patch('month_issue_analysis.DataLoader')
    def test_empty_issues(self, MockDataLoader):
        """Test behavior when no issues are loaded."""
        # Mock DataLoader to return an empty DataFrame
        MockDataLoader.return_value.load_and_process_issues.return_value = pd.DataFrame()
        
        analysis = MonthIssueAnalysis()
        with patch('builtins.print') as mock_print:
            analysis.run()
            mock_print.assert_called_with("No issues found to analyze.")

    @patch('month_issue_analysis.DataLoader')
    def test_valid_issues(self, MockDataLoader):
        """Test behavior with valid issue data."""
        # Mock DataLoader to return a sample DataFrame
        data = {
            'created_at': [pd.Timestamp('2023-01-15'), pd.Timestamp('2023-02-20')],
            'closed_at': [pd.Timestamp('2023-01-25'), pd.Timestamp('2023-03-10')],
            'state': ['closed', 'closed']
        }
        mock_df = pd.DataFrame(data)
        MockDataLoader.return_value.load_and_process_issues.return_value = mock_df

        analysis = MonthIssueAnalysis()
        with patch('matplotlib.pyplot.show') as mock_show:
            analysis.run()
            mock_show.assert_called_once()  # Ensure the histogram is displayed

    @patch('month_issue_analysis.DataLoader')
    def test_missing_closed_dates(self, MockDataLoader):
        """Test behavior when some issues are not closed."""
        # Mock DataLoader to return a DataFrame with missing closed_at dates
        data = {
            'created_at': [pd.Timestamp('2023-01-15'), pd.Timestamp('2023-02-20')],
            'closed_at': [None, pd.Timestamp('2023-03-10')],
            'state': ['open', 'closed']
        }
        mock_df = pd.DataFrame(data)
        MockDataLoader.return_value.load_and_process_issues.return_value = mock_df

        analysis = MonthIssueAnalysis()
        with patch('matplotlib.pyplot.show') as mock_show:
            analysis.run()
            mock_show.assert_called_once()  # Ensure the histogram is displayed

    def test_opened_closed_issue_extraction(self):
        """Test extraction of opened and closed issue months."""
        data = {
            'created_at': [pd.Timestamp('2023-01-15'), pd.Timestamp('2023-02-20')],
            'closed_at': [pd.Timestamp('2023-01-25'), None],
            'state': ['closed', 'open']
        }
        df = pd.DataFrame(data)

        # Simulate issue extraction logic
        opened_issue_month = df['created_at'].dt.month.tolist()
        closed_issue_month = df[df['state'] == 'closed']['closed_at'].dt.month.tolist()

        self.assertEqual(opened_issue_month, [1, 2])
        self.assertEqual(closed_issue_month, [1])

    

    @patch('month_issue_analysis.DataLoader')
    def test_invalid_data_handling(self, MockDataLoader):
        """Test behavior with invalid or corrupted data."""
        # Mock DataLoader to return a DataFrame with invalid dates
        data = {
            'created_at': ['invalid_date', pd.Timestamp('2023-02-20')],
            'closed_at': [pd.Timestamp('2023-01-25'), None],
            'state': ['closed', 'open']
        }
        mock_df = pd.DataFrame(data)
        MockDataLoader.return_value.load_and_process_issues.return_value = mock_df

        analysis = MonthIssueAnalysis()
        
        with self.assertRaises(ValueError):  # Expecting a ValueError due to invalid date parsing
            analysis.run()

    #@patch('month_issue_analysis.DataLoader')
    #def test_user_specific_events(self, MockDataLoader):
       # """Test behavior when a specific user is provided."""
        # Mock DataLoader to return a sample DataFrame
        
    

if __name__ == '__main__':
    unittest.main() # pragma: no cover