# Investigation: Fewmoretaps OU / Trustname.com

**Status:** Active
**Scope:** All domains registered under Fewmoretaps OU d/b/a Trustname.com
**Scan date:** June 2026
**Domains scanned:** 7,641 (complete zone, zero sampling)

---

## Registrar Profile

| Field | Value |
|---|---|
| Entity | Fewmoretaps OU |
| DBA | Trustname.com |
| Jurisdiction | Estonia |
| WHOIS shield | PrivacyGuardian heavily used |
| Zone size | 7,641 active domains (scan date) |

---

## Methodology

### Phase 1 — HTTP Fingerprint
**Tool:** AWS Lambda (Python 3.12 / aiohttp), 80 concurrent req/invocation
**Coverage:** 100% of zone (7,641 domains)
**Collected:**
- HTTP status code, redirect chain, final URL
- Server, X-Powered-By, ETag, Cache-Control headers
- Page title, visible text snippet
- Favicon URL → MurmurHash3 (Shodan-compatible operator fingerprint)
- Body SimHash (duplicate content detection)
- Server fingerprint: SHA-256(server | content-type | x-powered-by)

Results: **1,725 alive** / **5,916 dead or unreachable**

### Phase 2 — Full Browser Render
**Tool:** Playwright 1.49 + playwright-stealth, headless Chromium
**Coverage:** All 1,725 alive domains
**Collected per domain:**
- Full-page screenshot (PNG, SHA-256 verified)
- `<title>`, H1–H2 headings, meta description
- All form fields: name, type, placeholder, label, autocomplete attribute
- Page body text (up to 2,000 chars, scripts/nav stripped)
- External links, image alt texts, page language

**Form analysis** — automated detection of data-collection intent:

| Pattern | Severity | Meaning |
|---|---|---|
| `seed_phrase`, `mnemonic`, `recovery_phrase` | HIGH | Crypto wallet seed harvester |
| `private_key`, `secret_key` | HIGH | Private key extractor |
| `card_number`, `cvv`, `cvc` | HIGH | Financial card phishing |
| `ssn`, `social_security` | HIGH | Identity theft |
| `iban`, `bank_account` | MEDIUM | Banking phishing |
| `password`, `passwort` | MEDIUM | Credential harvesting |
| `otp`, `2fa_code`, `sms_code` | MEDIUM | 2FA bypass phishing |
| `wallet_address` | MEDIUM | Crypto wallet collection |

### Phase 3 — Threat Intelligence
Cross-referenced against:
- **Spamhaus DBL** (DNS): spam/phish/malware/botnet classification
- **SURBL** (DNS): URI reputation
- **URLhaus** (abuse.ch REST): active malware distribution URLs
- **ThreatFox** (abuse.ch REST): IOC database

---

## Key Findings

### Phishing Clusters

#### American Express Cluster
Five domains registered by identical WHOIS data (`max@unternehmen.de`, phone `4-23-10-17-10`), all targeting German-speaking Amex cardholders, all behind Cloudflare:

| Domain | Registered | IP |
|---|---|---|
| amex-security.app | 2026-05-26 | 188.114.97.3 |
| amex-safety.app | 2026-04-30 | 104.21.58.253 |
| safety-amex.app | 2026-05-02 | 188.114.96.3 |
| security-amex.app | 2026-04-30 | 188.114.97.3 |
| sicherheit-amex.app | 2026-05-02 | 104.21.41.44 |

Operator re-registration pattern: domain names rotate `security`/`safety`/`sicherheit` + `amex`. WHOIS contact consistent across all five.

#### Ledger Firmware Scam
- `ledgerfirmware.app` — fake Ledger hardware wallet firmware update page (IP: 64.187.97.204 US)
- `manage-firmware.app` — generic firmware scam (IP: 104.207.76.194)

Both registered 2026-06-05. Classic social-engineering attack against Ledger hardware wallet users.

#### Wallet Drainer Infrastructure
- `drainmebaby.bond` — explicit name, Cloudflare-protected
- `ghostqrpanel.bond` — QR-code drain panel (IP: 146.103.41.94 US)
- `instasolana.bond` — Solana wallet drainer

#### Clone Cards / Carding
- `buyclonecards.bond` — clone credit card shop (Cloudflare)
- `rollmaneycontrol.bond` — money mule / funds rolling infrastructure

#### Multilingual Gambling App Network
Eight language variants registered **same day** (2026-05-25), same Cloudflare IP cluster:

| Domain | Language |
|---|---|
| giochi-apps.bet | Italian |
| jeux-apps.bet | French |
| juegos-apps.bet | Spanish |
| igri-prilozheniya.app | Russian |
| pelit-sovellus.app | Finnish |
| spil-apps.app | Danish |
| hry-aplikace.app | Czech |
| gry-aplikacje.app | Polish |

Single coordinated operator registering a multilingual gambling distribution network.

#### Turkish Gambling Cluster
`artemisbet1169.cam`, `vaycasino-girorj.cam`, `vaycasino1107.cam`, `vaycasino-giris.cam`, `vaycasino-resmi-girisimiz.cam`, `matbet-orjgir.cam`, `lunabet987.cam` — all registered April 2026, Turkish-market betting/casino domains.

#### Brand Abuse — Law Firm
`aoshearman.associates`, `aoshearman.attorney` — impersonating A&O Shearman (international law firm). Registered 2026-05-18.

---

## Classification System

| Category | Severity | Description |
|---|---|---|
| `PHISHING_FINANCE` | HIGH | Bank, payment processor, fintech brand impersonation |
| `PHISHING_CRYPTO` | HIGH | Crypto exchange/wallet brand impersonation |
| `CRYPTO_DRAIN` | HIGH | Wallet drainer, seed phrase / private key harvester |
| `CARDING` | HIGH | Clone cards, dumps shops, money mule infrastructure |
| `MALWARE_DIST` | HIGH | Crackware, firmware scams, software trojanisation |
| `PHISHING_GENERIC` | HIGH | Credential harvesting pages (unbranded or multi-brand) |
| `BRAND_ABUSE` | MEDIUM | Law firm, corporate brand domain squatting |
| `SCAM_MISC` | MEDIUM | Fee scams, investment fraud, misc financial scams |
| `GAMBLING` | MEDIUM | Unlicensed casino/betting (many jurisdictions) |
| `PROXY_VPN` | MEDIUM | Proxy/VPN services (abuse enablement) |
| `ADULT` | LOW | Adult content |
| `ACTIVE` | LOW | Responds, no malicious pattern detected |
| `REDIRECT` | LOW | Redirect chain, destination not classified |
| `PARKING` | INFO | Parked page |
| `DEAD` | INFO | No DNS / no HTTP response |

---

## Evidence Integrity

All screenshots are SHA-256 hashed post-capture.
Verification:
```bash
sha256sum -c evidence/HASHES.txt
```

Raw data files in `pkg/raw_data/` are gzip-compressed and include original JSONL output from Lambda and Playwright stages.

---

## Intended Use

This evidence is suitable for:
- ICANN RAA Compliance complaints
- UDRP / URS proceedings (cybersquatting / brand abuse)
- Law enforcement referrals (financial fraud, carding)
- Registrar abuse reports (direct to Trustname.com / Fewmoretaps OU)
- Academic / threat intelligence research
