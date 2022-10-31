from getpass import getpass

class CredentialsHandler:
    """Collects login credentials from user.  Passes these credentials to other modules.
        
    Attributes
    ----------
    emailAddr : String
        The email address the user enters
    
    username : String
        The user's username

    password : String
        The user's password
    
    
    Methods
    ----------
    None
    """

    def __init__(self):
        """
        Parameters
        ----------
        emailAddr : String
            The email address the user enters
        
        username : String
            The username that is derived from the email address the user enters

        password : String
            The password the user enters
        """

        self._emailAddr = input("email address: ")
        self._username = self._emailAddr.split("@")[0]
        self._password = getpass("password: ")

    def __repr__(self):
        return f'CredentialsHandler({self._emailAddr}, {self._username}, passwordHidden)'

    @property
    def emailAddr(self):
        return self._emailAddr
    
    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password