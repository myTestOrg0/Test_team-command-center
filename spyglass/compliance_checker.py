from gh_branch_protection_rule import GHBranchProtectionRule
from compl_status import ComplianceStatus
from gh_repository import GHRepository
from gh_user import GHUser


class ComplianceChecker:
    """Class performing policy compliance checks"""

    def __init__(self):
        self.compl_status = ComplianceStatus()

    standard_repository = {
        "is_secrets_scanning_enable": (True, "Secrets scanning is turned off."),
        "is_secret_scanning_push_protection_enabled": (True, "Secrets scanning push protection is turned off."),
        "is_dependabot_enabled": (True, "Dependabot scanning is turned off."),
        "dependabot_open_alerts_number": (0, "Open Dependabot alerts found."),
        "secret_scan_alerts_number": (0, "Open secrets scanning found."),
        "have_codeowners_file": (True, "No CODEOWNERS file"),
    }

    standard_protection_rule = {
        "is_enabled": (True, "Branch is unprotected."),
        "dismiss_stale_reviews": (True, "Stale pull request approval is turned off."),
        "require_code_owner_reviews": (True, "CODEOWNERS pull request review is turned off."),
        "require_last_push_approval": (True, "Approval of the most recent reviewable push is turned off."),
        "required_approving_review_count": (1, "Pull request approval is turned off."),
        "required_signatures": (True, "Commit signatures are not required."),
        "enforce_admins": (True, "Admins can bypass branch protection."),
        "allow_force_pushes": (False, "Force pushes are turned on."),
        "allow_deletions": (False, "Users with push access can delete branch."),
        "required_conversation_resolution": (
        True, "Conversation resolution is not required for merge into default branch."),
        "required_pr": (True, "Pull request does not required before merging."),
        "push_restrictions": (True, "No push restrictions."),
        "bypass_pull_request_allowances": ({}, "can bypass branch protection rule.")
    }

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
            if name in self.standard_repository.keys():
                match name:
                    case "is_secrets_scanning_enable":
                        if repo.visibility != "public":
                            continue
                        else:
                            if value != self.standard_repository[name][0]:
                                self.compl_status.problems_2_fix.append(self.standard_repository[name][1])
                    case _:
                        if value != self.standard_repository[name][0]:
                            self.compl_status.problems_2_fix.append(self.standard_repository[name][1])

    def check_branch_protection(self, branch_protection_rule: GHBranchProtectionRule) -> None:
        """Check repository default branch protection for policy compliance"""
        for name, value in vars(branch_protection_rule).items():
            if name in self.standard_protection_rule.keys():
                match name:
                    case "is_enabled":
                        if value != self.standard_protection_rule[name][0]:
                            self.compl_status.problems_2_fix.append(
                                f"[BRANCH {branch_protection_rule.branch_name}] {self.standard_protection_rule[name][1]}")
                            return
                    case "required_approving_review_count":
                        if value < self.standard_protection_rule[name][0]:
                            self.compl_status.problems_2_fix.append(
                                f"[BRANCH {branch_protection_rule.branch_name}] {self.standard_protection_rule[name][1]}")
                    case "bypass_pull_request_allowances":
                        if value != self.standard_protection_rule[name][0]:
                            for user in branch_protection_rule.bypass_pull_request_allowances["users"]:
                                self.compl_status.problems_2_fix.append(
                                    f"[BRANCH {branch_protection_rule.branch_name}] User {user["login"]} {self.standard_protection_rule[name][1]}")
                            for team in branch_protection_rule.bypass_pull_request_allowances["teams"]:
                                self.compl_status.problems_2_fix.append(
                                    f"[BRANCH {branch_protection_rule.branch_name}] Team {team["name"]} {self.standard_protection_rule[name][1]}")
                            for app in branch_protection_rule.bypass_pull_request_allowances["apps"]:
                                self.compl_status.problems_2_fix.append(
                                    f"[BRANCH {branch_protection_rule.branch_name}] GitHub app {app["name"]} {self.standard_protection_rule[name][1]}")
                    case _:
                        if value != self.standard_protection_rule[name][0]:
                            self.compl_status.problems_2_fix.append(
                                f"[BRANCH {branch_protection_rule.branch_name}] {self.standard_protection_rule[name][1]}")
