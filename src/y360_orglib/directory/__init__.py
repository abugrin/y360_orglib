"""
Directory API module for interacting with the Y360 Service Applications.
"""

__version__ = "0.1.0"

from y360_orglib.directory.directory_client import DirectoryClient
from y360_orglib.directory.models import Contact, GroupMembers2, GroupsPage, User, UsersPage

__all__ = ["DirectoryClient", "Contact", "GroupMembers2", "GroupsPage", "User", "UsersPage"]