# Text and Image Plagiarism Detection

## Overview

The **text-and-image-plagiarism-detection** repository is designed to detect plagiarism in both text and image formats. This project provides a comprehensive solution for identifying copied content across different media types.

## Key Features

- **Command-Line Utility**: 
  - Detect text plagiarism using the command:
    ```
    python text-plagiarism.py suspicious-file.txt
    ```
  - Detect image plagiarism using the command:
    ```
    python image-plagiarism.py suspicious-image.jpg
    ```

- **Web Application**: 
  - Built with Django, featuring user authentication (signup and login).
  - Allows users to upload source files and check for relative plagiarism in both text and images.
  - Supports custom datasets or corpuses of text and images.

## Technologies Used

- **Python**: Main programming language for backend logic.
- **Django**: Framework used for building the web application.
- **SQLite3**: Database used for storing user data and uploaded files.
- **HTML/CSS**: Used for the frontend web application interface.
- **MIT License**: The project is open-source and available for modification and distribution under the MIT license.

## Installation

To get started with the project, follow these steps:

1. Clone the repository:
    ```
    git clone https://github.com/montux4yt/text-and-image-plagiarism-detection.git
    ```
2. Navigate to the project directory:
    ```
    cd text-and-image-plagiarism-detection
    ```
3. Install the required dependencies for the web application:
    ```
    pip install -r requirements.txt
    ```
4. Install the NLTK dependencies:
    ```
    python3 libs-requirements.py
    ```

## Running the Command-Line Utility

To use the command-line utilities for plagiarism detection:

- For text files:
    ```
    python text-plagiarism.py suspicious-file.txt
    ```

- For images:
    ```
    python image-plagiarism.py suspicious-image.jpg
    ```

## Running the Web Application

To run the web application, execute the following command:
```
python manage.py runserver
```

Then, open your web browser and go to `http://localhost:8000` to access the application.

## Contributing

Contributions are welcome! If you have suggestions for improvements or want to report issues, please create a pull request or open an issue in the repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
