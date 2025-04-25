data "github_repository" "repo_info" {
  for_each = local.unique_repositories
  name     = each.key
}

data "github_branch_protection_rules" "branch_protection_rules" {
  for_each = local.unique_repositories
  repository = each.key
}

data "github_team" "team_id" {
  for_each = local.team_list_set
  slug     = each.key
}
