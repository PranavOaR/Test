# Setup Summary

## Project Structure
This project follows a modern full-stack architecture:

- **Frontend**: `frontend/` (Next.js, Tailwind CSS)
- **Backend**: `backend/` (Express.js, MySQL)
- **Database**: `database.sql` (Schema)

## Quick Setup (Windows)

1.  **Run the Setup Script**:
    Double-click `setup.bat` or run it in the terminal:
    ```cmd
    setup.bat
    ```
    This will:
    - Install all dependencies (Root, Backend, Frontend).
    - Set up the environment variables (if missing).
    - Reset the database with the correct schema.

2.  **Start the Application**:
    ```cmd
    npm run dev
    ```

## Manual Setup

If you prefer to set up manually:

1.  **Install Dependencies**:
    ```bash
    npm install
    cd backend && npm install
    cd ../frontend && npm install
    ```

2.  **Database Setup**:
    - Ensure MySQL is running.
    - Run the reset script:
      ```bash
      cd backend
      node scripts/reset_db.js
      ```

3.  **Run**:
    ```bash
    npm run dev
    ```
