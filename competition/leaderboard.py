"""
Simple CLI Leaderboard for Competition
"""
def print_leaderboard(leaderboard):
    print("\n=== Leaderboard ===")
    for rank, (trader_id, pnl) in enumerate(leaderboard, 1):
        print(f"{rank}. {trader_id}: P&L = {pnl:.2f}")
