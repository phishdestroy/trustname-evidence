# Provenance & Chain of Custody

This document describes the origin, transformation, and verification of every artefact in this repository — sufficient for forensic admissibility, regulatory referral, and academic citation.

---

## 1 · Investigation Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                       Phase II Evidence Generation Pipeline                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│    [Registrar Zone List]                                                        │
│           │                                                                     │
│           ▼                                                                     │
│    ┌──────────────────┐    AWS Lambda (Python 3.11 + aiohttp)                   │
│    │  Phase 1 — HTTP  │    77 invocations × 80 concurrent, Googlebot UA         │
│    │  Fingerprint     │    output: lambda_results.jsonl                         │
│    └──────────────────┘                                                         │
│           │                                                                     │
│           ▼                                                                     │
│    ┌──────────────────┐    Playwright + stealth v2, headless Chromium           │
│    │  Phase 2 — Render│    Per-domain isolated context, form-field analysis     │
│    │                  │    output: deep_results.jsonl, screenshots/*.png        │
│    └──────────────────┘                                                         │
│           │                                                                     │
│           ▼                                                                     │
│    ┌──────────────────┐    SOCKS5 pool (2,600+ exits) + 2captcha                │
│    │  Phase 3 — CF    │    hCaptcha, reCAPTCHA v2/v3, Cloudflare Turnstile      │
│    │  Deep Scan       │    output: 1,953 screenshots, 92 CAPTCHAs solved        │
│    └──────────────────┘                                                         │
│           │                                                                     │
│           ▼                                                                     │
│    ┌──────────────────┐    Llama 3.1 (Groq) for content classification          │
│    │  Phase 4 — AI +  │    Spamhaus DBL · SURBL · URLhaus · ThreatFox            │
│    │  Threat Intel    │    output: threat_intel.jsonl                           │
│    └──────────────────┘                                                         │
│           │                                                                     │
│           ▼                                                                     │
│    ┌──────────────────┐    ipinfo.io API (3 tokens, rotated)                    │
│    │  Phase 5 — GeoIP │    Country code + ASN for every responding IP           │
│    │                  │    output: enriched ip_country, ip_asn fields           │
│    └──────────────────┘                                                         │
│           │                                                                     │
│           ▼                                                                     │
│    ┌──────────────────┐    Redaction pass:                                      │
│    │  Phase 6 — PII   │    • scan-server IP address                             │
│    │  Redaction       │    • local filesystem paths                              │
│    │                  │    • API tokens (Groq, 2captcha, proxy, ipinfo)         │
│    └──────────────────┘                                                         │
│           │                                                                     │
│           ▼                                                                     │
│    ┌──────────────────┐    Merge → enriched.csv (canonical source-of-truth)     │
│    │  Phase 7 — Merge │    Compress → pkg/raw_data/*.gz                         │
│    │  & Publication   │    Render → docs/data.json, docs/index.html             │
│    └──────────────────┘    Hash → evidence/HASHES.txt                           │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2 · Artefact Inventory

All artefacts are content-addressed by SHA-256 to support chain-of-custody verification.

| File | Size | SHA-256 prefix | Description |
|---|---:|---|---|
| `data/enriched.csv` | 2.8 MB | `83ea143175d8a378` | Full enriched dataset — all 7,641 domains with classification, IPs, country codes, AI descriptions, threat-intel hits |
| `data/high_severity.csv` | 748 KB | `ecee3b68b2fb34c8` | HIGH-only filtered subset (1,114 domains) |
| `data/dead_domains.csv` | 742 KB | `5ee84646c6872591` | Dead / parked / error enumeration (5,058 domains) |
| `ioc/domains_high.txt` | 19 KB | `ec9e43c15ff3cffc` | Production blocklist — 1,114 HIGH severity domains (newline-delimited) |
| `ioc/domains_all_malicious.txt` | 39 KB | `d27809c1a099c019` | Production blocklist — 2,221 HIGH + MEDIUM domains |
| `ioc/indicators.csv` | 775 KB | `4e9dcd3840be9f9a` | SIEM-ready indicators: domain, ip, server_fp, favicon_mmh3, category, severity, brand, threat_sources |
| `evidence/HASHES.txt` | 168 KB | `131ff258bd0c058c` | SHA-256 manifest of all 1,953 screenshots |
| `docs/data.json` | 4.2 MB | `5d4839a121793f97` | Slim per-domain dataset rendered by `docs/index.html` and `docs/domains.html` |
| `pkg/raw_data/enriched.csv.gz` | 560 KB | `a2a6f5fda9f364aa` | Compressed enriched dataset for download |
| `pkg/raw_data/lambda_results.jsonl.gz` | 509 KB | `c0add17921efada8` | Phase 1 raw HTTP fingerprint output (JSONL) |
| `pkg/raw_data/deep_results.jsonl.gz` | 1.1 MB | `60b943f03e7ac926` | Phase 2/3 raw browser render output (JSONL) |
| `pkg/raw_data/threat_intel.jsonl.gz` | 74 KB | `4a92dafe955b60d4` | Phase 4 threat-intel cross-reference (JSONL) |
| `SHA256SUMS.txt` | generated | repository manifest | SHA-256 manifest for committed repository files |

---

## 3 · Screenshot Capture Provenance

| Parameter | Value |
|---|---|
| Engine | Playwright 1.40 + headless Chromium |
| Stealth | `playwright-stealth` v2 (`Stealth().apply_stealth_async(page)`) |
| Viewport | 1280 × 800 |
| Settle delay | 2.5 s post-`domcontentloaded`; +5 s on Cloudflare JS challenge |
| Captcha solving | 2captcha — hCaptcha, reCAPTCHA v2/v3, Cloudflare Turnstile |
| Proxy pool | 2,600+ SOCKS5 exits, round-robin |
| Browser context | Isolated per domain (prevents `TargetClosedError` cascade) |
| Total captured | 1,953 |
| Naming | `<domain>.png` — 1:1 mapping with `data/enriched.csv` `domain` column |

---

## 4 · Verification Procedure

### Single archive
```bash
sha256sum pkg/raw_data/enriched.csv.gz
# expected prefix: a2a6f5fda9f364aa…
```

### Repository manifest
```bash
sha256sum -c SHA256SUMS.txt
```

### All screenshots
```bash
cd docs/screenshots
sha256sum -c ../../evidence/HASHES.txt
```

### Regenerate the manifest (reproducibility)
```bash
sha256sum docs/screenshots/*.png > evidence/HASHES.txt
```

### Re-derive `data.json` from canonical source
```bash
python docs/build_datajson.py
# input:  data/enriched.csv
# output: docs/data.json
```

Additional verification and release-signing instructions are in `VERIFY.md`.

---

## 5 · Redaction Disclosure

The following classes of data were removed from all published artefacts during Phase 6, in compliance with operational-security and third-party-confidentiality requirements:

| Class | Pattern | Replacement |
|---|---|---|
| Scan-server IPv4 | Internal scan address | `[REDACTED-SCAN-IP]` |
| Local filesystem paths | Scanner working directories | (removed) |
| Groq API tokens | Provider API keys | `[REDACTED-GROQ-KEY]` |
| 2captcha API token | Provider API key | `[REDACTED-2CAPTCHA]` |
| Proxy provider tokens | Provider API keys | `[REDACTED-PROXY-TOKEN]` |
| xAI API tokens | Provider API keys | `[REDACTED-XAI-KEY]` |
| Server-management credentials | Passwords and access material | `[REDACTED-PWD]` |

Original captured content (Cloudflare challenge pages and DNSProxy antibot pages) leaked our scan-server IP into the body-text column of certain rows. All 3,329 such occurrences across `enriched.csv`, `high_severity.csv`, `enriched.csv.gz`, and `deep_results.jsonl.gz` were programmatically replaced. A second pass verified zero residual occurrences across all `.html`, `.csv`, `.json`, `.md`, `.txt`, and `.py` files.

---

## 6 · Reproducibility

| Component | Version |
|---|---|
| Python | 3.11 (Lambda) · 3.12 (local) |
| aiohttp | ≥ 3.9 |
| Playwright | 1.40 |
| playwright-stealth | v2 |
| Groq SDK | latest at scan time |
| ipinfo.io | API v1 |
| 2captcha | API v1 |

Scan window: **June 2026.** No re-scan was performed after publication; data reflects the registrar's zone state at the time of capture.

---

## 7 · Contact

Technical or evidentiary questions: contact PhishDestroy via [phishdestroy.io](https://phishdestroy.io).
For law-enforcement liaison, reference *Phase II of the Trustname Investigation*; Phase I is published at [phishdestroy.io/trustname-bulletproof-exposed](https://phishdestroy.io/trustname-bulletproof-exposed/).

---

*PhishDestroy Research · TLP:CLEAR · MIT License · June 2026*
