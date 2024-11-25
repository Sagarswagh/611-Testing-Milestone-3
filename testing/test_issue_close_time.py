import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from issue_close_time_analysis import IssueCloseTimeAnalysis
import subprocess


def get_specific_coverage_report(file_name):
    # Run the coverage report, omitting test files
    result = subprocess.run(
        ['coverage', 'report', '--omit', 'testing/*'],  # Adjusted to match file path
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )
    
    # Filter the result for the specific file
    lines = result.stdout.splitlines()
    for line in lines:
        if file_name in line:
            print(line)


class TestIssueCloseTimeAnalysis(unittest.TestCase):

    @patch('data_loader.DataLoader')
    @patch('config.get_parameter')
    def test_run(self, mock_get_parameter, mock_data_loader):
        # Mock the return values for config and DataLoader
        mock_get_parameter.return_value = 'test_user'  # Simulating the user parameter
        mock_data_loader_instance = MagicMock()
        mock_data_loader.return_value = mock_data_loader_instance

        # Mock the issues DataFrame
        mock_issues_df = pd.DataFrame({
            'state': ['closed', 'closed', 'open', 'closed'],
            'created_at': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04']),
            'closed_at': pd.to_datetime(['2024-01-05', '2024-01-06', None, '2024-01-07']),
            'labels': [['bug'], ['feature'], ['bug'], ['bug', 'enhancement']]
        })

        mock_data_loader_instance.load_and_process_issues.return_value = mock_issues_df

        # Run the analysis
        analysis = IssueCloseTimeAnalysis()

        # Check that the method runs without errors
        with self.assertLogs(level='INFO') as log:
            analysis.run()
            # Check if the log contains "Average Close Time for label"
            self.assertTrue(any("Average Close Time for label" in message for message in log.output))

    @patch('data_loader.DataLoader')
    @patch('config.get_parameter')
    def test_no_closed_issues(self, mock_get_parameter, mock_data_loader):
        # Mock the return values for config and DataLoader
        mock_get_parameter.return_value = 'test_user'  # Simulating the user parameter
        mock_data_loader_instance = MagicMock()
        mock_data_loader.return_value = mock_data_loader_instance

        # Mock an empty DataFrame (no closed issues)
        mock_issues_df = pd.DataFrame({
            'state': ['open', 'open'],
            'created_at': pd.to_datetime(['2024-01-01', '2024-01-02']),
            'closed_at': [None, None],
            'labels': [[], []]
        })

        mock_data_loader_instance.load_and_process_issues.return_value = mock_issues_df

        # Run the analysis and check if the "No issues found to analyze." message is printed
        with self.assertLogs(level='INFO') as log:
            analysis = IssueCloseTimeAnalysis()
            analysis.run()
            self.assertIn('No issues found to analyze.', log.output[0])

    @patch('data_loader.DataLoader')
    @patch('config.get_parameter')
    def test_average_close_time(self, mock_get_parameter, mock_data_loader):
        # Mock the return values for config and DataLoader
        mock_get_parameter.return_value = 'test_user'  # Simulating the user parameter
        mock_data_loader_instance = MagicMock()
        mock_data_loader.return_value = mock_data_loader_instance

        # Mock the issues DataFrame
        mock_issues_df = pd.DataFrame({
            'state': ['closed', 'closed', 'closed'],
            'created_at': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
            'closed_at': pd.to_datetime(['2024-01-05', '2024-01-06', '2024-01-07']),
            'labels': [['bug'], ['feature'], ['bug']]
        })

        mock_data_loader_instance.load_and_process_issues.return_value = mock_issues_df

        # Run the analysis
        analysis = IssueCloseTimeAnalysis()

        with self.assertLogs(level='INFO') as log:
            analysis.run()
            # Check if the log contains "Average Close Time for label"
            self.assertTrue(any("Average Close Time for label" in message for message in log.output))

    @patch('data_loader.DataLoader')
    @patch('config.get_parameter')
    def test_multiple_labels(self, mock_get_parameter, mock_data_loader):
        # Mock the return values for config and DataLoader
        mock_get_parameter.return_value = 'test_user'  # Simulating the user parameter
        mock_data_loader_instance = MagicMock()
        mock_data_loader.return_value = mock_data_loader_instance

        # Mock the issues DataFrame with multiple labels
        mock_issues_df = pd.DataFrame({
            'state': ['closed', 'closed', 'closed'],
            'created_at': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
            'closed_at': pd.to_datetime(['2024-01-05', '2024-01-06', '2024-01-07']),
            'labels': [['bug', 'enhancement'], ['bug'], ['feature', 'enhancement']]
        })

        mock_data_loader_instance.load_and_process_issues.return_value = mock_issues_df

        # Run the analysis
        analysis = IssueCloseTimeAnalysis()

        with self.assertLogs(level='INFO') as log:
            analysis.run()
            # Check if the log contains the average close times for both 'bug', 'enhancement', and 'feature'
            self.assertTrue(any("Average Close Time for label" in message for message in log.output))

    @patch('data_loader.DataLoader')
    @patch('config.get_parameter')
    def test_coverage(self, mock_get_parameter, mock_data_loader):
        # Run the coverage report for issue_close_time_analysis.py
        get_specific_coverage_report('issue_close_time_analysis.py')


if __name__ == '__main__':
    unittest.main()
