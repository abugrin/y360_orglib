
from typing import List, Tuple
import httpx
from y360_orglib.directory.models import Contact, User, UsersPage
from y360_orglib.common.exceptions import APIError, DirectoryClientError
from y360_orglib.common.http import make_request
from y360_orglib.logging.config import configure_logger

log = configure_logger(logger_name=__name__, console=True)

class DirectoryClient():
    __url = 'https://api360.yandex.net/directory/v1/org/'
    __per_page = 100
    
    def __init__(self, api_key: str, org_id: str, ssl_verify=True):
        self._api_key = api_key
        self._org_id = org_id
        self.session = httpx.Client(verify=ssl_verify)
        self._headers = {
            "Authorization": f"OAuth {api_key}",
            "content-type": "application/json",
        }
        self.session.headers.update(self._headers)

    def count_pages(self)-> Tuple[int, int]:
        """Get number of pages in users list response
            Returns:
                Tuple[int, int]: (users_count, pages_count)
        """

        path = f'{self.__url}{self._org_id}/users?perPage={self.__per_page}'

        try:
            response_json = make_request(session=self.session, url=path, method='GET')
            pages_count = response_json['pages']
            users_count = response_json['total']
            return users_count, pages_count
        except APIError as e:
            log.error(f"Error getting users pages count: {e}")
            raise DirectoryClientError(e)
    
    def get_users_page(self, page) -> UsersPage:
        path = f'{self.__url}{self._org_id}/users?page={page}&perPage={self.__per_page}'

        try:
            response_json = response_json = make_request(session=self.session, url=path, method='GET')
            return UsersPage(**response_json)
        except APIError as e:
            log.error(f"Error getting users page: {e}")
            raise DirectoryClientError(e)
    
    def get_all_users(self) -> List[User]:
        """Get all users of an organization.

        Returns:
            list[User]: List of users
        """

        users = []
        _, total_pages = self.count_pages()
        for page in range(1, total_pages + 1):
            users_page = self.get_users_page(page)
            users.extend(users_page.users)

        return users
    
    
    def add_user_contacts(self, user: User, contacts: List[Contact], replace=False):
        """Add contacts to a user.

        Args:
            user (User): User object
            contacts (List[Contact]): List of contacts
            replace (bool, optional): Replace existing contacts. Defaults to False.
        
        Returns:
            dict: Response json
        """

        path = f'{self.__url}{self._org_id}/users/{user.uid}/contacts'
        
        if replace:
            for user_contact in user.contacts:
                if not user_contact.synthetic:
                    contacts.append(user_contact)
        contacts_json = {"contacts": []}
        for contact in contacts:
            contacts_json["contacts"].append(contact.model_dump(by_alias=True))
        try:
            response_json = make_request(session=self.session, url=path, method='PUT', json=contacts_json)
            return response_json
        except APIError as e:
            log.error(f"Error adding user contacts: {e}")
            raise DirectoryClientError(e)