class GHEnvironment:
    """Class representing state of a GitHub environment"""
  
    def __init__(self, name: str):
        self.name = name
        self.branches = []
        self.secrets_names = []
        self.can_admins_bypass = False
        self.is_review_needed = False
        self.is_self_review_enabled = False
        self.reviewers = []

    def to_json(self) -> dict:
        """Convert class to JSON"""
        j = {}
        for name, value in vars(self).items():
            match name:
                case "reviewers":
                    j["reviewers"] = []
                    for reviewer in self.reviewers:
                        j["reviewers"].append(reviewer.to_json())
                case _:
                    j[f"{name}"] = value
        return j
