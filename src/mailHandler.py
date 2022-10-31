import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path

class MailHandler:
    """Receives various values for an email (such as an author's email address and their individualized message), and then emails that message to that author.

    ref:  https://www.justintodata.com/send-email-using-python-tutorial/ (specifically the "Send HTML with attachment Emails" section)
        
    Attributes
    ----------
    fromAddr : String
        The departmental Gmail address the customized messages is getting sent from

    fromAddrPassword : String
        The app password for the departmental Gmail address

    toAddr : String
        The address of the Confluence author

    htmlMsg : String
        The HTML version of the customized message for the Confluence author
    

    Methods
    ----------
    sendEmailToAuthor()
        Emails the Confluence author their customized message.
    """

    def __init__(
        self,
        fromAddr,
        fromAddrPassword,
        toAddr,
        htmlMsg):
        """
        Parameters
        ----------
        fromAddr : String
            The departmental Gmail address the customized messages is getting sent from

        fromAddrPassword : String
            The app password for the departmental Gmail address

        toAddr : String
            The address of the Confluence author

        htmlMsg : String
            The HTML version of the customized message for the Confluence author
        """

        self.fromAddr = fromAddr
        self.fromAddrPassword = fromAddrPassword
        self.toAddr = toAddr
        self.htmlMsg = htmlMsg

        self.mimeMsg = MIMEMultipart()
        self.mimeMsg["From"] = self.fromAddr
        self.mimeMsg["To"] = self.toAddr
        self.mimeMsg["Subject"] = "Adding alternate text to images on public Confluence pages"
        self.mimeMsg.attach(MIMEText(self.htmlMsg, "html"))

        with open(str(Path.cwd())+"/src/sensitive/headerLogo.png", "rb") as f:
            self.embeddedImage = MIMEApplication(f.read())
        self.embeddedImage.add_header(
            "Content-Disposition",
            f"attachment; filename={str(Path.cwd())}/src/sensitive/headerLogo.png"
        )
        self.embeddedImage.add_header("Content-ID", "<headerLogo>")
        self.mimeMsg.attach(self.embeddedImage)

        with open(str(Path.cwd())+"/src/sensitive/footerLogo.png", "rb") as f:
            self.embeddedImage = MIMEApplication(f.read())
        self.embeddedImage.add_header(
            "Content-Disposition",
            f"attachment; filename={str(Path.cwd())}/src/sensitive/footerLogo.png"
        )
        self.embeddedImage.add_header("Content-ID", "<footerLogo>")
        self.mimeMsg.attach(self.embeddedImage)

        self.strMsg = self.mimeMsg.as_string()

    def __repr__(self):
        return f'MailHandler()'

    def sendEmailToAuthor(self):
        """
        Emails the Confluence author their customized message.
    
        Parameters
        ----------
        None
    
        Returns
        ----------
        None
        """
    
        sslContext = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=sslContext)
            server.login(self.fromAddr, self.fromAddrPassword)
            server.sendmail(self.fromAddr, self.toAddr, self.strMsg)