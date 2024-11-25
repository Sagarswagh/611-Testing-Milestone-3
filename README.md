# ENPM611 Project Group 2
This project contains a set of analysis that can be run against issues from the Poetry repo. These analysis were made to help contributors to poetry understand and visualize various statistics of issues.


### Install dependencies

In the root directory of the application, create a virtual environment, activate that environment, and install the dependencies like so:

```
pip install -r requirements.txt
```

### Download and configure the data file

Ensure you have a json data file of the poetry issues on github. Update the `config.json` with the path to the file.


### Run an analysis

With everything set up, you should be able to run various analysis.

Analysis One:
Analysis of most common labels from issues in poetry.
```
python run.py --feature 0
```

Analysis Two:
Analysis of most closed issues by user and labels. Can pass user or label arguments.
```
python run.py --feature 1 --user radoering
```
Analysis Three:
Analysis of monthly closed and opened issues.
```
python run.py --feature 2
```
Analysis Four:
Analysis of average time it takes to close various types of issues.
```
python run.py --feature 3
```

<h2>Testing</h2>

<h3>Test Strategy</h3>
<p>
  The testing strategy for this project includes unit tests and integration tests to ensure the correctness of the implemented functionalities and visualizations. The tests are designed to verify various scenarios using both mock data and real-world data examples.
</p>

<h3>Test Implementation</h3>
<p>
  Unit tests for this project are located in the <code>testing/</code> folder. They include tests for data filtering, visualization generation, and analytics computation. Tests also cover edge cases such as missing data, invalid data, and scenarios where no issues match the filtering criteria.
</p>

<h3>Running Tests</h3>
<p>To run the tests and generate a coverage report, use the following commands:</p>

<h4>Run All Tests</h4>
<pre>
<code>python -m coverage run -m unittest discover -s testing</code>
</pre>

<h4>View Coverage Report</h4>
<pre>
<code>python -m coverage report --omit="test_*"</code>
</pre>

<h4>Generate Specific Coverage Report</h4>
<p>To view the coverage for a specific file, use:</p>
<pre>
<code>get_specific_coverage_report('issue_close_time_analysis.py')</code>
</pre>

<h3>Testing Results</h3>

<h4>Key Observations</h4>
<ul>
  <li><strong>Coverage:</strong> The overall code coverage achieved during testing was 95%.</li>
  <li><strong>Performance:</strong> Average close times for various labels were computed successfully for most scenarios. However, errors were observed in cases with invalid or missing data.</li>
  <li><strong>Failures:</strong> Some tests failed due to:
    <ul>
      <li>Missing attributes in corrupted datasets (e.g., strings instead of <code>datetime</code> objects in <code>created_at</code>).</li>
      <li>Incorrect assumptions about the data in the test cases (e.g., no closed issues or missing columns in the dataset).</li>
    </ul>
  </li>
  <li><strong>Edge Cases:</strong> Scenarios with empty or null data were handled correctly, with appropriate error messages being logged.</li>
</ul>
