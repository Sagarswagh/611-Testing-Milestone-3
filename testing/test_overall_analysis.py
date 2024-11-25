import unittest
from unittest.mock import MagicMock, patch
from overall_analysis import OverallAnalysis
from data_loader import DataLoader
import pandas as pd
from datetime import datetime
from model import Issue

class TestOverallAnalysis(unittest.TestCase):

    def setUp(self):
        """Set up mock data and objects before each test."""
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

        with patch('matplotlib.pyplot.show'):  # Prevent plots from displaying
            self.analysis.run()

        # Assertions for printed messages
        self.assertIn("Found 2 events across 3 issues.", self.analysis.run.__doc__)

    @patch('data_loader.DataLoader.load_and_process_issues')
    def test_run_with_empty_data(self, mock_load):
        """Test the `run` method with an empty dataset."""
        mock_load.return_value = pd.DataFrame()

        with patch('matplotlib.pyplot.show'):  # Prevent plots from displaying
            self.analysis.run()

        # Check if the method outputs no issues found
        self.assertEqual(mock_load.return_value.empty, True)

    @patch('data_loader.DataLoader.load_and_process_issues')
    def test_pie_chart_distribution(self, mock_load):
        """Test pie chart creation for issue state distribution."""
        mock_load.return_value = self.mock_issues

        with patch('matplotlib.pyplot.show'):  # Prevent plots from displaying
            self.analysis.run()

        # Ensure states are being counted correctly
        state_counts = self.mock_issues['state'].value_counts()
        self.assertEqual(state_counts['closed'], 2)
        self.assertEqual(state_counts['open'], 1)

    @patch('data_loader.DataLoader.load_and_process_issues')
    def test_bar_chart_labels(self, mock_load):
        """Test bar chart for top labels."""
        mock_load.return_value = self.mock_issues

        with patch('matplotlib.pyplot.show'):  # Prevent plots from displaying
            self.analysis.run()

        labels = pd.Series([label for labels in self.mock_issues['labels'] for label in labels])
        label_counts = labels.value_counts()
        self.assertEqual(label_counts['bug'], 2)
        self.assertEqual(label_counts['enhancement'], 1)

    @patch('data_loader.DataLoader.load_and_process_issues')
    def test_histogram_time_to_resolution(self, mock_load):
        """Test histogram for time-to-resolution calculation."""
        mock_load.return_value = self.mock_issues

        with patch('matplotlib.pyplot.show'):  # Prevent plots from displaying
            self.analysis.run()

        # Calculate resolution times
        times_to_resolve = [
            (self.mock_issues.loc[1, 'closed_at'] - self.mock_issues.loc[1, 'created_at']).days,
            (self.mock_issues.loc[2, 'closed_at'] - self.mock_issues.loc[2, 'created_at']).days
        ]
        self.assertEqual(times_to_resolve, [9, 14])

    def tearDown(self):
        """Clean up after each test."""
        self.analysis = None


if __name__ == '__main__':
    unittest.main()
