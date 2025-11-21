# Student Learning Speed Analysis 📈

## Overview
This project delves into student performance data to simulate learning progression over multiple attempts and analyze differences in learning speeds between genders. Utilizing Python with popular data science libraries, it processes raw scores, calculates individual learning rates, performs statistical significance tests, and visualizes key findings through comprehensive dashboards.

## Features
- **Data Simulation**: Artificially generates multi-attempt score data for students based on initial performance, introducing variability and progression.
- **Learning Rate Calculation**: Employs linear regression to derive a "learning speed" (slope coefficient) for each student across different subjects (Mathematics, Reading, Writing).
- **Gender-Based Performance Analysis**: Compares the average learning speeds of male and female students in each subject.
- **Statistical Significance Testing**: Applies independent t-tests to determine if observed gender-based learning speed differences are statistically significant (p-value < 0.05).
- **Interactive Data Visualization**: Generates insightful plots and dashboards illustrating learning trends over attempts and comparative learning speeds by gender.
- **Analyzed Data Export**: Exports the calculated learning speeds for further analysis or reporting in a clean CSV format.

## Getting Started

### Installation
To set up and run this project locally, please follow these steps:

1.  👯‍♀️ **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd student-learning-speed-analysis
    ```
    (Replace `<repository-url>` with the actual URL of your repository.)

2.  🐍 **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    ```

3.  Activate the virtual environment:
    -   **On macOS and Linux**:
        ```bash
        source venv/bin/activate
        ```
    -   **On Windows**:
        ```bash
        .\venv\Scripts\activate
        ```

4.  📦 **Install Dependencies**:
    ```bash
    pip install pandas numpy matplotlib scipy
    ```

### Data Files
Ensure the following input data file is present in the project's root directory:
- `StudentsPerformance.csv`: Contains the initial student performance data.

## Usage
To execute the analysis and generate the visualizations, simply run the `main.py` script from your activated virtual environment:

```bash
python main.py
```

Upon successful execution, the script will:
1.  Process the `StudentsPerformance.csv` data and simulate learning attempts.
2.  Perform statistical analysis to calculate and compare learning speeds.
3.  Display two interactive matplotlib dashboards (which will appear as pop-up windows).
4.  Save these dashboards as image files in the project root:
    - `learning_trends_dashboard.png`
    - `detailed_conclusions_dashboard.png`
5.  Export a summary of the calculated learning speeds to a new CSV file:
    - `learning_speed_analysis.csv`

**Example Output Visualizations**:

**Learning Trends Dashboard**
![Learning Trends Dashboard](learning_trends_dashboard.png)
*(Image of learning_trends_dashboard.png would be displayed here)*

**Detailed Conclusions Dashboard**
![Detailed Conclusions Dashboard](detailed_conclusions_dashboard.png)
*(Image of detailed_conclusions_dashboard.png would be displayed here)*

## Technologies Used
This project leverages the following Python libraries for data manipulation, statistical analysis, and visualization:

| Technology     | Description                                     |
| :------------- | :---------------------------------------------- |
| **Python**     | The core programming language.                  |
| **Pandas**     | Powerful data manipulation and analysis library.|
| **NumPy**      | Essential for numerical operations and array manipulation. |
| **Matplotlib** | Comprehensive library for creating static, animated, and interactive visualizations. |
| **SciPy**      | Used for scientific computing, including statistical functions like t-tests. |

## Contributing
We welcome contributions to enhance this project! If you'd like to contribute, please follow these guidelines:

1.  🍴 **Fork the repository**.
2.  🌿 **Create a new branch** for your feature or bug fix: `git checkout -b feature/your-feature-name` or `git checkout -b bugfix/fix-bug-description`.
3.  💻 **Make your changes** and ensure the code adheres to existing style guidelines.
4.  🧪 **Test your changes** thoroughly.
5.  ➕ **Commit your changes** with a clear and descriptive message: `git commit -m "feat: Add new feature for X"` or `git commit -m "fix: Resolve issue Y"`.
6.  🚀 **Push your branch** to your forked repository: `git push origin feature/your-feature-name`.
7.  💬 **Open a Pull Request** to the `main` branch of this repository, describing your changes in detail.

## Author Info

-   **Name**: IMAFIDON EMMANUEL
-   **LinkedIn**: [Your LinkedIn Profile](https://www.linkedin.com/in/yourusername/)
-   **Portfolio**: [Your Portfolio Website](https://www.yourportfolio.com)
-   **Twitter**: [Your Twitter Handle](https://twitter.com/yourhandle)

---
[![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](requirements.txt)
[![Readme was generated by Dokugen](https://img.shields.io/badge/Readme%20was%20generated%20by-Dokugen-brightgreen)](https://www.npmjs.com/package/dokugen)
