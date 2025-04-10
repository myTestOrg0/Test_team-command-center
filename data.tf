data "github_repository" "repo_info" {
  for_each = toset(var.repositories)
  name     = each.key
}

data "github_team" "teams" {
  for_each = { for team in var.teams : team.team_id => team }
  slug     = each.key
}
