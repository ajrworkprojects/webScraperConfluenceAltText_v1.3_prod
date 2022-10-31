import sqlite3
from time import sleep
import os
from pathlib import Path
from datetime import datetime
from dbRecordHandler.sqlHelper import SQLHelper

class Creator:
    """Creates new records in the webscraper.db.
        
    Attributes
    ----------
    None
    
    Methods
    ----------
    addNewConfluencePageToDB(pageID, versionNum)
        Receives details about a new Confluence page and adds them to the DB.

    addConfluencePageMissingAltText(pageID, pageName, imageNamesLinks)
        Receives a pageID and other various details about a page that has images with missing alternate text, and adds these details to the CONFLUENCE_PAGES_MISSING_ALT_TEXT and LOG_CONFLUENCE_PAGES_TO_FIX tables.

        If the page is already in these two tables, then this method will update the existing records.  This method is one of the few creator methods that can update a record too.

    addAuthorToDB(pageID, username, fullname)
        Receives an author's name, username, and the pageID of the page the author recently updated, and adds those values to the db.

    assignPageIDtoConfluenceCoordinators(ageID, ConfluenceCoordinators)
        Receives a pageID and a list of Confluence Coordinators, and assigns that page to those Confluence Coordinators

    methodName(username, email, fullname)
        Receives info about a Confluence Coordinator and adds that coordinator to the db.
    """

    def __init__(self):
        """
        Parameters
        ----------
        None
        """

    def __repr__(self):
        return f'Creator()'

    def addNewConfluencePageToDB(
        self,
        pageID,
        versionNum
    ):
        """
        Receives details about a new Confluence page and adds them to the DB.
    
        Parameters
        ----------

        pageID : String
            Unique ID number for a Confluence page

        versionNum : String
            The number of the current version of the page
    
        Returns
        ----------
        None
        """
        
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        dbCursor.execute("""
            INSERT INTO ALL_CONFLUENCE_PAGES (pageID, oldPageVersion)
            VALUES (?, ?)
            """,
            (pageID, versionNum)
        )
        
        dbConnector.commit()
        dbConnector.close()

        sleep(1)

    def addConfluencePageMissingAltText(
        self,
        pageID,
        pageName,
        imageNamesLinks
    ):
        """
        Receives a pageID and other various details about a page that has images with missing alternate text, and adds these details to the CONFLUENCE_PAGES_MISSING_ALT_TEXT and LOG_CONFLUENCE_PAGES_TO_FIX tables.

        If the page is already in these two tables, then this method will update the existing records.  This method is one of the few creator methods that can update a record too.
    
        Parameters
        ----------
        pageID : String
            Unique ID of the Confluence page

        pageName : String
            Title of the Confluence page

        imageNamesLinks : String
            A string representation of key-value pairs; each pair is an image link and its respective image name
    
        Returns
        ----------
        None
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        todaysDate = datetime.today().strftime('%Y-%m-%d')

        if dbCursor.execute("""
            SELECT * FROM CONFLUENCE_PAGES_MISSING_ALT_TEXT
            WHERE pageID = (?)""", 
        (pageID,)).fetchone() is None:
        
            dbCursor.execute("""
                INSERT INTO CONFLUENCE_PAGES_MISSING_ALT_TEXT (pageID, pageName, imageNamesLinks)
                VALUES (?, ?, ?)
                """,
                (pageID, pageName, str(imageNamesLinks))
            )

            dbCursor.execute("""
                INSERT INTO LOG_CONFLUENCE_PAGES_TO_FIX (pageID, dateLastChecked) 
                VALUES (?, ?)""", 
                (pageID, todaysDate))

        else:

            dbCursor.execute("""
                SELECT dateLastChecked
                FROM LOG_CONFLUENCE_PAGES_TO_FIX
                WHERE pageID = (?)""", 
                (pageID, )
            )

            currentDate = dbCursor.fetchall()[0][0]
            currentDate_obj = datetime.strptime(currentDate, '%Y-%m-%d')

            todaysDate_obj = datetime.strptime(todaysDate, '%Y-%m-%d')
            
            newDaysToAdd = (todaysDate_obj - currentDate_obj).days

            dbCursor.execute("""
                UPDATE LOG_CONFLUENCE_PAGES_TO_FIX
                SET numDaysMissingAltText = numDaysMissingAltText + (?)
                WHERE pageID = (?)""",
                (newDaysToAdd, pageID)
            )
            
            dbCursor.execute("""
                UPDATE CONFLUENCE_PAGES_MISSING_ALT_TEXT 
                SET pageName = (?), 
                    imageNamesLinks = (?)
                WHERE pageID = (?)
                """,
                (pageName, str(imageNamesLinks), pageID)
            )
        
        dbConnector.commit()
        dbConnector.close()

        sleep(1)

    def addAuthorToDB(
        self,
        pageID,
        username,
        fullname
    ):
        """
        Receives an author's name, username, and the pageID of the page the author recently updated, and adds those values to the db.
    
        Parameters
        ----------
        pageID : String
            The unique ID of the Confluence page

        username : String
            The username of the author who recently updated the page

        fullname : String
            The full name of the author who recently updated the page
    
        Returns
        ----------
        None
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        if dbCursor.execute("""
            SELECT * FROM ALL_CONFLUENCE_AUTHORS
            WHERE username = (?)""", 
        (username,)).fetchone() is None:
        
            dbCursor.execute("""
                INSERT INTO ALL_CONFLUENCE_AUTHORS (username, fullname)
                VALUES (?, ?)
                """,
                (username, fullname)
            )

        if dbCursor.execute("""
            SELECT * FROM RECENT_CONFLUENCE_AUTHORS
            WHERE username = (?) 
                AND pageID = (?)""", 
        (username, pageID)).fetchone() is None:
        
            dbCursor.execute("""
                INSERT INTO RECENT_CONFLUENCE_AUTHORS (username, pageID)
                VALUES (?, ?)
                """,
                (username, pageID)
            )
        
        dbConnector.commit()
        dbConnector.close()

        sleep(1)

    def assignPageIDtoConfluenceCoordinators(self, pageID, ConfluenceCoordinators):
        """
        Receives a pageID and a list of Confluence Coordinators, and assigns that page to those Confluence Coordinators
    
        Parameters
        ----------
        pageID : String
            The unique ID to a Confluence page

        ConfluenceCoordinators : List
            A list of the Confluence Coordinators and their info.  This info is in tuples.
    
        Returns
        ----------
        None
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        for coord_t in ConfluenceCoordinators:
            username = coord_t[0]
        
            if dbCursor.execute("""
                SELECT * FROM RECENT_CONFLUENCE_AUTHORS
                WHERE username = (?) AND
                pageID = (?)
            """, (username, pageID)).fetchone() is None:
            
                dbCursor.execute("""
                    INSERT INTO RECENT_CONFLUENCE_AUTHORS
                    (username, pageID) 
                    VALUES (?, ?)
                    """,
                    (username, pageID)
                )
        
        dbConnector.commit()
        dbConnector.close()

        sleep(1)

    def addConfluenceCoordinatorToDB(self, username, email, fullname):
        """
        Receives info about a Confluence Coordinator and adds that coordinator to the db.
    
        Parameters
        ----------
        username : String
            The coordinator's username

        email : String
            The coordinator's email

        fullname : String
            The coordinator's fullname
    
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
        """, (username, )).fetchone() is None:
        
            dbCursor.execute("""
                INSERT INTO ALL_CONFLUENCE_AUTHORS
                (username, email, fullname) 
                VALUES (?, ?, ?)
                """,
                (username, email, fullname)
            )
        
        dbConnector.commit()
        dbConnector.close()

        sleep(1)