class EmailTemplate:
    """The email template that's used to build the individualized messages for the Confluence authors.
        
    Attributes
    ----------
    HTML_DECLARATION (class) : String
        The first part of the message.  This part includes the !DOCTYPE tag and the header image.

    INTRO_PARAGRAPH (class) : String
        The intro paragraphs of this message.  

    CONCLUSION_PARAGRAPH (class) : String
        The concluding paragraphs of the message.  This part includes the footer image, and the contact info for the department that sends out this email.

    NOTE -- The messageBuilder.py script builds the customized parts of this message, and the combines these customized parts with the default parts listed above.
    
    
    Methods
    ----------
    None
    """
    
    HTML_DECLARATION = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        body {
            margin-right: auto
        }
        </style>
        </head>
        <body>
        <img src="cid:headerLogo">
        <br><br>
    """

    INTRO_PARAGRAPH = """
        <p>You're receiving this automated email because of the following reasons:</p> <ul> <li>You're a Confluence author.</li> <li>You've updated pages in our public Confluence space.</li> <li>At least one of these PKB pages have images that are missing alternate text.</li> </ul> <p>To help our organization comply with the Americans with Disabilities Act, Confluence authors should ensure that the images on their pages have <a href=\"https://webaim.org/techniques/alttext/\">alternate text</a>. This way, audience members with vision issues can still know what your images are -- when these audience members use their <a href=\"https://www.afb.org/blindness-and-low-vision/using-technology/assistive-technology-products/screen-readers\">screen readers</a> to read what's on your PKB page and that reader comes across your images, that screen reader will read your alternate text.</p> <p>Below is a list of pages that have images missing alternate test. This list also contains links to the specific images that are missing alternate text:</p> <ul>
    """

    CONCLUSION_PARAGRAPH = """
        <p>Please visit the LINK_TO_INSTRUCTIONS page to learn how to update these public Confluence pages.</p> 
        <p>----</p>
        <p><b>But what if you are no longer responsible for the pages listed above?</b></p>
        <p>Please follow one of these two options:</p>
        <ul>
            <li>
                Contact the department who manages the public Confluence pages and let them know about the images on these public pages that are missing alternate text.
            </li>
            <li>
                Reply to this message, letting us know that you're no longer responsible for this content.
            </li>
        </ul>
        <p>----</p>
        <p>Please don't hesitate to reach back out to us, if you have any questions, comments, or concerns. Thanks!</p>
        <br><br>
        <img src="cid:footerLogo">
        <br>
        </body>
        </html>
    """

    def __init__(self):
        """
        Parameters
        ----------
        None
        """

    def __repr__(self):
        return f'EmailTemplate()'