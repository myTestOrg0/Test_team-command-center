import {
  for_each = var.repositories
  to = github_repository.repo[each.key]
  id = each.value
}

locals {
  default_branch_protections = [
    for repo in var.repositories : {
      repo_name    = repo
      default_branch = data.github_repository.repo_info[repo].default_branch
      repo_id      = data.github_branch_protection_rules.branch_protection_rules[repo].id
      node_id      = data.github_repository.repo_info[repo].node_id
      has_existing_protection = contains(
        [for rule in data.github_branch_protection_rules.branch_protection_rules[repo].rules : rule.pattern],
        data.github_repository.repo_info[repo].default_branch
      )
    }
  ]
  default_branch_protection_map = {
    for item in local.default_branch_protections :
    "${item.repo_name}-${item.default_branch}" => item
  }
}


import {
  for_each = {
    for key, value in local.default_branch_protection_map :
    key => value if value.has_existing_protection
  }
  to = github_branch_protection.main_protection[each.key]
  id = "${each.value.repo_id}:${each.value.default_branch}"
}

resource "github_repository" "repo" {
  count = length(var.repositories)
  name        = var.repositories[count.index]
  vulnerability_alerts = true
  security_and_analysis {
        secret_scanning {
            status = "enabled"
        }
        secret_scanning_push_protection {
            status = "enabled"
        }
    }
  lifecycle {
    ignore_changes = [
      allow_auto_merge,
      allow_merge_commit,
      allow_rebase_merge,
      allow_squash_merge,
      allow_update_branch,
      archive_on_destroy,
      archived,
      auto_init,
      delete_branch_on_merge,
      description,
      gitignore_template,
      has_discussions,
      has_downloads,
      has_issues,
      has_projects,
      has_wiki,
      homepage_url,
      id,
      default_branch,
      ignore_vulnerability_alerts_during_read,
      is_template,
      license_template,
      merge_commit_message,
      merge_commit_title,
      name,
      pages,
      private,
      squash_merge_commit_message,
      squash_merge_commit_title,
      template,
      topics,
      visibility,
      web_commit_signoff_required,
      private
    ]
  }
}


resource "github_branch_protection" "main_protection" {
    for_each = local.default_branch_protection_map
    repository_id = each.value.node_id
    allows_deletions                = false
    allows_force_pushes             = false
    enforce_admins                  = true
    force_push_bypassers            = []
    lock_branch                     = false
    pattern       = each.value.default_branch
    require_conversation_resolution = true
    require_signed_commits          = true

    required_pull_request_reviews {
        dismiss_stale_reviews           = true
        dismissal_restrictions          = []
        pull_request_bypassers          = []
        require_code_owner_reviews      = true
        require_last_push_approval      = false
        required_approving_review_count = 1
        restrict_dismissals             = false
    }

    restrict_pushes {
        blocks_creations = true
        push_allowances  = []
    }
}

resource "github_repository_collaborators" "repo_collaborators" {
  for_each = toset(var.repositories)
  repository = each.value

  dynamic "user" {
    for_each = var.collaborators
    content {
      username   = user.value.username
      permission = user.value.permission
    }
  }

  dynamic "team" {
    for_each = var.teams
    content {
      team_id    = data.github_team.teams[team.value.team_id].id
      permission = team.value.permission
    }
  }
}
