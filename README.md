# Notification Channels
Notification Channels is a Notification Handler app for Django based web applications. Currently the project has no installation procedure other than cloning the repository and pasting to your existing project. The integration of PyPi setup.py  is in the works.

Notification Channels helps you generate real time notifications related to django's native User model and let's you send push notifications too(coming in future commits). Notification Channels uses Channels app to send real time notifications to the recipients. The setup procedure for Django Channels can be referred to setup your project to start up with Notification Channels.

## Get Started
To setup Notification Channels to your existing projects just clone this repository inside your project and add it to your installed apps.

After this you can add this to your notification div so to check if everything is fine.

```
{% load notif_tags %}
.
.
{% get_all_notifs request.user %}
```

Please note that you need to be logged in as some user to make it work.

## Understanding Notification Channels

Notification Channels is made to track notifications and activities together as Activity Stream. The notification in Notification channels has the following attributes that have been explained briefly.

**`notif_type`** : Type of notification. Type is used to group different notification on the basis of their importance, belonging or behavior.

**`recipient`*** : This will be a Django User type object that represents the user that will be receiving the notification.

**`generator`** : This will be a Django User type object that represents the user that generated the notification.

**`target`** : This can be an object of any type. Target represents the object that is the cause of the notification generation. Like in "Rishi commented on Arun's Post." has comment object as the target.

**`action_obj`** : This can be an object of any type. Action object represents the object that is acted on in the notification. Like in "Rishi commented on Arun's Post." has Arun's  Post object as the Action object.

**`action_verb`*** : This is a text field that represents the verb describing the notification action. Like in "Rishi commented on Arun's Post." has "commented on" as the Action verb.

**`description`** : This is a text field that represents a sentence or two to describe the notification.

**`display_text`** : This is a text field that represents the text to be displayed on the notification bar. When not given this remains blank and an autogenerated text is shown.

**`reference_url`** : This is a text field representing the URL that the user need to be redirected when a click is observed on the notification.

**`timestamp`** : It's an automatic Date Time Field that changes everytime the notification is updated.

**`read`** : It is a boolean Field that tells whether the notification is read by the recipient or not.

**`seen`** : It is a boolean Field that tells whether the notification is seen by the recipient or not.

**`mark_seen()`** : It's a function to mark the current notification as seen.

**`mark_read()`** : It's a function to mark the current notification as read.

*The attributes marked * are required to be passed while creating a notification.*

Here are some examples to make the difference between Action object and Target more clear. 

* "Alice liked your profile picture"

	Here Profile Picture object (if exists) will be the Action object and like object (if exists) will be the Target.

* "Prof. Atul Gupta added new module to Fusion"

	Here Fusion object (if exists) will be the Action object and module object (if exists) will be the Target.

* "Prof. M. K. Bajpai added a new course"

	Here course object (if exists) will be the Action object and Target will be none.
    
These examples should make it clear that Target cannot exist without Action object, at least not in Notification Channels.

Notification Channels provides a unique abstraction of merging similar notifications. It is enabled by default but you can disable it just by adding this to your `settings.py`.

```
ALLOW_NOTIFICATION_MERGE=False
```

Let's take a look at how and when notifications get merged.

* Only Notifications with same `recipient`, `action_verb` and `action_obj` will get merged if they have  different `generators`.

* Notifications with same `action_obj` but different `target` would not get merged.

* Notifications without `target` can get merged if they follow all other constraints.

Now Let's take some examples of creating simple notifications.

* A basic notification
	
    ```
    from notification_channels.models import Notification
    .
    .
    .
    n = Notification.objects.create(recipient=user, action_verb="You have new notification")
    ```
    Output
    ```
    >> <Notification: user You have new notification>
    ```
    
    
* A Complex Notification
	
    ```
    n = Notification.objects.create(recipient=user1, generator=user2, action_verb="commented on", action_obj=post, target=comment)
    ```
    Output
    ```
    >> <Notification: user2 commented on post with comment>
    ```
    
* Merging Notification
	
    ```
    n = Notification.objects.create(recipient=user1, generator=user2, action_verb="commented on", action_obj=post)
    n = Notification.objects.create(recipient=user1, generator=user3, action_verb="commented on", action_obj=post)

    ```
    Output
    
 	```
    >> <Notification: user2 and user3 commented on post>
	```
    
    
Merging two or more notifications helps improve time to load all notifications and makes more sense. 

Merging two or more notifications in Notification Channels with different generators creates Activity objects for both the generators. The Activity object is created for a single generator too. The Activity object can be accessed to get information about the actions performed by any user and create an Activity stream accordingly. It's up to you to decide.  We will talk about this more later in the doc.

### Accessibility

You can directly access the Activity objects and the Notifications related to any particular user by using the accessor below.

`user.notifications.all()`

similarly for Activities

`user.activities.all()`


From a Notification object you can access the activities by

`notif.activities.all()`

As generators is a Django's ManyToManyField, to get all generators you can just use

`notif.generator.all()`

To access all notification objects related to any user's activities you can directly access by writing

`user.activity_notifications.all()`

To access all notifications for an object where it has been the `action_obj` you can write

`object.action_notifications.all()`

To access all notifications for an object where it has been the `target` you can write

`object.related_notifications.all()`



### Discarding notifications

Deleting notifications is easy in Notification Channels. You just need to write

`Notification.objects.discard(**kwargs)`

Note that kwargs must contain all fields required to get a unique notification instance or else it will throw an error.
It's important that you use `discard()` function instead of `delete()` to remove notifications as for the merged notifications, deleting it could cost permanent loss of some data. `discard()` function takes care of such situations and in all others deletes the notification along with its activity object(if any).

### Activity Class

Here I will briefly describe the Activity class attributes so that you can manipulate them the way you want.

**`user`** : This is a Django User type object representing the generator part of the notification of which the activity is.

**`notification`** : This gives the notification object for the current activity.

**`timestamp`** : This is a Date Time Field storing the instance when the activity was created.

**`seen`** : This is a boolean field representing wheather the part of the notification generated by the user is seen or not.

**`read`** : This is a boolean field representing wheather the part of the notification generated by the user is read or not.


# Upcoming Features

* Support for real time notification to the recipient.
* Push notification subscription and sending for subscribed users.

# Contribute

If you feel you can make this project better by then feel free to contribute. 
There are currently no hard guidelines to follow as such but it would be a good practice to follow the basic python development conventions. To contribute 
* Create an issue on this repository.
* Fork the project.
* Start coding and send a Pull request.