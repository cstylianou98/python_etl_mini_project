# Simple Weather Data ETL Pipeline

### Description
This mini-project extracts historical weather data, transforms it into daily summaries (e.g., daily max, min, and mean temperatures), and loads it into an SQLite database for further analysis. It also includes data visualization with Matplotlib to display trends.

### Purpose
To build an end-to-end ETL pipeline that handles data extraction from an API, performs data transformations, and stores the data in a relational database for querying.

### Features
- **Data Extraction**: Retrieves historical weather data from the Open-Meteo API.
- **Data Transformation**: Aggregates hourly data to compute daily statistics, including max, min, and mean temperatures.
- **Data Loading**: Saves both hourly and daily data in SQLite tables for structured storage.
- **Visualization**: Plots trends in temperature and humidity.

### Technologies Used
- **Python** (for ETL scripting)
- **SQLite** (for database storage)
- **Matplotlib** (for data visualization)

### ETL Workflow
1. **Extract**: Data is fetched from the Open-Meteo API for the specified location and date range.
2. **Transform**: Processes hourly data into daily max, min, and mean temperature summaries.
3. **Load**: Data is saved into an SQLite database for efficient querying and analysis.

### Setup Instructions
1. Clone the repository.
2. Install required packages: `requests`, `sqlite3`, `pandas`, `matplotlib`.
3. Run `python main.py` to execute the ETL pipeline.

### Usage
This ETL pipeline can be extended to process data for other locations and date ranges by adjusting the parameters in the API request.

### Sample Query
- Retrieve mean temperatures for a given time period.
   ```sql
    SELECT date, temperature_2m_mean 
    FROM daily_data
    WHERE date BETWEEN '1999-01-01' AND '1999-12-31'

### Future Work:

- **Expand Data Sources**: Integrate additional weather APIs for more comprehensive data coverage.
- **Add More Visualizations**: Create more complex visualizations to analyze weather patterns over time.
- **Enhance Query Capabilities**: Develop a user interface or command-line tool for users to easily create custom queries against the database.

