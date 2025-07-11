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
  for_each = local.default_team_list_set
  slug     = each.key
}

data "github_app" "app_id" {
  for_each = merge(local.app_list_set, local.default_app_list_set)
  slug     = each.key
}
