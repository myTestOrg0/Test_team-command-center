variable "GH_APP_TOKEN" {
  type = string
}

variable "repositories" {
  type    = list(string)
  default = ["NewRepoFor", "TestRepo"]
}

variable "team_list" {
  description = "List of github teams"
  default = [
    "test_team",       
  ]
}

variable "branch_protection" {
  description = "List of settings for branch protection"
  type = list(object({
    repo_name = string,
    branch_name = string,
    push_restrictions = string,
    protection_type = string,
    required_approving_review_count = number
  }))
  default = [
    {
      repo_name = "NewRepoFor", branch_name = "main", push_restrictions = "test_team", protection_type = "standart", "required_approving_review_count" = 4
    },
    {
      repo_name = "NewRepoFor", branch_name = "develop", push_restrictions = "test_team", protection_type = "custom", "required_approving_review_count" = 4
    },
    {
      repo_name = "TestRepo", branch_name = "main", push_restrictions = "test_team", protection_type = "standart", "required_approving_review_count" = 4
    }
  ]
}

variable "default_branch_protection_settings" {
  description = "Settings for default branch protection rules"
  type = object({
    push_restrictions = string,
    required_approving_review_count = number
  })
  default = {
    push_restrictions = "test_team", "required_approving_review_count" = 4
  } 
}

variable "collaborators" {
  type = list(object({
    username   = string
    permission = string
    repository = list(string)
  }))
  default = [
    { username = "dumnarix", permission = "admin", repository = ["NewRepoFor", "TestRepo"]},
  ]
}

variable "teams" {
  type = list(object({
    team_id    = string
    permission = string
    repository = list(string)
  }))
  default = [
    {
      team_id    = "test_team"
      permission = "push"
      repository = ["NewRepoFor", "TestRepo"]
    },
  ]
}
