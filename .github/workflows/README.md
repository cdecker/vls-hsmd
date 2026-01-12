# VLS-CLN Compatibility Matrix Workflow

This directory contains GitHub Actions workflows for testing compatibility between different versions of Core Lightning (CLN) and Validating Lightning Signer (VLS).

## compatibility-matrix.yml

The main compatibility testing workflow that runs the VLS test suite against different combinations of CLN and VLS versions.

### Features

- **Automatic Matrix Generation**: Dynamically generates all combinations of specified CLN and VLS versions
- **Parallel Testing**: Runs all version combinations in parallel for faster results
- **Scheduled Testing**: Automatically runs weekly to catch regressions
- **Manual Triggers**: Can be manually triggered with custom version lists
- **Comprehensive Reports**: Generates compatibility matrix reports with pass/fail status
- **Artifact Storage**: Saves test logs and results for 30 days

### Triggers

The workflow runs on:

1. **Push to main branch**: Tests with default version matrix
2. **Pull requests**: Tests with default version matrix and posts results as PR comment
3. **Weekly schedule**: Runs every Monday at 00:00 UTC with default versions
4. **Manual dispatch**: Can be triggered manually from GitHub Actions UI with custom versions

### Default Versions

The workflow tests these versions by default (configurable in the workflow file):

- **CLN versions**: v24.11.1, v24.08.2, v24.05
- **VLS versions**: v0.13.0, v0.12.1, v0.12.0

This creates 9 test combinations (3 CLN × 3 VLS).

### Manual Execution with Custom Versions

To run the workflow with custom versions:

1. Go to the **Actions** tab in GitHub
2. Select **VLS-CLN Compatibility Matrix** workflow
3. Click **Run workflow**
4. Enter comma-separated version lists:
   - CLN versions: `v24.11.1,v24.08.2,v24.05,v23.11`
   - VLS versions: `v0.13.0,v0.12.1,v0.11.0`
5. Click **Run workflow**

### Updating Default Versions

To change the default versions being tested, edit the `env` section at the top of `compatibility-matrix.yml`:

```yaml
env:
  DEFAULT_CLN_VERSIONS: 'v24.11.1,v24.08.2,v24.05'
  DEFAULT_VLS_VERSIONS: 'v0.13.0,v0.12.1,v0.12.0'
```

### Understanding Results

The workflow produces several outputs:

1. **Job Status**: Each matrix combination shows as a separate job with pass/fail status
2. **Step Summary**: Each job produces a summary with test counts (passed, failed, skipped, errors)
3. **Test Artifacts**: Full test logs are uploaded for each combination
4. **Compatibility Report**: A final report summarizing all combinations in a table format

### Compatibility Report Format

The generated report looks like:

```markdown
| CLN Version | VLS Version | Status | Passed | Failed | Skipped |
|-------------|-------------|--------|--------|--------|---------|
| v24.11.1    | v0.13.0     | ✅ Pass | 156   | 0      | 12      |
| v24.11.1    | v0.12.1     | ❌ Fail | 145   | 3      | 12      |
| ...         | ...         | ...    | ...   | ...    | ...     |
```

### Test Duration

- Individual test suite: ~30-60 minutes per combination
- Full matrix (9 combinations): ~30-60 minutes (runs in parallel)
- Workflow timeout: 120 minutes maximum per job

### Artifacts

Test results are stored as artifacts:

- **Test results**: Retained for 30 days, includes logs and reports
- **Compatibility report**: Retained for 90 days, summary of all test runs

### Viewing Results

1. Go to the **Actions** tab
2. Click on a workflow run
3. View individual job results or download artifacts
4. Check the final "Generate Compatibility Report" job for the summary table

### Known Limitations

- Some VLS/CLN combinations may be incompatible due to protocol changes
- Tests marked as `skipped` indicate known incompatibilities (see test files for details)
- Network timing issues may cause occasional flaky test failures

### Troubleshooting

If a test combination fails:

1. Download the test artifacts for that specific combination
2. Review the `test-output.log` for detailed error messages
3. Check if the failure is expected (some versions have known incompatibilities)
4. Run the test locally using: `task test-vls-socket`

### Local Testing

To test a specific version combination locally:

```bash
# Checkout desired CLN version
cd lightning
git checkout v24.11.1
cd ..

# Checkout desired VLS version
cd vls
git checkout v0.13.0
cd ..

# Run tests
task build
task test-vls-socket
```

### Contributing

When adding new test cases or fixing compatibility issues:

1. Update the test files in `tests/`
2. Mark incompatible tests as skipped with clear reasons
3. The CI will automatically test your changes against all version combinations
4. Review the compatibility report to ensure no regressions
