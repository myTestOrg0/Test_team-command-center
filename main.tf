import {
  for_each = local.standart_branches_to_import_map

  to = github_branch_protection.standart_protection[each.key]
  id = "${each.value.repo_name}:${each.value.branch_name}"
}
import {
  for_each = local.custom_branches_to_import_map

  to = github_branch_protection.custom_protection[each.key]
  id = "${each.value.repo_name}:${each.value.branch_name}"
}

import {
  for_each = local.default_branch_protection_rules_to_import

  to = github_branch_protection.default_branch_protection[each.key]
  id = "${each.key}:${each.value}"
}

resource "github_branch_protection" "default_branch_protection" {
  depends_on = [github_repository_collaborators.repo_collaborators]
  for_each = local.default_branch_protection_rules
  repository_id = data.github_repository.repo_info[each.key].node_id
  pattern       = each.value 
  allows_deletions = false
  allows_force_pushes = false
  enforce_admins = true
  force_push_bypassers = []
  lock_branch = false
  require_conversation_resolution = true
  require_signed_commits = true
  required_linear_history  = false
  required_pull_request_reviews {
    dismiss_stale_reviews  = true
    dismissal_restrictions = var.default_branch_protection_settings.push_restrictions == "" ? [] : [data.github_team.team_id[var.default_branch_protection_settings.push_restrictions].node_id]
    pull_request_bypassers = var.default_branch_protection_settings.push_restrictions == "" ? [] : [data.github_team.team_id[var.default_branch_protection_settings.push_restrictions].node_id]
    require_code_owner_reviews = true
    require_last_push_approval = true
    required_approving_review_count = lookup(var.default_branch_protection_settings, "required_approving_review_count", 1)
    restrict_dismissals = true
  } 
  restrict_pushes {
  blocks_creations = true
  push_allowances = var.default_branch_protection_settings.push_restrictions == "" ? [] : [data.github_team.team_id[var.default_branch_protection_settings.push_restrictions].node_id]
  }
}

resource "github_branch_protection" "standart_protection" {
  depends_on = [github_repository_collaborators.repo_collaborators]
  for_each = local.standart_branch_protection_rules
  repository_id = data.github_repository.repo_info[each.value.repo_name].node_id
  pattern       = each.value.branch_name
  allows_deletions = false
  allows_force_pushes = false
  enforce_admins = true
  force_push_bypassers = []
  lock_branch = false
  require_conversation_resolution = true
  require_signed_commits = true
  required_linear_history  = false
  required_pull_request_reviews {
    dismiss_stale_reviews  = true
    dismissal_restrictions = each.value.push_restrictions == "" ? [] : [data.github_team.team_id[each.value.push_restrictions].node_id]
    pull_request_bypassers = each.value.push_restrictions == "" ? [] : [data.github_team.team_id[each.value.push_restrictions].node_id]
    require_code_owner_reviews = true
    require_last_push_approval = true
    required_approving_review_count = lookup(each.value, "required_approving_review_count", 1)
    restrict_dismissals = true
  } 
  restrict_pushes {
  blocks_creations = true
  push_allowances = each.value.push_restrictions == "" ? [] : [data.github_team.team_id[each.value.push_restrictions].node_id]
  }
}

resource "github_branch_protection" "custom_protection" {
  depends_on = [github_repository_collaborators.repo_collaborators]
  for_each = local.custom_branch_protection_rules
  repository_id = data.github_repository.repo_info[each.value.repo_name].node_id
  pattern       = each.value.branch_name
  allows_deletions = true
  allows_force_pushes = true
  
}

resource "github_repository_collaborators" "repo_collaborators" {
  for_each = local.combined_collaborators

  repository = each.key

  dynamic "user" {
    for_each = each.value.users
    content {
      username   = user.value.username
      permission = user.value.permission
    }
  }

  dynamic "team" {
    for_each = each.value.teams
    content {
      team_id    = data.github_team.team_id[team.value.team_id].id
      permission = team.value.permission
    }
  }
}
