from api_helper import ApiHelper
from gh_repository import GHRepository
from gh_user import GHUser
import json


class GHOrganization:
    """Class representing state of a GitHub organization"""

    def __init__(self, org_name: str):
        self.org_name = org_name
        self.members = []
        self.repositories = []

    def __initialize_repo(self, api_helper: ApiHelper, repo_base_info: dict) -> GHRepository:
        """Extract basic information about repository"""
        repository = GHRepository()
        repository.set_base_info(repo_base_info)
        repository.is_dependabot_enabled = api_helper.get_dependabot_status(self.org_name,
                                                                            repo_base_info["name"])
        main_branch_protection_rule = api_helper.get_branch_protection(
            self.org_name,
            repo_base_info["name"],
            repo_base_info["default_branch"]
        )
        repository.set_branch_protection_rule_info(main_branch_protection_rule)
        repository_members = api_helper.get_repo_members_list(self.org_name, repo_base_info["name"])
        repository.proceed_members_info(repository_members)
        return repository

    def proceed_members_info(self, members_info: list) -> None:
        """Extract members info from API response to object's properties"""
        for member_info in members_info:
            member = GHUser()
            member.login = member_info["login"]
            member.id = member_info["id"]
            self.members.append(member)

    def initialize(self, api_helper: ApiHelper) -> None:
        """Uses API to get collaborators and repositories lists"""
        repos_base_info = api_helper.get_org_repositories_list(self.org_name)
        for repo in repos_base_info:
            self.repositories.append(self.__initialize_repo(api_helper, repo))
        org_members = api_helper.get_org_members_list(self.org_name)
        self.proceed_members_info(org_members)

    def print_info(self):
        """Print organization info in console"""
        for name, value in vars(self).items():
            match name:
                case "repositories":
                    print("Organization repositories:")
                    for repo in self.repositories:
                        repo.print_info()
                    print("")
                case "members":
                    print("Organization members:")
                    for member in self.members:
                        member.print_info()
                        print("")
                    print("")
                case _:
                    print(f"{name} = {value}")

    def to_json(self) -> str:
        """Convert class to JSON"""
        j = {}
        for name, value in vars(self).items():
            match name:
                case "repositories":
                    j["repositories"] = []
                    for repo in self.repositories:
                        j["repositories"].append(repo.to_json())
                case "members":
                    j["members"] = []
                    for member in self.members:
                        j["members"].append(member.to_json())
                case _:
                    j[f"{name}"] = value
        return json.dumps(j)
