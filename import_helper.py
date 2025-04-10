import re
import requests
import os
import json

GITHUB_URL = "https://api.github.com"
token = os.environ.get('TOKEN')
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28"
}
owner_name = "myTestOrg0"


def get_repositories() -> list:
    """Parse file variables.tf and get repository list from it"""
    with open("variables.tf", "r") as f:
        file_contents = f.read()
        pattern = r'variable "repositories" {\s+type\s+=\s+list\(string\)\s+default\s+=\s+\[(.*?)\]\s*}'
        matches = re.findall(pattern, file_contents, re.DOTALL)
        if len(matches) >= 1:
            return [value.strip().strip('"') for value in matches[0].split(',')]
        else:
            return []


def get_repository_default_branch(repo_name: str) -> str:
    """Get default branch name by repository name"""
    url = f"{GITHUB_URL}/repos/{owner_name}/{repo_name}"
    response = requests.get(url=url, headers=headers)
    match response.status_code:
        case 200:
            return response.json()["default_branch"]
        case _:
            print(f"Failed to execute a request to {url}. Code: {response.status_code} "
                  f"Error: {response.text}")
            exit(1)


def is_default_branch_protected(repo: str, default_branch: str) -> bool:
    """Check whether repository's default branch is protected or not"""
    url = f"{GITHUB_URL}/repos/{owner_name}/{repo}/branches/{default_branch}/protection"
    response = requests.get(url=url, headers=headers)
    match response.status_code:
        case 200:
            return True
        case 404:
            return False
        case _:
            print(f"Failed to execute a request to {url}. Code: {response.status_code} "
                  f"Error: {response.text}")
            exit(1)


def create_import_commands(protected_branches: list) -> list:
    """Create commands to for branch protection rules import to Terraform"""
    commands = []
    for i in range(len(protected_branches)):
        commands.append(
            f'terraform import "github_branch_protection.main_protection[{i}]" "{protected_branches[i][0]}:{protected_branches[i][1]}"')
    return commands


def get_protected_branches_from_terraform_state() -> list:
    """Parse terraform.tfstate file and get list of protected branches in format
    (repo_name, protected_branch)"""
    terraformed_protected_branches = []
    with open("terraform.tfstate", "r") as f:
        data = json.load(f)
        resources = data["resources"]
        for res in resources:
            if res["type"] == "github_branch_protection":
                for inst in res["instances"]:
                    repo_name = inst["attributes"]["repository_id"]
                    protected_branch_name = inst["attributes"]["pattern"]
                    terraformed_protected_branches.append((repo_name, protected_branch_name))
    return terraformed_protected_branches


if __name__ == '__main__':
    repos = get_repositories()
    protected_branches = []
    commands = []
    for repo in repos:
        default_branch = get_repository_default_branch(repo)
        if is_default_branch_protected(repo, default_branch):
            protected_branches.append((repo, default_branch))
    if os.path.exists("terraform.tfstate"):
        traced_protected_branches = get_protected_branches_from_terraform_state()
        branches_to_import = []
        for branch in protected_branches:
            if branch not in protected_branches:
                branches_to_import.append(branch)
        commands = create_import_commands(branches_to_import)
    else:
        commands = create_import_commands(protected_branches)
    for command in commands:
        os.system(command)
