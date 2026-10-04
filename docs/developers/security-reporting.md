---
title: Report a vulnerability
description: If you find a security vulnerability in reNgine, report it privately through GitHub, so it can be fixed before the details become public.
sources:
  - .github/SECURITY.md
  - README.md
revised: 2026-10-03
---

Reports go through GitHub's private vulnerability reporting on the yogeshojha/rengine repository.

## Report a vulnerability

1. **Keep it private.** Do not disclose the vulnerability in a GitHub issue, a forum or any other public place before the fix is released.
2. **Open the Security tab.** Go to the [Security tab](https://github.com/yogeshojha/rengine/security) of the repository.
3. **Open the form.** Select **Report a vulnerability**. GitHub opens its private vulnerability reporting form.
4. **Describe the vulnerability.** Include:
    - the steps to reproduce it
    - its impact
    - suggested fixes or mitigations, when known

## What happens next

Here is what you can expect after you report:

| Item | Policy |
|---|---|
| First answer | Reports are usually answered within 72 hours. |
| Credit | Responsible disclosure is credited after the fix is released. A reporter may stay anonymous. |
| CVE | A confirmed vulnerability receives a CVE ID. |

## Policy files

The policy is written down in two places in the repository:

| File | Content |
|---|---|
| `.github/SECURITY.md` | The reporting steps, the response time, the credit and CVE policy, and past vulnerabilities by year with their reporters |
| `README.md` | The section Reporting Security Vulnerabilities, with the same steps |

To learn how an instance protects itself, see [Security model](../pentesters/security-model.md).
