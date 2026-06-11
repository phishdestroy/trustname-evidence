# GitHub Repository Settings — `trustname-evidence`

Use the values below when configuring the GitHub repository (Settings → General, About sidebar, Topics).

---

## Repository name

```
trustname-evidence
```

## Description (160 chars max — shown in repo header)

```
Phase II evidence package: complete-zone scan of ICANN registrar #4318 Trustname.com / Fewmoretaps OÜ — 7,641 domains, 86% of active content confirmed malicious.
```

*(159 chars — fits the GitHub header field exactly.)*

## Website URL

```
https://phishdestroy.github.io/trustname-evidence/
```

## Topics (GitHub repository tags — paste each separately into the Topics field)

```
phishdestroy
trustname
fewmoretaps
registrar-abuse
icann
icann-4318
iana-4318
bulletproof-registrar
phishing
carding
crypto-drainer
malware
threat-intelligence
threat-hunting
ioc
ioc-feed
blocklist
indicators-of-compromise
estonia
belarus
cybersecurity
osint
forensics
evidence-package
tlp-clear
abuse-reporting
shodan
spamhaus
urlhaus
threatfox
zone-scan
domain-abuse
registrar-zone-analysis
incident-response
```

*(34 topics — GitHub limits to 20 per repo, pick the first 20 if you want the lot. Recommended top-20 in priority order below.)*

## Recommended top-20 Topics

```
phishdestroy
trustname
fewmoretaps
icann
icann-4318
registrar-abuse
bulletproof-registrar
phishing
carding
crypto-drainer
malware
threat-intelligence
ioc
blocklist
estonia
belarus
osint
forensics
zone-scan
evidence-package
```

## "About" section checkboxes

| Setting | Value |
|---|---|
| Use your GitHub Pages website | ✅ checked → `https://phishdestroy.github.io/trustname-evidence/` |
| Releases | ✅ checked |
| Packages | ⬜ unchecked |
| Deployments | ✅ checked (Pages) |

## Social preview image

Upload `docs/assets/og-card.jpg` (1280×720) at
Settings → General → Social preview.

## Pages settings

| Setting | Value |
|---|---|
| Source | Deploy from a branch |
| Branch | `main` |
| Folder | `/docs` |
| Custom domain | *(none — phishdestroy.io is independent)* |
| Enforce HTTPS | ✅ |

## Security & Analysis

| Setting | Value |
|---|---|
| Dependabot alerts | ✅ |
| Secret scanning | ✅ |
| Push protection | ✅ — prevents accidental credential commits |

---

## Release naming convention

```
v1.0.0-phase2 — Phase II Initial Publication (June 2026)
v1.0.1-phase2 — Hotfix: redaction completeness pass
v1.1.0-phase2 — geo-enrichment refresh
v2.0.0-phase2 — Phase II quarterly re-scan
```

## Suggested first GitHub Release notes

```markdown
## Phase II — Initial Publication

This release is the initial public publication of Phase II of the Trustname
investigation. It contains:

- Complete-zone scan of all 7,641 domains under IANA registrar #4318
  (Trustname.com / Fewmoretaps OÜ)
- 1,114 HIGH severity findings · 1,107 MEDIUM severity findings
- 86 % of active-content domains confirmed malicious
- 1,953 forensic screenshots (SHA-256-manifested)
- AI-classified content (Llama 3.1 via Groq)
- Threat-intel cross-reference (Spamhaus DBL · SURBL · URLhaus · ThreatFox)
- Operator-cluster analysis (server fingerprint + favicon MurmurHash3)
- SIEM-ready IOC feed (1,114 HIGH · 2,221 HIGH+MEDIUM)
- Complete provenance documentation (PROVENANCE.md)

**Phase I** (operator profile): https://phishdestroy.io/trustname-bulletproof-exposed/
**Live report**: https://phishdestroy.github.io/trustname-evidence/

License: MIT · TLP:CLEAR
```

---

*PhishDestroy Research · June 2026*
