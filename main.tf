import {
  for_each = var.repositories
  to = github_repository.repo[each.key]
  id = each.value
}

import {
  for_each = var.repositories
  to = github_branch_protection.main_protection[each.key]
  id = "${each.value}:${data.github_repository.repo_info[each.value].default_branch}"
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
    count = length(var.repositories)
    repository_id = var.repositories[count.index]
    allows_deletions                = false
    allows_force_pushes             = false
    enforce_admins                  = true
    force_push_bypassers            = []
    lock_branch                     = false
    pattern                         = data.github_repository.repo_info[var.repositories[count.index]].default_branch
    require_conversation_resolution = true
    require_signed_commits          = true
    required_linear_history         = false

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


resource "github_repository_collaborator" "a_repo_collaborator" {
  for_each = toset(flatten([for repo in var.repositories : [for collab in var.collaborators : "${repo}:${collab}"]]))
  repository = split(":", each.key)[0]
  username   = split(":", each.key)[1]
  permission = "push"
}

resource "github_team_repository" "some_team_repo" {
  for_each = toset(flatten([for repo in var.repositories : [for collab in var.teams : "${repo}:${collab}"]]))  
  repository = split(":", each.key)[0]
  team_id   = split(":", each.key)[1]
  permission = "push"
}

