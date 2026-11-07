# Public Release Checklist

- [ ] Written confirmation that the publisher owns the code or has authorization to publish it.
- [ ] Review vendor names, internal workflows, URLs, IP ranges, screenshots, and business rules.
- [ ] Rotate any credential ever stored in or near the source tree.
- [x] Run `tools/verify-public.ps1` against the release candidate.
- [ ] Manually review every staged file and the complete first commit.
- [ ] Choose an open-source license only after ownership is confirmed.
- [ ] Add public contact details and a short professional biography.
- [ ] Create the GitHub repository with secret scanning and private vulnerability reporting enabled.
- [ ] Protect the default branch and require CI before merge.
- [x] Configure Dependabot updates for GitHub Actions and both packaged Python applications.
- [x] Keep demos and public documentation limited to synthetic examples.
- [x] Add CI for tests, compilation, secret-like content, and public-tree verification.
- [x] Add a tagged release workflow that builds, tests, hashes, and publishes the GUARDIAN installer.
- [x] Add a professional inquiry form that warns against sharing confidential information.

## Remaining owner decisions

1. Confirm ownership or written permission for every project being published.
2. Choose whether the entire portfolio receives an open-source license; GUARDIAN already uses MIT.
3. Provide a public professional contact or use GitHub Issues as the only contact channel.
4. Choose the GitHub account and final repository name.
5. After publication, enable secret scanning, private vulnerability reporting, branch protection, and required CI in repository settings.

