## Unofficial library collection for Y360 API

#### Installation

```bash
pip install y360-orglib

```
#### Import
```
import y360_orglib
```

### Available Modules:

- `serviceapp`: ServiceApps module for interacting with the Y360 Service Applications.
- `disk`: Disk Client module for interacting with the Y360 Disk REST API.
- `directory`: Directory API module for interacting with the Y360 Directory API.
- `audit`: Audit Log module for interacting with the Y360 Audit Log API.


### ServiceAppClient

Init client
```python
service_apps_client = ServiceAppClient(client_id, client_secret)
```

Get a service app token for for given User (subject_token).
- subject_token: User Id or Email<br/>
- subject_token_type: The type of the subject token.<br/>
    - If the subject_token is a User ID, the subject_token_type should be 'urn:yandex:params:oauth:token-type:uid'.
    - If the subject_token is an Email, the subject_token_type should be 'urn:yandex:params:oauth:token-type:email'.
    - Default value is 'urn:yandex:params:oauth:token-type:email'.
- Returns: ServiceAppTokenResponse - Response with service app token for provided User
        
```

service_apps_client.get_service_app_token(subject_token="user@email.com").access_token

or

service_apps_client.get_service_app_token(subject_token="12344556", subject_token_type = "urn:yandex:params:oauth:token-type:uid").access_token

```

### Directory Client

#### Features
- User management (retrieve users, modify contacts)
- Group management (retrieve groups, add users to groups)
- Contact management
- 2FA status checking

#### Initialization
```python
from y360_orglib.directory.client import DirectoryClient
import logging

# Initialize the client
client = DirectoryClient(
    api_key="your-api-key",
    org_id="your-organization-id",
    ssl_verify=True,
    log_level=logging.INFO
)

```

Working with UsersGet all users in the organizationtry:
    # Get all users
    all_users = client.get_all_users()
    
    # Process users
    for user in all_users:
        print(f"User: {user.display_name} ({user.email})")
except Exception as e:
    print(f"Error retrieving users: {e}")
Get users by page# Get users count and total pages
users_count, pages_count = client.count_pages()
print(f"Organization has {users_count} users across {pages_count} pages")

# Get a specific page of users
users_page = client.get_users_page(page=1)
for user in users_page.users:
    print(f"User: {user.name.first} {user.name.last} ({user.email})")
Working with Contactsfrom y360_orglib.directory.models import Contact, User

# Example: Add a phone contact to a user
user = client.get_users_page(page=1).users[0]  # Get first user from first page
phone_contact = Contact(
    contact_type='phone',
    value='+71234567890',
    main=True
)

# Add contact to user
client.add_user_contacts(
    user=user, 
    contacts=[phone_contact], 
    replace=False  # Set to True to replace all existing contacts
)
Working with GroupsGet groups# Get groups with pagination
groups_page = client.get_groups_page(page=1, per_page=10)
for group in groups_page.groups:
    print(f"Group: {group.name} (ID: {group.group_id})")
Get group members# Get members of a specific group
group_id = 123  # Replace with actual group ID
group_members = client.get_group_members_v2(group_id)

# Print users in the group
for user in group_members.users:
    print(f"User in group: {user.name.first} {user.name.last}")

# Print subgroups in the group
for group in group_members.groups:
    print(f"Subgroup: {group.name}")
Add user to group# Add a user to a group
user_id = "123456"  # Replace with actual user ID
group_id = 789  # Replace with actual group ID
response = client.add_user_to_group(user_id=user_id, group_id=group_id)
Working with 2FA# Check 2FA status for a user
user_id = "123456"  # Replace with actual user ID
user_2fa = client.get_user_2fa(user_id)
print(f"2FA enabled: {user_2fa.has2fa}")
print(f"Security phone: {user_2fa.has_security_phone}")
ModelsThe library uses Pydantic models to represent Yandex 360 entities:Contactclass Contact(BaseModel):
    contact_type: Literal['email', 'phone_extension', 'phone', 'site', 'icq', 'twitter', 'skype', 'staff']
    value: str
    main: bool = False
    alias: bool = False
    synthetic: bool = False
UserUsers are represented by ShortUser and User models. User extends ShortUser with additional fields.GroupGroups are represented by ShortGroup and Group models. Group extends ShortGroup with additional fields.Error HandlingThe library raises the following exceptions:
DirectoryClientError: Base exception for directory client errors
APIError: Raised when the API returns an error
Example:from y360_orglib.common.exceptions import DirectoryClientError, APIError

try:
    users = client.get_all_users()
except DirectoryClientError as e:
    print(f"Directory client error: {e}")
except APIError as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
License[Include license information here]Contributing[Include contribution guidelines here]