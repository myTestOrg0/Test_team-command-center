variable "repositories" {
  type    = list(string)
  default = ["NewRepoFor"]
}

variable "collaborators" {
  type    = list(string)
  default = ["dumnarix"]
}

variable "teams" {
  type    = list(string)
  default = ["Test_team"]
}

variable "GITHUB_TOKEN" {
  type = string
}
