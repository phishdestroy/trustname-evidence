<img src="https://capsule-render.vercel.app/api?type=waving&color=0:030810,100:6ea8d7&height=110&fontColor=ffffff&animation=fadeIn&text=Evidence&fontSize=28&desc=Trustname%20Investigation%20%C2%B7%20Evidence%20Artifacts&descAlignY=62&descSize=13" width="100%"/>

# Evidence — Screenshot Chain of Custody

This directory contains the cryptographic provenance for every screenshot captured during the Phase II zone scan.


<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## Contents

| File | Description |
|---|---|
| `screenshots/` | Local/generated 1,953 PNG screenshot archive. Keep out of normal git commits; publish via S3/Git LFS when needed. |
| `HASHES.txt` | SHA-256 hash for every screenshot file, one per line, in `<sha256>  <filename>` format. |


<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## Capture Method

| Parameter | Value |
|---|---|
| Engine | Playwright 1.40 + headless Chromium |
| Stealth | `playwright-stealth` v2 (`Stealth().apply_stealth_async(page)`) |
| Viewport | 1280 × 800 |
| User-Agent | Default Chrome desktop; per-domain rotation in CF deep scan |
| Settle delay | 2.5 s post-`domcontentloaded`; +5 s on Cloudflare JS challenge |
| Captcha solving | 2captcha (hCaptcha, reCAPTCHA v2/v3, Cloudflare Turnstile) |
| Proxy pool | 2,600+ SOCKS5 exits, round-robin |
| Browser context | Isolated per domain (prevents `TargetClosedError` cascade) |


<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## Statistics

| Metric | Value |
|---|---:|
| Total screenshots captured | **1,953** |
| Cloudflare-protected domains in scope | 2,072 |
| CAPTCHAs solved during capture | 92 |
| Capture success rate (alive ∩ rendered) | 75.6 % |
| Average file size | 365 KB |


<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## Naming Convention

Files are named `<domain>.png` — direct 1:1 mapping to the `domain` column of
`../data/enriched.csv`.


<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## Integrity Verification

```bash
# verify the full manifest
cd screenshots && sha256sum -c ../HASHES.txt

# spot-check a single file
sha256sum screenshots/buyclonecards.bond.png
```

`HASHES.txt` is generated deterministically and re-runnable from the
`screenshots/` directory via:

```bash
sha256sum screenshots/*.png > HASHES.txt
```


<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## CAPTCHA-Blocked Domains

Where a domain returned a CAPTCHA that 2captcha could not bridge, the captured
screenshot shows the challenge page itself. Domain classification in these
cases is based on:

1. Domain-name pattern matching against known abuse families.
2. HTTP fingerprint from the Phase 1 Lambda scan.
3. Operator-cluster membership via favicon MurmurHash3 / server fingerprint.

These rows are annotated with `captcha=<type>` in `../data/enriched.csv`.


<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## TLP

TLP:CLEAR — screenshots may be redistributed for research and law-enforcement purposes.

---

*Phase II evidence package — see [`../README.md`](../README.md) for the full investigation.*

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:6ea8d7,100:030810&height=60&section=footer" width="100%"/>
