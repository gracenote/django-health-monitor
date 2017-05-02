from health_monitor.views import HealthTestView, HealthAlarmView, HealthView

from .models import BodyHealth, BodyHealthAlarm


class BodyHealthView(HealthView):
    health_model = BodyHealth


class BodyHealthAlarmView(HealthAlarmView):
    health_alarm_model = BodyHealthAlarm


class BodyHealthTestView(HealthTestView):
    pass
