import requests
from constants import *


class ApiHelper:
    """Class for GitHub API interaction"""
    GITHUB_URL = "https://api.github.com"

    def __init__(self, token: str):
        self.__headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }

    def __get_list_from_api(self, url: str) -> list:
        """Executes a GET request to get list of data from GitHub API."""
        response = requests.get(url=url, headers=self.__headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError(f"API call failed with status {response.status_code} for {url}\n{response.text}")

    def __get_dict_from_api(self, url: str) -> dict:
        """Executes a GET request to get single object from GitHub API."""
        response = requests.get(url=url, headers=self.__headers)
        match response.status_code:
            case 200:
                return response.json()
            case 404:
                return {}
            case _:
                raise RuntimeError(f"API call failed with status {response.status_code} for {url}\n{response.text}")

    def get_org_repositories_list(self, org_name: str) -> list:
        """Get list of all repositories names by org_name"""
        url = f"{self.GITHUB_URL}/orgs/{org_name}/repos"
        return self.__get_list_from_api(url)

    def get_org_members_list(self) -> list:
        """Get list of all organization members by org_name"""
        url = f"{self.GITHUB_URL}/orgs/{org_name}/members"
        return self.__get_list_from_api(url)

    def get_repo_members_list(self, repo_name: str) -> list:
        """Get list of all repository members by and repo_name"""
        url = f"{self.GITHUB_URL}/repos/{org_name}/{repo_name}/collaborators?affiliation=direct"
        return self.__get_list_from_api(url)

    def get_repo_teams_list(self, repo_name: str) -> list:
        """Get list of all repository teams by org_name and repo_name"""
        url = f"{self.GITHUB_URL}/repos/{org_name}/{repo_name}/teams"
        return self.__get_list_from_api(url)

    def get_team_members_list(self, team_slug: str) -> list:
        """Get list of all team members"""
        url = f"{self.GITHUB_URL}/orgs/{org_name}/teams/{team_slug}/members"
        return self.__get_list_from_api(url)

    def get_branch_protection(self, repo_name: str, branch_name: str) -> dict:
        """Get list of all repository rulests for branch"""
        url = f"{self.GITHUB_URL}/repos/{org_name}/{repo_name}/branches/{branch_name}/protection"
        return self.__get_dict_from_api(url)

    def get_dependabot_status(self, repo_name: str) -> bool:
        """Check if Dependabot updates are enabled in repository
        https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#check-if-dependabot-security-updates-are-enabled-for-a-repository
        """
        url = f"{self.GITHUB_URL}/repos/{org_name}/{repo_name}/vulnerability-alerts"
        response = requests.get(url=url, headers=self.__headers)
        match response.status_code:
            case 204:
                return True
            case 404:
                return False
            case _:
                raise RuntimeError(f"API call failed with status {response.status_code} for {url}\n{response.text}")

    def get_repository_base_info(self, repo_name: str) -> dict:
        """Collect base information about repository"""
        url = f"{self.GITHUB_URL}/repos/{org_name}/{repo_name}"
        return self.__get_dict_from_api(url)

    def get_repo_dependabot_alerts_list(self, repo_name: str) -> list:
        """Get list of all open Dependabot alerts for repository"""
        url = f"{self.GITHUB_URL}/repos/{org_name}/{repo_name}/dependabot/alerts?state=open"
        return self.__get_list_from_api(url)

    def get_repo_secret_scan_alerts_list(self, repo_name: str) -> list:
        """Get list of all open secret scan alerts"""
        url = f"{self.GITHUB_URL}/repos/{org_name}/{repo_name}/secret-scanning/alerts?state=open"
        return self.__get_list_from_api(url)

    def search_codeowners_file(self, repo_name: str) -> bool:
        """Check whether a repository have CODEOWNERS file or not."""
        url = f"{self.GITHUB_URL}/repos/{org_name}/{repo_name}/contents/.github/CODEOWNERS"
        response = requests.get(url=url, headers=self.__headers)
        match response.status_code:
            case 404:
                return False
            case 200:
                return True
            case _:
                raise RuntimeError(f"API call failed with status {response.status_code} for {url}\n{response.text}")

    def get_repo_branch(self, repo_name: str, branch_name: str) -> dict:
        """Get repository branch info"""
        url = f"{self.GITHUB_URL}/repos/{org_name}/{repo_name}/branches/{branch_name}"
        return self.__get_dict_from_api(url)
