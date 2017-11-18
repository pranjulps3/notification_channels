from .models import Notifications
from django.contrib.auth.models import User
from django.conf import settings


""" notify takes arguments of notification values and returns the notification object """


def notify(recipient, action_verb, **kwargs):
	notif_type = kwags.pop(notif_type, "")
	generator = kwags.pop(generator, None)
	target = kwags.pop(target, None)
	action_obj = kwags.pop(action_obj, None)
	description = kwags.pop(description, "")
	url = kwags.pop(url, "#")
	""" Notifications to a recipient will get merged when the action_obj, target and action_verb
		all are same for the notifications. In the case of merge url and description for the more
		recent notification will be ignored. """
	if getattr(settings, "ALLOW_NOTIFICATION_MERGE", True):
		try:
			notif = Notification.objects.get(
					recipient=recipient,
					target=target,
					action_obj=action_obj,
					action_verb=action_verb
					)
		except:
			notif = Notification.objects.create(
					notif_type=notif_type,
					recipient=recipient,
					target=target,
					action_obj=action_obj,
					url=url,
					description=description
					)
	else:
		notif = Notification.objects.create(
				notif_type=notif_type,
				recipient=recipient,
				target=target,
				action_obj=action_obj,
				url=url,
				description=description
				)
	if generator:
		notif.generator.add(generator)
	notif.save()
	return notif
	




	