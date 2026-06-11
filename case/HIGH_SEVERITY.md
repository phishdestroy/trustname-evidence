# High Severity Domains

All domains classified HIGH severity with evidence details.
Source: `data/enriched.csv` — full data including screenshots and form analysis.

---

## CRYPTO_DRAIN (2 domains)

### fragapi.com
- **Form analysis:** `seed_phrase` field detected ← direct evidence of seed phrase harvesting
- **Server fingerprint cluster:** shared with 103 other domains (`server_fp: 24be2aa9d598`)
- **Screenshot:** `evidence/screenshots/fragapi.com.png`

### instasolana.bond
- **Category:** Solana wallet drainer (domain name + page content)
- **Cloudflare-protected**
- **Infrastructure cluster:** shares fingerprint with 1,673 other domains
- **Screenshot:** `evidence/screenshots/instasolana.bond.png`

---

## PHISHING_FINANCE (5 domains)

### busrecharge.com ☁ Cloudflare
- **Form analysis:** `card_number + cvv` — direct evidence of financial card data collection
- **Screenshot:** `evidence/screenshots/busrecharge.com.png`

### drmelaxincorp.com ☁ Cloudflare
- **Brand:** AmericanExpress (detected from page content)
- **Screenshot:** `evidence/screenshots/drmelaxincorp.com.png`

### marrcopizza.com ☁ Cloudflare
- **Form analysis:** `cvv` field detected
- **Screenshot:** `evidence/screenshots/marrcopizza.com.png`

### toto911link.com ☁ Cloudflare
- **Form analysis:** `card_number + password` — credential + card data collection
- **Screenshot:** `evidence/screenshots/toto911link.com.png`

### de-oc.app
- **Pattern:** `de-oc.app` matches German bank phishing pattern (EU Bank Phish cluster)
- **Infrastructure cluster:** Stake lookalike cluster (`server_fp: d8c33640a2fc`, 149 domains)
- **Screenshot:** `evidence/screenshots/de-oc.app.png`

---

## PHISHING_CRYPTO (3 domains)

### ledgerfirmware.app
- **IP:** 64.187.97.204 (US)
- **Registered:** 2026-06-05
- **Page:** Fake Ledger hardware wallet firmware update page
- **Screenshot:** `evidence/screenshots/ledgerfirmware.app.png`

### manage-firmware.net
- **Pattern:** Generic firmware update scam targeting hardware wallet users
- **Infrastructure cluster:** Stake cluster (`server_fp: d8c33640a2fc`)
- **Screenshot:** `evidence/screenshots/manage-firmware.net.png`

### [third domain — see enriched.csv]

---

## MALWARE_DIST (2 domains)

### kmspico.zip ☁ Cloudflare
- **Category:** KMSpico Windows activation crack distribution
- **Infrastructure cluster:** Giant 1,674-domain cluster
- **Screenshot:** `evidence/screenshots/kmspico.zip.png`

### oficial-kmspico.org ☁ Cloudflare
- **Category:** KMSpico mirror/distribution
- **Infrastructure cluster:** Giant 1,674-domain cluster
- **Screenshot:** `evidence/screenshots/oficial-kmspico.org.png`

---

## CARDING (1 domain)

### buyclonecards.bond ☁ Cloudflare
- **Domain name:** Explicit — "buy clone cards"
- **IP:** 188.114.97.3
- **Screenshot:** `evidence/screenshots/buyclonecards.bond.png`

---

## PHISHING_GENERIC (75 domains)

Domains with login/password/credential forms detected by browser form analysis. Many are gambling sites collecting account credentials. Subset with notable patterns:

| Domain | CF | Form | Notes |
|---|---|---|---|
| `argonex.net` | ☁ | password | |
| `artemex.app` | ☁ | password | |
| `revolut-slots.com` | ☁ | password | Revolut brand impersonation |
| `amazon-slotes.com` | ☁ | password | Amazon brand impersonation |
| `stake-go.net` | ☁ | password | Stake.com lookalike |
| `stake-planet.net` | ☁ | password | Stake.com lookalike |
| `stake-play.net` | ☁ | password | Stake.com lookalike |
| `stake-world.net` | ☁ | password | Stake.com lookalike |
| `captchacore.com` | — | password | |
| `vichpagereg.com` | — | password | Cluster with fragapi.com (seed drainer) |
| `vuapagesu.com` | — | password | Cluster with fragapi.com |
| `vupageinso.com` | — | password | Cluster with fragapi.com |

Full list: see `data/high_severity.csv`, filter `category=PHISHING_GENERIC`

---

## MEDIUM Severity Summary (819 domains)

| Sub-category | Count |
|---|---|
| `GAMBLING` — unlicensed casino/betting | 772 |
| `SCAM_MISC` | 1 |
| `PROXY_VPN` | 1 |
| Others | 45 |

Full list: `data/high_severity.csv`
