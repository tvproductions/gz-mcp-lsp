# T8 guarded filesystem transactions â€” 2026-11-01

The user authorized T8 only and requested a stop at its completion. Base:
22fb1ddb9af949aba9a3a91d23cd4ef522ad7d0f on feat/reference-parity.
The transaction adapter is internal; no MCP mutation tools or production startup
recovery were added. Those remain T9.

Transactions owns an operator-private outside-source directory, single-writer
lock, same-filesystem before/after images, journal transitions and durable
receipts. Targets use pinned directory descriptors and no-follow opens.
All targets are preflighted before staging/replacement. Each replacement
rechecks exact bytes, identity and mode after persisting intent. Rollback restores
only the adapter's own matching postimages; external changes are preserved and
return per-file recovery_required status with mutation lockout. Receipts include
before/after/restore identities and survive expiry/session replacement.

Eight initial Linux assertions failed before the adapter existed. Additional
source-change-after-intent and malformed-receipt tests reproduced defects before
their fixes. All 16 T8 tests now pass on native Linux x86_64; disposable workers
exit with code 73 at prepared, replacement intent, replacement, replaced,
rolling-back, restore intent, restored, rolled-back, committed and receipt
boundaries. An unpublished journal fails closed. Recovery never replays an
incomplete transaction; committed retries perform no source replacement.
Tests check exact bytes, modes, external-writer preservation, lock exclusion,
hardlinks, parent symlink swaps, quota, corrupt state and no-op inode preservation.

Both complete local Windows and native Linux gates passed: locked all-group sync,
the four pre-commit hooks, source build and outside-checkout distribution check.
C901 source checks at 20 and ty pass. Windows executes the explicit disabled/
unsupported denial, creates no state and changes no source; the 15 POSIX-only
tests are not applicable there. The full suite discovers 130 tests.

## Portability decisions and limits

- _posix_files.py isolates syscall/ABI handling from the transaction state machine;
  neither imports SDK or LSP code.
- Fail closed on unverified filesystems. Initial local type allowlist is Linux
  ext4/XFS/Btrfs and macOS APFS/HFS. State and sources must share a device.
  Linux statfs and Darwin statfs64 layouts follow their platform headers.
- Regular files use fsync (plus F_FULLFSYNC on macOS); directories use fsync.
  Missing required primitives fail supported lanes rather than skipping tests.
- Conservative quota reservation includes images and temporary metadata. Receipts
  are retained until explicit operator acknowledgment/cleanup; this adapter has
  no cleanup API. State exhaustion rejects new writes.
- Crash injection exists only in disposable test subclasses. These establish
  process-crash recovery, not power-loss certification or cross-file atomicity.
- A quiescent workspace is required; independent writers are not serialized by
  this private adapter lock. Recovery preserves detected external changes.
- Unsafe/corrupt unidentifiable metadata leaves operator recovery required;
  source-free generic status is used when trustworthy file identities are absent.

Hosted macOS arm64 safety remains pending at this checkpoint. T8 closes only after
both supported write lanes pass on the actual candidate. W4/W6/W7 also contain
T9 production coordination/startup requirements; these are not claimed here.
The remaining cognitive qualification/native-host/final milestone gaps persist.
