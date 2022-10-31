from selenium import webdriver # webdriver is necessary for UI automation for specific web browsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sys
from time import sleep

class SeleniumManager:
    """Uses the Selenium module to get the page source of Confluence pages
        
    Attributes
    ----------
    driver (class) : WebDriver
        Necessary to use Selenium to retrieve webpages

    chrome_options (class) : Options
        Necessary to add arguments to pass to the driver attribute
    
    
    Methods
    ----------
    getImagesMisssingAltText(baseLink, pageID)
        Receives a pageID, then identifies images on the Confluence page that are missing alternate text, and then returns a tuple of detailed information about the page and its images

    logInToConfluence(serverAddr, username, password)
        Receives the user's login credentials and logs the Selenium instance that this Python script uses into Confluence

    getEmailAddressFromConfluence(username, baseLink)
        Receives an author's username and returns the author's email address

    getDeptVIPsEmails(directoryURL)
        Scrapes the organizational directory for the email addresses of the users who should not be notified about Confluence pages with missing alternate text.

    logInToGmailAccount(emailAddr, password)
        Logs in to your assigned organizational Gmail account.  Your Gmail account has access to the necessary Google Sheet that lists other VIPs that shouldn't be contacted about pages missing alternate text.

    getOtherVIPsUsernames(pageURL)
        Scrapes a published Google Sheet for the usernames of the other users who should not be notified about Confluence pages with missing alternate text.  

        NOTE -- Google does have an API that for getting info from a Google Sheet, but that API is a paid service.
    """

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(5)
    
    def __init__(self):
        """
        Parameters
        ----------
        None
        """

    def __repr__(self):
        return f'SeleniumManager()'

    def getImagesMisssingAltText(self, baseLink, pageID):
        """
        Receives a pageID, then identifies images on the  Confluence page that are missing alternate text, and then returns a tuple of detailed information about the page and its images
    
        Parameters
        ----------
        baseLink : String
            The base link for a Confluence page.  Will look something like "https://confluence.xyz.com/pages/viewpage.action?pageId="

        pageID : String
            The unique ID for a Confluence page
    
        Returns
        ----------
        Tuple
            A two item tuple
            - The first item is a dict of key-value pairs of links to images and the image names.  Will return an empty dict if either the page has no images, or all images have alernate text.
            - The second item is the page name.
        """
    
        self.driver.get(baseLink+pageID)
        self.driver.implicitly_wait(0)

        imgElements = []
        imagesNamesLinks = {}

        try:
            imgElements = self.driver.find_elements(
                By.CLASS_NAME,
                "confluence-embedded-image"
            )
        except:
            pass

        print(f"\tNumber of images found: {len(imgElements)}")

        for imgElement in imgElements:
            if imgElement.get_attribute("alt") == "":
                imagesNamesLinks[
                    imgElement.get_attribute("src")
                ] = imgElement.get_attribute("data-linked-resource-default-alias")

        print(f"\tNumber of images that have alternate text: {len(imgElements)-len(imagesNamesLinks)}")
        
        print(f"\tNumber of images that are missing alternate text: {len(imagesNamesLinks)}")

        pageName = self.driver.find_element(
            By.CSS_SELECTOR,
            "meta[name=\"ajs-page-title\"]"
        ).get_attribute("content")

        self.driver.implicitly_wait(5)

        return (imagesNamesLinks, pageName)

    def logInToConfluence(self, serverAddr, username, password):
        """
        Receives the user's login credentials and logs the Selenium instance that this Python script uses into Confluence
    
        Parameters
        ----------
        serverAddr : String
            The Confluence instance this Selenium instance should log in to

        username : String
            The user's username

        password : String
            The user's password
    
        Returns
        ----------
        None
        """
    
        self.driver.get(serverAddr)
        
        self.driver.find_element(
            By.ID,
            "username"
        ).send_keys(username)
        self.driver.find_element(
            By.ID,
            "password"
        ).send_keys(password)
        
        self.driver.find_element(
            By.ID,
            "login-button"
        ).click()

        welcomeElem = "not found yet"
        
        try:
            welcomeElem = self.driver.find_element(
                By.CSS_SELECTOR,
                "meta[name=\"ajs-show-space-welcome-dialog\"]"
            )
        except:
            pass

    def getEmailAddressFromConfluence(self, username, baseLink):
        """
        Receives an author's username and returns the author's email address
    
        Parameters
        ----------
        username : String
            The author's username

        baseLink : String
            The base link for an author's profile page in Confluence
    
        Returns
        ----------
        String
            The author's email address
        """
    
        self.driver.get(baseLink+username)

        self.driver.implicitly_wait(0)

        try:
            address = self.driver.find_element(
                By.ID,
                "email"
            ).text
        except:
            address = "Address not found"

        self.driver.implicitly_wait(5)
        
        return address

    def getDeptVIPsEmails(self, directoryURL):
        """
        Scrapes the organizational directory for the email addresses of the users who should not be notified about Confluence pages with missing alternate text.
    
        Parameters
        ----------
        directoryURL : String
            The URL to the departmental directory page
    
        Returns
        ----------
        List
            The email addresses for the users in a specific department who should not receive notifications.
        """
    
        self.driver.get(directoryURL)

        keyElements = self.driver.find_elements(
            By.CSS_SELECTOR,
            "clr-dg-cell[role=\"gridcell\"]"
        )

        emails = []

        for element in keyElements:
            if "@" in element.text:
                emails.append(element.text)

        return emails

    def logInToGmailAccount(self, emailAddr, password):
        """
        Logs in to your assigned organizational Gmail account.  Your Gmail account has access to the necessary Google Sheet that lists other VIPs that shouldn't be contacted about pages missing alternate text.
    
        Parameters
        ----------
        emailAddr : String
            The email address for the Confluence coordinator running this script.

        password : String
            The password to the  Confluence coordinator running this script.
    
        Returns
        ----------
        Boolean
            True if the login was successful, False otherwise.
            NOTE -- Odds are, if the user is providing the correct credentials but this method still returns False, then the UI for the Google login has changed.  These changes have broken this script.  This script needs to be updated.  The updates should be relatively minor.
        """

        print("A new Chrome window will open in ~3 seconds.")
        print("The script will automatically enter in the credentials you provided earlier.")
        print("Complete the two-step verification.")
        
        self.chrome_options = Options()
        self.chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        
        self.driver.get("https://accounts.google.com")

        try:
            
            self.driver.find_element(
                By.ID,
                "identifierId"
            ).send_keys(emailAddr)
            self.driver.find_element(
                By.XPATH,
                "//*[@id=\"identifierNext\"]/div/button"
            ).click()

            sleep(5)

            self.driver.find_element(
                By.CSS_SELECTOR,
                "input[type=\"password\"]"
            ).send_keys(password)
            self.driver.find_element(
                By.XPATH,
                "//*[@id=\"passwordNext\"]/div/button"
            ).click()

            print("You'll have 30 seconds to provide the two-factor option.")
            print("A full 30 seconds will have to pass, for this script to continue.")
            print("Leave the Chrome window open.")

            for i in range(30, 0, -1):
                print(f"\r\t{i} seconds remaining...", end="")
                sys.stdout.flush()
                sleep(1)
            print("\r", end="")
            sys.stdout.flush()

            if emailAddr in self.driver.find_element(
                By.CSS_SELECTOR,
                "a[role=\"button\"]"
            ).get_attribute("aria-label"):
                pass

            return True
            
        except:
            
            return False

    def getOtherVIPsUsernames(self, pageURL):
        """
        Scrapes a published Google Sheet for the usernames of the other users who should not be notified about Confluence pages with missing alternate text.  

        NOTE -- Google does have an API that for getting info from a Google Sheet, but that API is a paid service.
    
        Parameters
        ----------
        pageURL : String
            The URL to the published Google Sheet
    
        Returns
        ----------
        List
            The usernames for the other users who should not receive notifications
        """
        
        print("Navigating to the published Google Sheet that has the usernames of the other VIPs (non-departmental members)")
        print("The new Chrome window will automatically close, after the script gets the VIPs' usernames.")
        
        sleep(5)

        self.driver.get(pageURL)

        sleep(5)

        tdElems = self.driver.find_elements(
            By.CLASS_NAME,
            "s0"
        )

        usernames = [elem.text for elem in tdElems]
        
        self.driver.switch_to.default_content()
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        self.driver.implicitly_wait(5)

        return usernames