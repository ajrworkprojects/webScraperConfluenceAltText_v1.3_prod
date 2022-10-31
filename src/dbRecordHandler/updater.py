import sqlite3
from datetime import datetime
from pathlib import Path
from time import sleep
from dbRecordHandler.sqlHelper import SQLHelper


class Updater:
    """Updates existing records in the webscraper.db.
        
    Attributes
    ----------
    None
    
    Methods
    ----------
    changeCLIMajorTasksLogValue(value, dbCode)
        Receives "TRUE" or "FALSE" and updates the value in the respective LOG_CLI_MAJOR_TASKS table

    updateOldPageVersion(pageID, newPageVersion)
        Receives a pageID and updates ALL_CONFLUENCE_PAGES.oldPageVersion

    updateWasPageCheckedThisRun(pageID, value)
        Receives a pageID and updates ALL_CONFLUENCE_PAGES.wasPageCheckedThisRun

    updateWasPageRecentlyUpdated(pageID, value)
        Receives a pageID and updates ALL_CONFLUENCE_PAGES.wasPageRecentlyUpdated

    addAuthorEmailToDB(username, address)
        Receives the author's username and address, and updates the appropriate record in the db

    resetKeyDBValuesToDefault()
        Reset key DB values back to their default values.  This method is called when the script has emailed the individualized messages to the Confluence authors
    """

    def __init__(self):
        """
        Parameters
        ----------
        None
        """

    def __repr__(self):
        return f'Updater()'

    def changeCLIMajorTasksLogValue(self, value, dbCode):
        """
        Receives "TRUE" or "FALSE" and updates the value in the respective LOG_CLI_MAJOR_TASKS table
    
        Parameters
        ----------
        value : String
            The value to pass to the db

        dbCode: String
            A shortened (code) representation of a given major CLI task
    
        Returns
        ----------
        none
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)
        
        dbCursor.execute("""
            UPDATE LOG_CLI_MAJOR_TASKS
            SET wasTaskCompletedThisRun = (?)
            WHERE majorTaskCode = (?)
            """,
            (value, dbCode)
        )
        
        dbConnector.commit()
        dbConnector.close()

        sleep(1)

    def updateOldPageVersion(self, pageID, newPageVersion):
        """
        Receives a pageID and updates ALL_CONFLUENCE_PAGES.oldPageVersion
    
        Parameters
        ----------
        pageID : String
            The unique ID for a Confluence page

        newPageVersion : String
            The new page version number
    
        Returns
        ----------
        none
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        dbCursor.execute("""
            UPDATE ALL_CONFLUENCE_PAGES
            SET oldPageVersion = (?)
            WHERE pageID = (?)
            """,
            (newPageVersion, pageID)
        )
        
        dbConnector.commit()
        dbConnector.close()

        sleep(1)

    def updateWasPageCheckedThisRun(self, pageID, value):
        """
        Receives a pageID and updates ALL_CONFLUENCE_PAGES.wasPageCheckedThisRun
    
        Parameters
        ----------
        pageID : String
            The unique ID for a Confluence page

        value : String
            The value that waspageCheckedThisRun should be (either "TRUE" or "FALSE")
    
        Returns
        ----------
        none
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        dbCursor.execute("""
            UPDATE ALL_CONFLUENCE_PAGES
            SET waspageCheckedThisRun = (?)
            WHERE pageID = (?)
            """,
            (value, pageID)
        )
        
        dbConnector.commit()
        dbConnector.close()

        sleep(1)

    def updateWasPageRecentlyUpdated(self, pageID, value):
        """
        Receives a pageID and updates ALL_CONFLUENCE_PAGES.wasPageRecentlyUpdated
    
        Parameters
        ----------
        pageID : String
            The unique ID for a Confluence page

        value : String
            The value that wasPageRecentlyUpdated should be (either "TRUE" or "FALSE")
    
        Returns
        ----------
        none
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)
        
        dbCursor.execute("""
            UPDATE ALL_CONFLUENCE_PAGES
            SET wasPageRecentlyUpdated = (?)
            WHERE pageID = (?)
            """,
            (value, pageID)
        )
        
        dbConnector.commit()
        dbConnector.close()

        sleep(1)

    def addAuthorEmailToDB(self, username, address):
        """
        Receives the author's username and address, and updates the appropriate record in the db
    
        Parameters
        ----------
        username : String
            The author's username

        address : String
            The author's email address
    
        Returns
        ----------
        None
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)
        
        if dbCursor.execute("""
            SELECT * FROM ALL_CONFLUENCE_AUTHORS
            WHERE username = (?)
        """, (username,)).fetchone():
        
            dbCursor.execute("""
                UPDATE ALL_CONFLUENCE_AUTHORS
                SET email = (?)
                WHERE username = (?)
                """,
                (address, username)
            )
        
        dbConnector.commit()
        dbConnector.close()

        sleep(1)

    def resetKeyDBValuesToDefault(self):
        """
        Reset key DB values back to their default values.  This method is called when the script has emailed the individualized messages to the Confluence authors
    
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
            UPDATE LOG_CLI_MAJOR_TASKS
            SET wasTaskCompletedThisRun = "FALSE"
            """
        )

        dbCursor.execute("""
            UPDATE ALL_CONFLUENCE_PAGES
            SET wasPageCheckedThisRun = "FALSE",
            wasPageRecentlyUpdated = "FALSE"
            """
        )
        
        dbConnector.commit()
        dbConnector.close()

        sleep(1)