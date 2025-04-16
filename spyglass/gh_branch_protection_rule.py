class GHBranchProtectionRule:
    """Class representing state of a repository default branch protection rule"""

    def __init__(self):
        self.is_enabled = False
        self.dismiss_stale_reviews = False
        self.require_code_owner_reviews = False
        self.require_last_push_approval = False
        self.required_approving_review_count = 0
        self.required_signatures = False
        self.enforce_admins = False
        self.required_linear_history = False
        self.allow_force_pushes = False
        self.allow_deletions = False
        self.block_creations = False
        self.required_conversation_resolution = False
        self.lock_branch = False
        self.allow_fork_syncing = False
        self.required_pr = False
        self.push_restrictions = False

    def print_info(self):
        """Print default branch protection rule in console"""
        for name, value in vars(self).items():
            print(f"{name} = {value}")
        print("")

    def to_json(self) -> dict:
        """Convert class to JSON"""
        j = {}
        for name, value in vars(self).items():
            j[f"{name}"] = value
        return j


