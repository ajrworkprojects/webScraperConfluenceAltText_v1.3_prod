import sqlite3
from datetime import datetime
from pathlib import Path
from time import sleep
from dbRecordHandler.sqlHelper import SQLHelper


class Deleter:
    """Deletes existing records in the webscraper.db.
        
    Attributes
    ----------
    None
    
    Methods
    ----------
    removePageIDfromMissingAltTextTable(pageID)
        Remove pageID from the CONFLUENCE_PAGES_MISSING_ALT_TEXT table

    removePageIDfromAllConfluencePagesTable(pageID)
        Remove pageID from the ALL_CONFLUENCE_PAGES table.

    removeAuthorFromDB(username, email)
        Removes author from webscraper.db

    unassignPageIDFromConfluenceCoordinators(pageID, username)
        Receives a pageID and the username of a Confluence Coordinator, and unassigns that Coordinator from from that Confluence page

    removeInactiveAuthorsFromDB()
        Removes inactive authors and automated admin accounts from db.
    """

    def __init__(self):
        """
        Parameters
        ----------
        None
        """

    def __repr__(self):
        return f'Deleter()'

    def removePageIDfromMissingAltTextTable(self, pageID):
        """
        Remove pageID from the CONFLUENCE_PAGES_MISSING_ALT_TEXT table
    
        Parameters
        ----------
        pageID : String
            Unique ID for a Confluence page
    
        Returns
        ----------
        None
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        dbCursor.execute("""
            DELETE FROM CONFLUENCE_PAGES_MISSING_ALT_TEXT
            WHERE pageID = (?)""",
            (pageID,)
        )
        
        dbConnector.commit()
        dbConnector.close()

        sleep(1)

    def removePageIDfromAllConfluencePagesTable(self, pageID):
        """
        Remove pageID from the ALL_CONFLUENCE_PAGES table.
    
        Parameters
        ----------
        pageID : String
            Unique ID for a Confluence page
    
        Returns
        ----------
        None
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        dbCursor.execute("""
            DELETE FROM ALL_CONFLUENCE_PAGES
            WHERE pageID = (?)""",
            (pageID,)
        )
        
        dbConnector.commit()
        dbConnector.close()

        sleep(1)

    def removeAuthorFromDB(
        self,
        username="not given",
        email="not given"
    ):
        """
        Removes author from webscraper.db
    
        Parameters
        ----------
        username (optional) : String
            The author's username

        email (optional) : String
            The author's email address
    
        Returns
        ----------
        None
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        if username == "not given":
            dbCursor.execute("""
                DELETE FROM ALL_CONFLUENCE_AUTHORS
                WHERE email = (?)""",
                (email,)
            )
        elif email == "not given":
            dbCursor.execute("""
                DELETE FROM ALL_CONFLUENCE_AUTHORS
                WHERE username = (?)""",
                (username,)
            )
        
        dbConnector.commit()
        dbConnector.close()

        sleep(1)

    def unassignPageIDFromConfluenceCoordinators(self, pageID, username):
        """
        Receives a pageID and the username of a Confluence Coordinator, and unassigns that Coordinator from from that Confluence page
    
        Parameters
        ----------
        pageID : String
            The unique ID for a Confluence page

        username : String
            The username of the Confluence Coordinator
    
        Returns
        ----------
        None
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        dbCursor.execute("""
                DELETE FROM RECENT_CONFLUENCE_AUTHORS
                WHERE pageID = (?) AND 
                username = (?)""",
                (pageID, username,)
            )
        
        dbConnector.commit()
        dbConnector.close()

        sleep(1)

    def removeInactiveAuthorsFromDB(self):
        """
        Removes inactive authors and automated admin accounts from db.
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        None
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        dbCursor.execute("""
                DELETE FROM ALL_CONFLUENCE_AUTHORS
                WHERE fullname = (?)""",
                ("Confluence Admin", )
            )

        dbCursor.execute("""
                DELETE FROM ALL_CONFLUENCE_AUTHORS
                WHERE email = (?)""",
                ("Address not found", )
            )
        
        dbConnector.commit()
        dbConnector.close()

        sleep(1)

    def unassignAuthorsFromStalePageIDs(self):
        """
        Searches db for pageIDs that have been missing alternate text for 30 days, and then unassigns the current authors from those Confluence pages
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        None
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        stalePageIDs = dbCursor.execute("""
                SELECT pageID FROM LOG_CONFLUENCE_PAGES_TO_FIX
                WHERE numDaysMissingAltText > 30"""
            ).fetchall()
        
        dbCursor.executemany("""
                DELETE FROM RECENT_CONFLUENCE_AUTHORS
                WHERE pageID = (?)""",
                stalePageIDs
            )
        
        dbConnector.commit()
        dbConnector.close()

        sleep(1)