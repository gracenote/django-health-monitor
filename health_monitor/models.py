from django.db import models
from django.utils import timezone
from health_monitor import health_helper
from jsonfield import JSONField


class Health(models.Model):
    uid = models.IntegerField(unique=True, db_index=True, verbose_name="UID")
    state = JSONField(default={}, blank=True, null=True)
    severity = JSONField(default={}, blank=True, null=True)
    change_date = models.DateTimeField(default=None, blank=True, null=True)

    def __unicode__(self):      # For Python 2, use __str__ on Python 3
        return unicode(self.uid)

    def add_state_keys(self, group, test_name):
        # Initialize self.state for group if needed
        if group not in self.state.keys():
            self.state[group] = {}
        # Initialize self.state[group] for test if needed
        if test_name not in self.state[group].keys():
            self.state[group][test_name] = {}

    def update_score(self, test_name, score):
        """Update the health based on the test name and score."""
        now = timezone.now()

        for group in health_helper.get_group_list_for_test(test_name):
            # update score in state dict
            if test_name in health_helper.get_health_keys(group):
                self.add_state_keys(group, test_name)
                # Update score and updated_at
                self.state[group][test_name]['score'] = score
                self.state[group][test_name]['updated_at'] = now
                # update severity
                old_severity = self.severity[group] if group in self.severity.keys() else None
                self.severity[group] = health_helper.calculate_severity(self.state[group])

                if old_severity != self.severity[group]:
                    self.change_date = now
        self.save()
