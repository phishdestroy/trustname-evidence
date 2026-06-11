# Data — Schema and Source Files

Source datasets for the Phase II zone scan of Fewmoretaps OÜ / Trustname.com.

## File Inventory

| File | Rows | Size | Description |
|---|---:|---:|---|
| `enriched.csv` | 7,641 | 2.8 MB | Full per-domain dataset — primary evidence file |
| `high_severity.csv` | 1,114 | 748 KB | HIGH-only filtered subset (severity_label = HIGH) |
| `dead_domains.csv` | 5,058 | 742 KB | Dead / parked / error enumeration |

## `enriched.csv` — Schema

One row per domain. CSV with UTF-8 BOM, RFC-4180 quoting.

### Identification

| Column | Description |
|---|---|
| `domain` | Registered domain name |
| `registrar` | `Fewmoretaps OU d/b/a Trustname.com` |
| `registered_at` | Registration date (ISO 8601) |
| `expiring_at` | Expiry date (ISO 8601) |
| `emails` | WHOIS registrant email (where exposed); retained only in canonical CSV evidence |
| `phones` | WHOIS registrant phone (where exposed); retained only in canonical CSV evidence |
| `ip` | Resolved IPv4 address |
| `ip_country` | IP geolocation country |

### Phase 1 — HTTP Fingerprint

| Column | Description |
|---|---|
| `status_code` | HTTP response code |
| `final_url` | URL after redirect chain |
| `server` | Raw `Server` response header |
| `server_fp` | SHA-256 prefix of `server \| content-type \| x-powered-by` — operator cluster key |
| `is_cloudflare` | Boolean — domain behind Cloudflare |
| `favicon_mmh3` | MurmurHash3 of `/favicon.ico` — Shodan-compatible operator fingerprint |
| `body_simhash` | 64-bit body SimHash — near-duplicate detection |
| `parking_service` | Detected parking provider |
| `page_type` | Classifier output: `active_content`, `active_with_forms`, `parking`, `dead`, etc. |

### Phase 2/3 — Browser Render

| Column | Description |
|---|---|
| `title` | `<title>` tag content |
| `h1` | First H1 heading |
| `meta_desc` | `<meta name="description">` content |
| `body_text_500` | First 500 chars of visible body text |
| `lang` | `<html lang="">` attribute |
| `form_count` | Number of `<form>` elements |
| `field_types` | Sampled form `type:name` pairs |
| `form_labels` | **Sensitive-data collection flags**: `seed_phrase`, `card_number`, `cvv`, `password`, `otp_2fa`, `iban`, `ssn`, `wallet_addr`, `private_key` |
| `captcha` | Blocking CAPTCHA type: `hcaptcha`, `recaptcha`, `turnstile`, `cf_js` |
| `screenshot` | Path to PNG capture |

### Phase 4 — Classification & Threat Intel

| Column | Description |
|---|---|
| `category` | Classifier output — see categories below |
| `severity` | 0 = INFO, 1 = LOW, 2 = MEDIUM, 3 = HIGH |
| `severity_label` | `INFO` / `LOW` / `MEDIUM` / `HIGH` |
| `brand` | Impersonated brand, where detected |
| `groq_desc` | LLM natural-language description |
| `threat_hits` | Number of threat-intel feed hits |
| `threat_sources` | Comma-separated list of feeds: `spamhaus_dbl`, `surbl`, `urlhaus`, `threatfox` |
| `notes` | Cluster hints, operator notes |

## Classification Categories — Actual Counts

| Category | Severity | Count |
|---|:---:|---:|
| `GAMBLING` | MEDIUM | 733 |
| `PHISHING_GENERIC` | HIGH | 396 |
| `PHISHING_FINANCE` | HIGH | 236 |
| `CARDING` | HIGH | 182 |
| `PHISHING_CRYPTO` | HIGH | 178 |
| `CRYPTO_SCAM` | HIGH | 146 |
| `MALWARE_DIST` | HIGH | 105 |
| `BRAND_ABUSE` | MEDIUM | 83 |
| `ADULT` | MEDIUM | 81 |
| `CRYPTO_DRAIN` | HIGH | 60 |
| `SPAM_INFRA` | MEDIUM | 56 |
| `PROXY_VPN` | MEDIUM | 48 |
| `ILLEGAL_DRUGS` | HIGH | 42 |
| `CRYPTO_MIXER` | HIGH | 28 |
| `ACTIVE` | LOW | 207 |
| `PARKING` | INFO | 27 |
| `ERROR` | INFO | 286 |
| `DEAD` | INFO | 4,745 |

## Raw Output Archives (`../pkg/raw_data/`)

| File | Size | Phase | Format |
|---|---:|---|---|
| `lambda_results.jsonl.gz` | 509 KB | 1 — HTTP fingerprint | One JSON per line, gzip |
| `deep_results.jsonl.gz` | 1.1 MB | 2/3 — Browser + CF deep | One JSON per line, gzip |
| `threat_intel.jsonl.gz` | 74 KB | 4 — Threat-intel | One JSON per line, gzip |
| `enriched.csv.gz` | 559 KB | Merge of all | gzipped CSV |

## Scan Parameters

| Parameter | Value |
|---|---|
| Scan window | June 2026 |
| Zone size | 7,641 domains (complete) |
| Lambda concurrency | 80 req/invocation × 77 invocations |
| Browser concurrency | 5 parallel Chromium contexts |
| HTTP timeout | 8 s (curl_cffi, Chrome TLS fingerprint) |
| Browser timeout | 22 s |
| Capture viewport | 1280 × 800 |
| Stealth | `playwright-stealth` v2 |

---

*Schema reference for Phase II of the Trustname investigation. See [`../README.md`](../README.md).*
