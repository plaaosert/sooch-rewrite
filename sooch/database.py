"""Module that allows for interaction with the database."""
import logging
import sqlite3
import sys

import mysql.connector
import psycopg2


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
            self.connection = sqlite3.connect(db_config["file"])
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
            create table if not exists `server`(
                `discord_id` bigint primary key,
                `name` varchar(256),
                `command_prefix` varchar(32)
            );
            """
        ]
        cursor = self.connection.cursor()
        # This is run outside of the migrations since it needs to exist to
        # query what migrations need to be run.
        logging.info("Ensuring migrations table exists")
        cursor.execute(
            """
            create table if not exists `migration`(
                `migration_id` int primary key
            );
            """
        )
        self.connection.commit()
        logging.info("Querying migrations")
        cursor.execute(
            "select `migration_id` from `migration`;"
        )
        rows = cursor.fetchall()
        migrations_run = [row[0] for row in rows]
        for i, migration_step in enumerate(migration_steps):
            if i not in migrations_run:
                self.logger.info("Running migration %d", i)
                cursor.execute(migration_step)
                cursor.execute("insert into `migration`(`migration_id`) values(?)", (i,))
                self.connection.commit()
            else:
                self.logger.info("Skipping migration %d, already run.", i)


