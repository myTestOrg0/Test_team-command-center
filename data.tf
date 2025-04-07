data "github_repository" "repo_info" {
  for_each = toset(var.repositories)
  name     = each.key
}
