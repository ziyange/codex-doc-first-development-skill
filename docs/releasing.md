# Release Maintenance

This repository distributes skill directories, not npm or pip packages. Pending
`.changeset/*.md` files drive releases through `.github/scripts/release_version.py`.
No package.json or npm publishing is required.

## Prepare a Version

Preview without writing:

```bash
python .github/scripts/release_version.py --json
```

In an isolated release branch, add `--apply` to update `pyproject.toml`, the main
skill title, README version labels, and CHANGELOG. The greatest pending bump wins;
minor plus patch at 2.3.0 produces 2.4.0. Processed changesets are removed only after
all source inputs have been validated and version files written. Invalid changesets
or metadata drift return Exit 2 before writes. No pending changes is an idempotent
no-op. Historical changelog entries and unrelated files remain intact.

## Automation and Permissions

The Release workflow uses the Python planner, tests the generated changes, and
opens or updates `changeset-release/<base>` as a **Version Skills** PR. It never
approves or merges the PR. Keep the repository's default workflow permission read-only;
the version job alone requests contents, pull-requests, and actions write access.
Enable the GitHub repository setting allowing Actions to create pull requests.
GitHub combines this with the ability to approve PRs; this workflow does not use
approval functionality. No personal token is installed in workflow secrets.

Bot-created PRs using GITHUB_TOKEN do not automatically trigger normal PR CI,
so Release explicitly dispatches CI on the generated version branch. That branch
runs the existing three-OS, Python 3.9/3.12 matrix plus lint and docs checks. Workflow
dispatch is available for intentional reruns; do not rerun historical failing code
and expect it to include later fixes.

After review and an explicit merge, changesets are consumed on the base branch.
Publishing remains separate: an explicitly pushed `v*` tag invokes GitHub Release
creation. The version PR itself does not publish a release or push a tag.

## Diagnosing Action Failures

Use the commit SHA to distinguish current failures from historical red runs. Earlier
failures were an overlong Python line, Python 3.9 unavailable on Ubuntu 26.04, and
the npm Changesets action requiring package.json. The fixed test matrix pins Ubuntu
24.04, Windows 2022, and macOS 15 Intel for supported Python installations.

If the version PR cannot be created, inspect repository/organization Actions policy
and the job's token permissions; do not mask that failure with a passing step. If
the generated CI fails, repair the underlying input/code and rerun the fixed commit.
