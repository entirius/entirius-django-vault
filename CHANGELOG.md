# Changelog

## Unreleased

- Keys verified by django-access when installed: the X-API-KEY routes check access tokens through
  `verify_api_key` (scope `vault.api` on the URL channel — a pinned token passes on its own
  channel only), never the legacy table; the refusal stays
  401 "Invalid api key". Without django-access nothing changes. `vault-generate-api-key` then refuses and
  names `access_token create`; the key admin becomes read-only.
- The legacy key admin states that keys come from `vault-generate-api-key` (a row added by hand is unreadable).
- The key admin shows only the last four characters of a key and no longer searches by key.
