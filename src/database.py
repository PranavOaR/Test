import mysql.connector
from mysql.connector import pooling
import os
import logging
from typing import List, Tuple, Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self):
        self.pool = None
        self.init_pool()

    def init_pool(self):
        """Initialize the database connection pool."""
        try:
            db_config = {
                "host": os.getenv("DB_HOST", "localhost"),
                "user": os.getenv("DB_USER", "root"),
                "password": os.getenv("DB_PASSWORD", ""),
                "database": os.getenv("DB_NAME", "FootballLeagueDB"),
                "pool_name": "mypool",
                "pool_size": 5
            }
            self.pool = mysql.connector.pooling.MySQLConnectionPool(**db_config)
            logging.info("Database connection pool created successfully.")
        except mysql.connector.Error as e:
            logging.error(f"Error creating connection pool: {e}")
            raise

    def get_connection(self):
        """Get a connection from the pool."""
        try:
            return self.pool.get_connection()
        except mysql.connector.Error as e:
            logging.error(f"Error getting connection from pool: {e}")
            raise

    def execute_query(self, query: str, params: Tuple = None, fetch: bool = False) -> Optional[List[Tuple]]:
        """Execute a generic SQL query."""
        conn = None
        cursor = None
        result = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
            else:
                conn.commit()
                
        except mysql.connector.Error as e:
            logging.error(f"Database query error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return result

    def fetch_teams(self) -> List[Tuple]:
        """Fetch all teams."""
        query = "SELECT team_id, team_name, coach_name, foundation_year, tournament_id FROM Team"
        return self.execute_query(query, fetch=True)

    def add_team(self, name: str, coach: str, year: Optional[int], tournament_id: int = 1):
        """Add a new team."""
        query = "INSERT INTO Team (team_name, coach_name, foundation_year, tournament_id) VALUES (%s, %s, %s, %s)"
        self.execute_query(query, (name, coach, year, tournament_id))

    def delete_team(self, team_id: int):
        """Delete a team by ID."""
        query = "DELETE FROM Team WHERE team_id = %s"
        self.execute_query(query, (team_id,))

    def fetch_matches(self) -> List[Tuple]:
        """Fetch all matches with team names."""
        query = """
            SELECT m.match_id,
                   m.team1_id, t1.team_name,
                   m.team2_id, t2.team_name,
                   m.match_date, m.venue, m.status
            FROM Matches m
            LEFT JOIN Team t1 ON m.team1_id = t1.team_id
            LEFT JOIN Team t2 ON m.team2_id = t2.team_id
            ORDER BY m.match_date, m.match_id;
        """
        return self.execute_query(query, fetch=True)

    def create_match(self, team1_id: int, team2_id: int, date: str, venue: str, tournament_id: int = 1):
        """Create a new match."""
        query = "INSERT INTO Matches (tournament_id, team1_id, team2_id, match_date, venue, status) VALUES (%s, %s, %s, %s, %s, 'Scheduled')"
        self.execute_query(query, (tournament_id, team1_id, team2_id, date, venue))

    def add_match_result(self, match_id: int, team1_id: int, goals1: int, team2_id: int, goals2: int):
        """Add match result using the stored procedure."""
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.callproc('AddMatchResult', (match_id, team1_id, goals1, team2_id, goals2))
            conn.commit()
        except mysql.connector.Error as e:
            logging.error(f"Error adding match result: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def fetch_leaderboard(self) -> List[Tuple]:
        """Fetch the leaderboard."""
        query = "SELECT team_id, team_name, matches_played, wins, draws, losses, goals_for, total_points FROM Leaderboard"
        return self.execute_query(query, fetch=True)

    def update_player_weight(self, player_name: str, new_weight: float):
        """Update a player's weight."""
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SET SQL_SAFE_UPDATES = 0;")
            cursor.execute("UPDATE Player SET weight_kg = %s WHERE name = %s", (new_weight, player_name))
            cursor.execute("SET SQL_SAFE_UPDATES = 1;")
            conn.commit()
        except mysql.connector.Error as e:
            logging.error(f"Error updating player weight: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_win_percentage(self, team_id: int) -> float:
        """Get win percentage for a team."""
        query = "SELECT GetWinPercentage(%s)"
        result = self.execute_query(query, (team_id,), fetch=True)
        return result[0][0] if result else 0.0

    def fetch_players(self) -> List[Tuple]:
        """Fetch all players with their team names."""
        query = """
            SELECT p.player_id, p.name, p.age, p.gender, p.position, 
                   p.height_cm, p.weight_kg, p.jersey_number, 
                   p.team_id, t.team_name
            FROM Player p
            LEFT JOIN Team t ON p.team_id = t.team_id
            ORDER BY p.name
        """
        return self.execute_query(query, fetch=True)

    def add_player(self, name: str, age: int, gender: str, position: str, 
                   height: float, weight: float, jersey: int, team_id: int):
        """Add a new player."""
        query = """
            INSERT INTO Player (name, age, gender, position, height_cm, weight_kg, jersey_number, team_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.execute_query(query, (name, age, gender, position, height, weight, jersey, team_id))

    def update_player(self, player_id: int, name: str, age: int, gender: str, position: str, 
                      height: float, weight: float, jersey: int, team_id: int):
        """Update an existing player."""
        query = """
            UPDATE Player 
            SET name=%s, age=%s, gender=%s, position=%s, 
                height_cm=%s, weight_kg=%s, jersey_number=%s, team_id=%s
            WHERE player_id=%s
        """
        self.execute_query(query, (name, age, gender, position, height, weight, jersey, team_id, player_id))

    def delete_player(self, player_id: int):
        """Delete a player."""
        query = "DELETE FROM Player WHERE player_id = %s"
        self.execute_query(query, (player_id,))

    def fetch_tournaments(self) -> List[Tuple]:
        """Fetch all tournaments."""
        query = "SELECT tournament_id, name, type, host_country, no_of_teams, no_of_matches, start_date, end_date FROM Tournament"
        return self.execute_query(query, fetch=True)

    def add_tournament(self, name: str, type: str, host: str, teams: int, matches: int, start: str, end: str):
        """Add a new tournament."""
        query = """
            INSERT INTO Tournament (name, type, host_country, no_of_teams, no_of_matches, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.execute_query(query, (name, type, host, teams, matches, start, end))

    def update_tournament(self, t_id: int, name: str, type: str, host: str, teams: int, matches: int, start: str, end: str):
        """Update an existing tournament."""
        query = """
            UPDATE Tournament 
            SET name=%s, type=%s, host_country=%s, no_of_teams=%s, no_of_matches=%s, start_date=%s, end_date=%s
            WHERE tournament_id=%s
        """
        self.execute_query(query, (name, type, host, teams, matches, start, end, t_id))

    def delete_tournament(self, t_id: int):
        """Delete a tournament."""
        query = "DELETE FROM Tournament WHERE tournament_id = %s"
        self.execute_query(query, (t_id,))
