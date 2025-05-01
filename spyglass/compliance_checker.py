from gh_branch_protection_rule import GHBranchProtectionRule
from compl_status import ComplianceStatus
from gh_repository import GHRepository
import json


class ComplianceChecker:
    """Class performing policy compliance checks"""

    def __init__(self):
        self.compl_status = ComplianceStatus()
        with open("check_configuration.json", "r") as f:
            self.check_configuration = json.load(f)

    def check_repo_compl(self, repo: GHRepository) -> ComplianceStatus:
        """Check repository for policy compliance"""
        self.compl_status.repository_name = repo.name
        self.compl_status.status = ""
        self.compl_status.problems_2_fix = []
        self.compl_status.comments = []
        if repo.is_archived:
            self.compl_status.status = "Policy inapplicable."
            self.compl_status.problems_2_fix.append("- Repository is archived. Policy inapplicable.")
            return self.compl_status
        self.check_repo_members(repo.members)
        self.check_repo(repo)
        for branch_protection_rule in repo.branch_protection_rules:
            self.check_branch_protection(branch_protection_rule)
        if len(self.compl_status.problems_2_fix) == 0:
            self.compl_status.status = "COMPLIANT"
        else:
            self.compl_status.status = "NON COMPLIANT"
        return self.compl_status

    def check_repo_members(self, members: list) -> None:
        """Check whether repository members are in compliance with security policy"""
        admins = []
        writers = []
        for member in members:
            if member.permissions["admin"]:
                admins.append(member)
            if member.permissions["push"]:
                writers.append(member)
        if len(admins) > 1:
            current_admins = []
            for admin in admins:
                current_admins.append(admin.login)
            self.compl_status.problems_2_fix.append(f"More than 1 admins. Current admins are: {current_admins}.")
        if len(members) == 0:
            self.compl_status.comments.append(f"No direct collaborators.")
        self.compl_status.comments.append(f"Users with write permission: {len(writers)}.")

    def check_repo(self, repo: GHRepository) -> None:
        """Check repository properties for policy compliance"""
        for name, value in vars(repo).items():
            if name in self.check_configuration["repository"].keys():
                if value != self.check_configuration["repository"][name]["st_value"]:
                    self.compl_status.problems_2_fix.append(self.check_configuration["repository"][name]["error_msg"])
    def check_branch_protection(self, protection_rule: GHBranchProtectionRule) -> None:
        """Check repository default branch protection for policy compliance"""
        branch_name = protection_rule.branch_name
        for name, value in vars(protection_rule).items():
            if name in self.check_configuration["protection_rule"].keys():
                error_msg = self.check_configuration["protection_rule"][name]["error_msg"]
                st_value = self.check_configuration["protection_rule"][name]["st_value"]
                match name:
                    case "is_enabled":
                        if value != st_value:
                            self.compl_status.problems_2_fix.append(f"[BRANCH {branch_name}] {error_msg}")
                            return
                    case "required_approving_review_count":
                        if value < st_value:
                            self.compl_status.problems_2_fix.append(f"[BRANCH {branch_name}] {error_msg}")
                    case "bypass_pull_request_allowances":
                        if value != st_value:
                            for user in protection_rule.bypass_pull_request_allowances["users"]:
                                self.compl_status.problems_2_fix.append(f"[BRANCH {branch_name}] User {user["login"]} {error_msg}")
                            for team in protection_rule.bypass_pull_request_allowances["teams"]:
                                self.compl_status.problems_2_fix.append(f"[BRANCH {branch_name}] Team {team["name"]} {error_msg}")
                            for app in protection_rule.bypass_pull_request_allowances["apps"]:
                                self.compl_status.problems_2_fix.append(f"[BRANCH {branch_name}] GitHub app {app["name"]} {error_msg}")
                    case _:
                        if value != st_value:
                            self.compl_status.problems_2_fix.append(f"[BRANCH {branch_name}] {error_msg}")
