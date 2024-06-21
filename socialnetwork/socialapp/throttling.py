from rest_framework.throttling import BaseThrottle
from django.core.cache import cache
from datetime import datetime, timedelta

class UserRateThrottle(BaseThrottle):
    scope = 'friend_request'

    def allow_request(self, request, view):
        # Limit: 3 requests per minute
        throttle_rate = (3, 60)  # (num_requests, duration_in_seconds)
        num_requests, duration = throttle_rate
        self.key = self.get_cache_key(request, view)
        history = cache.get(self.key, [])
        now = datetime.now()

        # Remove expired requests from history
        while history and history[-1] <= now - timedelta(seconds=duration):
            history.pop()

        if len(history) >= num_requests:
            return False

        # Add current request timestamp to history
        history.insert(0, now)
        cache.set(self.key, history, duration)
        return True

    def wait(self):
        history = cache.get(self.key, [])
        if history:
            remaining_duration = (history[-1] + timedelta(seconds=60)) - datetime.now()
            return remaining_duration.total_seconds()
        return 0

    def get_cache_key(self, request, view):
        # Generate a unique cache key based on the user and view
        return f'throttle_{self.scope}_{request.user.pk}'
