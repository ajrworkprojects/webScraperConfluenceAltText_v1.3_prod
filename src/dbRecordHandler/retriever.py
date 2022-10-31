import sqlite3
import os
from pathlib import Path
from dbRecordHandler.sqlHelper import SQLHelper


class Retriever:
    """Retrieves existing records in the webscraper.db.
        
    Attributes
    ----------
    None
    
    Methods
    ----------
    wasMajorCLItaskCompleted(dbCode)
        Retrieves the value that reflects if a given major CLI task was completed

    isPageIDInDB(pageID)
        Receives pageID, and determines if pageID exists in db.

    getAllPageIDsFromDB()
        Gets and returns all pageIDs from ALL_CONFLUENCE_PAGES

    getOldPageVersion(pageID)
        Receives a pageID and returns that the old page and returns ALL_CONFLUENCE_PAGES.oldPageVersion

    getPageIDsToCheck()
        Returns all CONFLUENCE_PAGES_MISSING_ALT_TEXT.pageID, as well as ALL_CONFLUENCE_PAGES.pageID where wasPageRecentlyUpdated is "TRUE"

    getPageIDsMissingAltTextFromDB()
        Returns all pageIDs in DB that have images with missing alternate text

    getAuthorsUsernames()
        Gets all of the author's usernames from the db

    doesPageHaveRecentAuthor(pageID)
        Receives a pageID and determines if the db has a recent author listed for the page

    getRecentAuthorsForAllPagesMissingAltText()
        Get all recent authors for all pages that have images missing alternate text.

    pairUsernamesWithPageIDsImagesMissingAltText(usernames)
        Receives usernames, and then pairs all of these usernames with the pageIDs with images missing alternate text that are assigned to those usernames.

    getFullName(username)
        Receives the author's username and returns the author's full name.

    getEmail(username)
        Receives the author's username and returns the author's email.

    getImagesBundle(pageID)
        Receives a pageID and returns the name of the page, as well as a string representation of key-value pairs of the image links (key) and the image names (value)

    getNumberOfStalePages()
        Returns the number of pages that have been missing alternate text for 30_ days.
    """

    def __init__(self):
        """
        Parameters
        ----------
        None
        """

    def __repr__(self):
        return f'Retriever()'

    def wasMajorCLItaskCompleted(self, dbCode):
        """
        Retrieves the value that reflects if a given major CLI task was completed
    
        Parameters
        ----------
        dbCode : String
            A shortened (code) representation of a given major CLI task
    
        Returns
        ----------
        String
            "TRUE" if a given major CLI task was completed, "FALSE" otherwise 
        """
        
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        dbCursor.execute("""
            SELECT wasTaskCompletedThisRun FROM LOG_CLI_MAJOR_TASKS
            WHERE majorTaskCode = (?)
        """,
        (dbCode,))

        value = dbCursor.fetchall()[0][0]
        
        dbConnector.commit()
        dbConnector.close()

        return value

    def isPageIDInDB(self, pageID):
        """
        Receives pageID, and determines if pageID exists in db.
    
        Parameters
        ----------
        pageID : String
            Unique ID number for Confluence page
    
        Returns
        ----------
        Boolean
            True if pageID is in db, False otherwise
        """
        
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        dbCursor.execute("""
            SELECT * FROM ALL_CONFLUENCE_PAGES
            WHERE pageID = (?)
        """,
        (pageID,))

        result = dbCursor.fetchall()
        
        dbConnector.commit()
        dbConnector.close()

        return True if result else False

    def getAllPageIDsFromDB(self):
        """
        Gets and returns all pageIDs from ALL_CONFLUENCE_PAGES
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        List
            IDs for all Confluence pages in DB
        """
        
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        dbCursor.execute("""
            SELECT * FROM ALL_CONFLUENCE_PAGES
        """
        )

        t_rows = dbCursor.fetchall()
        results = []

        for t_row in t_rows:
            results.append(t_row[0])
        
        dbConnector.commit()
        dbConnector.close()

        return results

    def getOldPageVersion(self, pageID):
        """
        Receives a pageID and returns that the old page and returns ALL_CONFLUENCE_PAGES.oldPageVersion
    
        Parameters
        ----------
        pageID : String
            Unique ID for a Confluence page
    
        Returns
        ----------
        String
            Old version number for the Confluence page
        """
        
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        dbCursor.execute("""
            SELECT oldPageVersion FROM ALL_CONFLUENCE_PAGES
            WHERE pageID = (?)
        """, (pageID,)
        )

        result = dbCursor.fetchall()[0][0]
        
        dbConnector.commit()
        dbConnector.close()

        return result

    def getPageIDsToCheck(self):
        """
        Returns all CONFLUENCE_PAGES_MISSING_ALT_TEXT.pageID, as well as ALL_CONFLUENCE_PAGES.pageID where wasPageRecentlyUpdated is "TRUE"
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        List
            All pageIDs
        """
        
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        allPageIDs = []
        results = []

        results = dbCursor.execute("""
                SELECT pageID FROM CONFLUENCE_PAGES_MISSING_ALT_TEXT
                """
        ).fetchall()

        [allPageIDs.append(result[0]) for result in results]

        results = dbCursor.execute("""
            SELECT pageID FROM ALL_CONFLUENCE_PAGES
            WHERE wasPageRecentlyUpdated = "TRUE"
            """
        ).fetchall()

        [allPageIDs.append(result[0]) for result in results]
        
        dbConnector.commit()
        dbConnector.close()

        noDups_allPageIDs = list(dict.fromkeys(allPageIDs))

        return noDups_allPageIDs
    
    def getPageIDsMissingAltTextFromDB(self):
        """
        Returns all pageIDs in DB that have images with missing alternate text
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        List
            PageIDs of Confluence pages with images missing alternate text
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        results = dbCursor.execute("""
                SELECT pageID FROM CONFLUENCE_PAGES_MISSING_ALT_TEXT
                """
        ).fetchall()
        
        dbConnector.commit()
        dbConnector.close()

        return [result[0] for result in results]

    def getAuthorsUsernames(self):
        """
        Gets all of the author's usernames from the db
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        List
            All of the author's usernames
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        results = dbCursor.execute("""
                SELECT username FROM ALL_CONFLUENCE_AUTHORS
                """
        ).fetchall()
        
        dbConnector.commit()
        dbConnector.close()

        return [result[0] for result in results]

    def doesPageHaveRecentAuthor(self, pageID):
        """
        Receives a pageID and determines if the db has a recent author listed for the page
    
        Parameters
        ----------
        pageID : String
            Unique ID for a Confluence page
    
        Returns
        ----------
        Boolean
            True if the db has a recent author for the page, False otherwise
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        result = dbCursor.execute("""
                SELECT * FROM RECENT_CONFLUENCE_AUTHORS
                WHERE pageID = (?)
                """, (pageID,)
        ).fetchone()
        
        dbConnector.commit()
        dbConnector.close()

        if result is None:
            return False
        else:
            return True

    def getRecentAuthorsForAllPagesMissingAltText(self):
        """
        Get all recent authors for all pages that have images missing alternate text.
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        List
            Usernames of all recent authors
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        results = dbCursor.execute("""
                SELECT username FROM RECENT_CONFLUENCE_AUTHORS
                """
        ).fetchall()

        usernames = []

        for result in results:
            usernames.append(result[0])

        usernames_NoDups = list(dict.fromkeys(usernames))
        
        dbConnector.commit()
        dbConnector.close()

        return usernames_NoDups

    def pairUsernamesWithPageIDsImagesMissingAltText(self, usernames):
        """
        Receives usernames, and then pairs all of these usernames with the pageIDs with images missing alternate text that are assigned to those usernames.
    
        Parameters
        ----------
        usernames : List
            The usernames of the authors who are assigned
    
        Returns
        ----------
        Dict
            Key-value pairs of an author's username, and a list of the pageIDs assigned to that author
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        pairings_usernames_pageIDs = {}
        
        for username in usernames:
        
            results = dbCursor.execute("""
                    SELECT pageID FROM RECENT_CONFLUENCE_AUTHORS
                    WHERE username = (?)
                    """, (username,)
            ).fetchall()

            pageIDs = [result[0] for result in results]

            pairings_usernames_pageIDs[username] = pageIDs
        
        dbConnector.commit()
        dbConnector.close()

        return pairings_usernames_pageIDs

    def getFullName(self, username):
        """
        Receives the author's username and returns the author's full name.

        Parameters
        ----------
        username : String
            The author's username
    
        Returns
        ----------
        String
            The author's full name
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        result = dbCursor.execute("""
            SELECT fullname FROM ALL_CONFLUENCE_AUTHORS
            WHERE username = (?)
        """, (username,)).fetchone()
        
        return result[0]

    def getEmail(self, username):
        """
        Receives the author's username and returns the author's email.

        Parameters
        ----------
        username : String
            The author's username
    
        Returns
        ----------
        String
            The author's email address
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        result = dbCursor.execute("""
            SELECT email FROM ALL_CONFLUENCE_AUTHORS
            WHERE username = (?)
        """, (username,)).fetchone()
        
        return result[0]

    def getImagesBundle(self, pageID):
        """
        Receives a pageID and returns the name of the page, as well as a string representation of key-value pairs of the image links (key) and the image names (value)

        Parameters
        ----------
        pageID : String
            The unique ID for a Confluence page
    
        Returns
        ----------
        Tuple
            A two item tuple containing the name of the Confluence page, and a dict of the image links (key) and the image names (value)
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        result = dbCursor.execute("""
            SELECT pageName, imageNamesLinks FROM CONFLUENCE_PAGES_MISSING_ALT_TEXT
            WHERE pageID = (?)
        """, (pageID,)).fetchone()
        
        return result

    def getNumberOfStalePages(self):
        """
        Returns the number of pages that have been missing alternate text for 30_ days.
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        String
            A string reprensation of the number of stale pages in db
        """
    
        dbConnector = sqlite3.connect(str(Path.cwd())+"/src/sensitive/webscraper.db")
        dbCursor = dbConnector.cursor()

        dbCursor.executescript(SQLHelper().SQL_QUERIES)

        stalePageIDs = dbCursor.execute("""
                SELECT pageID FROM LOG_CONFLUENCE_PAGES_TO_FIX
                WHERE numDaysMissingAltText > 30"""
            ).fetchall()
        
        dbConnector.commit()
        dbConnector.close()

        return str(len(stalePageIDs))