from credentialsHandler import CredentialsHandler
from ACLIController import ACLIController
from DBCreator import DBCreator
from dbRecordHandler.creator import Creator
from dbRecordHandler.deleter import Deleter
from dbRecordHandler.retriever import Retriever
from dbRecordHandler.updater import Updater
from sensitive.keyInfo import KeyInfo
from seleniumManager import SeleniumManager
from sensitive.emailTemplate import EmailTemplate
from messageBuilder import MessageBuilder
from mailHandler import MailHandler
from getpass import getpass
import sys

acli = ACLIController()
while True:
    print("Provide the credentials for your assigned organizational Gmail account.")
    credsConfCoord = CredentialsHandler()

    if (acli.testACLIauthentication(
        username=credsConfCoord.username,
        password=credsConfCoord.password,
        serverAddr=KeyInfo().CONFLUENCE_SERVER_ADDRESS
    ) == True 
    and "@" in credsConfCoord.emailAddr):
        break # <-- The user provided the correct credentials and likely a valid email address.
    else:
        print("credentials were invalid.  please try again.")

dbCrtr = DBCreator()
if dbCrtr.doesDBexist() == True:
    print("webscraper.db detected")
else:
    print("webscraper.db not detected")
    print("creating base webscraper.db now")
    dbCrtr.createDB()

# Instantiating all necessary objs, for this Python script to interact with webscraper.db
creator = Creator()
deleter = Deleter()
retriever = Retriever()
updater = Updater()

# Instantiating SeleniumManager object and using the user's credentials, to log in to Confluence.
# This script uses Selenium to scrape specific Confluence pages for images missing alternate text.
slmMgr = SeleniumManager()
slmMgr.logInToConfluence(
    serverAddr=KeyInfo().CONFLUENCE_SERVER_ADDRESS, 
    username=credsConfCoord.username, 
    password=credsConfCoord.password
)

print("Getting all current pageIDs from public Confluence space now...")

currentDetailedInfo = acli.getAllConfluencePageIDs(
    username=credsConfCoord.username, 
    password=credsConfCoord.password,
    serverAddr=KeyInfo().CONFLUENCE_SERVER_ADDRESS
)

if len(currentDetailedInfo) == 0:
    sys.exit("""
        This script was able to connect to Bob Swift's Atlassian Command Line Interface (ACLI), but ACLI did not return any public Confluence pages.
        Something may be wrong with ACLI.
        Exiting this script now.
        Review /src/ACLIController.py:getAllConfluencePageIDs and try again.
    """)
    

# This script will add pageIDs-pageVersions as key-value pairs to the following dict.  
# Later on, this script will loop through this dict later, to find pages that were recently updated, and to ensure that pages in the db are currently public and accessible
dict_currentDetailedInfo = {}

for detailedItem in currentDetailedInfo:
    pageID, currentVersionNum = detailedItem
    dict_currentDetailedInfo[pageID] = currentVersionNum

if retriever.wasMajorCLItaskCompleted("GOTIDS") == "FALSE":

    print(f"Number of pageIDs found in public Confluence space: {len(currentDetailedInfo)}")
    print("Checking to see if each of these pageIDs are in the db now...")
    
    for index, detailedItem in enumerate(currentDetailedInfo):
        pageID, currentVersionNum = detailedItem
        
        if retriever.isPageIDInDB(pageID) is False:
            print(f"Page #{index+1} ({pageID}) wasn't in db.  Adding it now...")
            
            creator.addNewConfluencePageToDB(
                versionNum=currentVersionNum, 
                pageID=pageID
            )

            # Technically speaking, when a pageID is added to the db, that counts as a recent update too.  Calling this method and passing "TRUE" ensures that newly added pages get checked for missing alternate text when they're added to the db 
            updater.updateWasPageRecentlyUpdated(
                pageID=pageID, 
                value="TRUE"
            )

        else:
            print(f"Page #{index+1} ({pageID}) was already in db.")

            if (
                pageID in dict_currentDetailedInfo.keys() 
                and int(currentVersionNum) > int(retriever.getOldPageVersion(pageID))
            ):
                
                print(f"Page #{index+1} ({pageID}) has recently been updated.  Updating db now...")
                
                updater.updateOldPageVersion(
                    pageID=pageID, 
                    newPageVersion=dict_currentDetailedInfo[pageID]
                )

                updater.updateWasPageRecentlyUpdated(
                    pageID=pageID, 
                    value="TRUE"
                )

            elif pageID not in dict_currentDetailedInfo.keys():
                print(f"Page #{index+1} ({pageID}) is no longer public.  Removing it from db now...")
                deleter.removePageIDfromAllConfluencePagesTable(pageID)

            else:
                print(f"Page #{index+1} ({pageID}) hasn't been updated recently.  So this CLI will not check this page for missing alternate text...")

        updater.updateWasPageCheckedThisRun(
            pageID=pageID, 
            value="TRUE")

    updater.changeCLIMajorTasksLogValue(
        value="TRUE", 
        dbCode="GOTIDS"
    )

if retriever.wasMajorCLItaskCompleted("PAGESCHECKED") == "FALSE":
    
    print("Gathering pageIDs to check for images missing alternate text now...")

    allPageIDsFromDB = retriever.getPageIDsToCheck()

    allPageIDsPublic = []

    for pageID in allPageIDsFromDB:
        if pageID in dict_currentDetailedInfo.keys():
            allPageIDsPublic.append(pageID)
    
    print(f"Getting ready to check {len(allPageIDsPublic)} pages for missing alternate text now...")

    for index, pageID in enumerate(allPageIDsPublic):
        print(f"\nChecking page #{index+1} ({pageID}) for alternate text now...")

        imagesNamesLinks, pageName = slmMgr.getImagesMisssingAltText(
            baseLink=(
                KeyInfo().CONFLUENCE_SERVER_ADDRESS + 
                KeyInfo().SUB_LINK_VIEW_CONFLUENCE_PAGE
            ), 
            pageID=pageID
        )
        
        if imagesNamesLinks:
            print(f"Page #{index+1} ({pageID}) has images missing alternate text")
            
            creator.addConfluencePageMissingAltText(
                pageID=pageID, 
                pageName=pageName, 
                imageNamesLinks=str(imagesNamesLinks)
            )

        else:
            print(f"Page #{index+1} ({pageID}) either has no images, or all images have alternate text")

            deleter.removePageIDfromMissingAltTextTable(pageID)

    updater.changeCLIMajorTasksLogValue(
        value="TRUE", 
        dbCode="PAGESCHECKED"
    )
    
print("Getting pageIDs of pages missing alternate text...")
pageIDs = retriever.getPageIDsMissingAltTextFromDB()

print(f"Number of pageIDs found: {len(pageIDs)}")

print("Gathering recent authors for all pages missing alternate text...")

for index, pageID in enumerate(pageIDs):
    print(f"Getting recent authors for page #{index+1} ({pageID}) and adding them to db now...")

    recentAuthors = acli.getRecentAuthors(
        username=credsConfCoord.username, 
        password=credsConfCoord.password, 
        serverAddr=KeyInfo().CONFLUENCE_SERVER_ADDRESS, 
        pageID=pageID
    )

    for author_t in recentAuthors:
        username, fullname = author_t
        creator.addAuthorToDB(
            pageID=pageID, 
            username=username, 
            fullname=fullname
        )

print("Getting the author's usernames now, in order to find their email addresses")

usernames = retriever.getAuthorsUsernames()

print(f"Number of usernames found: {len(usernames)}")
print("Finding the authors' email addresses now...")

for index, username in enumerate(usernames):
    print(f"Finding the email address for author #{index+1} ({username}) now and pushing it (or a placeholder) to the db now...")

    address = slmMgr.getEmailAddressFromConfluence(
        username=username, 
        baseLink=(
            KeyInfo().CONFLUENCE_SERVER_ADDRESS +
            KeyInfo().SUB_LINK_AUTHOR_PAGE
        )
    )

    updater.addAuthorEmailToDB(
        username=username, 
        address=address
    )

print("Getting email addresses of some VIPs (departmental members) now...")

VIPsInDept = slmMgr.getDeptVIPsEmails(
    KeyInfo().VIP_DIRECTORY_DEPT_URL
)

if len(VIPsInDept) == 0:
    sys.exit(f"""
        This script did not detect any email addresses in the departmental directory.
        Something about the departmental directory may have changed.
        Exiting this script now.
        Review /src/seleniumManager.py:getDeptVIPsEmails and the departmental directory, and try again.
        Link to the departmental directory: {KeyInfo().VIP_DIRECTORY_DEPT_URL}
    """)

print(f"Number of email addresses for VIPs in department found: {len(VIPsInDept)}")

print("Removing these VIPs from db now...")
for index, email in enumerate(VIPsInDept):
    print(f"Removing VIP address #{index+1} ({email}) now...")
    deleter.removeAuthorFromDB(
        email=email
    )

print("Logging in to your assigned organizational Gmail account now...")

while True:
    if (slmMgr.logInToGmailAccount(
        emailAddr=credsConfCoord.emailAddr, 
        password=credsConfCoord.password
        )):
        break
    else:
        print("Either the credentials were invalid, or the two-factor option wasn't authenticated soon enough, or the Google UI has changed.  Please try again")

print("Getting usernames of the other VIPs (non-departmental members) now...")

VIPsInOrg = slmMgr.getOtherVIPsUsernames(
    KeyInfo().URL_PUBLISHED_GOOGLE_SHEET_USERNAMES_OTHER_VIPS
)

if len(VIPsInOrg) == 0:
    sys.exit(f"""
        This script did not detect any email addresses on the associated Google Sheet.
        Something about this Google Sheet.
        Exiting this script now.
        Review /src/seleniumManager.py:getDeptVIPsEmails and the Google Sheet, and try again.
        Link to the Google Sheet: {KeyInfo().URL_PUBLISHED_GOOGLE_SHEET_USERNAMES_OTHER_VIPS}
    """)

print(f"Number of usernames for VIPs in other departments found: {len(VIPsInOrg)}")

print("Removing these VIPs from db now...")
for index, username in enumerate(VIPsInOrg):
    print(f"Removing VIP username #{index+1} ({username}) now...")
    deleter.removeAuthorFromDB(
        username=username
    )

print("Removing inactive authors from db now...")

deleter.removeInactiveAuthorsFromDB()

print("Unassign authors from stale Confluence pages now...")
print("A \"stale Confluence page\" is a Confluence page that has been missing alternate text for 30 days.")
print("Unassigning authors from stale Confluence pages now, so that the script can reassign these to the Confluence Coordinators later on.")

deleter.unassignAuthorsFromStalePageIDs()

print("Adding Confluence Coordinators to db now...")

for author_t in KeyInfo().CONFLUENCE_COORDINATORS_INFO:
    username, email, fullname = author_t
    creator.addConfluenceCoordinatorToDB(
        username=username, 
        email=email,
        fullname=fullname
    )

print("Assigning pages with no recent authors to Confluence Coordinators now...")

pageIDsMissingAltText = retriever.getPageIDsMissingAltTextFromDB()

print(f"Number of pages with images missing alternate text: {len(pageIDsMissingAltText)}")

for index, pageID in enumerate(pageIDsMissingAltText):
    print(f"Checking page #{index+1} ({pageID}) now...")
    if retriever.doesPageHaveRecentAuthor(pageID) is False:
        creator.assignPageIDtoConfluenceCoordinators(
            pageID=pageID, 
            ConfluenceCoordinators=KeyInfo().CONFLUENCE_COORDINATORS_INFO
        )

print("Building individualized emails to the Confluence authors now...")    
print("Getting usernames of all authors who are assigned to update Confluence pages with images missing alternate text...")

usernames = retriever.getRecentAuthorsForAllPagesMissingAltText()

pairings_usernames_pageIDs = retriever.pairUsernamesWithPageIDsImagesMissingAltText(usernames)

messages = {}

print(f"Number of individual messages to generate: {len(pairings_usernames_pageIDs)}")

for index, (username, pageIDs) in enumerate(pairings_usernames_pageIDs.items()):
    print(f"Generating message #{index+1} for {username} now...")

    fullname = retriever.getFullName(username)
    email = retriever.getEmail(username)

    bundles_pageIDs = [{pageID : retriever.getImagesBundle(pageID)} for pageID in pageIDs]
    
    msgBldr = MessageBuilder()
    
    customMsg = msgBldr.buildHTMLmessage(
        htmlDeclaration=EmailTemplate().HTML_DECLARATION,
        introParagraph=EmailTemplate().INTRO_PARAGRAPH,
        conclusionParagraph=EmailTemplate().CONCLUSION_PARAGRAPH,
        fullname=fullname, 
        bundles_pageIDs=bundles_pageIDs,
        baseLink=(
            KeyInfo().CONFLUENCE_SERVER_ADDRESS + 
            KeyInfo().SUB_LINK_VIEW_CONFLUENCE_PAGE
        )
    )

    messages[email] = customMsg

if retriever.wasMajorCLItaskCompleted("SENTMSGS") == "FALSE":
    print("Provide the credentials for the departmental Gmail account now.")
    print("Be sure to provide the app password for this account (not the main password).")
    credsDeptAcct = CredentialsHandler()
    
    print(f"Number of emails to send: {len(messages)}")
    
    for index, (authorAddr, message) in enumerate(messages.items()):
        print(f"Emailing message #{index+1} to {authorAddr} now...")
        mlHdr = MailHandler(
            fromAddr=credsDeptAcct.emailAddr, 
            fromAddrPassword=credsDeptAcct.password, 
            toAddr=credsConfCoord.emailAddr, # <-- FIXME: Change this arg to 'authorAddr', to send these emails to the authors. 
            htmlMsg=message
        )
        mlHdr.sendEmailToAuthor()

    updater.changeCLIMajorTasksLogValue(
        value="TRUE", 
        dbCode="SENTMSGS"
    )

updater.resetKeyDBValuesToDefault()

print("Summary:")
print(f"Number of pages that have images with missing alternate text: {len(pageIDsMissingAltText)}")
print(f"Number of pages that have been missing this alternate text for 30+ days: {retriever.getNumberOfStalePages()}")
print(f"Number of authors that have been notified about this missing text: {len(messages)}")
