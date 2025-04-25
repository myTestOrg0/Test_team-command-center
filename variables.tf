variable "GH_APP_TOKEN" {
  type = string
}

variable "repositories" {
  type    = list(string)
  default = ["NewRepoFor", "TestRepo"]
}

variable "branch_protection" {
  description = "List of repositories which need a protection"
  type = list(object({
    repo_name = string,
    branch_name = string,
    push_restrictions = string,
    protection_type = string
  }))
  default = [
    {
      repo_name = "NewRepoFor", branch_name = "main", push_restrictions = "test_team", protection_type = "standart"
    },
    {
      repo_name = "NewRepoFor", branch_name = "develop", push_restrictions = "test_team", protection_type = "custom"
    },
    {
      repo_name = "TestRepo", branch_name = "main", push_restrictions = "test_team", protection_type = "standart"
    }
  ]
}

variable "collaborators" {
  type = list(object({
    username   = string
    permission = string
    repository = list(string)
  }))
  default = [
    { username = "dumnarix", permission = "admin", repository = ["NewRepoFor"]},
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
      repository = ["NewRepoFor"]
    },
  ]
}

variable "team_list" {
  description = "List of github teams"
  default = [
    "test_team",       
  ]
}
