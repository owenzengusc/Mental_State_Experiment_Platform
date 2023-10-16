# EEG Sensor Interface

This project provides an interface for EEG sensor tests in [Khan Lab @ USC](https://khan.usc.edu/). It allows users to participate in various tests, view instructions, and receive feedback based on their performance.

## Author

- **Owen Zeng**: Sole developer and maintainer of this project. You can contact me at [owenzeng@usc.edu](mailto:owenzeng@usc.edu).

## Features

- **Data File**: Contains the output data and feedback for each test.
- **Test File**: A JSON file that holds information about the available tests.
- **Feedback Screen**: Displays feedback to the user after completing a test.
- **Instruction Screen**: Provides instructions to the user before starting a test.
- **Test Editor**: Allows users to modify, add, or delete tests.
- **Supported Tests**: Currently supports `MathTest` and `StroopTest`.

## File Structure

data/: Contains the output data and feedback.
test/: Contains a JSON file with test configurations.
FeedbackScreen.py: Handles the feedback display after tests.
InstructionScreen.py: Displays instructions before each test.
main.py: The main entry point for the application.
MathTest.py: Logic and interface for the Math Test.
StroopTest.py: Logic and interface for the Stroop Test.
user.py: User-related functionalities.
window.py: Basic window creation and management functions.
test_editor: A utility to modify, add, or delete tests.

## Getting Started

### For macOS Users:

1. Clone the repository:
   ```
   git clone git@github.com:owenzengusc/EEG_Senor_Interface.git
   ```

2. Navigate to the project directory:
   ```
   cd EEG_Senor_Interface
   ```

3. Run the main script:
   ```
   python3 main.py
   ```

### For Windows Users:

**Note**: Before running the script, ensure that Python is added to your PATH. If not, refer to the section below on "Adding Python to PATH on Windows".

**Using Command Prompt (cmd):**

1. Clone the repository:
   ```
   git clone git@github.com:owenzengusc/EEG_Senor_Interface.git
   ```

2. Navigate to the project directory:
   ```
   cd EEG_Senor_Interface
   ```

3. Run the main script:
   ```
   py main.py
   ```

**Using PowerShell:**

1. Clone the repository:
   ```
   git clone git@github.com:owenzengusc/EEG_Senor_Interface.git
   ```

2. Navigate to the project directory:
   ```
   cd EEG_Senor_Interface
   ```

3. Run the main script:
   ```
   py main.py
   ```

**Using Anaconda Prompt:**

1. If you have an environment, activate it, otherwise continue to next step:
   ```
   activate <your-environment-name>
   ```

2. Navigate to the project directory:
   ```
   cd EEG_Senor_Interface
   ```

3. Run the main script:
   ```
   python main.py
   ```

### For Linux Users:

1. Clone the repository:
   ```
   git clone git@github.com:owenzengusc/EEG_Senor_Interface.git
   ```

2. Navigate to the project directory:
   ```
   cd EEG_Senor_Interface
   ```

3. Run the main script:
   ```
   python3 main.py
   ```

## Setting Up and Modifying the Test

If you wish to set up and customize the test parameters, follow the steps below:

### 1. Adjusting the Test Duration:

Both the MathTest and StroopTest have a default duration of 3 minutes. To modify this:

- Open MathTest.py or StroopTest.py.
- Locate the line TOTAL_GAME_TIME = 60*3.
- Change the 3 to your desired duration in minutes.

### 2. Modifying the Math Test Parameters:

In MathTest.py:

- MAX_NUM_OPERATIONS and MIN_NUM_OPERATIONS: Adjust the range of operations in the math expression.
- DIFFICULTY_INCREMENT: Control how much to increase the difficulty.
- TIME_THRESHOLD: Set the time threshold for adjusting difficulty.
- PARENTHESIS_PROBABILITY: Adjust the probability of including parentheses in the expression.

### 3. Modifying the Stroop Test Parameters:

In StroopTest.py:

- QUESTION_FREQUENCY: Set the initial frequency of questions per second.
- INCREASE_RATE: Control the rate at which the question frequency increases.
- MAX_QUESTION_FREQUENCY: Set the maximum question frequency.

### 4. Adjusting Window and Test Duration Parameters in `main.py:

In `main.py`, there are parameters that define the window dimensions and the average test duration. If you modify the test duration in the individual test files (`MathTest.py` or `StroopTest.py`), ensure you also update the `AVERAGE_TEST_DURATION` parameter (unit of minute) in `main.py` to reflect the changes.
```python
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000
TEST_WINDOW_WIDTH = 900
TEST_WINDOW_HEIGHT = 700
AVERAGE_TEST_DURATION = 5
```

## Using the Test Editor (test_editor.py)

The test_editor.py script allows users to view, add, edit, or delete tests. Here's how to use it:

1. Initialization: On the first run, the script checks for the existence of the test.json file in the test/ directory. If it doesn't exist or is invalid, the script will initialize a new JSON file with default values.

2. View Tests: Enter 1 when prompted to view the list of tests.

3. Add a Test: Enter 2 and provide the name of the test you want to add.

4. Edit a Test: Enter 3, provide the test number you want to edit, and then provide the new test name.

5. Delete a Test: Enter 4 and provide the test number you want to delete.

6. Exit: Enter 5 to exit the script.

Remember to always backup your test.json file before making any changes.

## Adding Python to PATH on Windows

If you haven't added Python to the PATH during the installation, you can do it manually.

1. Search for "Environment Variables" on your computer (you can use the Windows search).
2. Click on "Edit the system environment variables".
3. In the System Properties window, click on the "Environment Variables" button.
4. In the Environment Variables window, highlight the Path variable in the "System variables" section and click the Edit button.
5. In the Edit Environment Variable window, click the New button and then paste in the path to your Python folder, e.g., `C:\Python39`, and also add the path to the Scripts folder, e.g., `C:\Python39\Scripts`.
6. Click OK to close each of the windows.

Now, you should be able to run Python from the Command Prompt, PowerShell, or any other terminal.

## Contributing

Contributions to this project are welcomed. To contribute, please fork the repository and submit your pull request.

## Acknowledgments

This EEG Sensor Interface project is a part of the larger "Precision Psychiatry" initiative led by [Munia Ferdoushi](mailto:ferdoush@usc.edu). I am grateful for the opportunity to work under her guidance and be a part of her research group at [Khan Lab @ USC](https://khan.usc.edu/) with Professor [Yasser Khan](mailto:yasser.khan@usc.edu). Her expertise and mentorship have been invaluable in the development and progression of this project.