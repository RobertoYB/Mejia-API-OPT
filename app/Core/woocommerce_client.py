from woocommerce import API
from app.Core.config import settings

wcapi = API(
    url=settings.WP_URL,
    consumer_key=settings.WP_CONSUMER_KEY,
    consumer_secret=settings.WP_CONSUMER_SECRET,
    version="wc/v3",
    timeout=20
)