#!/bin/bash
# GRU Token Deployment Script

set -e

MINT_KEYPAIR="/Users/zak/gru-airdrop-tools/gru_mint_keypair.json"
PAYER_KEYPAIR="/Users/zak/.config/solana/id.json"
MINT_ADDRESS="S782cLXpcS5agE3T6g7ADZ8LkmQsiDMKd7S2GzfGapp"
TOTAL_SUPPLY="1088861984"
DECIMALS=6

echo "=========================================="
echo "GRU TOKEN DEPLOYMENT"
echo "=========================================="
echo ""
echo "Mint Address: $MINT_ADDRESS"
echo "Total Supply: $TOTAL_SUPPLY GRU"
echo "Decimals: $DECIMALS"
echo ""

# Check balance
echo "Checking wallet balance..."
BALANCE=$(solana balance --keypair $PAYER_KEYPAIR | cut -d' ' -f1)
echo "Current balance: $BALANCE SOL"
echo ""

# Step 1: Create token
echo "Step 1: Creating token..."
spl-token create-token \
    --decimals $DECIMALS \
    --mint-authority $PAYER_KEYPAIR \
    --fee-payer $PAYER_KEYPAIR \
    $MINT_KEYPAIR

echo ""

# Step 2: Create token account for payer
echo "Step 2: Creating token account..."
spl-token create-account $MINT_ADDRESS --fee-payer $PAYER_KEYPAIR

echo ""

# Step 3: Mint total supply
echo "Step 3: Minting $TOTAL_SUPPLY GRU..."
spl-token mint $MINT_ADDRESS $TOTAL_SUPPLY --fee-payer $PAYER_KEYPAIR

echo ""
echo "Token created and minted!"
echo ""
echo "Next steps:"
echo "1. Add metadata (name: GRU, symbol: GRU)"
echo "2. Run airdrop script"
echo "3. Create LP pool"
