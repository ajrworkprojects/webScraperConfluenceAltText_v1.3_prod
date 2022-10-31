import subprocess
import gc
from datetime import date, datetime

class ACLIController:
    """Makes and returns calls to Bob Swift's ACLI app.
        
        Link to ACLI overview page -- https://bobswift.atlassian.net/wiki/spaces/CSOAP/overview

    Attributes
    ----------
    None
    
    Methods
    ----------
    runACLIaction(username, password, serverAddr, acliAction extraArgs)
        Makes a call to the ACLI app.
        Many of the methods in this ACLIController class calls this method.

    testACLIauthentication(username, password, serverAddr)
        Ensure that the user provided the correct username and password

    getAllConfluencePageIDs(username, password, serverAddr)
        Calls runACLIaction method to get pageIDs and current version numbers for all public Confluence pages

    instanceMethodName(username, password, serverAddr, pageID)
        Receives a pageID and returns a list of the authors who've recently updated the page.
    """
    
    def __init__(self):
        """
        Parameters
        ----------
        none
        """

    def __repr__(self):
        return f'ACLIController()'

    def runACLIaction(
        self, 
        username,
        password,
        serverAddr,
        acliAction,
        extraArgs=[]
    ):
        """
        Makes a call to the ACLI app.
        Many of the methods in this ACLIController class calls this method.
    
        Parameters
        ----------
        username: String
            The user's username

        password: String
            The user's password

        serverAddr: String
            The address to the specific Confluence server the ACLI should connect to

        acliAction : String
            The name of the specific ACLI action getting called.
            Links to documentation:
                - List of Confluence actions -- https://bobswift.atlassian.net/wiki/spaces/CSOAP/pages/10584066/Examples
                - List of Jira actions -- https://bobswift.atlassian.net/wiki/spaces/JCLI/pages/266178329/Actions
        
        extraArgs : List
            A list of extra arguments that could get passed to the ACLI, based on the specific ACLI action
    
        Returns
        ----------
        Class (of type 'subprocess.CompletedProcess')
            Value that is returned after calling a specific ACLI Action
        """

        acliAuthenticationObj = subprocess.run(
            [
                "acli",
                "confluence",
                "--server",
                serverAddr,
                "--user",
                username, 
                "--password",
                password,
                "--action",
                acliAction
            ] + extraArgs,
            capture_output=True, 
            encoding="utf-8"
        )

        return acliAuthenticationObj

    def testACLIauthentication(
        self,
        username,
        password,
        serverAddr
    ):
        """
        Ensure that the user provided the correct username and password
    
        Parameters
        ----------
        username : String
            The user's username

        password : String
            The user's password

        serverAddr : String
            The URL to the server
    
        Returns
        ----------
        Boolean
            True if the user's credentials were authenticated, False otherwise
        """
    
        
        
        if ACLIController.runACLIaction(
            self,
            username=username,
            password=password,
            serverAddr=serverAddr,
            acliAction="getSpaceList"
        ).stderr != "":
            return False
        else:
            return True

    def getAllConfluencePageIDs(
        self,
        username,
        password,
        serverAddr
    ):
        """
        Calls runACLIaction method to get pageIDs and current version numbers for all public Confluence pages
    
        Parameters
        ----------
        username : String
            The user's username

        password : String
            The user's password

        serverAddr : String
            The URL to the server
    
        Returns
        ----------
        List
            A list of tuples, where each tuple contains
            
            - the ID number for a Confluence page,
            - the number of the current version of the page,
        """
    
        results = ACLIController.runACLIaction(
            self,
            username=username,
            password=password,
            serverAddr=serverAddr,
            acliAction="getPageList",
            extraArgs=["--cql", "space=public", "--outputFormat", "2"]
        ).stdout

        results_SplitNewLine = results.split("\n")
        results_SplitCommas = []

        for index, result in enumerate(results_SplitNewLine):
            if index >= 2 and result:
                results_SplitCommas.append([item for item in result.split("\",\"")])

        results_NoQuotes = []

        for result in results_SplitCommas:
            results_NoQuotes.append([item.replace("\"", "") for item in result])

        detailedInfo = []

        for result in results_NoQuotes:
            detailedInfo.append((
                result[1], # <-- PageID number
                result[7], # <-- Number of current version of Confluence page
            ))

        return detailedInfo

    def getRecentAuthors(self, 
        username, 
        password,
        serverAddr,
        pageID
    ):
        """
        Receives a pageID and returns a list of the authors who've recently updated the page.
    
        Parameters
        ----------
        username : String
            The user's username

        password : String
            The user's password

        serverAddr : String
            The URL to the server

        pageID : String
            The unique ID of a Confluence page
    
        Returns
        ----------
        List
            A list of tuples.  Each tuple will contain the authors username and full name.  This list will contain no duplicates.
        """
    
        result = ACLIController.runACLIaction(
            self,
            username=username,
            password=password,
            serverAddr=serverAddr,
            acliAction="getContentHistoryList",
            extraArgs=["--id", pageID, "--dateFormat", "yyyy-MM-dd"]
            # extraArgs=["--id", pageID, "--outputFormat", "2", "--dateFormat", "yyyy-MM-dd"]
        ).stdout
        
        results_SplitNewLine = result.split("\n")
        results_SplitCommas = []

        for index, result in enumerate(results_SplitNewLine):
            if index >= 2 and result:
                results_SplitCommas.append([item for item in result.split("\",\"")])

        results_NoQuotes = []

        for result in results_SplitCommas:
            results_NoQuotes.append([item.replace("\"", "") for item in result])

        allRevisions = []

        for result in results_NoQuotes:
            allRevisions.append((
                result[5], # <-- Date of page revision
                result[6], # <-- Username of the author who published the revision
                result[8] # <-- Name of the author who published the revision
            ))

        # Converts revision dates from yyyy-mm-dd to the number of days since the revision
        
        todaysDate = datetime.today().strftime('%Y-%m-%d')
        todaysDate_obj = date(
            int(todaysDate[0:4]), 
            int(todaysDate[5:7]), 
            int(todaysDate[8:10])
        )
        allRevisions_daysSinceLastEdit = []

        for revision in allRevisions:
            revisionDate = revision[0]
            revisionDate_obj = date(
                int(revisionDate[0:4]), 
                int(revisionDate[5:7]), 
                int(revisionDate[8:10])
            )

            delta = todaysDate_obj - revisionDate_obj

            allRevisions_daysSinceLastEdit.append((
                delta.days,
                revision[1],
                revision[2]
            ))

        # Identifies and returns recent revisions

        recentRevisions_daysSinceLastEdit = []

        if allRevisions_daysSinceLastEdit[0][0] > 30:
            if len(allRevisions_daysSinceLastEdit) < 5:
                recentRevisions_daysSinceLastEdit = allRevisions_daysSinceLastEdit
            else:
                index = 0

                for num in range(5):
                    recentRevisions_daysSinceLastEdit.append(allRevisions_daysSinceLastEdit[index])
                    index+=1
        else:
            for revision in allRevisions_daysSinceLastEdit:
                if revision[0] <= 30:
                    recentRevisions_daysSinceLastEdit.append(revision)

        # Removes duplicate authors

        recentAuthors_dict = {}

        for revision in recentRevisions_daysSinceLastEdit:
            recentAuthors_dict[revision[1]] = revision[2]

        recentAuthors_t = []
        
        for username, fullname in recentAuthors_dict.items():
            recentAuthors_t.append((
                username,
                fullname
            ))

        return recentAuthors_t

