#################### DO NOT CHANGE THIS FILE! ##############################
data "github_repository" "repo_info" {
  for_each = toset(var.repositories)
  name     = each.key
}

data "github_branch_protection_rules" "branch_protection_rules" {
  for_each = toset(var.repositories)
  repository = each.key
}

data "github_team" "team_id" {
  for_each = local.team_list_set
  slug     = each.key
}
