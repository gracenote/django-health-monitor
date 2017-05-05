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
    history = JSONField(default={}, blank=True, null=True)

    def __unicode__(self):      # For Python 2, use __str__ on Python 3
        return unicode(self.uid)

    def _calculate_severity(self, group):
        """Return a severity calculation (i.e. highest score in state dict) of a group.

        Arguments:
        g -- group
        """
        test_scores = [1, ]
        for t in self.state[group].keys():
            if self.state[group][t]['score']:
                test_scores.append(self.state[group][t]['score'])

        return max(test_scores)

    def update_score(self, test, score):
        """Update the health state, health severity, and health history based on the test name and score.

        Arguments:
        test  -- test
        score -- score
        """

        # update state and severity
        for group in HealthTest._get_groups(test):
            if test in HealthTest._get_tests(group):
                if group not in self.state.keys():
                    self.state[group] = {}
                self.state[group] = utils.init_score_dict(self.state[group], test)
                self.state[group][test] = utils.update_score_dict(self.state[group][test], score)
                self.severity = utils.init_score_dict(self.severity, group)
                self.severity[group] = utils.update_score_dict(self.severity[group], self._calculate_severity(group))

        # update history
        if test not in self.history.keys():
            self.history[test] = [score]
        else:
            self.history[test] = utils.push_pop_deque(score, self.history[test])

        self.save()

    def delete_test(self, test):
        """Delete test from all groups in health state and update health severity."""
        for group in self.state.keys():
            if test in self.state[group].keys():
                del(self.state[group][test])
                self.severity[group] = utils.update_score_dict(self.severity[group], self._calculate_severity(group))
        self.save()

    def delete_group(self, group):
        """Delete group from health state and severity."""
        del(self.state[group])
        del(self.severity[group])
        self.save()

    def delete_group_test(self, group, test):
        """Delete test entry from specified group within health state and update severity."""
        if test in self.state[group].keys():
            del(self.state[group][test])
            self.severity[group] = utils.update_score_dict(self.severity[group], self._calculate_severity(group))
        self.save()

    def get_latest_scores(self, test, repetition):
        """Get latest x scores from HealthTest historical records where x is the number of repetitions."""
        test_model = HealthTest._get_model(test)
        return [x.get_score() for x in test_model.objects.filter(uid=self.uid).order_by('-time')[:repetition]]

    def get_history(self, test, repetition):
        """Return the cached x test scores or retrieve from historical records where x is the number of repetitions."""
        try:
            if not len(self.history[test]) >= repetition:
                raise Exception
        except Exception:
            self.history[test] = self.get_latest_scores(test, repetition)
            self.save()
        return self.history[test][0:repetition]

    class Meta(object):
        abstract = True


class HealthAlarm(object):
    @classmethod
    def _get_associated_healths(cls, group, test):
        """Return a subset of healths that contain the nested group and test key."""
        healths = []
        for health in cls.health_model.objects.all():
            if group in health.state.keys():
                if test in health.state[group].keys():
                    healths.append(health)

        return healths

    @classmethod
    def calculate_alarms(cls, group, test, score, aggregate_percent=0, repetition=1, repetition_percent=100, **kwargs):
        """Return a list of asset uids based off of filtering criteria.

        Arguments:
        group              -- group name
        test               -- test name
        score              -- minimum score to tigger an alarm
        aggregate_percent  -- minimum percentage of test failures to trigger an alarm
        repetition         -- minimum number of test failures in a row to trigger an alarm
        repetition_percent -- minimum percentage of failures within repetition to trigger an alarm
        """
        healths = cls._get_associated_healths(group, test)

        # step 1: filter failing assets by score, if repetition is less than 100%, all healths must be checked
        if repetition == 100:
            failing_healths_by_score = [x for x in healths if x.state[group][test]['score'] >= score]
        else:
            failing_healths_by_score = healths

        # step 2: filter failing assets by repetition criteria
        failing_healths = []
        for health in failing_healths_by_score:
            score_history = health.get_history(test, repetition)
            if (100 * len([x for x in score_history if x >= score]) / len(score_history)) >= repetition_percent:
                failing_healths.append(health)

        # step 3: return empty array if percentage of failing assets is below aggregate_percent
        if (len(failing_healths) / len(healths)) < (aggregate_percent / 100):
            return []
        else:
            return [x.uid for x in failing_healths]


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
        h.update_score(test=cls.test, score=cls.calculate_score(**kwargs))

        return health_test

    @classmethod
    def calculate_score(cls, **kwargs):
        """Returns the score calculated from derived class' score() method and inputted kwargs."""
        score = cls.score(**kwargs)
        if type(score) != int:
            raise TypeError('score method should return an integer')
        elif score < 0:
            raise ValueError('score method should return a positive integer')
        else:
            return score

    def get_score(self):
        """Returns the score calculated using self.calculate_score() and instance attributes (db columns)."""
        kwargs = {x.name: getattr(self, x.name) for x in type(self)._meta.fields}
        return type(self).calculate_score(**kwargs)

    @classmethod
    def get_history(cls, uids, start_time=timezone.datetime.min.replace(tzinfo=pytz.UTC), end_time=timezone.datetime.max.replace(tzinfo=pytz.UTC)):
        """Returns historical test results.

        Arguments:
        uids       -- a list of uids
        start_time -- a datetime object
        end_time   -- a datetime object
        """
        return cls.objects.filter(uid__in=uids, **{'time__range': (start_time, end_time)})

    @staticmethod
    def _get_tests(group=None):
        """Return list of test names associated with a group."""
        if not group:
            return [t.test for t in HealthTest.__subclasses__()]
        return [t.test for t in HealthTest.__subclasses__() if group in t.groups]

    @staticmethod
    def _get_groups(test):
        """Return a list of group names that a test belongs to."""
        for t in HealthTest.__subclasses__():
            if test == t.test:
                return t.groups
        return []

    @staticmethod
    def _get_model(test):
        """Return the model associated with a test."""
        for t in HealthTest.__subclasses__():
            if test == t.test:
                return t
        raise TypeError('test {} does not exist'.format(test))

    class Meta(object):
        abstract = True
