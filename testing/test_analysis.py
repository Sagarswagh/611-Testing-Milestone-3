import unittest
from unittest.mock import patch
import pandas as pd
from analysis import Analysis


class TestAnalysis(unittest.TestCase):
    def setUp(self):
        self.mock_data = [
            {
                "creator": "dbrtly",
                "labels": ["kind/bug", "status/triage"],
                "closed_at": pd.Timestamp("2024-10-20"),
                "created_at": pd.Timestamp("2024-10-15"),
            },
            {
                "creator": "srittau",
                "labels": ["area/docs", "status/triage"],
                "closed_at": None,
                "created_at": pd.Timestamp("2024-10-19"),
            },
        ]
        self.mock_df = pd.DataFrame(self.mock_data)

    def test_filter_issues_by_label(self):
        analysis=Analysis()
        filtered_df=analysis.filter_issues(self.mock_df,label="kind/bug")
        self.assertEqual(len(filtered_df), 1)
        self.assertEqual(filtered_df.iloc[0]["labels"], "kind/bug")

    def test_filter_issues_by_creator(self):
        analysis=Analysis()
        filtered_df=analysis.filter_issues(self.mock_df,creator="dbrtly")
        self.assertEqual(len(filtered_df),2)

    def test_empty_dataframe(self):
        analysis=Analysis()
        empty_df=pd.DataFrame()
        with patch("builtins.print") as mock_print:
            analysis.analyze_and_visualize(empty_df,empty_df)
            mock_print.assert_called_once_with(
                "No issues found for the specified label and/or creator. Analysis and visualization skipped."
            )

    def test_no_closed_issues(self):
        analysis=Analysis()
        filtered_df=self.mock_df[self.mock_df["closed_at"].isna()]
        with patch("builtins.print") as mock_print:
            analysis.analyze_and_visualize(filtered_df, self.mock_df)
            mock_print.assert_any_call("No closed issues found. Average time to close cannot be calculated.")

    def test_explode_labels(self):
        analysis= Analysis()
        with patch("builtins.print") as mock_print:
            filtered_df=self.mock_df.explode("labels")
            analysis.analyze_and_visualize(filtered_df, self.mock_df)
            avg_time_to_close=5.0
            mock_print.assert_any_call(f"Average time to close (days): {avg_time_to_close:.2f}")

    def test_no_labels_for_creator(self):
        analysis=Analysis()
        filtered_df = pd.DataFrame({
            "creator": ["new_user"],
            "labels": [None],
            "closed_at": [pd.Timestamp("2024-10-21")],
            "created_at": [pd.Timestamp("2024-10-20")],
        })
        with patch("builtins.print") as mock_print:
            analysis.analyze_and_visualize(filtered_df, self.mock_df)
            mock_print.assert_any_call("No labels found for user 'new_user'.")


    def test_valid_visualization(self):
        analysis=Analysis()
        filtered_df=self.mock_df[~self.mock_df["closed_at"].isna()]
        with patch("matplotlib.pyplot.show") as mock_show:
            analysis.analyze_and_visualize(filtered_df, self.mock_df)
            mock_show.assert_called()

    def test_labels_distribution_visualization(self):
        analysis=Analysis()
        filtered_df=self.mock_df[self.mock_df["creator"] == "dbrtly"]
        with patch("matplotlib.pyplot.show") as mock_show:
            analysis.analyze_and_visualize(filtered_df, self.mock_df)
            mock_show.assert_called()


if __name__ == "__main__":
    unittest.main()
