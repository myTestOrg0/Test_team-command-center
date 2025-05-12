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

# this block contols settings for branch protection rules for NON DEFAULT branches
variable "branch_protection" {
  description = "List of settings for branch protection"
  type = list(object({
    repo_name = string,
    branch_name = string,
    push_restrictions = string, # who can push to the branch without maintain permission
    protection_type = string,   # high or moderate
    required_approving_review_count = number, # numer of PR reviewers
    review_dismissals = string # team that can dismiss PR review
  }))
  default = [
    {
      repo_name = "NewRepoFor", 
      branch_name = "develop", 
      push_restrictions = "test_team",
      review_dismissals = "review_dismissals",
      protection_type = "high", 
      "required_approving_review_count" = 4
    },
    {
      repo_name = "NewRepoFor", 
      branch_name = "a", 
      push_restrictions = "test_team",
      review_dismissals = "review_dismissals",
      protection_type = "moderate", 
      "required_approving_review_count" = 4
    }
  ]
}

# this block contols settings for branch protection rules for DEFAULT branches
variable "default_branch_protection_settings" {
  description = "Settings for default branch protection rules"
  type = object({
    push_restrictions = string, # who can push to the branch without maintain permission
    required_approving_review_count = number # numer of PR reviewers
  })
  default = {
    push_restrictions = "test_team", 
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
