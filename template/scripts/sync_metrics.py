#!/usr/bin/env python3
"""Synchronize current file metadata without changing historical scan findings."""
from collections import Counter
from pathlib import Path
import csv
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[2]


def write_changed(path, text):
    if not path.exists() or path.read_text(encoding='utf-8') != text:
        path.write_text(text, encoding='utf-8', newline='\n')


def domain_count(path):
    return len({line.strip() for line in (ROOT / path).read_text(encoding='utf-8').splitlines() if line.strip()})


def file_size(size):
    return f'{size / 1024**2:.2f} MiB' if size >= 1024**2 else f'{size / 1024:.1f} KiB'


def synchronize():
    index = json.loads((ROOT / 'data/index.json').read_text(encoding='utf-8'))
    csv.field_size_limit(10_000_000)
    with (ROOT / 'data/enriched.csv').open(encoding='utf-8-sig', newline='') as handle:
        rows = list(csv.DictReader(handle))
    severities = Counter(row['severity_label'] for row in rows)
    template = ROOT / 'template/upstream/docs/index.html'
    explorer = (ROOT / 'template/upstream/docs/domains.html').read_text(encoding='utf-8')
    match = re.search(r'window\._INLINE_DATA\s*=\s*', explorer)
    historical = json.JSONDecoder().raw_decode(explorer[match.end():])[0]
    summary = {
        'last_updated': index['last_updated'],
        'domains_tracked': domain_count('data/all.txt'),
        'ioc_classified': domain_count('ioc/domains_all_malicious.txt'),
        'ioc_high': domain_count('ioc/domains_high.txt'),
        'estimated_annual_value': index['total_revenue_estimate'],
        'cumulative_domains_observed': index['total_new_all_time'],
        'dataset_records': len(rows),
        'scan_snapshot_records': len(historical['domains']),
    }
    if summary['domains_tracked'] != index['total_domains']:
        raise ValueError('Current domain list and analytics total disagree')
    write_changed(ROOT / 'docs/current-data.json', json.dumps(summary, indent=2) + '\n')

    paths = [
        'data/enriched.csv', 'data/high_severity.csv', 'data/dead_domains.csv',
        'ioc/domains_high.txt', 'ioc/domains_all_malicious.txt', 'ioc/indicators.csv',
        'evidence/HASHES.txt', 'pkg/raw_data/enriched.csv.gz',
        'pkg/raw_data/lambda_results.jsonl.gz', 'pkg/raw_data/deep_results.jsonl.gz',
        'pkg/raw_data/threat_intel.jsonl.gz', 'docs/data.json',
    ]
    artifacts = {}
    for path in paths:
        raw = (ROOT / path).read_bytes()
        artifacts[path] = (file_size(len(raw)), hashlib.sha256(raw).hexdigest()[:16])

    for filename in ['README.md', 'PROVENANCE.md']:
        path = ROOT / filename
        text = path.read_text(encoding='utf-8')
        # Inventory rows refer to today's downloads, not the June scan totals.
        for asset, (size, digest) in artifacts.items():
            pattern = r'(?m)^(\| [^\n|]*`' + re.escape(asset) + r'` \| )[^|]+\| [^|]+\| (.*) \|$'
            def inventory(match, asset=asset, size=size, digest=digest):
                description = match[2]
                if asset == 'data/enriched.csv':
                    description = f'Full enriched dataset — {len(rows):,} domain records, all columns'
                elif asset == 'docs/data.json':
                    description = f'Current per-domain export — {len(rows):,} records; June 2026 explorer snapshot is separate'
                elif asset == 'ioc/domains_high.txt':
                    description = f'Production blocklist — {summary["ioc_high"]:,} HIGH domains'
                elif asset == 'ioc/domains_all_malicious.txt':
                    description = f'HIGH + MEDIUM blocklist — {summary["ioc_classified"]:,} domains'
                return f'{match[1]}{size} | `{digest}` | {description} |'
            text = re.sub(pattern, inventory, text)
        text = re.sub(r'(# expected prefix: )[0-9a-f]+', lambda m: m[1] + artifacts['pkg/raw_data/enriched.csv.gz'][1], text)
        if filename == 'README.md':
            classifications = ' · '.join(f'{severities[level]:,} {level}' for level in ['HIGH', 'MEDIUM', 'CRITICAL'] if severities[level])
            text = re.sub(r'\([\d,]+ HIGH · [\d,]+ MEDIUM(?: · [\d,]+ CRITICAL)? across [\d,]+ rows\)', f'({classifications} across {len(rows):,} rows)', text)
            text = re.sub(r'(\[`data/enriched.csv`\]\(data/enriched.csv\) )\([\d,]+ rows\)', lambda m: m[1] + f'({len(rows):,} rows)', text)
            text = re.sub(r'(domains_all_malicious\.txt\s+)[\d,]+ HIGH \+ MEDIUM blocklist', lambda m: m[1] + f'{summary["ioc_classified"]:,} HIGH + MEDIUM blocklist', text)
            text = re.sub(r'(domains_high\.txt\s+)[\d,]+ HIGH blocklist', lambda m: m[1] + f'{summary["ioc_high"]:,} HIGH blocklist', text)
            text = re.sub(r'(domains\.html\s+)Searchable[^\n]+', lambda m: m[1] + f'Searchable June 2026 HTTP-scan snapshot ({summary["scan_snapshot_records"]:,} records)', text)
            # This sentence describes the published IOC files, not CSV severity labels.
            text = re.sub(r'(currently lists \*\*)[\d,]+(\*\* domains \(\*\*)[\d,]+(\*\* HIGH, )[\d,]+( MEDIUM\))', lambda m: f'{m[1]}{summary["ioc_classified"]:,}{m[2]}{summary["ioc_high"]:,}{m[3]}{summary["ioc_classified"] - summary["ioc_high"]:,}{m[4]}', text)
        write_changed(path, text)

    text = template.read_text(encoding='utf-8')
    text = re.sub(r'enriched\.csv \([\d,]+(?: records)?\)', f'enriched.csv ({len(rows):,} records)', text)
    text = re.sub(r'domains_high\.txt \([\d,]+\)', f'domains_high.txt ({summary["ioc_high"]:,})', text)
    text = re.sub(r'[\d,]+ HIGH · indicators\.csv', f'{summary["ioc_high"]:,} HIGH · indicators.csv', text)
    write_changed(template, text)
    print(json.dumps(summary))
    return summary


if __name__ == '__main__':
    synchronize()
