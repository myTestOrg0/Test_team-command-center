import json

from gh_user import GHUser
from api_helper import ApiHelper
from gh_branch_protection_rule import GHBranchProtectionRule


class GHRepository:
    """Class representing state of a GitHub repository"""

    def __init__(self, name: str):
        self.owner = GHUser()
        self.members = []
        self.id = 0
        self.name = name
        self.is_private = False
        self.is_fork = False
        self.default_branch = ""
        self.is_archived = False
        self.is_disabled = False
        self.visibility = ""
        self.is_secrets_scanning_enable = False
        self.is_secret_scanning_push_protection_enabled = False
        self.is_secret_scanning_non_provider_patterns_enabled = False
        self.default_branch_protection_rule = GHBranchProtectionRule()
        self.is_dependabot_enabled = False
        self.updated_at = ""
        self.created_at = ""
        self.dependabot_open_alerts_number = 0
        self.secret_scan_alerts_number = 0
        self.have_codeowners_file = False

    def initialize(self, api_helper: ApiHelper) -> None:
        """Extract basic information about repository"""
        self.get_all_members(api_helper)
        self.set_base_info(api_helper)
        self.is_dependabot_enabled = api_helper.get_dependabot_status(self.name)
        self.set_branch_protection_rule_info(api_helper)
        self.set_open_dependabot_alerts_number(api_helper)
        self.set_open_secret_scan_alerts_number(api_helper)
        self.have_codeowners_file = api_helper.search_codeowners_file(self.name)


    def set_base_info(self, api_helper: ApiHelper) -> None:
        """Extract base repository info from API response to object's properties"""
        base_info = api_helper.get_repository_base_info(self.name)
        self.id = base_info["id"]
        self.is_private = base_info["private"]
        self.is_fork = base_info["fork"]
        self.owner.id = base_info["owner"]["id"]
        self.owner.login = base_info["owner"]["login"]
        self.default_branch = base_info["default_branch"]
        self.is_archived = base_info["archived"]
        self.is_disabled = base_info["disabled"]
        self.updated_at = base_info["updated_at"]
        self.created_at = base_info["created_at"]
        self.visibility = base_info["visibility"]
        if base_info["security_and_analysis"]["secret_scanning"]["status"] == "enabled":
            self.is_secrets_scanning_enable = True
        else:
            self.is_secrets_scanning_enable = False

        if base_info["security_and_analysis"]["secret_scanning_push_protection"]["status"] == "enabled":
            self.is_secret_scanning_push_protection_enabled = True
        else:
            self.is_secret_scanning_push_protection_enabled = False

        if base_info["security_and_analysis"]["secret_scanning_non_provider_patterns"]["status"] == "enabled":
            self.is_secret_scanning_non_provider_patterns_enabled = True
        else:
            self.is_secret_scanning_non_provider_patterns_enabled = False

    def proceed_members_info(self, members_info: list) -> None:
        """Extract members info from API response to object's properties"""
        for member_info in members_info:
            member = GHUser()
            member.login = member_info["login"]
            member.id = member_info["id"]
            member.permissions = member_info["permissions"]
            self.members.append(member)

    def set_branch_protection_rule_info(self, api_helper: ApiHelper) -> None:
        """Extract default branch protection rule info from API response to object's properties"""
        rule_info = api_helper.get_branch_protection(self.name, self.default_branch)
        if rule_info == {}:
            return
        self.default_branch_protection_rule.is_enabled = True
        if "required_pull_request_reviews" in rule_info:
            self.default_branch_protection_rule.required_pr = True
            self.default_branch_protection_rule.dismiss_stale_reviews = rule_info["required_pull_request_reviews"][
            "dismiss_stale_reviews"]
            self.default_branch_protection_rule.require_code_owner_reviews = rule_info["required_pull_request_reviews"][
            "require_code_owner_reviews"]
            self.default_branch_protection_rule.required_approving_review_count = rule_info["required_pull_request_reviews"][
            "required_approving_review_count"]
            self.default_branch_protection_rule.require_last_push_approval = rule_info["required_pull_request_reviews"][
            "require_last_push_approval"]
        if "restrictions" in rule_info:
            self.default_branch_protection_rule.push_restrictions = True
        self.default_branch_protection_rule.required_signatures = rule_info["required_signatures"]["enabled"]
        self.default_branch_protection_rule.required_linear_history = rule_info["required_linear_history"]["enabled"]
        self.default_branch_protection_rule.allow_force_pushes = rule_info["allow_force_pushes"]["enabled"]
        self.default_branch_protection_rule.allow_deletions = rule_info["allow_deletions"]["enabled"]
        self.default_branch_protection_rule.block_creations = rule_info["block_creations"]["enabled"]
        self.default_branch_protection_rule.required_conversation_resolution = rule_info["required_conversation_resolution"]["enabled"]
        self.default_branch_protection_rule.lock_branch = rule_info["lock_branch"]["enabled"]
        self.default_branch_protection_rule.allow_fork_syncing = rule_info["allow_fork_syncing"]["enabled"]
        self.default_branch_protection_rule.enforce_admins = rule_info["enforce_admins"]["enabled"]


    def get_all_members(self, api_helper: ApiHelper) -> None:
        """Collect info about repository direct collaborators and from teams"""
        reposiory_teams = api_helper.get_repo_teams_list(self.name)
        for team in reposiory_teams:
            team_members = api_helper.get_team_members_list(team["slug"])
            for team_member in team_members:
                team_member["permissions"] = team["permissions"]
            self.proceed_members_info(team_members)
        repository_members = api_helper.get_repo_members_list(self.name)
        self.proceed_members_info(repository_members)

    def set_open_dependabot_alerts_number(self, api_helper: ApiHelper) -> None:
        """Set up number of open Dependabot alerts"""
        alerts_info = api_helper.get_repo_dependabot_alerts_list(self.name)
        self.dependabot_open_alerts_number = len(alerts_info)

    def set_open_secret_scan_alerts_number(self, api_helper: ApiHelper) -> None:
        """Set up number of open Dependabot alerts"""
        alerts_info = api_helper.get_repo_secret_scan_alerts_list(self.name)
        self.secret_scan_alerts_number = len(alerts_info)


    def print_info(self):
        """Print repository info in console"""
        for name, value in vars(self).items():
            match name:
                case "owner":
                    print("Repository owner:")
                    self.owner.print_info()
                    print("")
                case "members":
                    print("Repository members:")
                    for member in self.members:
                        member.print_info()
                        print("")
                    print("")
                    print("Repository data")
                case "main_branch_protection_rule":
                    print("Default branch protection rule:")
                    if not self.default_branch_protection_rule.is_enabled:
                        print("Branch protection disabled")
                        print("")
                    else:
                        self.default_branch_protection_rule.print_info()
                case _:
                    print(f"{name} = {value}")
        print("---------------")

    def to_json(self) -> str:
        """Convert class to JSON"""
        j = {}
        for name, value in vars(self).items():
            match name:
                case "owner":
                    j["owner"] = self.owner.to_json()
                case "members":
                    j["members"] = []
                    for member in self.members:
                        j["members"].append(member.to_json())
                case "default_branch_protection_rule":
                    if not self.default_branch_protection_rule.is_enabled:
                        j["default_branch_protection_rule"] = {"enabled": False}
                    else:
                        j["default_branch_protection_rule"] = self.default_branch_protection_rule.to_json()
                case _:
                    j[f"{name}"] = value
        return json.dumps(j)
