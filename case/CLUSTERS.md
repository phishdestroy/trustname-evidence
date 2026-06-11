# Operator Clusters

Domains grouped by shared technical fingerprints — evidence of coordinated infrastructure operated by the same threat actor.

---

## Method

Two independent signals:
1. **Server fingerprint** (`server_fp`) — SHA-256 prefix of `Server header | Content-Type | X-Powered-By` response headers
2. **Favicon MurmurHash3** (`favicon_mmh3`) — Shodan-compatible hash of favicon bytes

Identical fingerprint = same hosting stack / same operator template.

---

## Giant Infrastructure Cluster (1,674 domains)

`server_fp: 811e0897f489`

The single largest cluster in the dataset — **1,674 domains** sharing identical server fingerprint.
Includes confirmed malicious domains:

| Domain | Category | Notes |
|---|---|---|
| `instasolana.bond` | CRYPTO_DRAIN | Solana wallet drainer |
| `kmspico.zip` | MALWARE_DIST | KMSpico crackware distribution |
| `oficial-kmspico.org` | MALWARE_DIST | KMSpico mirror |
| `busrecharge.com` | PHISHING_FINANCE | Card number + CVV collection confirmed |
| `drmelaxincorp.com` | PHISHING_FINANCE | AmericanExpress phishing |
| `toto911link.com` | PHISHING_FINANCE | Card + password form |
| `3xcas.com` | PHISHING_GENERIC | Casino credential harvester |
| `amazon-slotes.com` | PHISHING_GENERIC | Amazon-branded slots scam |

**Implication:** A single hosting infrastructure provider or CDN configuration is shared across 1,674 domains including confirmed phishing, malware, and crypto drain sites.

---

## Casino Affiliate Network (305 domains)

`server_fp: 0ab5f121ab0d`

305 casino/gambling domains on identical infrastructure:

`22bet-casino-cz.net`, `7-bit-casino.net`, `7-bit-casino.org`, `argent-reel-casino1.com`, `bdg-win-casino-cz.com`, `best-au-onlinecasino.com`, `betafex.com`, `besovex.com` … (305 total)

Pattern: Country-specific casino affiliate domains registered in bulk.

---

## Turkish Gambling Cluster (161 domains)

`server_fp: 4492f7f3e69c`

Turkish-market gambling domains:

`bahisgiris.icu`, `bahiskorumam.icu`, `bycasino583.com`, `byconticasino.icu`, `casinogiris.icu`, `casinositeleriguncel.icu`, `casinositeleriguncelvip.icu`, `guncelcasinositeleri.icu` … (161 total)

---

## Stake.com Lookalikes (149 domains)

`server_fp: d8c33640a2fc`

149 domains using Stake.com branding or similar crypto gambling:

`stake1208.com`, `stake1305.com`, `stake1307.com`, `stake-go.net`, `stake-planet.net`, `stake-play.net`, `stake-world.net` + `manage-firmware.net`, `de-oc.app`, `captchacore.com`, `stakesdaily.com`

Notable: `manage-firmware.net` (PHISHING_CRYPTO — Ledger firmware scam) shares fingerprint with Stake lookalikes — same operator.

---

## Modafinil Drug Shop (122 domains)

`server_fp: 4b8db6e031cc`

Pharmaceutical/drug sales cluster:

`buymodafinilonline.com`, `freemodafinil.org`, `modafinil-online.com`, `modafinil247.net`, `modafinilbuyonline.com`, `modafinilusa.com`, `modafinilxl.com`, `modalertonline.net` … (122 total)

Online drug shop infrastructure registered through Trustname.com.

---

## Seed Phrase / Credential Harvester Cluster (104 domains)

`server_fp: 24be2aa9d598`

Domains with confirmed data-collection forms:

| Domain | Forms Detected |
|---|---|
| `fragapi.com` | `seed_phrase` ← **CONFIRMED CRYPTO DRAIN** |
| `vichpagereg.com` | `password` |
| `vosturera.com` | `password` |
| `vuapagesu.com` | `password` |
| `vupageinso.com` | `password` |
| `boacux.com` | `password` |

**104 domains total** sharing the same infrastructure fingerprint as `fragapi.com` (confirmed seed phrase harvester).

---

## Binance Phishing Ring (8 domains, same favicon)

`favicon_mmh3: -1851603426`

8 domains with identical Binance-branded favicon:

`binance-as.com`, `binance-bs.com`, `binance-invite.com`, `binance-op.com`, `binance-qw.com`, `binance-ud.com`, `binance-fans.com`, `binance-fly.com`

Same operator registering permutations of `binance-*` across Trustname.com.

---

## Firehouse Subs Brand Impersonation (8 domains, same favicon)

`favicon_mmh3: -1215639649`

8 domains impersonating the Firehouse Subs restaurant chain:

`fiireehousesubs.com`, `fireehouse.com`, `fireehousessubs.com`, `firehausesubs.com`, `fireshousessubbs.com`, `fireshousessubbss.com`, `firehousesubs-coupons.com`, `firehousesubs-deals.com`

Classic brand squatting / coupon scam pattern.

---

## vex/wex Casino Domain Factory (88 domains, same favicon)

`favicon_mmh3: -736095526`

88 domains sharing identical favicon — same operator generated casino template sites:

`gerovex.com`, `hemivex.com`, `kedovex.com`, `kenovex.com`, `wincas.org`, `begowex.com`, `harudex.com`, `keriwex.com` … (88 total)

Naming pattern: `[random][vex|wex|nex|dex].com` — programmatically generated casino brand names.

---

## Buffalo Wild Wings Impersonation (12 domains, same favicon)

`favicon_mmh3: -1638754719`

`bufallowildswing.com`, `bufallowildswings.com`, `bufalosswildswing.com`, `bufalosswildswings.com`, `bufalosswildwing.com`, `bufalosswildwings.com` … (12 total)

Restaurant brand impersonation cluster — coupon/phishing sites.

---

## Multilingual Gambling App Network (8 domains, same day registration)

Registered **2026-05-25**, same Cloudflare IP cluster — 8 language variants of the same gambling app distribution site:

| Domain | Language | IP |
|---|---|---|
| `giochi-apps.bet` | Italian | 188.114.96.3 |
| `jeux-apps.bet` | French | 188.114.96.3 |
| `juegos-apps.bet` | Spanish | 188.114.96.3 |
| `igri-prilozheniya.app` | Russian | 104.21.53.137 |
| `pelit-sovellus.app` | Finnish | 188.114.96.3 |
| `spil-apps.app` | Danish | 104.21.15.69 |
| `hry-aplikace.app` | Czech | 172.67.149.79 |
| `gry-aplikacje.app` | Polish | 172.67.140.154 |

Same operator targeting 8 European markets simultaneously.
