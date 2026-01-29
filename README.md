# GRU Token Airdrop

Records for the GRU token airdrop following the January 23, 2026 incident.

## What Happened

During a livestream on January 23, 2026, the original GRU token airdrop was broken. A new GRU token was deployed and airdropped to all holders at the exact moment the stream started.

## Airdrop Logic

**Original GRU holders (1:1 ratio)**

If you held the original GRU token (`HXU8HiXKbLmxKjSVdZ97xzCRSLqVDNyAmQnhVLz7pump`) at the snapshot, you received the same amount of new GRU.

**96NbR holders (2:1 ratio)**

If you held 96NbR token at the snapshot, you received 2 GRU for every 1 96NbR held. This ratio was chosen because there was information asymmetry in the 96NbR trade. Holders who swapped into 96NbR did so without full context of the situation, and the 2:1 ratio compensates for that.

**Both tokens**

Wallets holding both tokens received both allocations.

## Token Details

| Field | Value |
|-------|-------|
| Name | GRU |
| Symbol | GRU |
| Mint | [`S782cLXpcS5agE3T6g7ADZ8LkmQsiDMKd7S2GzfGapp`](https://solscan.io/token/S782cLXpcS5agE3T6g7ADZ8LkmQsiDMKd7S2GzfGapp) |
| Decimals | 6 |
| Total Supply | 1,088,861,984 GRU |
| Metadata | [meat.apps.fun](https://meat.apps.fun/tokens/S782cLXpcS5agE3T6g7ADZ8LkmQsiDMKd7S2GzfGapp.json) |

## Liquidity

| Field | Value |
|-------|-------|
| Pool | [Meteora DAMM v2](https://app.meteora.ag/dammv2/4qqBAWTbHd5st8gS5e4ifnsv2ECjLSnyLLG5Bd5Pdptg) |
| Pool Address | `4qqBAWTbHd5st8gS5e4ifnsv2ECjLSnyLLG5Bd5Pdptg` |
| GRU Deposited | 40,000,000 |
| SOL Deposited | ~85 SOL (~$10,500) |
| LP Status | [Permanently locked](https://solscan.io/tx/4xKDEzqg18H82968hmk2DcGzvY8axRpQDzm872P8Gn4pyrgT7mGw1BxGQE3cY7fFRtkojAv1WbVEdAn9aBwibRXv) |
| Mint Authority | [Burned](https://solscan.io/tx/4GCcS91MYL1erGb5JqiZT9zGVWUQNzxZgG2fCbx85p1hVUJJhwbhdougoVq2S6WjTX6mqidcvzHhk9XnQf6LzD5z) |
| Remaining Supply | Burned |

## Airdrop Summary

| Metric | Value |
|--------|-------|
| Total GRU Distributed | 948,059,138 |
| Wallets Received | 1,602 |
| Failed Transfers | 47 (PDAs and invalid accounts) |
| Remediation Transfers | 6 wallets, ~32,561,929 GRU |

## Remediation

The initial filtering logic incorrectly classified some holders as pool accounts. Wallets that traded on DEXes (Meteora, Raydium, Orca) were flagged even when they were legitimate users. Six wallets were verified and sent their allocations before the mint authority was burned.

| Wallet | Amount (GRU) |
|--------|-------------|
| `7wHL61XTMPX9se3f7F9JqoDtXaTMfikx8un8xqj57DjZ` | 13,457,026 |
| `4n4BvbfQL5BjkDXFkbmopEui6pMZWJMG57rbhYRs5oi3` | 8,900,000 |
| `DNJXTT2NytZU5rhwyqz1qsGjaLdShNsBY2hc9drCe32w` | 3,929,993 |
| `DD4XBSq2hQsqndq4qdr162bxs5w1yNNwGaHn4QYHr6en` | 3,002,856 |
| `9N2dwsCjru9F7vxET5fyYvFAMPCpaRcr9zrhs82QtdGG` | 2,611,978 |
| `DJXxXa2XDkctZkcRnwMxxnc9v9v82mERZJkvP3GPW9X1` | 660,076 |

## Final Distribution

| Allocation | Amount |
|------------|--------|
| Airdrop (1,602 wallets) | 948,059,138 |
| Remediation (6 wallets) | 32,561,929 |
| Liquidity Pool | 40,000,000 |
| Burned | Remaining supply |

## Snapshot

| Field | Value |
|-------|-------|
| Block Height | 395457513 |
| Timestamp | 2026-01-23 12:30:00 CST (18:30:00 UTC) |
| Original GRU Holders | 1,788 |
| Final Airdrop List | 1,649 wallets |

## Verify Airdrop

Check if a wallet received the airdrop:

```bash
grep "WALLET_ADDRESS" airdrop_success.csv
```

## Files

| File | Description |
|------|-------------|
| `combined_airdrop_final.csv` | Final airdrop list (1,649 wallets) |
| `airdrop_success.csv` | Completed transfers (1,602 wallets) |
| `airdrop_failed.csv` | Failed transfers (47 wallets) |
| `snapshot_final_HXU8HiXK_1769193000.csv` | Original unfiltered snapshot |
| `96nbr_airdrop_2to1.csv` | 96NbR holder allocations |

## Scripts

| Script | Purpose |
|--------|---------|
| `airdrop_gru.py` | Airdrop execution |
| `deploy_gru.sh` | Token deployment |
| `send_missed.sh` | Remediation transfers |

## Links

- Token: [Solscan](https://solscan.io/token/S782cLXpcS5agE3T6g7ADZ8LkmQsiDMKd7S2GzfGapp)
- Pool: [Meteora](https://app.meteora.ag/dammv2/4qqBAWTbHd5st8gS5e4ifnsv2ECjLSnyLLG5Bd5Pdptg)
- Contact: [@0xzak](https://x.com/0xzak)
