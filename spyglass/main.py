import gh_token_helper
from api_helper import ApiHelper
from gh_token_helper import *
from gh_repository import GHRepository
from compliance_checker import ComplianceChecker
from compl_status import ComplianceStatus
from prettytable import PrettyTable
from datetime import datetime, timezone
if __name__ == '__main__':
    utc_dt = datetime.now(timezone.utc)
    token = gh_token_helper.get_access_token()
    api_helper = ApiHelper(token)
    compliance_checker = ComplianceChecker()
    table = PrettyTable()
    table.field_names = ["Repository", "Compliance status", "To fix", "Comments"]
    for repo_name in repositories:
        repository = GHRepository(repo_name)
        repository.initialize(api_helper)
        status = compliance_checker.check_repo_compl(repository)
        table.add_row([status.repository_name, status.status, "\n".join(status.problems_2_fix), "\n".join(status.comments)])
        table.add_row(["-" * 5, "-" * 5, "-" * 15, "-" * 15])
    print(f"Date: {utc_dt.strftime("%d-%m-%Y")} Time UTC: {utc_dt.strftime("%H:%M")}")
    print(table)
