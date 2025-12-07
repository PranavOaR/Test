import os
from dotenv import load_dotenv
from src.database import DatabaseManager
from src.gui import FootballApp
import logging

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize Database
    try:
        db_manager = DatabaseManager()
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return

    # Start GUI
    app = FootballApp(db_manager)
    
    # Initial data load
    app.refresh_teams()
    app.load_team_options()
    app.refresh_matches()
    app.refresh_leaderboard()
    
    app.mainloop()

if __name__ == "__main__":
    main()
