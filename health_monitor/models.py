"""
   Copyright 2017 Gracenote

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from django.db import models
from jsonfield import JSONField

from health_monitor import scoring_helper, utils


class Health(models.Model):
    uid = models.CharField(primary_key=True, db_index=True, max_length=64, verbose_name="UID")
    state = JSONField(default={}, blank=True, null=True)
    severity = JSONField(default={}, blank=True, null=True)

    def __unicode__(self):      # For Python 2, use __str__ on Python 3
        return unicode(self.uid)

    def _calculate_severity(self, g):
        """Return the highest score in state dict."""
        test_scores = [1, ]
        for t in self.state[g].keys():
            if self.state[g][t]['score']:
                test_scores.append(self.state[g][t]['score'])

        return max(test_scores)

    def update_score(self, test_name, score):
        """Update the health based on the test name and score."""
        for group in scoring_helper.get_group_list_for_test(test_name):
            if test_name in scoring_helper.get_health_keys(group):
                if group not in self.state.keys():
                    self.state[group] = {}
                self.state[group] = utils.init_score_dict(self.state[group], test_name)
                self.state[group][test_name] = utils.update_score_dict(self.state[group][test_name], score)
                self.severity = utils.init_score_dict(self.severity, group)
                self.severity[group] = utils.update_score_dict(self.severity[group], self._calculate_severity(group))
        self.save()

    def delete_test_state(self, test_name):
        """Delete test state"""
        for group in self.state.keys():
            if test_name in self.state[group].keys():
                del(self.state[group][test_name])
                self.severity[group] = utils.update_score_dict(self.severity[group], self._calculate_severity(group))
        self.save()
