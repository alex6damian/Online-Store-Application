import schedule
import time
import django
import os
import sys
from storeapp import tasks
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()

def run_scheduler():
    # Schedule tasks
    schedule.every(30).minutes.do(tasks.delete_inactives) # Delete inactive users
    schedule.every().monday.at("12:00").do(tasks.send_newsletter) # Send newsletter every monday at 12:00
    schedule.every(20).minutes.do(tasks.delete_old_discounts) # Delete old discounts
    schedule.every().friday.at("12:00").do(tasks.send_black_friday) # Send Black Friday promotion every friday at 12:00
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    try:
        run_scheduler()
    except KeyboardInterrupt:
        sys.exit(0)