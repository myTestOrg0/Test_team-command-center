variable "repositories" {
  type    = list(string)
  default = ["NewRepoFor", "TestRepo"]
}

variable "collaborators" {
  type    = list(string)
  default = ["dumnarix"]
}

variable "teams" {
  type    = list(string)
  default = ["Test_team"]
}

variable "token" {
  type = string
}
