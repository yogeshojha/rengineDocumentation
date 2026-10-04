---
title: Sign in to the API
description: Sign your script in with a reNgine user account, keep the session alive, and sign out when you are done. This page also covers two-factor sign-in, the sign-in limits and the operations only administrators can call.
layout: pane
sources:
  - api/app/api/v1/auth.py
  - api/app/api/v1/totp.py
  - api/app/api/deps.py
  - api/app/core/security.py
  - api/app/core/ratelimit.py
  - api/app/core/body_limit.py
  - api/app/core/client_ip.py
  - api/app/config.py
  - api/app/services/totp.py
  - api/app/api/v1/users.py
  - api/app/api/v1/mcp.py
  - api/app/api/v1/connectors.py
  - shared/definitions/auth.py
  - shared/utils/bearer.py
  - mcp/auth.py
  - connectors/auth.py
  - .env.example
revised: 2026-10-03
---

Your script signs in with a reNgine user account, the same way you do in the browser. reNgine then sets two cookies: an access token for your calls, and a refresh token that gets you a new access token when the old one expires. The sign-in answer does not include the tokens, so keep the cookies in a cookie jar. If your client does not send the cookies back, as happens with httpx on the API port, read the access token from the jar and send it as a bearer header.

<div class="rn-split" markdown>
<div class="rn-prose" markdown>

## Sign in and call the API

1. **Sign in.** Send your username and password to `POST /api/v1/auth/login`. If the account has no two-factor authentication, the answer is `{"mfa_required": false, "mfa_token": null}` and reNgine sets both cookies. The answer body does not carry the session tokens. <span class="rn-ref" data-tab="curl" data-mark="login">Shown in the pane</span>
2. **Enter the second factor, if the account has one.** For an account with two-factor authentication, the answer is `{"mfa_required": true, "mfa_token": "<token>"}` and no cookie is set yet. Within five minutes, send the `mfa_token` with a code from the authenticator app, or a backup code, to `POST /api/v1/auth/2fa/login`. That answer sets both cookies. <span class="rn-ref" data-tab="curl" data-mark="mfa">Shown in the pane</span>
3. **Call the API.** Send the `access_token` cookie, or the same token as `Authorization: Bearer <token>`. When a request carries a bearer header, reNgine authenticates it by the header alone. <span class="rn-ref" data-tab="curl" data-mark="call">Shown in the pane</span>
4. **Refresh when the access token expires.** The access token lasts 30 minutes by default. When a call returns 401, send the `refresh_token` cookie to `POST /api/v1/auth/refresh`. You get 204 and a new pair of cookies. Then repeat the call. <span class="rn-ref" data-tab="curl" data-mark="refresh">Shown in the pane</span>
5. **Sign out when your script is done.** `POST /api/v1/auth/logout` revokes every token the request carries and clears both cookies. <span class="rn-ref" data-tab="curl" data-mark="logout">Shown in the pane</span>

</div>
<div class="rn-pane" markdown>
<div class="rn-pane-head"><b>Session</b><span>asm.example.com</span></div>

/// tab | curl
<div class="rn-pane-label" data-mark="login">request · sign in</div>

```bash
# RENGINE=https://asm.example.com
curl -c jar -X POST "$RENGINE/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "rengine", "password": "'"$PASSWORD"'"}'
```

<div class="rn-pane-label">response · 200</div>

```json
{ "mfa_required": false, "mfa_token": null }
```

<div class="rn-pane-label" data-mark="mfa">request · second factor</div>

```bash
curl -c jar -X POST "$RENGINE/api/v1/auth/2fa/login" \
  -H "Content-Type: application/json" \
  -d '{"mfa_token": "'"$MFA_TOKEN"'", "code": "492039"}'
```

<div class="rn-pane-label" data-mark="call">request · call</div>

```bash
curl -b jar "$RENGINE/api/v1/auth/me"
```

<div class="rn-pane-label">response · 200</div>

```json
{
  "id": "4c1e8a2b-7d3f-4b6a-9e05-2f8c1d7a6b3e",
  "username": "rengine",
  "email": "admin@asm.example.com",
  "is_active": true,
  "is_superuser": true,
  "totp_enabled": false,
  "created_at": "2026-10-01T09:12:44.512031Z",
  "updated_at": null
}
```

<div class="rn-pane-label" data-mark="refresh">request · refresh</div>

```bash
curl -b jar -c jar -X POST "$RENGINE/api/v1/auth/refresh"
```

<div class="rn-pane-label" data-mark="logout">request · sign out</div>

```bash
curl -b jar -c jar -X POST "$RENGINE/api/v1/auth/logout"
```
///

/// tab | Python
<div class="rn-pane-label">httpx client with a cookie jar</div>

```python
import httpx

client = httpx.Client(base_url="https://asm.example.com/api/v1")

r = client.post("/auth/login",
                json={"username": USERNAME, "password": PASSWORD})
r.raise_for_status()
step = r.json()
if step["mfa_required"]:
    r = client.post("/auth/2fa/login",
                    json={"mfa_token": step["mfa_token"], "code": CODE})
    r.raise_for_status()


def call(method, url, **kwargs):
    r = client.request(method, url, **kwargs)
    if r.status_code == 401:
        client.post("/auth/refresh").raise_for_status()
        r = client.request(method, url, **kwargs)
    r.raise_for_status()
    return r


me = call("GET", "/auth/me").json()
client.post("/auth/logout")
```

<div class="rn-pane-label">bearer header</div>

```python
token = client.cookies["access_token"]
headers = {"Authorization": f"Bearer {token}"}
httpx.get("http://127.0.0.1:8000/api/v1/auth/me", headers=headers)
```
///

</div>
</div>

## Session tokens

reNgine uses three tokens for sign-in and sessions. This table shows how long each one lasts, which setting changes it, and where to send it.

| Token | Carried in | Default lifetime | Setting | Accepted by |
|---|---|---|---|---|
| Access | `access_token` cookie | 30 minutes | `ACCESS_TOKEN_EXPIRE_MINUTES` | Every authenticated operation, as the cookie or as `Authorization: Bearer` |
| Refresh | `refresh_token` cookie | 7 days | `REFRESH_TOKEN_EXPIRE_DAYS` | `POST /api/v1/auth/refresh`, as the cookie only |
| Second factor | `mfa_token` in the login response | 5 minutes | Fixed | `POST /api/v1/auth/2fa/login`, once |

Both cookies carry these attributes:

| Attribute | Value |
|---|---|
| `HttpOnly` | Set |
| `Secure` | Set when `DEBUG` is false |
| `SameSite` | `Lax` |
| `Path` | `/` |
| `Max-Age` | The token lifetime in seconds |

The tokens are JWTs signed with HS256 and `JWT_SECRET_KEY`. Each one carries its type and a unique `jti`, and a token sent where another type is expected gets 401 `Invalid token type`. If you change `JWT_SECRET_KEY`, every token already issued stops working. See [Configuration variables](../../reference/configuration.md).

On the plain-HTTP API port, the Python standard cookie jar, which httpx uses, does not send `Secure` cookies back. On that port, read `access_token` from the jar after you sign in and send it as a bearer header, as the Python tab shows. curl does send the cookies to `127.0.0.1`.

## Sign-in requests

These are the fields the two sign-in calls take and return. Neither call needs authentication.

`POST /api/v1/auth/login` takes:

| Name | In | Type | Required | Default | Description |
|---|---|---|---|---|---|
| `username` | body | string, at most 50 characters | Yes | | Account username, matched exactly |
| `password` | body | string, at most 1,024 characters | Yes | | Account password |

`POST /api/v1/auth/2fa/login` takes:

| Name | In | Type | Required | Default | Description |
|---|---|---|---|---|---|
| `mfa_token` | body | string, at most 2,048 characters | Yes | | The `mfa_token` from the login response |
| `code` | body | string, at most 32 characters | Yes | | A six-digit authenticator code or a backup code of the form `xxxx-xxxx` |

Both return `LoginResponse`:

| Field | Type | Description |
|---|---|---|
| `mfa_required` | boolean | `true` when the account requires a second factor. No cookie is set. |
| `mfa_token` | string or null | The second-factor token, valid for five minutes and one use |

reNgine accepts an authenticator code for the current 30-second step and for the step on either side. Each step works once per account. A backup code works once. An account gets ten backup codes when two-factor authentication is turned on.

Request bodies under `/api/v1/auth/` are limited to 64 KB. A larger body gets 413 `The request body is larger than the 64 KB limit.`

## Refresh

Refresh keeps a long-running script signed in after its access token expires. Each refresh replaces both tokens, so always keep the newest refresh token: reusing an old one after the grace period signs the account out on every client.

| Rule | Behaviour |
|---|---|
| Input | The `refresh_token` cookie. A bearer header is not read. |
| Success | 204. New `access_token` and `refresh_token` cookies. |
| Rotation | The presented refresh token is revoked. It remains usable for 30 seconds counted from its first rotation. |
| Reuse after the grace | Every token of the account is revoked and the call returns 401 `Refresh token has been revoked`. The account is signed out on every client. |

## Sign out

Sign out when your script finishes, so its tokens stop working right away instead of at the end of their lifetime. `POST /api/v1/auth/logout` needs no authentication. It revokes the `access_token` cookie, the `refresh_token` cookie and a bearer token when present, each for its remaining lifetime, clears both cookies and returns `{"message": "Logged out"}`.

## When sessions end

Some events revoke tokens before they expire. Use this table to see when your script has to sign in again.

| Event | Tokens revoked |
|---|---|
| `POST /api/v1/auth/logout` | The tokens the request carries |
| Password change, `POST /api/v1/auth/change-password` | Every token of the account. The calling client receives new cookies. |
| Two-factor enrolment, `POST /api/v1/auth/2fa/verify` | Every token of the account. The calling client receives new cookies. |
| Two-factor removal, `POST /api/v1/auth/2fa/disable` | Every token of the account. The calling client receives new cookies. |
| Deactivation, `PATCH /api/v1/users/{user_id}` with `"is_active": false` | Every token of the account |
| Refresh token reuse after the grace | Every token of the account |

A revoked token gets 401 `Token has been revoked`. An inactive account gets 403 `Account is inactive`.

## Sign-in limits

To slow down password and code guessing, reNgine counts failed attempts in Redis and refuses more attempts once a limit is reached. The window opens at the first failure.

| Counter | Limit | Window |
|---|---|---|
| Failed sign-ins per username and client address | 10 | 15 minutes |
| Failed sign-ins per client address | 50 | 15 minutes |
| Failed second-factor codes per account | 5 | 5 minutes |
| Failed second-factor codes per account | 30 | 24 hours |
| Failed current-password confirmations per account | 5 | 15 minutes |

- A counter at its limit refuses the request before the password or code is checked, with 429 `Too many attempts. Try again in {n} seconds.`
- A successful sign-in clears the counter for its username and address.
- Second-factor failures in the web sign-in and in remote control over Telegram count against the same per-account budget.
- The client address is the peer address that uvicorn resolves through the trusted proxy.
- When Redis is unreachable these limiters refuse the request with 503 `The rate limiter is unavailable. Check that the redis service is running.`

On top of these, the instance-wide request limit applies to every operation outside its exempt paths. See [Errors, limits and counts](errors.md#global-rate-limit).

## Administrator operations

reNgine has two privilege levels: user and administrator. If your script manages users, keys, connectors or instance settings, it has to sign in as an administrator. 93 operations are reserved to administrators and return 403 `Administrator access is required` to a user. [All paths](../../reference/http-api.md) shows who can call each operation.

| Area | Administrator-only operations |
|---|---|
| Users | `GET` and `POST /api/v1/users`, `PATCH` and `DELETE /api/v1/users/{user_id}` |
| Projects | `POST /api/v1/projects` |
| Provider keys | Every operation under `/api/v1/api-keys` |
| MCP | `PATCH /api/v1/mcp/settings`, `GET /api/v1/mcp/calls`, every operation under `/api/v1/mcp/tokens` |
| Remote control | Every operation under `/api/v1/remote-control/channels/{channel}` except `GET .../status` and `GET .../commands` |
| Connectors | `POST /api/v1/connectors`, `PATCH` and `DELETE /api/v1/connectors/{connector_id}`, `POST .../rotate` |
| Out-of-band testing | `PATCH /api/v1/oast`, `POST /api/v1/oast/reset`, `POST /api/v1/oast/test` |
| Check library | `POST /api/v1/vuln-templates/sync`, `POST /api/v1/vuln-templates/upload`, `PATCH` and `DELETE /api/v1/vuln-templates/{template_id}`, `PUT .../source` |
| Threat intelligence and datasets | `PUT /api/v1/threat-intel/auto-sync`, `POST /api/v1/threat-intel/sync`, `POST /api/v1/datasets/{kind}/sync` |
| Bug bounty | `PUT /api/v1/bounty-programs/settings`, `POST /api/v1/bounty-programs/sync`, `POST /api/v1/bounty-programs/sync-feed`, `POST /api/v1/bounty-programs/{platform}/{handle}/sync`, `POST /api/v1/bounty-reports/{platform}/sync` |
| Wordlists | `POST /api/v1/wordlists`, `DELETE /api/v1/wordlists/{wordlist_id}` |
| Reports | `POST /api/v1/reports/themes`, `DELETE /api/v1/reports/themes/{slug}`, `POST /api/v1/reports/fonts`, `DELETE /api/v1/reports/fonts/{slug}`, `PUT /api/v1/reports/defaults` |
| AI | `PATCH /api/v1/ai/settings`, `POST /api/v1/ai/connections`, `PATCH` and `DELETE /api/v1/ai/connections/{connection_id}`, `POST .../use`, `POST .../test`, `POST /api/v1/ai/models`, `POST /api/v1/ai/test`, `DELETE /api/v1/ai/cache` |
| Instance | `PATCH /api/v1/instance-settings`, `GET /api/v1/health/queues`, every operation under `/api/v1/proxies` and `/api/v1/notification-channels` |
| Issue trackers | `POST /api/v1/issue-trackers`, `POST /api/v1/issue-trackers/test`, `PUT /api/v1/issue-trackers/routes`, `DELETE /api/v1/issue-trackers/routes/{route_id}`, `PATCH` and `DELETE /api/v1/issue-trackers/{tracker_id}`, `POST .../test`, `GET .../destinations`, `GET .../issue-types` |
| Onboarding | `PATCH /api/v1/onboarding/progress`, `POST /api/v1/onboarding/complete`, `GET` and `PUT /api/v1/onboarding/ai` |

A scan engine or scan context that carries credentials can be launched only by its creator or an administrator. Another user gets 403 `Engine {name} carries credentials. Its creator or an administrator can launch with it.` or the same sentence for a context.

## Other tokens

Your scripts sign in with a user account, as above. MCP clients and connectors use tokens of their own, which work only on their own endpoints. Every other operation refuses them with 401 `Invalid or expired token`.

| Token | Format | Accepted by |
|---|---|---|
| MCP token | `rngmcp_` followed by 48 hexadecimal characters | `POST /api/v1/mcp` and the stdio transport. See [Control what an agent can do](../../agents/mcp/capabilities.md). |
| Connector token | `rngconn_` followed by 48 hexadecimal characters | `/api/v1/connectors/ingest`, `/actions`, `/targets`, `/notices`, `/findings`, `/scope` and `/host`. See [Burp Suite](../../pentesters/burp-suite.md). |

Keys stored under `/api/v1/api-keys` are something else: they let reNgine sign in to third-party data providers.

## Errors

If a call is refused, find its status and `detail` below.

| Status | `detail` | What to do |
|---|---|---|
| 401 | `Not authenticated` | Send the `access_token` cookie or a bearer header. |
| 401 | `Invalid or expired token` | Refresh the session, or sign in again. |
| 401 | `Token has been revoked` | Sign in again. |
| 401 | `Invalid token type` | Send the access token. |
| 401 | `User not found` | The account no longer exists. |
| 401 | `Incorrect username or password` | Check the credentials. |
| 401 | `Invalid or expired MFA token` | Sign in again for a new `mfa_token`. |
| 401 | `MFA token has been used` | Sign in again for a new `mfa_token`. |
| 401 | `Invalid verification code` | Send the current code or an unused backup code. |
| 401 | `The stored two-factor secret is unreadable. Use a backup code.` | Sign in with a backup code. |
| 401 | `Refresh token not found` | Send the `refresh_token` cookie. |
| 401 | `Invalid or expired refresh token` | Sign in again. |
| 401 | `Refresh token has been revoked` | Sign in again. Every session of the account was ended. |
| 403 | `Account is inactive` | An administrator reactivates the account. |
| 403 | `Administrator access is required` | Call with an administrator account. |
| 413 | `The request body is larger than the 64 KB limit.` | Send a smaller body. |
| 429 | `Too many attempts. Try again in {n} seconds.` | Wait for the window to close. |
| 503 | `The rate limiter is unavailable. Check that the redis service is running.` | Start the redis service. |

401 responses carry `WWW-Authenticate: Bearer`.
