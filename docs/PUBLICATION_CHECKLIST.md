# Public Release Checklist

- [ ] Written confirmation that the publisher owns the code or has authorization to publish it.
- [ ] Review vendor names, internal workflows, URLs, IP ranges, screenshots, and business rules.
- [ ] Rotate any credential ever stored in or near the source tree.
- [ ] Run `tools/export-public.ps1`, then `tools/verify-public.ps1`.
- [ ] Manually review every staged file and the complete first commit.
- [ ] Choose an open-source license only after ownership is confirmed.
- [ ] Add public contact details and a short professional biography.
- [ ] Create the GitHub repository with secret scanning and private vulnerability reporting enabled.
- [ ] Protect the default branch and require CI before merge.
- [ ] Enable Dependabot alerts and updates.
- [ ] Publish with synthetic examples only.

