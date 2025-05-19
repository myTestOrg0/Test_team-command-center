import json
import fnmatch

from gh_user import GHUser
from api_helper import ApiHelper
from gh_branch_protection_rule import GHBranchProtectionRule
from gh_environment import GHEnvironment


class GHRepository:
    """Class representing state of a GitHub repository"""

    def __init__(self, name: str):
        self.owner = GHUser()
        self.members = []
        self.id = 0
        self.name = name
        self.is_private = False
        self.is_fork = False
        self.default_branch = "main"
        self.is_archived = False
        self.is_disabled = False
        self.visibility = ""
        self.is_secrets_scanning_enable = False
        self.is_secret_scanning_push_protection_enabled = False
        self.is_secret_scanning_non_provider_patterns_enabled = False
        self.branch_protection_rules = []
        self.is_dependabot_enabled = False
        self.updated_at = ""
        self.created_at = ""
        self.dependabot_open_alerts_number = 0
        self.secret_scan_alerts_number = 0
        self.have_codeowners_file = False
        self.branches = []
        self.branches_2_protect = ["main", "develop"]
        self.environments = []

    def __clarify_branches_2_protect(self, api_helper: ApiHelper) -> None:
        """Clarify what exact branches must be protected"""
        self.branches_2_protect = [
            branch for branch in self.branches_2_protect
            if branch in self.branches
        ]
        if self.default_branch not in self.branches_2_protect:
            self.branches_2_protect.append(self.default_branch)

    def initialize(self, api_helper: ApiHelper) -> None:
        """Extract basic information about repository"""
        self.set_base_info(api_helper)
        self.set_branches(api_helper)
        self.__clarify_branches_2_protect(api_helper)
        self.set_environments(api_helper)
        self.set_members(api_helper)
        self.is_dependabot_enabled = api_helper.get_dependabot_status(self.name)
        for branch in self.branches_2_protect:
            self.branch_protection_rules.append(self.set_branch_protection_rule_info(api_helper, branch))
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

    def proceed_members_info(self, members_info: list) -> list:
        """Extract members info from API response to object's properties"""
        members = []
        for member_info in members_info:
            member = GHUser()
            member.login = member_info["login"]
            member.id = member_info["id"]
            if "permissions" not in member_info.keys():
                member.permissions = []
            else:
                member.permissions = member_info["permissions"]
            members.append(member)
        return members
    def set_branch_protection_rule_info(self, api_helper: ApiHelper, branch_name: str) -> GHBranchProtectionRule:
        """Extract default branch protection rule info from API response to object's properties"""
        branch_protection_rule = GHBranchProtectionRule()
        branch_protection_rule.branch_name = branch_name
        rule_info = api_helper.get_branch_protection(self.name, branch_name)
        if rule_info == {}:
            return branch_protection_rule
        branch_protection_rule.is_enabled = True
        if "required_pull_request_reviews" in rule_info:
            branch_protection_rule.required_pr = True
            branch_protection_rule.dismiss_stale_reviews = rule_info["required_pull_request_reviews"][
                "dismiss_stale_reviews"]
            branch_protection_rule.require_code_owner_reviews = rule_info["required_pull_request_reviews"][
                "require_code_owner_reviews"]
            branch_protection_rule.required_approving_review_count = rule_info["required_pull_request_reviews"][
                "required_approving_review_count"]
            branch_protection_rule.require_last_push_approval = rule_info["required_pull_request_reviews"][
                "require_last_push_approval"]
            if "bypass_pull_request_allowances" in rule_info["required_pull_request_reviews"]:
                branch_protection_rule.bypass_pull_request_allowances["users"] = \
                    rule_info["required_pull_request_reviews"]["bypass_pull_request_allowances"]["users"]
                branch_protection_rule.bypass_pull_request_allowances["teams"] = \
                    rule_info["required_pull_request_reviews"]["bypass_pull_request_allowances"]["teams"]
                branch_protection_rule.bypass_pull_request_allowances["apps"] = \
                    rule_info["required_pull_request_reviews"]["bypass_pull_request_allowances"]["apps"]
        if "restrictions" in rule_info:
            branch_protection_rule.push_restrictions = True

        branch_protection_rule.required_signatures = rule_info["required_signatures"]["enabled"]
        branch_protection_rule.required_linear_history = rule_info["required_linear_history"]["enabled"]
        branch_protection_rule.allow_force_pushes = rule_info["allow_force_pushes"]["enabled"]
        branch_protection_rule.allow_deletions = rule_info["allow_deletions"]["enabled"]
        branch_protection_rule.block_creations = rule_info["block_creations"]["enabled"]
        branch_protection_rule.required_conversation_resolution = rule_info["required_conversation_resolution"][
            "enabled"]
        branch_protection_rule.lock_branch = rule_info["lock_branch"]["enabled"]
        branch_protection_rule.allow_fork_syncing = rule_info["allow_fork_syncing"]["enabled"]
        branch_protection_rule.enforce_admins = rule_info["enforce_admins"]["enabled"]
        return branch_protection_rule

    def set_members(self, api_helper: ApiHelper) -> None:
        """Collect info about repository direct collaborators and from teams"""
        reposiory_teams = api_helper.get_repo_teams_list(self.name)
        for team in reposiory_teams:
            team_members = api_helper.get_team_members_list(team["slug"])
            for team_member in team_members:
                team_member["permissions"] = team["permissions"]
            self.members += self.proceed_members_info(team_members)
        repository_members = api_helper.get_repo_members_list(self.name)
        self.members += self.proceed_members_info(repository_members)

    def set_open_dependabot_alerts_number(self, api_helper: ApiHelper) -> None:
        """Set up number of open Dependabot alerts"""
        alerts_info = api_helper.get_repo_dependabot_alerts_list(self.name)
        self.dependabot_open_alerts_number = len(alerts_info)

    def set_open_secret_scan_alerts_number(self, api_helper: ApiHelper) -> None:
        """Set up number of open Dependabot alerts"""
        alerts_info = api_helper.get_repo_secret_scan_alerts_list(self.name)
        self.secret_scan_alerts_number = len(alerts_info)

    def set_branches(self, api_helper: ApiHelper) -> None:
        """Set up repository branches list"""
        branches_info = api_helper.get_repo_branches_list(self.name)
        for branch in branches_info:
            self.branches.append(branch["name"])
    def set_environments(self, api_helper: ApiHelper) -> None:
        """Collect information about repository environments"""
        env_info = api_helper.get_repo_environments(self.name)
        for env in env_info["environments"]:
            repo_env = GHEnvironment(env["name"])
            repo_env.can_admins_bypass = env["can_admins_bypass"]
            for protection_rule in env["protection_rules"]:
                if protection_rule["type"] == "required_reviewers":
                    repo_env.is_review_needed = True
                    repo_env.is_self_review_enabled = protection_rule["prevent_self_review"]
                    for reviewer in protection_rule["reviewers"]:
                        if reviewer["type"] == "User":
                            user = GHUser()
                            user.id = reviewer["reviewer"]["id"]
                            user.login = reviewer["reviewer"]["login"]
                            repo_env.reviewers.append(user)
                        if reviewer["type"] == "Team":
                            team_members = api_helper.get_team_members_list(reviewer["reviewer"]["slug"])
                            repo_env.reviewers += self.proceed_members_info(team_members)
            self.environments.append(repo_env)
        for env in self.environments:
            branches_info = api_helper.get_env_deployments_branches(self.name, env.name)
            if branches_info == {}:
                env.branches = self.branches
            else:
                for branch_policy in branches_info["branch_policies"]:
                    for branch in self.branches:
                        if fnmatch.fnmatch(branch, branch_policy["name"]):
                            env.branches.append(branch)


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
                case "branch_protection_rules":
                    j["branch_protection_rules"] = []
                    for rule in self.branch_protection_rules:
                        j["branch_protection_rules"].append(rule.to_json())
                case "environments":
                    j["environments"] = []
                    for env in self.environments:
                        j["environments"].append(env.to_json())
                case _:
                    j[f"{name}"] = value
        return json.dumps(j)
