"""Module that allows for interaction with the database."""
import logging
import sqlite3
import sys

import mysql.connector
import psycopg2

from sooch import path


class Database:
    """An instance of database the bot can communicate with."""

    def __init__(self, config):
        self.logger = logging.getLogger("sooch")
        self.logger.info("Initializing database")

        db_config = config["database"]
        db_type = db_config["type"]

        if db_type == "postgres":
            self.logger.info("Connecting to postgres")
            self.connection = psycopg2.connect(
                url=db_config["url"],
                username=db_config["username"],
                password=db_config["password"]
            )
        elif db_type == "mysql":
            self.logger.info("Connecting to mysql")
            self.connection = mysql.connector.connect(
                url=db_config["url"],
                username=db_config["username"],
                password=db_config["password"]
            )
        elif db_type == "sqlite":
            self.logger.info("Connecting to sqlite")

            db_file_path = path.from_root(db_config["file"])
            self.connection = sqlite3.connect(db_file_path)
        else:
            self.connection = None
            self.logger.error("Invalid database type %s",
                              config["database"]["type"])
            sys.exit()
        self.migrate()

    def migrate(self):
        """Migrate the database as necessary."""
        self.logger.info("Running migrations")
        migration_steps = [
            """
            CREATE TABLE IF NOT EXISTS `server`(
                `discord_id` BIGINT PRIMARY KEY,
                `name` VARCHAR(256)
            );
            """,
            self.get_reg_building_query(),
            """
            CREATE TABLE IF NOT EXISTS `player` (
                `discord_id` BIGINT PRIMARY KEY,
                `name` VARCHAR(32),
                `sooch_skin` VARCHAR(50),
                `embed_color` INT,
                `sooch` DOUBLE PRECISION NOT NULL DEFAULT 0,
                `tsooch` DOUBLE PRECISION NOT NULL DEFAULT 0,
                `csooch` DOUBLE PRECISION NOT NULL DEFAULT 0,
                `last_claim` BIGINT
            );
            """,
        ]
        cursor = self.connection.cursor()
        # This is run outside of the migrations since it needs to exist to
        # query what migrations need to be run.
        logging.info("Ensuring migrations table exists")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS `migration`(
                `migration_id` INT PRIMARY KEY
            );
            """
        )
        self.connection.commit()
        logging.info("Querying migrations")
        cursor.execute(
            "SELECT `migration_id` FROM `migration`;"
        )
        rows = cursor.fetchall()
        migrations_run = [row[0] for row in rows]
        for i, migration_step in enumerate(migration_steps):
            if i not in migrations_run:
                self.logger.info("Running migration %d", i)
                cursor.execute(migration_step)
                cursor.execute(
                    "INSERT INTO `migration` (`migration_id`) VALUES(?)",
                    (i,))
                self.connection.commit()
            else:
                self.logger.info("Skipping migration %d, already run.", i)

    @staticmethod
    def get_reg_building_query() -> str:
        """Generate the layout of the regular building query."""
        return ("CREATE TABLE IF NOT EXISTS `reg_buildings`("
                + "    `discord_id` BIGINT PRIMARY KEY,"
                + ", ".join([f"`b{building_id}` INT NOT NULL DEFAULT 0" for building_id in range(1, 51+1)])
                + ");")
