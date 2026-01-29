#!/bin/bash
# Send GRU to missed wallets
# 5 legitimate claims verified on-chain

MINT="S782cLXpcS5agE3T6g7ADZ8LkmQsiDMKd7S2GzfGapp"
PAYER="/Users/zak/.config/solana/id.json"

echo "Sending GRU to missed wallets..."
echo ""

# 7wHL61 - owed 13,457,026.445777347
echo "[1/5] 7wHL61XTMPX9se3f7F9JqoDtXaTMfikx8un8xqj57DjZ - 13457026.445777 GRU"
spl-token transfer $MINT 13457026.445777 7wHL61XTMPX9se3f7F9JqoDtXaTMfikx8un8xqj57DjZ --fund-recipient --fee-payer $PAYER --allow-unfunded-recipient

# DNJXTT - owed 3,929,992.947060469
echo "[2/5] DNJXTT2NytZU5rhwyqz1qsGjaLdShNsBY2hc9drCe32w - 3929992.947060 GRU"
spl-token transfer $MINT 3929992.947060 DNJXTT2NytZU5rhwyqz1qsGjaLdShNsBY2hc9drCe32w --fund-recipient --fee-payer $PAYER --allow-unfunded-recipient

# DD4XBS - owed 3,876,943.518708 minus 874,087.922068 already held = 3,002,855.596640
echo "[3/5] DD4XBSq2hQsqndq4qdr162bxs5w1yNNwGaHn4QYHr6en - 3002855.596640 GRU"
spl-token transfer $MINT 3002855.596640 DD4XBSq2hQsqndq4qdr162bxs5w1yNNwGaHn4QYHr6en --fund-recipient --fee-payer $PAYER --allow-unfunded-recipient

# 9N2dws - owed 2,611,978.024123615
echo "[4/5] 9N2dwsCjru9F7vxET5fyYvFAMPCpaRcr9zrhs82QtdGG - 2611978.024123 GRU"
spl-token transfer $MINT 2611978.024123 9N2dwsCjru9F7vxET5fyYvFAMPCpaRcr9zrhs82QtdGG --fund-recipient --fee-payer $PAYER --allow-unfunded-recipient

# DJXxXa - owed 660,076.116528418
echo "[5/5] DJXxXa2XDkctZkcRnwMxxnc9v9v82mERZJkvP3GPW9X1 - 660076.116528 GRU"
spl-token transfer $MINT 660076.116528 DJXxXa2XDkctZkcRnwMxxnc9v9v82mERZJkvP3GPW9X1 --fund-recipient --fee-payer $PAYER --allow-unfunded-recipient

echo ""
echo "Done. Total sent: ~23,661,929 GRU"
