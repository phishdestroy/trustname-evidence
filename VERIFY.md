# Verification

This package uses SHA-256 manifests for reproducibility and chain-of-custody
checks.

## Repository Manifest

`SHA256SUMS.txt` contains SHA-256 hashes for committed repository files,
excluding the manifest itself and detached signature files.

Verify on Linux/macOS:

```bash
sha256sum -c SHA256SUMS.txt
```

Verify with PowerShell:

```powershell
Get-Content .\SHA256SUMS.txt | ForEach-Object {
  $hash, $path = $_ -split '  ', 2
  $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToLowerInvariant()
  if ($actual -ne $hash) { throw "hash mismatch: $path" }
}
```

## Screenshot Manifest

`evidence/HASHES.txt` contains SHA-256 hashes for the screenshot archive. The
PNG screenshots are intentionally kept out of normal git commits because of
size. Verify them from whichever screenshot mirror is present:

```bash
cd docs/screenshots
sha256sum -c ../../evidence/HASHES.txt
```

or:

```bash
cd evidence/screenshots
sha256sum -c ../HASHES.txt
```

## Detached Signatures

No private signing key is stored in this repository. For a stronger public
release, sign the release tag and/or the repository manifest after the final
commit:

```bash
git tag -s v2026-06-10 -m "Trustname evidence package, Phase II"
gpg --armor --detach-sign SHA256SUMS.txt
```

Commit only the public signature file, never a private key.
