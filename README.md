- **Modern UI**: Sleek interface with dark/light mode support.

## Prerequisites
- Python 3.8+
- MySQL Server

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd Football-League-Management-System
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Database**:
    - Import `database.sql` into your MySQL server.
    - Update the `.env` file with your database credentials:
        ```env
        DB_HOST=localhost
        DB_USER=root
        DB_PASSWORD=your_password
        DB_NAME=FootballLeagueDB
        ```

## Running the Application
To start the application, run:
```bash
python run.py
```

## Project Structure
- `src/main.py`: Entry point of the application.
- `src/gui.py`: User interface implementation using CustomTkinter.
- `src/database.py`: Database connection and operations.
- `database.sql`: SQL script to set up the database schema.
