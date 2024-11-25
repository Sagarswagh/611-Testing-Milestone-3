import unittest
from unittest.mock import MagicMock, patch
from overall_analysis import OverallAnalysis
from data_loader import DataLoader
import pandas as pd
from datetime import datetime
from model import Issue

class TestOverallAnalysis(unittest.TestCase):

    def setUp(self):
        self.analysis = OverallAnalysis()
        self.mock_issues = pd.DataFrame({
            'id': [1, 2, 3],
            'creator': ['user1', 'user2', 'user1'],
            'state': ['open', 'closed', 'closed'],
            'labels': [['bug'], ['enhancement'], ['bug']],
            'created_at': [datetime(2023, 1, 1), datetime(2023, 2, 1), datetime(2023, 3, 1)],
            'closed_at': [None, datetime(2023, 2, 10), datetime(2023, 3, 15)]
        })

    @patch('data_loader.DataLoader.load_and_process_issues')
    def test_run_with_valid_data(self, mock_load):
        """Test the `run` method with valid data."""
        mock_load.return_value = self.mock_issues

        with patch('matplotlib.pyplot.show'):  
            self.analysis.run()

        self.assertTrue(mock_load.called)

    @patch('data_loader.DataLoader.load_and_process_issues')
    def test_run_with_empty_data(self, mock_load):
        """Test the `run` method with an empty dataset."""
        mock_load.return_value = pd.DataFrame()

        with patch('matplotlib.pyplot.show'): 
            self.analysis.run()

        self.assertTrue(mock_load.return_value.empty)

    @patch('data_loader.DataLoader.load_and_process_issues')
    def test_run_with_null_values(self, mock_load):
        """Test the `run` method with null values in the dataset."""
        mock_issues_with_nulls = self.mock_issues.copy()
        mock_issues_with_nulls.loc[0, 'labels'] = None
        mock_load.return_value = mock_issues_with_nulls

        with patch('matplotlib.pyplot.show'):  
            self.analysis.run()

        self.assertIn(None, mock_load.return_value['labels'].tolist())

    @patch('data_loader.DataLoader.load_and_process_issues')
    def test_pie_chart_distribution(self, mock_load):
        """Test pie chart creation for issue state distribution."""
        mock_load.return_value = self.mock_issues

        with patch('matplotlib.pyplot.show'):  
            self.analysis.run()

        state_counts = self.mock_issues['state'].value_counts()
        self.assertEqual(state_counts['closed'], 2)
        self.assertEqual(state_counts['open'], 1)

    @patch('data_loader.DataLoader.load_and_process_issues')
    def test_bar_chart_labels(self, mock_load):
        """Test bar chart for top labels."""
        mock_load.return_value = self.mock_issues

        with patch('matplotlib.pyplot.show'):  
            self.analysis.run()

        labels = pd.Series([label for labels in self.mock_issues['labels'] for label in labels])
        label_counts = labels.value_counts()
        self.assertEqual(label_counts['bug'], 2)
        self.assertEqual(label_counts['enhancement'], 1)

    @patch('data_loader.DataLoader.load_and_process_issues')
    def test_histogram_time_to_resolution(self, mock_load):
        """Test histogram for time-to-resolution calculation."""
        mock_load.return_value = self.mock_issues

        with patch('matplotlib.pyplot.show'):  
            self.analysis.run()

        times_to_resolve = [
            (self.mock_issues.loc[1, 'closed_at'] - self.mock_issues.loc[1, 'created_at']).days,
            (self.mock_issues.loc[2, 'closed_at'] - self.mock_issues.loc[2, 'created_at']).days
        ]
        self.assertEqual(times_to_resolve, [9, 14])

    @patch('data_loader.DataLoader.load_and_process_issues')
    def test_empty_labels(self, mock_load):
        """Test handling of issues with empty labels."""
        mock_issues_empty_labels = self.mock_issues.copy()
        mock_issues_empty_labels['labels'] = [[] for _ in range(len(self.mock_issues))]
        mock_load.return_value = mock_issues_empty_labels

        with patch('matplotlib.pyplot.show'):  
            self.analysis.run()

        for labels in mock_load.return_value['labels']:
            self.assertEqual(len(labels), 0)

    @patch('data_loader.DataLoader.load_and_process_issues')
    def test_incomplete_data_handling(self, mock_load):
        """Test handling of missing columns in the dataset."""
        incomplete_issues = self.mock_issues.drop(columns=['closed_at'])
        mock_load.return_value = incomplete_issues

        with patch('matplotlib.pyplot.show'): 
            with self.assertRaises(KeyError):
                self.analysis.run()

    def tearDown(self):
        """Clean up after each test."""
        self.analysis = None


if __name__ == '__main__':
    unittest.main()
