from .scripts.update_monthly_stats import monthly_stats
from .scripts.reward_top_rankers import reward_top_rankers

def update_stats_cron():
    monthly_stats()

def reward_rankers_cron():
    reward_top_rankers()