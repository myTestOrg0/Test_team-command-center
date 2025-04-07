import {
  for_each = var.repositories
  to = github_repository.repo[each.key]
  id = each.value
}


resource "github_branch_protection" "main_protection" {
    for_each = toset(var.repositories)
    repository_id = each.key
    allows_deletions                = false
    allows_force_pushes             = false
    enforce_admins                  = true
    force_push_bypassers            = []
    lock_branch                     = false
    pattern                         = data.github_repository.repo_info[each.key].default_branch
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
  for_each = zipmap(var.repositories, var.collaborators)
  username = each.value
  permission = "push"
  repository = each.key
}

resource "github_team_repository" "some_team_repo" {
  for_each = zipmap(var.repositories, var.teams)
  team_id    = each.value
  repository = each.key
  permission = "push"
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
