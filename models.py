from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class ChoreType(models.Model):
    """ master list of chore types """
    description = models.CharField(max_length = 40)
    def __str__(self):
        return self.description

class Chore(models.Model):
    """ an individual chore assigned to the user """
    chore_type = models.ForeignKey(ChoreType)
    description = models.CharField(max_length = 40)
    due_date = models.DateTimeField('due date')
    reward = models.IntegerField(default = 100)
    daily_penalty = models.IntegerField(default = 0)

    assigner = models.ForeignKey(User, related_name="assigner")
    assignee = models.ForeignKey(User, related_name="assignee")

    def __str__(self):
        return self.chore_type.description + ": " + self.description

    def overdue(self):
        if self.completed() or self.due_date > timezone.now():
            return False
        else:
            delta = self.due_date - timezone.now()
            return delta

    def finish(self):
        cl = ChoreLog(chore = self, reward = self.current_reward(), completion_date = timezone.now())
        cl.save()

    def completed(self):
        cl = ChoreLog.objects.filter(chore = self)
        return cl.count() > 0 and cl[0] or False

    def current_reward(self):
        if timezone.now() < self.due_date:
            return self.reward
        delta = timezone.now() - self.due_date
        return max(0, self.reward - self.daily_penalty * delta.days)

class ChoreLog(models.Model):
    """ a log file of chores that have been completed """
    chore = models.ForeignKey(Chore)
    completion_date = models.DateTimeField('completed on')
    reward = models.IntegerField(default = 0)
    notes = models.CharField(max_length = 40)

    def __str__(self):
        return self.chore.description

