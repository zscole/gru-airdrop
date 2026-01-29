#!/usr/bin/env python3
"""
GRU Token Airdrop Script
Airdrops GRU tokens to all recipients in combined_airdrop_final.csv

Features:
- Auto-resume: Automatically skips already completed transfers
- Checkpoint: Saves progress after each successful transfer
- Retry failed: Can retry only failed transfers

Usage:
    python3 airdrop_gru.py --dry-run          # Test without sending
    python3 airdrop_gru.py                    # Execute airdrop (auto-resumes)
    python3 airdrop_gru.py --retry-failed     # Retry only failed transfers
    python3 airdrop_gru.py --reset            # Reset progress and start fresh
"""

import csv
import subprocess
import sys
import time
import argparse
import os
import json

MINT_ADDRESS = "S782cLXpcS5agE3T6g7ADZ8LkmQsiDMKd7S2GzfGapp"
AIRDROP_FILE = "/Users/zak/gru-airdrop-tools/combined_airdrop_final.csv"
PAYER_KEYPAIR = "/Users/zak/.config/solana/id.json"
CHECKPOINT_FILE = "/Users/zak/gru-airdrop-tools/airdrop_checkpoint.json"
FAILED_FILE = "/Users/zak/gru-airdrop-tools/airdrop_failed.csv"
SUCCESS_FILE = "/Users/zak/gru-airdrop-tools/airdrop_success.csv"
DECIMALS = 6


def load_checkpoint():
    """Load checkpoint with completed wallets."""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r') as f:
            return json.load(f)
    return {"completed": set(), "last_index": 0}


def save_checkpoint(completed_wallets, last_index):
    """Save checkpoint to file."""
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump({
            "completed": list(completed_wallets),
            "last_index": last_index
        }, f)


def load_completed_from_success():
    """Load completed wallets from success file."""
    completed = set()
    if os.path.exists(SUCCESS_FILE):
        with open(SUCCESS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                completed.add(row['wallet_address'])
    return completed


def run_command(cmd, dry_run=False):
    """Run a shell command and return output."""
    if dry_run:
        print(f"  [DRY RUN] Would execute: {' '.join(cmd)}")
        return True, ""

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            return False, result.stderr.strip()
        return True, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)


def transfer_tokens(recipient, amount_ui, dry_run=False):
    """Transfer tokens to a recipient."""
    cmd = [
        "spl-token", "transfer",
        MINT_ADDRESS,
        str(amount_ui),
        recipient,
        "--fund-recipient",
        "--fee-payer", PAYER_KEYPAIR,
        "--allow-unfunded-recipient"
    ]
    return run_command(cmd, dry_run)


def load_recipients(filepath):
    """Load recipients from CSV file."""
    recipients = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            recipients.append({
                'wallet': row['wallet_address'],
                'amount_raw': int(row['amount_raw']),
                'amount_ui': float(row['amount_ui'])
            })
    return recipients


def load_failed():
    """Load failed transfers from file."""
    failed = []
    if os.path.exists(FAILED_FILE):
        with open(FAILED_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                failed.append({
                    'wallet': row['wallet_address'],
                    'amount_ui': float(row['amount_ui'])
                })
    return failed


def main():
    parser = argparse.ArgumentParser(description='GRU Token Airdrop')
    parser.add_argument('--dry-run', action='store_true', help='Test without sending')
    parser.add_argument('--retry-failed', action='store_true', help='Retry only failed transfers')
    parser.add_argument('--reset', action='store_true', help='Reset progress and start fresh')
    parser.add_argument('--batch-pause', type=int, default=50, help='Pause after N transfers')
    parser.add_argument('--yes', action='store_true', help='Skip confirmation prompt')
    args = parser.parse_args()

    # Reset if requested
    if args.reset:
        for f in [CHECKPOINT_FILE, FAILED_FILE, SUCCESS_FILE]:
            if os.path.exists(f):
                os.remove(f)
                print(f"Removed {f}")
        print("Progress reset. Run again to start fresh.")
        sys.exit(0)

    # Verify files exist
    if not os.path.exists(AIRDROP_FILE):
        print(f"Error: Airdrop file not found: {AIRDROP_FILE}")
        sys.exit(1)

    if not os.path.exists(PAYER_KEYPAIR):
        print(f"Error: Payer keypair not found: {PAYER_KEYPAIR}")
        sys.exit(1)

    # Load recipients or failed list
    if args.retry_failed:
        recipients = load_failed()
        if not recipients:
            print("No failed transfers to retry.")
            sys.exit(0)
        # Clear failed file for fresh retry tracking
        if os.path.exists(FAILED_FILE):
            os.remove(FAILED_FILE)
        print(f"Retrying {len(recipients)} failed transfers...")
        completed_wallets = set()
    else:
        recipients = load_recipients(AIRDROP_FILE)
        # Load already completed wallets
        completed_wallets = load_completed_from_success()

    total = len(recipients)
    total_amount = sum(r['amount_ui'] for r in recipients)

    # Count pending
    pending = [r for r in recipients if r['wallet'] not in completed_wallets]
    pending_count = len(pending)
    already_done = total - pending_count

    print("=" * 60)
    print("GRU TOKEN AIRDROP")
    print("=" * 60)
    print(f"Mint: {MINT_ADDRESS}")
    print(f"Total recipients: {total}")
    print(f"Already completed: {already_done}")
    print(f"Pending: {pending_count}")
    print(f"Total amount: {total_amount:,.2f} GRU")
    print(f"Dry run: {args.dry_run}")
    print("=" * 60)
    print()

    if pending_count == 0:
        print("All transfers already completed!")
        sys.exit(0)

    if not args.dry_run:
        # Check balance
        result = subprocess.run(
            ["solana", "balance", "--keypair", PAYER_KEYPAIR],
            capture_output=True, text=True
        )
        print(f"Payer SOL balance: {result.stdout.strip()}")

        # Check token balance
        result = subprocess.run(
            ["spl-token", "balance", MINT_ADDRESS],
            capture_output=True, text=True
        )
        print(f"GRU token balance: {result.stdout.strip()}")
        print()

        if not args.yes:
            confirm = input("Proceed with airdrop? (yes/no): ")
            if confirm.lower() != 'yes':
                print("Aborted.")
                sys.exit(0)

    # Open output files
    failed_f = open(FAILED_FILE, 'a', newline='')
    success_f = open(SUCCESS_FILE, 'a', newline='')
    failed_writer = csv.writer(failed_f)
    success_writer = csv.writer(success_f)

    # Write headers if files are new
    if not os.path.exists(FAILED_FILE) or os.path.getsize(FAILED_FILE) == 0:
        failed_writer.writerow(['wallet_address', 'amount_ui', 'error'])
    if not os.path.exists(SUCCESS_FILE) or os.path.getsize(SUCCESS_FILE) == 0:
        success_writer.writerow(['wallet_address', 'amount_ui'])

    success_count = 0
    fail_count = 0
    session_count = 0

    for i, recipient in enumerate(recipients):
        wallet = recipient['wallet']
        amount = recipient['amount_ui']

        # Skip already completed
        if wallet in completed_wallets:
            continue

        session_count += 1
        print(f"[{already_done + session_count}/{total}] {wallet[:20]}... {amount:,.2f} GRU", end=" ")

        success, error = transfer_tokens(wallet, amount, args.dry_run)

        if success:
            print("OK")
            success_count += 1
            completed_wallets.add(wallet)
            if not args.dry_run:
                success_writer.writerow([wallet, amount])
                success_f.flush()
                # Save checkpoint every 10 successful transfers
                if success_count % 10 == 0:
                    save_checkpoint(completed_wallets, i)
        else:
            print(f"FAILED: {error[:60]}")
            fail_count += 1
            if not args.dry_run:
                failed_writer.writerow([wallet, amount, error])
                failed_f.flush()

        # Rate limiting
        if not args.dry_run:
            time.sleep(0.3)

        # Batch pause
        if session_count % args.batch_pause == 0 and not args.dry_run:
            save_checkpoint(completed_wallets, i)
            print(f"\n--- Checkpoint saved. Session: {success_count} success, {fail_count} failed ---")
            print(f"--- Total progress: {already_done + success_count}/{total} ({(already_done + success_count)*100//total}%) ---\n")
            time.sleep(1)

    failed_f.close()
    success_f.close()

    # Final checkpoint save
    if not args.dry_run:
        save_checkpoint(completed_wallets, total)

    print()
    print("=" * 60)
    print("AIRDROP SESSION COMPLETE")
    print("=" * 60)
    print(f"This session - Success: {success_count}, Failed: {fail_count}")
    print(f"Total progress: {already_done + success_count}/{total}")
    if fail_count > 0:
        print(f"Run with --retry-failed to retry failed transfers")


if __name__ == "__main__":
    main()
