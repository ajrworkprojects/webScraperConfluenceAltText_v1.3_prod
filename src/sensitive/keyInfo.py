class KeyInfo:
    """Variables containing key, sensitive data that this script needs, in order to run
        
    Attributes
    ----------
    CONFLUENCE_SERVER_ADDRESS(class) : String
        The Confluence server that this Python script connects to

    SUB_LINK_VIEW_CONFLUENCE_PAGE(class) : String
        The subdirectory for viewing a specific Confluence page. When a pageID is added to the end of this sub link, the link will be a working link and go to the specific page.

    SUB_LINK_AUTHOR_PAGE(class) : String
        The subdirectory for viewing an author's Confluence page.

    VIP_DIRECTORY_DEPT_URL(class) : String
        The link to the directory for the Confluence Coordinator's department.  Members in this department should not be notified about their pages missing alternate text.  Those pages will get reassigned to the Confluence Coordinator(s).

    URL_PUBLISHED_GOOGLE_SHEET_USERNAMES_OTHER_VIPS : String
        The URL to the published Google Sheet that lists the usernames of the other users/VIPs who should not be notified about Confluence pages with missing alternate text.  

        NOTE -- Google does have an API that for getting info from a Google Sheet, but that API is a paid service.
    
    CONFLUENCE_COORDINATORS_INFO(class) : List
        A list containing tuples of the coordinator's username, email, and fullname.

        NOTE -- These Confluence Coordinators are in the VIP_DIRECTORY_DEPT_URL referenced above.  These coordinators will initially be unassigned all pages that are missing alternate text, but then these same coordinators will be assigned all pages that don't already have recent authors.
    
    Methods
    ----------
    None
    """

    CONFLUENCE_SERVER_ADDRESS = "https://confluence.xyz.com"
    SUB_LINK_VIEW_CONFLUENCE_PAGE = "/pages/viewpage.action?pageId="
    SUB_LINK_AUTHOR_PAGE = "/display/~"

    VIP_DIRECTORY_DEPT_URL = "LINK_TO_URL"
    URL_PUBLISHED_GOOGLE_SHEET_USERNAMES_OTHER_VIPS = "https://docs.google.com/spreadsheets/u/1/d/e/SPECIFIC_ID_FOR_GOOGLE_SHEET/pubhtml?gid=0&single=true"

    CONFLUENCE_COORDINATORS_INFO = [
        ("scarter", "scarter@acme.com", "Stacey Carter")
    ]
    
    def __init__(self):
        """
        Parameters
        ----------
        none
        """

    def __repr__(self):
        return f'KeyInfo()'