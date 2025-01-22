
# Fantasy Football League Manager

This script is a tool for managing, analyzing, and generating reports for a fantasy football league. It processes weekly data for league participants, calculates scores, rankings, and trends, and generates summary files for review.

## Features
- Parses player data and calculates weekly scores.
- Evaluates the performance of starters and bench players.
- Generates JSON and CSV reports for each week.
- Calculates trends, rankings, and performance metrics.
- Supports managing multiple managers' data in a structured format.

---

## Prerequisites
1. **Python**: Ensure Python 3.8 or newer is installed.
2. **Dependencies**:
   - `pandas`: For managing data and generating reports.
   - `json`: For reading and writing JSON files.

   Install dependencies using:
   ```bash
   pip install pandas
   ```

3. **Input Files**:
   - Player data files for each manager (`Inputs/{Manager}.txt`).
   - A schedule file (`schedule.json`), defining matchups for each week.

4. **Output Directory**:
   - The script generates output files in the `Outputs/Week{week}` directory.

---

## Input Data Format
### Player Data Files
From the ESPN Fantasy Box Score page you can highlight the player data for a particular roster and copy paste it into the .txt file for that manager.
No need to adjust the data (See /Inputs folder for an example of what that should look like).

### Schedule File (`schedule.json`)
The schedule file should include weekly matchups in the following format:
```json
[
    [
        {"home": "Player1", "away": "Player2"},
        {"home": "Player3", "away": "Player4"}
    ],
    ...
]
```

---

## How to Use

### Step 1: Prepare Input Files
1. Add player data files for each manager to the `Inputs` directory.
2. Add a `schedule.json` file to define weekly matchups.

### Step 2: Run the Script
1. Execute the script:
   ```bash
   python parser.py
   ```
2. Enter the week number when prompted.

### Step 3: Review Outputs
- JSON files for each manager's weekly performance will be saved in:
  ```bash
  Outputs/Week{week}/{manager}.json
  ```
- Weekly summary CSV files:
  ```bash
  Outputs/Week{week}/summary.csv
  ```
- Bench performance summary:
  ```bash
  Outputs/Week{week}/bench_summary.csv
  ```

---

## Key Functions
### Main Components
1. **`parse_roster(filename)`**: Parses a roster file and extracts player data.
2. **`find_ideal(roster)`**: Determines the ideal starting lineup.
3. **`save_to_json(roster, filename)`**: Saves a roster's data as a JSON file.
4. **`main()`**: Orchestrates the entire process, including parsing inputs, computing scores, and generating outputs.

---

## Example Workflow
1. Add player files for all managers in the `Inputs` directory.
2. Add or update the `schedule.json` file with matchups.
3. Run the script for the desired week.
4. Open the output files in the `Outputs` directory for analysis.
5. Upload CSV file to Spreadsheet Example can be found here - https://docs.google.com/spreadsheets/d/1ZWPc7dQF_WMAdlNDDNJcLJ8m7R1G2gV7Kufje5-_M8c/edit?usp=sharing

---

## Troubleshooting
- **Missing Data**: Ensure all required files (e.g., `Inputs` and `schedule.json`) are present.
- **Incorrect Format**: Verify the format of player data files and the schedule file.
- **Dependency Errors**: Install missing packages using `pip`.

---

This script streamlines the management of your fantasy football league by automating tedious tasks and generating insightful performance metrics for analysis. Enjoy managing your league efficiently!
