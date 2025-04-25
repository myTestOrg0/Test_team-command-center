variable "repositories" {
  type    = list(string)
  default = ["NewRepoFor"]
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
      permission = "pull"
      repository = ["NewRepoFor"]
    },
  ]
}

variable "standart_branch_protection" {
  description = "List of repositories which need a protection"
  default = {
    "NewRepoFor" : {
      "repo" : "NewRepoFor",
      "branch" : "main",
      "push_restrictions" : "test_team"
    }
  }
}
