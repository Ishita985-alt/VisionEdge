import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional


logger = logging.getLogger("VisionEdge.DatabaseManager")


class DatabaseManager:
    """
    Manages the SQLite database for VisionEdge surveillance events.

    Responsibilities:
    - Create and initialize the SQLite database
    - Create the events table
    - Insert surveillance events
    - Retrieve stored events
    - Handle database connections safely
    """

    def __init__(self, database_path: Optional[str] = None):
        if database_path is None:
            project_root = Path(__file__).resolve().parents[2]
            database_directory = project_root / "output" / "database"
            database_directory.mkdir(parents=True, exist_ok=True)

            self.database_path = database_directory / "visionedge.db"
        else:
            self.database_path = Path(database_path)
            self.database_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

        logger.info(
            "DatabaseManager initialized: %s",
            self.database_path,
        )

    def connect(self):
        """
        Create and return a connection to the SQLite database.
        """

        try:
            connection = sqlite3.connect(self.database_path)
            connection.row_factory = sqlite3.Row

            logger.debug("Database connection established.")

            return connection

        except sqlite3.Error:
            logger.exception("Failed to connect to database.")
            raise

    def initialize_database(self):
        """
        Create the events table if it does not already exist.
        """

        create_table_query = """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            camera_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            description TEXT,
            severity TEXT DEFAULT 'INFO'
        )
        """

        try:
            with self.connect() as connection:
                connection.execute(create_table_query)
                connection.commit()

            logger.info("Database initialized successfully.")

        except sqlite3.Error:
            logger.exception("Failed to initialize database.")
            raise

    def add_event(
        self,
        camera_id: str,
        event_type: str,
        description: str = "",
        severity: str = "INFO",
    ) -> int:
        """
        Insert a surveillance event into the database.

        Returns:
            ID of the newly created event.
        """

        timestamp = datetime.now().isoformat(timespec="seconds")

        insert_query = """
        INSERT INTO events (
            timestamp,
            camera_id,
            event_type,
            description,
            severity
        )
        VALUES (?, ?, ?, ?, ?)
        """

        try:
            with self.connect() as connection:
                cursor = connection.execute(
                    insert_query,
                    (
                        timestamp,
                        camera_id,
                        event_type,
                        description,
                        severity,
                    ),
                )

                connection.commit()

                event_id = cursor.lastrowid

            logger.info(
                "Event added successfully: id=%s, type=%s",
                event_id,
                event_type,
            )

            return event_id

        except sqlite3.Error:
            logger.exception("Failed to add event.")
            raise

    def get_events(self, limit: int = 100):
        """
        Retrieve the most recent surveillance events.

        Args:
            limit: Maximum number of events to retrieve.

        Returns:
            List of event dictionaries.
        """

        query = """
        SELECT
            id,
            timestamp,
            camera_id,
            event_type,
            description,
            severity
        FROM events
        ORDER BY id DESC
        LIMIT ?
        """

        try:
            with self.connect() as connection:
                cursor = connection.execute(query, (limit,))
                rows = cursor.fetchall()

            events = [dict(row) for row in rows]

            logger.info(
                "Retrieved %s events from database.",
                len(events),
            )

            return events

        except sqlite3.Error:
            logger.exception("Failed to retrieve events.")
            raise

    def close(self):
        """
        Database connections are handled using context managers.

        This method is provided for API consistency and future
        connection-pool support.
        """

        logger.debug(
            "Database connections are managed automatically."
        )