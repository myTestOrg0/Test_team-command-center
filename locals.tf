#################### DO NOT CHANGE THIS FILE! ##############################
locals {

  branch_protection_rules = {
    for item in var.branch_protection :
    "${item.repo_name}:${item.branch_name}" => item
  }

  protected_branches = flatten([
    for repo_key, repo_val in data.github_branch_protection_rules.branch_protection_rules : [
      for rule in repo_val.rules : {
        repo_name   = repo_val.repository
        branch_name = rule.pattern
      }
    ]
  ])

  default_branch_protection_rules = {
    for repo_name in var.repositories :
    repo_name => data.github_repository.repo_info[repo_name].default_branch
  }

  default_branch_protection_rules_to_import = {
  for repo_name in var.repositories : 
  repo_name => data.github_repository.repo_info[repo_name].default_branch
  if contains(
    [for rule in data.github_branch_protection_rules.branch_protection_rules[repo_name].rules : rule.pattern],
    data.github_repository.repo_info[repo_name].default_branch
  )
}

  branches_to_import = [
    for item in var.branch_protection : item
    if contains([
      for protected in local.protected_branches : "${protected.repo_name}:${protected.branch_name}"
    ], "${item.repo_name}:${item.branch_name}")
  ]

  branches_to_import_map = {
    for item in local.branches_to_import :
    "${item.repo_name}:${item.branch_name}" => item
  }

  team_list_set = toset(var.team_list)

 standart_branch_protection_rules = {
    for item in var.branch_protection :
    "${item.repo_name}:${item.branch_name}" => item
    if item.protection_type == "high"
  }

  custom_branch_protection_rules = {
    for item in var.branch_protection :
    "${item.repo_name}:${item.branch_name}" => item
    if item.protection_type == "moderate"
  }

  standart_branches_to_import_map = {
    for item in var.branch_protection :
    "${item.repo_name}:${item.branch_name}" => item
    if item.protection_type == "high" &&
      contains([
        for protected in local.protected_branches : "${protected.repo_name}:${protected.branch_name}"
      ], "${item.repo_name}:${item.branch_name}")
  }

  custom_branches_to_import_map = {
    for item in var.branch_protection :
    "${item.repo_name}:${item.branch_name}" => item
    if item.protection_type == "moderate" &&
      contains([
        for protected in local.protected_branches : "${protected.repo_name}:${protected.branch_name}"
      ], "${item.repo_name}:${item.branch_name}")
  }

repositories_from_collaborators_and_teams = toset(concat(
    flatten([for t in var.teams : t.repository])
  ))

  teams_by_repo = {
    for repo in local.repositories_from_collaborators_and_teams :
    repo => [
      for team in var.teams : {
        team_id    = team.team_id
        permission = team.permission
      }
      if contains(team.repository, repo)
    ]
  }

  combined_collaborators = {
    for repo in local.repositories_from_collaborators_and_teams : repo => {
      teams = lookup(local.teams_by_repo, repo, [])
    }
  }

}
