variable "repositories" {
  type    = list(string)
  default = ["NewRepoFor", "TestRepo"]
}

variable "collaborators" {
  type = list(object({
    username   = string
    permission = string
  }))
  default = [
    { username = "dumnarix", permission = "admin" },
  ]
}

variable "teams" {
  type = list(object({
    team_id    = string
    permission = string
  }))
  default = [
    { team_id = "test_team", permission = "pull" },
  ]
}

