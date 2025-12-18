# Branch Protection Configuration

This document describes the recommended branch protection settings for this repository.

## Main Branch Protection Rules

Navigate to **Settings → Branches → Add branch protection rule** and configure:

### Branch name pattern
```
main
```

### Protect matching branches

#### Required Reviews
- [x] **Require a pull request before merging**
  - [x] Require approvals: `1` (or more for larger teams)
  - [x] Dismiss stale pull request approvals when new commits are pushed
  - [x] Require review from Code Owners
  - [x] Require approval of the most recent reviewable push

#### Required Status Checks
- [x] **Require status checks to pass before merging**
  - [x] Require branches to be up to date before merging
  - Required checks:
    - `test` (from CI workflow)
    - `lint_and_test` (from Quality workflow)
    - `docker_build_and_scan` (from Quality workflow)
    - `pr_title` (conventional commits)

#### Additional Settings
- [x] **Require conversation resolution before merging**
- [x] **Require signed commits** (optional, but recommended)
- [x] **Require linear history** (optional, enforces squash/rebase)
- [x] **Do not allow bypassing the above settings**

#### Restrictions
- [ ] Restrict who can push to matching branches
  - Add specific teams/users if needed

## Ruleset Configuration (Alternative)

For more granular control, use **Repository Rulesets**:

### Settings → Rules → Rulesets → New ruleset

```yaml
name: Main Branch Protection
enforcement: active
target: branch
conditions:
  ref_name:
    include:
      - refs/heads/main

rules:
  - type: pull_request
    parameters:
      required_approving_review_count: 1
      dismiss_stale_reviews_on_push: true
      require_code_owner_review: true
      require_last_push_approval: true

  - type: required_status_checks
    parameters:
      strict_required_status_checks_policy: true
      required_status_checks:
        - context: test
        - context: lint_and_test
        - context: docker_build_and_scan

  - type: non_fast_forward
    # Prevents force pushes

  - type: required_linear_history
    # Enforces squash or rebase merging
```

## Environment Protection Rules

### Staging Environment
- **Settings → Environments → staging**
- No required reviewers (auto-deploy on main push)
- Wait timer: 0 minutes

### Production Environment
- **Settings → Environments → production**
- [x] Required reviewers: Add 1-2 team members
- [x] Wait timer: 5 minutes (allows cancellation)
- [x] Limit to protected branches only

## Secret Scanning

- **Settings → Code security and analysis**
- [x] Dependency graph: Enabled
- [x] Dependabot alerts: Enabled
- [x] Dependabot security updates: Enabled
- [x] Secret scanning: Enabled
- [x] Push protection: Enabled

## CODEOWNERS Enforcement

The `.github/CODEOWNERS` file automatically requests reviews from code owners.
Ensure "Require review from Code Owners" is enabled in branch protection.

## Merge Settings

- **Settings → General → Pull Requests**
- [x] Allow squash merging (recommended default)
- [x] Default to PR title for squash merge commits
- [ ] Allow merge commits (optional)
- [ ] Allow rebase merging (optional)
- [x] Automatically delete head branches

## Tag Protection

To protect release tags:

- **Settings → Tags → New rule**
- Pattern: `v*`
- Restrict to: Repository administrators only
