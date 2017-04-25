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
from jsonfield import JSONField
import pytz

from django.db import models
from django.utils import timezone

from . import utils


class Health(models.Model):
    uid = models.IntegerField(primary_key=True, db_index=True)
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

    def update_score(self, test, score):
        """Update the health based on the test name and score."""
        for group in HealthTest._get_groups(test):
            if test in HealthTest._get_tests(group):
                if group not in self.state.keys():
                    self.state[group] = {}
                self.state[group] = utils.init_score_dict(self.state[group], test)
                self.state[group][test] = utils.update_score_dict(self.state[group][test], score)
                self.severity = utils.init_score_dict(self.severity, group)
                self.severity[group] = utils.update_score_dict(self.severity[group], self._calculate_severity(group))
        self.save()

    def delete_test(self, test):
        """Delete test from all groups."""
        for group in self.state.keys():
            if test in self.state[group].keys():
                del(self.state[group][test])
                self.severity[group] = utils.update_score_dict(self.severity[group], self._calculate_severity(group))
        self.save()

    def delete_group(self, group):
        """Delete group from state and severity."""
        del(self.state[group])
        del(self.severity[group])
        self.save()

    def delete_group_test(self, group, test):
        """Delete test from specified group."""
        if test in self.state[group].keys():
            del(self.state[group][test])
            self.severity[group] = utils.update_score_dict(self.severity[group], self._calculate_severity(group))
        self.save()

    class Meta(object):
        abstract = True


class HealthTest(models.Model):
    uid = models.IntegerField(db_index=True)
    time = models.DateTimeField()

    test = None
    groups = []
    health_model = Health

    def __unicode__(self):      # For Python 2, use __str__ on Python 3
        return unicode(self.uid)

    @classmethod
    def create(cls, uid, **kwargs):
        health_test = cls(uid=uid, time=timezone.now(), **kwargs)
        health_test.save()

        h, _ = cls.health_model.objects.get_or_create(uid=uid)
        h.update_score(test=cls.test, score=cls.get_score(**kwargs))

        return health_test

    @classmethod
    def get_score(cls, **kwargs):
        score = cls.score(**kwargs)
        if type(score) != int:
            raise TypeError('score method should return an integer')
        elif score < 0:
            raise ValueError('score method should return a positive integer')
        else:
            return score

    @classmethod
    def get_history(cls, uids, start_time=timezone.datetime.min.replace(tzinfo=pytz.UTC), end_time=timezone.datetime.max.replace(tzinfo=pytz.UTC)):
        return cls.objects.filter(uid__in=uids, **{'time__range': (start_time, end_time)})

    @staticmethod
    def _get_tests(group=None):
        if not group:
            return [t.test for t in HealthTest.__subclasses__()]
        return [t.test for t in HealthTest.__subclasses__() if group in t.groups]

    @staticmethod
    def _get_groups(test):
        for t in HealthTest.__subclasses__():
            if test == t.test:
                return t.groups
        return []

    @staticmethod
    def _get_model(test):
        for t in HealthTest.__subclasses__():
            if test == t.test:
                return t
        raise TypeError('test {} does not exist'.format(test))

    class Meta(object):
        abstract = True
