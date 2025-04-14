variable "repositories" {
  type    = list(string)
  default = ["NewRepoFor", "TestRepo"]
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
      permission = "pull"
      repository = ["NewRepoFor", "TestRepo"]
    },
  ]
}

variable "GH_APP_TOKEN" {
  type = string
}
