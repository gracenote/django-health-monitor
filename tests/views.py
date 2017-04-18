from health_monitor.views import HealthView

from .models import BodyHealth


class BodyHealthView(HealthView):
    health_model = BodyHealth
