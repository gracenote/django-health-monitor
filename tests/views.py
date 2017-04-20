from health_monitor.views import HealthTestView, HealthView

from .models import BodyHealth


class BodyHealthView(HealthView):
    health_model = BodyHealth


class BodyHealthTestView(HealthTestView):
    pass
