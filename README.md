# EEG Sensor Interface

This project provides an interface for EEG sensor tests in Khan Lab @ USC. It allows users to participate in various tests, view instructions, and receive feedback based on their performance.

## Author

- **Owen Zeng**: Sole developer and maintainer of this project. You can contact me at [owenzeng@usc.edu](owenzeng@usc.edu).

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

1. If you have an environment, activate it:
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