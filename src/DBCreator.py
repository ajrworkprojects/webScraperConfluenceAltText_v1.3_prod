import sqlite3
import os
from pathlib import Path

class DBCreator:
    """Creates .db for script
        
    Attributes
    ----------
    none
    
    
    Methods
    ----------
    createDB
        Creates .db for .py script

    doesDBexist
        Checks to see if webscraper.db already exists 
    """
    
    def __init__(self):
        """
        Parameters
        ----------
        none
        """

    def __repr__(self):
        return f'className(none)'

    def createDB(self):
        """
        Creates .db for .py script
    
        Parameters
        ----------
        none
    
        Returns
        ----------
        nonef
        """

        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.execute("""CREATE TABLE ALL_CONFLUENCE_PAGES (
            pageID TEXT NOT NULL PRIMARY KEY,
            oldPageVersion TEXT NOT NULL,
            wasPageRecentlyUpdated TEXT NOT NULL DEFAULT "FALSE",
            wasPageCheckedThisRun TEXT NOT NULL DEFAULT "FALSE"
        )""")

        dbCursor.execute("""CREATE UNIQUE INDEX UX_ALL_CONFLUENCE_PAGES_PAGEID ON ALL_CONFLUENCE_PAGES(pageID)""")

        dbCursor.execute("""CREATE TABLE CONFLUENCE_PAGES_MISSING_ALT_TEXT (
            pageID TEXT NOT NULL PRIMARY KEY,
            pageName TEXT NOT NULL,
            imageNamesLinks TEXT NOT NULL,
            FOREIGN KEY (pageID) REFERENCES ALL_CONFLUENCE_PAGES (pageID)
                ON DELETE CASCADE ON UPDATE CASCADE
        )""")

        dbCursor.execute("""CREATE UNIQUE INDEX UX_CONFLUENCE_PAGES_MISSING_ALT_TEXT_PAGEID ON CONFLUENCE_PAGES_MISSING_ALT_TEXT(pageID)""")

        dbCursor.execute("""CREATE TABLE RECENT_CONFLUENCE_AUTHORS (
            pageID TEXT NOT NULL,
            username TEXT NOT NULL,
            FOREIGN KEY (pageID) REFERENCES CONFLUENCE_PAGES_MISSING_ALT_TEXT (pageID)
                ON DELETE CASCADE ON UPDATE CASCADE
            FOREIGN KEY (username) REFERENCES ALL_CONFLUENCE_AUTHORS (username)
                ON DELETE CASCADE ON UPDATE CASCADE
            PRIMARY KEY(pageID, username)
        )""")

        dbCursor.execute("""CREATE TABLE LOG_CONFLUENCE_PAGES_TO_FIX (
            pageID TEXT NOT NULL PRIMARY KEY,
            dateLastChecked TEXT NOT NULL,
            numDaysMissingAltText INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (pageID) REFERENCES CONFLUENCE_PAGES_MISSING_ALT_TEXT (pageID)
                ON DELETE CASCADE ON UPDATE CASCADE
        )""")

        dbCursor.execute("""CREATE TABLE ALL_CONFLUENCE_AUTHORS (
            username TEXT NOT NULL PRIMARY KEY,
            email TEXT NOT NULL DEFAULT "will get email soon",
            fullname TEXT NOT NULL
        )""")

        dbCursor.execute("""CREATE UNIQUE INDEX UX_CONFLUENCE_AUTHORS_USERNAME ON ALL_CONFLUENCE_AUTHORS(username)""")

        dbCursor.execute("""CREATE TABLE LOG_CLI_MAJOR_TASKS (
            majorTaskCode TEXT NOT NULL PRIMARY KEY,
            majorTaskDesc TEXT NOT NULL,
            wasTaskCompletedThisRun TEXT NOT NULL DEFAULT "FALSE"
        )""")

        defaultValues_LOG_CLI_MAJOR_TASKS = [
            ("GOTIDS", "Got pageIDs to all PKB Confluence pages"),
            ("PAGESCHECKED", "Checked PKB Confluence pages for images missing alternate text"),
            ("SENTMSGS", "Sent individualized messages to all of the Confluence authors")
        ]
        
        dbCursor.executemany("""INSERT INTO LOG_CLI_MAJOR_TASKS (majorTaskCode, majorTaskDesc) VALUES (?,?)""", 
                            defaultValues_LOG_CLI_MAJOR_TASKS)

        dbConnector.commit()
        dbConnector.close()

    def doesDBexist(self):
        """
        Checks to see if webscraper.db already exists
    
        Parameters
        ----------
        none
    
        Returns
        ----------
        Boolean
            True if .db exist, False otherwise
        """
    
        return os.path.exists(str(Path.cwd())+"/src/sensitive/webscraper.db")