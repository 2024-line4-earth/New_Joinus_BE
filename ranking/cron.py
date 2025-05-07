from .scripts.update_monthly_stats import monthly_stats

def update_stats_cron():
    monthly_stats()