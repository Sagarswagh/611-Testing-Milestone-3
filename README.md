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

Testing
Unit tests for this project are located in the tests/ folder. The tests include mock data for various scenarios to ensure the correctness of the code.

Running Tests
To run the tests and generate a coverage report, follow these steps:

Run the tests with coverage:

To execute the tests and measure code coverage, use the following command:


python -m coverage run -m unittest discover
This command will automatically find and run all tests in the tests/ folder.

View the coverage report:

After running the tests, you can view the code coverage report using this command:


python -m coverage report --omit="test_*"
This will show you the coverage for the application code while excluding the test files.

Specific Coverage Report:

To view the coverage for a specific file (e.g., issue_close_time_analysis.py), you can run:


python -m unittest discover
Or, for detailed analysis, you can call the specific coverage report directly for feature 1:


get_specific_coverage_report('issue_close_time_analysis.py')
This function will filter and print the specific coverage information for the given file.