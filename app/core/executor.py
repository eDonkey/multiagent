from concurrent.futures import ThreadPoolExecutor
from app.core.config import settings

executor = ThreadPoolExecutor(max_workers=settings.MAX_THREADS)
