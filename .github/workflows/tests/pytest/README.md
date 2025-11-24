# Pytest Integration Tests

This folder contains pytest-based integration tests that validate the GitHub Action behaviour by triggering test workflows and asserting results in S3 / CloudFront. The tests provide quick feedback if changes break the action.

Prerequisites
- Python 3.11 (CI uses this version)
- pip, pytest, boto3
- AWS credentials that can assume the test role used by the workflows
- GitHub CLI (`gh`) authenticated with a token that can trigger workflows:
  ```sh
  echo "$GITHUB_TOKEN" | gh auth login --with-token
  ```

How the tests work
- The integration trigger workflow: `.github/workflows/run-integration-tests.yml` (runs on PR activity).
- Tests usually call `trigger_workflow` (utils/act_test_utils) to dispatch a workflow, then poll/fetch logs and assert outcomes.
- Some tests make direct AWS assertions (S3 objects, CloudFront invalidations) using boto3.

Key files
- Test utilities: `.github/workflows/tests/pytest/utils/act_test_utils.py`
- Expected error messages: `.github/workflows/tests/pytest/utils/expected_errors.json`
- Example workflow to run tests: `.github/workflows/test-run-action.yml`

Configuration notes
- The test S3 bucket and CloudFront distribution ID are defined in `act_test_utils.py` (`bucket_name`, inputs).
- Negative tests refer to expected CLI error messages in `expected_errors.json`.
- The workflows are expected to exist on the repository default branch (e.g. `main`). The trigger helper accepts an override branch name when needed.

Run CI workflow directly
- Dispatch the example workflow with `gh`:
```sh
gh workflow run test-run-action.yml --ref=<branch>
```
- To run the integration tests workflow against a feature branch (workflow file must exist on the default branch to be visible to `gh`), push/merge the workflow to the default branch or use the branch override in the test utilities.

Debugging tips
- View logs for a run:
```sh
gh run view <run_id> --log
```
- The test utilities emit helpful logs; inspect `act_test_utils.py` for bucket/distribution settings if tests target different resources.

Contributing / Safety
- Ensure AWS and GitHub credentials are scoped minimally before running tests.
- Update `act_test_utils.py` if you need to point tests to different