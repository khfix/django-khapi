from khapi.auth_system.models import ApiGroup, ApiRole, Token
from khapi.cache_system.cache_models import *


class ApiPermissionCore:
    """
    Class for managing API permissions.

    Attributes:
        Tokens_dict (dict): A dictionary to store tokens.
        Api_Groups_dict (dict): A dictionary to store API groups.
        Api_Roles_dict (dict): A dictionary to store API roles.
        status (bool): The status of the permission check.
        erorr_message (str): The error message if the permission check fails.
    """

    Tokens_dict = {}
    Api_Groups_dict = {}
    Api_Roles_dict = {}
    status = False
    erorr_message = ""
    found_check = False

    def __init__(self, *args, **kwargs):
        """
        Initializes an instance of ApiPermissionCore.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
                - store (bool): If True, store tokens, API groups, and API roles.
                - update (str): The type of update to perform (Token, ApiGroup, ApiRole).
                - check (str): The API role to check.
                - token (str): The token to check.
                - api_key (str): The API key to check.
        """
        if "store" in kwargs and kwargs["store"] == True:
            self.store_tokens()
            self.store_api_groups()
            self.store_api_roles()
        elif "update" in kwargs:
            if kwargs["update"] == "token":
                self.update_tokens(kwargs["token"], kwargs["email"])
            self.update(kwargs["update"])
        elif "check" in kwargs:
            self.check(kwargs["check"], kwargs["token"], kwargs["api_key"])

        else:
            self.Tokens_dict = globals()["Tokens_dict"]
            self.Api_Groups_dict = globals()["Api_Groups_dict"]
            self.Api_Roles_dict = globals()["Api_Roles_dict"]

    def store_tokens(self):
        """
        Stores tokens in the Tokens_dict dictionary.
        """
        self.Tokens_dict.clear()
        tokens = Token.objects.all()
        for token in tokens:
            self.Tokens_dict[token.token] = token.user.email

    def update_tokens(self, token, email):
        """
        Updates the Tokens_dict dictionary.
        """
        for key, value in self.Tokens_dict.items():
            if key == token or value == email:
                del self.Tokens_dict[key]
                self.Tokens_dict[token] = email
                self.found_check = True
        if self.found_check:
            pass
        else:
            self.Tokens_dict[token] = email

    def store_api_groups(self):
        """
        Stores API groups in the Api_Groups_dict dictionary.
        """
        self.Api_Groups_dict.clear()
        api_groups = ApiGroup.objects.all()
        for api_group in api_groups:
            self.Api_Groups_dict[api_group.name] = []
            for user in api_group.user.all():
                self.Api_Groups_dict[api_group.name].append(user.email)

    def store_api_roles(self):
        """
        Stores API roles in the Api_Roles_dict dictionary.
        """
        self.Api_Roles_dict.clear()
        api_roles = ApiRole.objects.filter(security_check=True)
        for api_role in api_roles:
            self.Api_Roles_dict[api_role.name] = []
            if api_role.auth_type == "AUTHENTICATED":
                self.Api_Roles_dict[api_role.name].append("AUTHENTICATED")
                for token in self.Tokens_dict:
                    self.Api_Roles_dict[api_role.name].append(token)
                if api_role.api_key_status:
                    self.Api_Roles_dict[api_role.name].append("HTTP_API_KEY")
                    self.Api_Roles_dict[api_role.name].append(
                        f"API-KEY{api_role.api_key}"
                    )
            elif api_role.auth_type == "API-GROUP":
                self.Api_Roles_dict[api_role.name].append("AUTHENTICATED")
                for api_group in api_role.api_groups.all():
                    for user in self.Api_Groups_dict[api_group.name]:
                        for token in self.Tokens_dict:
                            if user == self.Tokens_dict[token]:
                                self.Api_Roles_dict[api_role.name].append(token)
                if api_role.api_key_status:
                    self.Api_Roles_dict[api_role.name].append("HTTP_API_KEY")
                    self.Api_Roles_dict[api_role.name].append(
                        f"API-KEY{api_role.api_key}"
                    )
            elif api_role.auth_type == "PUBLIC":
                self.Api_Roles_dict[api_role.name].append("PUBLIC")
                if api_role.api_key_status:
                    self.Api_Roles_dict[api_role.name].append("HTTP_API_KEY")
                    self.Api_Roles_dict[api_role.name].append(
                        f"API-KEY{api_role.api_key}"
                    )

    def update(self, update):
        """
        Updates the specified component (Token, ApiGroup, ApiRole) or all components.

        Args:
            update (str): The type of update to perform.
        """
        if update == "Token":
            self.store_tokens()
        elif update == "ApiGroup":
            self.store_api_groups()
        elif update == "ApiRole":
            self.store_api_roles()
        else:
            self.store_tokens()
            self.store_api_groups()
            self.store_api_roles()

    def check(self, check, token, api_key):
        """
        Checks if the given token and API key have the required permissions.

        Args:
            check (str): The API role to check.
            token (str): The token to check.
            api_key (str): The API key to check.
        """
        data = self.Api_Roles_dict.get(check)
        if data is not None:
            if "AUTHENTICATED" in data and "HTTP_API_KEY" in data:
                api_key = f"API-KEY{api_key}"
                token = token.replace("Token ", "")
                if token in data and api_key in data:
                    self.status = True
                else:
                    if token not in data:
                        self.erorr_message = "You are not authenticated"
                        self.status = False
                    elif api_key not in data:
                        self.erorr_message = "API-KEY is not valid"
                        self.status = False
            elif "AUTHENTICATED" in data:
                token = token.replace("Token ", "")
                if token in data:
                    self.status = True
                else:
                    if token not in data:
                        self.erorr_message = "You are not authenticated"
                        self.status = False
            elif "HTTP_API_KEY" in data:
                api_key = f"API-KEY{api_key}"
                if api_key in data:
                    self.status = True
                else:
                    if api_key not in data:
                        self.erorr_message = "API-KEY is not valid"
                        self.status = False
            elif "PUBLIC" in data:
                self.status = True
        else:
            self.status = True
