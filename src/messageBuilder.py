import ast

class MessageBuilder:
    """Builds the custom message for the Confluence author
        
    Attributes
    ----------
    None
    
    
    Methods
    ----------
    buildHTMLmessage(parameter)
        Receives the necessary parts and other details for the individualized message, and then builds the message.
    """

    def __init__(self):
        """
        Parameters
        ----------
        None
        """

    def __repr__(self):
        return f'MessageBuilder()'
    
    def buildHTMLmessage(
        self,
        htmlDeclaration,
        introParagraph,
        conclusionParagraph,
        fullname,
        bundles_pageIDs,
        baseLink
    ):
        """
        Receives the necessary parts and other details for the individualized message, and then builds the message.
    
        Parameters
        ----------
        firstPartOfMessage : String
            The first part of the message.  This part is a template.

        lastPartOfMessage : String
            The last part of the message.  This part is a template.

        fullname : String
            The author's fullname

        bundles_pageIDs : List
            Each item in the list consist of the following key-value pairs:
                Key = pageID
                Value = two-item tuple
                    - pageName
                    - string representation of a dict
                        Key = image link
                        Value = image name

        baseLink : String
            The baselink for a Confluence page
    
        Returns
        ----------
        String
            The customized message
        """

        salutations = f"<p>Hello {fullname},</p>"
        bigBulletedList = ""
        terminatingBigList = "</ul>"
        
        for bundle in bundles_pageIDs:
            pageID = list(bundle.keys())[0]
            pageName = bundle.get(pageID)[0]
            imagesLinksNames_d = ast.literal_eval(
                bundle.get(pageID)[1]
            )

            completeListItem = f"<li><a href=\"{baseLink+pageID}\">{pageName}</a><ul>"

            for imageLink, imageName in imagesLinksNames_d.items():
                completeListItem += f"<li><a href=\"{imageLink}\">{imageName}</a></li>"
            
            completeListItem += "</ul></li>"

            bigBulletedList += completeListItem
        
        return "".join(
            htmlDeclaration+
            salutations +
            introParagraph +
            bigBulletedList +
            terminatingBigList +
            conclusionParagraph
        )