# Public Release Checklist

- [x] Repository owner explicitly authorized public publication from the authenticated owner account.
- [x] Review vendor names, internal workflows, URLs, IP ranges, screenshots, and business rules.
- [ ] Rotate any credential ever stored in or near the source tree.
- [x] Run `tools/verify-public.ps1` against the publication tree.
- [x] Manually review every staged file and the complete publication commit.
- [x] Apply the MIT license to the public repository.
- [x] Use GitHub Issues as the public contact channel without exposing a personal email address.
- [x] Select the authenticated owner account and final repository name.
- [ ] Protect the default branch and require CI before merge.
- [x] Configure Dependabot updates for GitHub Actions and both packaged Python applications.
- [x] Keep demos and public documentation limited to synthetic examples.
- [x] Add CI for tests, compilation, secret-like content, and public-tree verification.
- [x] Add a tagged release workflow that builds, tests, hashes, and publishes the GUARDIAN installer.
- [x] Add a professional inquiry form that warns against sharing confidential information.

## Post-publication repository settings

1. Enable every security feature supported by the account plan.
2. Protect the default branch after the first CI run is available to require.
3. Publish a tagged GUARDIAN installer release and verify its SHA-256 asset.

