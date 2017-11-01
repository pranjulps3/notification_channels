from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timesince import timesince
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# TODO: Make an activity stream model that keeps notifications and user and time as field and generate them on every
# save event that occurs on any notification.

class Notification(models.Model):
	""" Notification Fields """

	""" Type can be used to group different types of notifications together """
	Type = models.CharField(max_length=255, blank=True, null=True)

	recipient = models.ForeignKey(User, null=False, blank=False, related_name="notifications", on_delete=models.CASCADE)

	""" Generator can be a single person in order to maintain activity stream for a user. """
	generator = models.ManyToManyField(User, related_name='activity_notifications', blank=True)

	""" target of any type can create a notification """
	target_ctype = models.ForeignKey(ContentType, related_name='related_notifications', blank=True, null=True, on_delete=models.CASCADE)
	target_id = models.CharField(max_length=255, blank=True, null=True,)
	target = GenericForeignKey('target_ctype', 'target_id') #change it to manytomany relation for merging similar notification

	""" Action object can be of any type that's related to any certain notification
		for eg. a notification like '<generator> liked your post' has post as action object """
	action_obj_ctype = models.ForeignKey(ContentType, related_name='action_notifications', blank=True, null=True, on_delete=models.CASCADE)
	action_obj_id = models.CharField(max_length=255, blank=True, null=True,)
	action_obj = GenericForeignKey('action_obj_ctype', 'action_obj_id')

	"""" Notification read or not """
	read = models.BooleanField(default=False, blank=False)

	""" Notification seen or not """
	seen = models.BooleanField(default=False, blank=False)

	""" Action verb is the activity that produced the notification
		eg. <generator> commented on <action_obj>
			<description>
		where 'commented on' is an action verb """

	action_verb = models.CharField(max_length=255, default="You recieved a notification.")
	description = models.TextField(null=True, blank=True)

	""" Reference URL points to the web address the notification needs to redirect the recipient to """
	reference_url = models.CharField(max_length=1023, blank=True, null=True, default="#")

	timestamp = models.DateTimeField(auto_now=True)

	def __str__(self):

		timedlta = timesince(self.timestamp, timezone.now())
		count = self.generator.all().count()
		if count == 1:
			gen = self.generator.all()[0].username
		elif count == 2:
			gen = self.generator.all()[0].username + " and " + self.generator.all()[1].username
		elif count == 0:
			gen = ""
		else:
			gen = self.generator.all()[0].username + " , " + self.generator.all()[1].username + " and " + str(count-2) + " others"
		fields = {
			'recipient': self.recipient,
			'generator': gen,
			'action_obj': self.action_obj,
			'target': self.target,
			'action_verb': self.action_verb,
			'timesince': timedlta,
		}

		if self.generator:
			if self.action_obj:
				if self.target:
					return u'%(generator)s %(action_verb)s %(target)s on %(action_obj)s %(timesince)s ago' % fields
				return u'%(generator)s %(action_verb)s %(action_obj)s %(timesince)s ago' % fields
			return u'%(generator)s %(action_verb)s %(timesince)s ago' % fields

		if self.action_obj:
			if self.target:
				return u'%(action_verb)s %(target)s on %(action_obj)s %(timesince)s ago' % fields
			return u'%(action_verb)s %(action_obj)s %(timesince)s ago' % fields
		return u'%(action_verb)s %(timesince)s ago' % fields

	def __unicode__(self):
		return self.__str__(self)


""" Activities are to keep track of user's activity for mergeable and non-mergeable notifications for notification generators """
class Activity(models.Model):
	user = models.ForeignKey(User, null=False, blank=False, related_name="activities", on_delete=models.CASCADE)
	notification = models.ForeignKey(Notification, null=False, blank=False, related_name="activities", on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username+" "+self.user.__str__()

	def __unicode__(self):
		return __str__(self)


from .models import Notification

@receiver(post_save, sender=Notification)
def create_activity(sender, instance, created, **kwargs):
	generators = instance.generator.all()
	for user in generators:
		try:
			activity = Activity.objects.get(user = user, notification = instance)
		except:
			activity = Activity.objects.create(user=user, notification=instance)
			activity.save()
		if not activity:
			activity = Activity.objects.create(user=user, notification=instance)
			activity.save()
	for activ in instance.activities.all():
		print(activ.user not in generators)
		if activ.user not in generators:
			activ.delete()
			activ.save()