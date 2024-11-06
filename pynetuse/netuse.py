
import subprocess
import re
from typing import Self


class NetUseError(Exception):
    """An exception from this module.
    """

    def __init__(self, message = ""):
        self.message = message        
        super().__init__(self.message)


class NetUseCommandBuilder:
    """Builder to build cmd commands.
    """

    def __init__(self):
        self.command = ['net', 'use']

    def driveLetter(self, driveLetter: str) -> Self:
        """Adds drive letter to the `net use` command.

        Args:
            driveLetter (str): A drive letter in form e.g. 'C:'

        Raises:
            ValueError: If the drive letter does not match the pattern.

        Returns:
            Self: The builder object.
        """
        pat = re.compile(r"^[A-Z]:$")
        if not pat.fullmatch(driveLetter) or not driveLetter: raise ValueError("Invalid drive letter.")  
        self.command.append(driveLetter)
        return self

    def networkPath(self, networkPath: str) -> Self:
        """Adds network path to the `net use` command.

        Args:
            networkPath (str): A UNC network path e. g. `r"\\\\server\\foo"`

        Raises:
            ValueError: If the network path does not match the the pattern.

        Returns:
            Self: The builder object.
        """
        pat = re.compile(r"^\\\\[\S*\\]+$")
        if not pat.fullmatch(networkPath) or not networkPath: raise ValueError("Invalid network path.")  
        self.command.append(networkPath)
        return self

    def persistent(self, isPersistent: bool) -> Self:
        """Adds persistent parameter to the `net use` command.

        Args:
            isPersistent (bool): True if it is persistent, false if not.

        Returns:
            Self: The builder object.
        """
        if(isPersistent):
            self.command.append('/persistent:yes')
        else:
            self.command.append('/persistent:no')
        return self

    def savecred(self) -> Self:
        """Adds `/savecred` parameter to the `net use` command.

        Returns:
            Self: The builder object.
        """
        self.command.append('/savecred')
        return self

    def smartcard(self) -> Self:
        """Adds `/smartcard` parameter to the `net use` command.

        Returns:
            Self: The builder object.
        """
        self.command.append('/smartcard')
        return self

    def force(self) -> Self:
        """Adds `/yes` parameter to force the `net use` command. Used primarily with `net use X: /delete /yes`.

        Returns:
            Self: The builder object.
        """
        self.command.append('/yes')
        return self

    def user() -> Self:
        pass

    def delete(self) -> Self:
        """Adds delete parameter to indicate removal of mounted drive.

        Returns:
            Self: The builder object.
        """
        self.command.append('/delete')
        return self

    def build(self) -> list[str]:
        return self.command


class NetUseUser:
    def __init__(self, username: str, domain: str = "", password: str = "", save_credentials=False, use_smartcard=False):
        if not username: raise ValueError("Missing required parameter 'username'.")

        # Retrieve the domain username from strings in format "user@domain"
        domain_username = username.split("@")
        if len(domain_username) > 1: username, domain = domain_username[0], domain_username[1]

        # Validate username
        username_pattern = re.compile(r"^[a-zA-Z1-9]+$")
        if not username_pattern.fullmatch(username): raise ValueError("Invalid username.")
        self.username = username

        # Validate domain
        domain_pattern = re.compile(r"^[a-zA-Z]+(\.[a-zA-Z]+)?$")
        if domain and not domain_pattern.fullmatch(domain): raise ValueError("Invalid domain.")
        self.domain = domain

        # Process other parameters
        self.password = password
        self.save_credentials = save_credentials
        self.use_smartcard = use_smartcard

    def build(self, builder: NetUseCommandBuilder) -> NetUseCommandBuilder:
        builder.user()


class NetUseConnection:
    """Represents the net use connection.
    """

    @staticmethod
    def connect(driveLetter: str, path: str, user: NetUseUser = None) -> Self:
        """Connects new network shared drive.

        Args:
            driveLetter (str): Drive letter connection can connect to.
            path (str): Network path to be connected.
            user (NetUseUser, optional): User credentials to use for the connection. Defaults to None.

        Returns:
            Self: The newly created network connection.
        """
        command = NetUseCommandBuilder().driveLetter(driveLetter).networkPath(path)

        subprocess.run(command.build(), capture_output=True, text=True, shell=True)
        return NetUseConnection(driveLetter, path)

    @staticmethod
    def list() -> list[Self]:
        """Lists all available network connections.

        Raises:
            NetUseError: If the command invocation fails.

        Returns:
            list[Self]: List of network connections.
        """
        result = subprocess.run(NetUseCommandBuilder().build(), capture_output=True, text=True, shell=True)
        pattern = re.compile(r"([A-Z]:)\s+(\\\\[\w\\]+)")
        connections = list()

        if result.returncode == 0:
            lines = result.stdout.splitlines()

            for line in lines:
                match = pattern.search(line)
                if match:
                    driveLetter, path = match.groups()
                    connections.append(NetUseConnection(driveLetter, path))
                
            return connections

        else:
            raise NetUseError("An error during net use occured.")

    def __init__(self, driveLetter: str, path: str):
        self.driveLetter = driveLetter
        self.path = path

    def __str__(self) -> str:
        return f"{self.driveLetter} {self.path}"

    def __repr__(self) -> str:
        return f"{self.driveLetter} {self.path}"

    def delete(self, force=False) -> Self:
        """Disconnects network connection.

        Args:
            force (bool, optional): Whether to force disconnection. Defaults to False.

        Returns:
            Self: The disconnected connection.
        """
        command = NetUseCommandBuilder()
        command.driveLetter(self.driveLetter).delete()
        if force: command.force()

        subprocess.run(command.build(), capture_output=True, text=True, shell=True)
        return self
           

def net_use(drive_letter: str = None, network_path: str = None, user: NetUseUser = None) -> list[NetUseConnection]|NetUseConnection:
    """A wrapper for windows `net use` command. Returns a list of connections if no arguments present or creates a new connection.

    Args:
        drive_letter (str, optional): _description_. Defaults to None.
        network_path (str, optional): _description_. Defaults to None.
        user (NetUseUser, optional): _description_. Defaults to None.

    Returns:
        list[NetUseConnection]|NetUseConnection: Newly connected connection or list of connections.
    """
    if not drive_letter and not network_path:
        return NetUseConnection.list()
    else:
        return NetUseConnection.connect(drive_letter, network_path, user)