################################ DO NOT CHANGE! ########################################
variable "GH_APP_TOKEN" {
  type = string
}
#######################################################################################

###################### PUT YOU REPOSITORIES DATA HERE #################################
 variable "repositories" {
  type    = list(string)
  default = ["NewRepoFor", "TestRepo"] # list of repositories for set up
}


variable "team_list" {
  description = "List of github teams"
  default = [ # list of teams that will be used for repository/branch configuration
    "test_team",
    "review_dismissals"     
  ]
}

variable "app_list" {
  description = "List of github apps"
  default = [ # list of apps that will be used for repository/branch configuration
    "empty-github-app"     
  ]
}

# this block contols settings for branch protection rules for NON DEFAULT branches
variable "branch_protection" {
  description = "List of settings for branch protection"
  type = list(object({
    repo_name = string,
    branch_name = string,
    push_teams  = list(string), # GitHub teams without maintain role who can push into the branch
    push_apps   = list(string), # GitHub Apps that can push into the branch
    protection_type = string,   # high or moderate
    required_approving_review_count = number, # numer of PR reviewers
    review_dismissals = string # team that can dismiss PR review
    required_status_checks = list(string)
  }))
  default = [
    {
      repo_name = "NewRepoFor", 
      branch_name = "develop", 
      push_teams = ["test_team", "review_dismissals"],
      push_apps = [],
      review_dismissals = "review_dismissals",
      protection_type = "high", 
      required_approving_review_count = 4
      required_status_checks = ["run_check"]
    },
    {
      repo_name = "TestRepo", 
      branch_name = "develop", 
      push_teams = ["test_team", "review_dismissals"],
      push_apps = ["empty-github-app"],
      review_dismissals = "",
      protection_type = "moderate", 
      required_approving_review_count = 4
      required_status_checks = []
    },
    {
      repo_name = "TestRepo", 
      branch_name = "main", 
      push_teams = ["test_team"],
      push_apps = [],
      review_dismissals = "",
      protection_type = "high", 
      required_approving_review_count = 2
      required_status_checks = []
    }
  ]
}

# this block contols settings for branch protection rules for DEFAULT branches
variable "default_branch_protection" {
  description = "Settings for default branch protection rules"
  type = object({
    push_teams  = list(string), # GitHub teams without maintain role who can push into the branch
    push_apps   = list(string), # GitHub Apps that can push into the branch
    required_approving_review_count = number # numer of PR reviewers
  })
  default = {
    push_teams = ["test_team"], 
    push_apps = []
    required_approving_review_count = 4
  } 
}

# this block contols team permissions in repositories
variable "teams" {
  type = list(object({
    team_id    = string
    # write --> push
    # read -->  pull
    # admin --> admin
    # maintain --> maintain
    permission = string 
    repository = list(string)
  }))
  default = [
    {
      team_id    = "test_team"
      permission = "push"
      repository = ["NewRepoFor"]
    },
    {
      team_id    = "review_dismissals"
      permission = "push"
      repository = ["NewRepoFor"]
    },
  ]
}
#######################################################################################
