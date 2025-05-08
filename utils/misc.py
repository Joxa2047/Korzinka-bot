from config import CURRENCY

def format_price(price):
    """Format price with thousand separators and currency"""
    return f"{price:,} {CURRENCY}"

def is_admin(user_id, admin_ids):
    """Check if user is an admin"""
    return user_id in admin_ids
