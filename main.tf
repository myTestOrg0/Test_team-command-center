################ IMPORT BLOCKS. DO NOT CHANGE! #####################
import {
  for_each = local.standart_branches_to_import_map
  to = github_branch_protection.high_protection[each.key]
  id = "${each.value.repo_name}:${each.value.branch_name}"
}

import {
  for_each = local.custom_branches_to_import_map
  to = github_branch_protection.moderate_protection[each.key]
  id = "${each.value.repo_name}:${each.value.branch_name}"
}

import {
  for_each = local.default_branch_protection_rules_to_import
  to = github_branch_protection.default_branch_protection[each.key]
  id = "${each.key}:${each.value}"
}
####################################################################

#################### BRANCH PROTECTION FOR DEFAULT BRANCH ##########
resource "github_branch_protection" "default_branch_protection" {

############################ DO NOT CHANGE! ########################
  depends_on = [github_repository_collaborators.repo_collaborators]  
  for_each = local.default_branch_protection_rules                   
  repository_id = data.github_repository.repo_info[each.key].node_id 
  pattern       = each.value                                         
####################################################################

  # allow users with write permission to delete branch
  allows_deletions = false 

  # allow force pushes to the branch
  allows_force_pushes = false 

  # do not allow repository admins to bypass this rule
  enforce_admins = true 

  # list of collaborators who can bypass force push restriction
  force_push_bypassers = [] 

  # make branch read only
  lock_branch = false 

  # all conversations on code must be resolved before a pull request can be merged
  require_conversation_resolution = true 

  # commits pushed to matching branches must have verified signatures
  require_signed_commits = true  

  # prevent merge commits from being pushed
  required_linear_history  = false 

  required_pull_request_reviews {

    # new reviewable commits pushed to a matching branch will dismiss pull request review approvals
    dismiss_stale_reviews  = true 

    # teams/users/apps allowed to dismiss pull request reviews 
    dismissal_restrictions = [] 

    # teams/users/apps who are allowed to bypass required pull requests
    pull_request_bypassers = []

    # require an approved review in pull requests including files with a designated code owner
    require_code_owner_reviews = true 

    # whether the most recent reviewable push must be approved by someone other than the person who pushed it
    require_last_push_approval = true 

    # number of approvals needed DO NOT CHANGE!
    required_approving_review_count = lookup(var.default_branch_protection, "required_approving_review_count", 1)
    restrict_dismissals = false 
  } 

  restrict_pushes {

    # only people, teams, or apps allowed to push will be able to create new branches matching this rule
    blocks_creations = true 

    ############################ DO NOT CHANGE! ########################
    push_allowances = concat(
      [for team in var.default_branch_protection.push_teams : data.github_team.team_id[team].node_id],
      [for app in var.default_branch_protection.push_apps   : data.github_app.app_id[app].node_id]
    )
  }

required_status_checks {
    contexts = lookup(var.default_branch_protection, "required_status_checks", [])
    strict = true # ensures pull requests targeting a matching branch have been tested with the latest code
  }
}
#####################################################################

#################### HIGH LEVEL BRANCH PROTECTION RULE ##############
resource "github_branch_protection" "high_protection" {

  ############################ DO NOT CHANGE! ########################
  depends_on = [github_repository_collaborators.repo_collaborators] 
  for_each = local.standart_branch_protection_rules                 
  repository_id = data.github_repository.repo_info[each.value.repo_name].node_id 
  pattern       = each.value.branch_name 
  #####################################################################

  # allow users with write permission to delete branch
  allows_deletions = false 

  # allow force pushes to the branch
  allows_force_pushes = false 

  # do not allow repository admins to bypass this rule
  enforce_admins = true 

  # list of collaborators who can bypass force push restriction
  force_push_bypassers = [] 

  # make branch read only
  lock_branch = false 

  # all conversations on code must be resolved before a pull request can be merged
  require_conversation_resolution = true 

  # commits pushed to matching branches must have verified signatures
  require_signed_commits = true 

  # prevent merge commits from being pushed
  required_linear_history  = false


  required_pull_request_reviews {

    # new reviewable commits pushed to a matching branch will dismiss pull request review approvals
    dismiss_stale_reviews  = true 

    # teams/users/apps who are allowed to bypass required pull requests
    pull_request_bypassers = [] 

    # require an approved review in pull requests including files with a designated code owner
    require_code_owner_reviews = true 

    # whether the most recent reviewable push must be approved by someone other than the person who pushed it
    require_last_push_approval = true 

    ############################ DO NOT CHANGE! ########################
    required_approving_review_count = lookup(each.value, "required_approving_review_count", 1)
    restrict_dismissals = false 
    dismissal_restrictions = []
  } 

  restrict_pushes {
    # only people, teams, or apps allowed to push will be able to create new branches matching this rule
    # teams that can push to these branch. 
    blocks_creations = true 
    push_allowances = concat(
      [for team in each.value.push_teams : data.github_team.team_id[team].node_id],
      [for app in each.value.push_apps  : data.github_app.app_id[app].node_id]
    )
  }

  required_status_checks {
    contexts = each.value.required_status_checks 
    strict = true # ensures pull requests targeting a matching branch have been tested with the latest code
  }
}
#####################################################################

#################### MODERATE LEVEL BRANCH PROTECTION RULE ##########
resource "github_branch_protection" "moderate_protection" {

  ############################ DO NOT CHANGE! ########################
  depends_on = [github_repository_collaborators.repo_collaborators] 
  for_each = local.custom_branch_protection_rules                 
  repository_id = data.github_repository.repo_info[each.value.repo_name].node_id 
  pattern       = each.value.branch_name 
  #####################################################################

  # allow users with write permission to delete branch
  allows_deletions = false 

  # allow force pushes to the branch
  allows_force_pushes = false 

  # do not allow repository admins to bypass this rule
  enforce_admins = true 

  # list of collaborators who can bypass force push restriction
  force_push_bypassers = [] 

  # make branch read only
  lock_branch = false 

  # all conversations on code must be resolved before a pull request can be merged
  require_conversation_resolution = true

  # commits pushed to matching branches must have verified signatures
  require_signed_commits = true

  # prevent merge commits from being pushed
  required_linear_history  = false 


  required_pull_request_reviews {

    # new reviewable commits pushed to a matching branch will dismiss pull request review approvals
    dismiss_stale_reviews  = true 

    # teams/users/apps who are allowed to bypass required pull requests
    pull_request_bypassers = [] 

    # require an approved review in pull requests including files with a designated code owner
    require_code_owner_reviews = true 

    # whether the most recent reviewable push must be approved by someone other than the person who pushed it
    require_last_push_approval = true 

############################ DO NOT CHANGE! ########################
    # number of approvals needed 
    required_approving_review_count = lookup(each.value, "required_approving_review_count", 1)
    restrict_dismissals = true 

    # teams/users/apps allowed to dismiss pull request reviews 
    dismissal_restrictions = each.value.review_dismissals == "" ? [] : [data.github_team.team_id[each.value.review_dismissals].node_id]
  } 

  restrict_pushes {

    # only people, teams, or apps allowed to push will be able to create new branches matching this rule
    # teams that can push to these branch. 
    blocks_creations = true 
    
    push_allowances = concat(
      [for team in each.value.push_teams : data.github_team.team_id[team].node_id],
      [for app in each.value.push_apps  : data.github_app.app_id[app].node_id]
    )
  }

required_status_checks {
    contexts = each.value.required_status_checks 
    strict = true # ensures pull requests targeting a matching branch have been tested with the latest code
  }
}
#####################################################################

################## COLLABORATORS SETTINGS. DO NOT CHANGE! #############
resource "github_repository_collaborators" "repo_collaborators" {
  for_each = local.combined_collaborators
  repository = each.key
  dynamic "team" {
    for_each = each.value.teams
    content {
      team_id    = data.github_team.team_id[team.value.team_name].id
      permission = team.value.permission
    }
  }
}
######################################################################
