# Stress Test Interface

This project provides an interface for tests in [Khan Lab @ USC](https://khan.usc.edu/). It allows users to participate in various tests, view instructions, and receive feedback based on their performance.

## Author

- **Owen Zeng**: Sole developer and maintainer of this project. You can contact me at [owenzeng@usc.edu](mailto:owenzeng@usc.edu).

## Features

- **Data File**: Contains the output data and feedback for each test.
- **Test File**: A JSON file that holds information about the available tests.
- **Feedback Screen**: Displays feedback to the user after completing a test.
- **Instruction Screen**: Provides instructions to the user before starting a test.
- **Test Editor**: Allows users to modify, add, or delete tests.
- **Supported Tests**: Currently supports `MathTest`, `StroopTest`, and `ColdPressorTest`.
- **Logging Function**: Logs events with timestamps and durations to CSV files, covering the entire testing process.

## File Structure

data/: Contains the output data and feedback.
test/: Contains a JSON file with test configurations.
FeedbackScreen.py: Handles the feedback display after tests.
InstructionScreen.py: Displays instructions before each test.
main.py: The main entry point for the application.
MathTest.py: Logic and interface for the Math Test.
StroopTest.py: Logic and interface for the Stroop Test.
ColdPressorTest.py: Logic and interface for the Cold Pressor Test.
user.py: User-related functionalities.
window.py: Basic window creation and management functions.
test_editor: A utility to modify, add, or delete tests.

## Getting Started

### For macOS Users:

1. Clone the repository:
   ```
   git clone git@github.com:owenzengusc/Stress_Test_Interface.git
   ```

2. Navigate to the project directory:
   ```
   cd Stress_Test_Interface
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
   git clone git@github.com:owenzengusc/Stress_Test_Interface.git
   ```

2. Navigate to the project directory:
   ```
   cd Stress_Test_Interface
   ```

3. Run the main script:
   ```
   py main.py
   ```

**Using PowerShell:**

1. Clone the repository:
   ```
   git clone git@github.com:owenzengusc/Stress_Test_Interface.git
   ```

2. Navigate to the project directory:
   ```
   cd Stress_Test_Interface
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
   cd Stress_Test_Interface
   ```

3. Run the main script:
   ```
   python main.py
   ```

### For Linux Users:

1. Clone the repository:
   ```
   git clone git@github.com:owenzengusc/Stress_Test_Interface.git
   ```

2. Navigate to the project directory:
   ```
   cd Stress_Test_Interface
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

### 4. Modifying the Cold Pressor Test Parameters

In `ColdPressorTest.py`, you can adjust the durations of different phases of the test:

- `first_relaxation_duration`: Initial relaxation duration before the test starts (in seconds). Default is 180 seconds (3 minutes).
- `test_duration`: Duration for which the user keeps their hand in cold water (in seconds). Default is 180 seconds (3 minutes).
- `post_test_relaxation_duration`: Post-test relaxation duration (in seconds). Default is 175 seconds to accommodate a 5-second recording, making a total of 3 minutes.

### 5. Adjusting Window and Test Duration Parameters in `main.py:

In `main.py`, there are parameters that define the window dimensions and the average test duration. If you modify the test duration in the individual test files (`MathTest.py` or `StroopTest.py`), ensure you also update the `AVERAGE_TEST_DURATION` parameter (unit of minute) in `main.py` to reflect the changes.
```python
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000
TEST_WINDOW_WIDTH = 900
TEST_WINDOW_HEIGHT = 700
AVERAGE_TEST_DURATION = 5
```
## Logging Function

The logging function logs events with timestamps and durations in a CSV file named after the user's name. This is used across all tests, including the Cold Pressor Test.

### Example Log

The logging function creates entries in the following format:

```csv
Event,Start Time,End Time,Duration (milliseconds)
Program Start,2024-03-20 15:31:30.457,,
First Relaxation Start,2024-03-20 15:31:30.465,,
First Relaxation End,2024-03-20 15:31:30.465,2024-03-20 15:31:39.459,8993
StroopTest Start,2024-03-20 15:31:39.459,,
StroopTest End,2024-03-20 15:31:39.459,2024-03-20 15:31:41.826,2367
MathTest Start,2024-03-20 15:31:41.828,,
MathTest End,2024-03-20 15:31:41.828,2024-03-20 15:31:44.723,2895
Video Feedback Start,2024-03-20 15:31:44.791,,
Video 1 Start,2024-03-20 15:31:47.313,,
Video 1 End,2024-03-20 15:31:47.313,2024-03-20 15:32:01.432,14118
Video 2 Start,2024-03-20 15:32:03.992,,
Video 2 End,2024-03-20 15:32:03.992,2024-03-20 15:32:19.924,15932
Video Feedback End,2024-03-20 15:31:44.791,2024-03-20 15:32:23.112,38321
Cold Pressure Test Start,2024-03-20 15:32:25.071,,
CPT Initial Relaxation Start,2024-03-20 15:32:25.569,,
CPT Initial Relaxation End,2024-03-20 15:32:25.569,2024-03-20 15:32:35.571,10002
CPT Test Start,2024-03-20 15:32:35.573,,
CPT Test End,2024-03-20 15:32:35.573,2024-03-20 15:32:45.576,10002
CPT Post Test Relaxation Start,2024-03-20 15:32:50.578,,
CPT Post Test Relaxation End,2024-03-20 15:32:50.578,2024-03-20 15:33:00.581,10003
Cold Pressure Test End,2024-03-20 15:32:25.071,2024-03-20 15:33:05.588,40517
Program End,2024-03-20 15:31:30.457,2024-03-20 15:33:07.723,97265
```

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

This project is a part of the larger "Cognitive Stress Evaluation and Prediction" initiative led by [Munia Ferdoushi](mailto:ferdoush@usc.edu). I am grateful for the opportunity to work under her guidance and be a part of her research group at [Khan Lab @ USC](https://khan.usc.edu/) with Professor [Yasser Khan](mailto:yasser.khan@usc.edu). Her expertise and mentorship have been invaluable in the development and progression of this project.
