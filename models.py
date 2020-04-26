from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
#from tinymce.models import HTMLField
from ckeditor_uploader.fields import RichTextUploadingField
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
genders = (
    ("M" , "Male"),
    ("F" , "Female")
)

level_of_teaching = (
    ("O-Level","Ordinary level"),
    ("A-Level","Advanced level"),
    ("Both" , "Both levels")
)


ACCOUNT = (
    ('Student', 'Student'),
    ('Teacher', 'Teacher'),
    ('User', 'User'),
)

CATEGORY_CLASS = (
    ('S1', 'S1'),
    ('S2', 'S2'),
    ('S3', 'S3'),
    ('S4', 'S4'),
    ('S5', 'S5'),
    ('S6', 'S6'),
    
)

CATEGORY_SUBJECTS = (
    ('Mathematics', 'Mathematics'),
    ('Physics', 'Physics'),
    ('Chemistry', 'Chemistry'),
    ('Biology', 'Biology'),
    ('History', 'History'),
    ('Geography', 'Geography'),
    
)

class UserProfile(models.Model):
    #dateofbirth
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    gender = models.CharField(max_length=20,choices=genders)
    location = models.CharField(max_length=30)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    image = models.ImageField()
    role = models.CharField( max_length=8,choices=ACCOUNT,default='User')
    date_of_record = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


# class Users(models.Model): 
#     #username = models.CharField(max_length=30)
#     #password = models.CharField(max_length=30)
#     firstname = models.CharField(max_length=30)
#     lastname = models.CharField(max_length=30)
#     gender = models.CharField(max_length=20,choices=genders)
#     location = models.CharField(max_length=30)
#     telephone = models.CharField(max_length=15)
#     #email = models.EmailField()
#     #user_role = models.CharField( max_length=30 , default="Student")
#     date_of_record = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return self.username

class Subjects(models.Model):
    subject_name = models.CharField(max_length=30)
    subject_image = models.ImageField()
    date_of_record = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.subject_name

class Class_table(models.Model):
    name = models.CharField( max_length=30)

    def __str__(self):
        return self.name



class Topics(models.Model):
    subject = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    #teacher = models.ForeignKey(Teacher_apply)
    class_n = models.ForeignKey(Class_table ,on_delete=models.CASCADE)
    topic_name = models.CharField( max_length=30)
    date_of_record = models.DateTimeField(default=timezone.now)
    #user
    #content

    def __str__(self):
        return self.topic_name
        
class Content(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    topic = models.ForeignKey(Topics,on_delete=models.CASCADE)
    #price = models.IntegerField()
    #discount_price = models.IntegerField(blank=True, null=True)
    class_level = models.ForeignKey(Class_table,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    #label = models.CharField(choices=LABEL_CHOICES, max_length=1 )
    slug = models.SlugField(blank=True, null=True)
    #overview = models.TextField()
    #content = HTMLField()
    content = RichTextUploadingField(blank=True, null=True)
    notes = models.FileField(blank=True, null=True)
    video = models.FileField(blank=True, null=True)

    def __int__(self):
        return self.topic
    
    def get_absolute_url(self):
        return reverse("e_learning:index", args=[str(self.pk)
        ])
    def get_video_url(self):
        return reverse("e_learning:video", args=[str(self.pk)
        ])
    def get_document_url(self):
        return reverse("e_learning:document", args=[str(self.pk)
        ])



class Teacher_apply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    schools_taught = models.CharField( max_length=30)
    user_profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    current_school = models.CharField(  max_length=30)
    level_of_teaching = models.CharField( max_length=30 , choices=level_of_teaching )
    subject_one = models.CharField(max_length=20,choices=CATEGORY_SUBJECTS)
    subject_two = models.CharField(max_length=20,choices=CATEGORY_SUBJECTS)
    Brief_Self_description = models.TextField()
    Age = models.IntegerField()
    date_of_record = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s - %s" % (self.user, self.current_school)
        #return self.current_school



# class Overview(models.Model):
# 	#getting topics
# 	#price
# 	#content
#     subject = models.ForeignKey(Subjects ,on_delete=models.CASCADE)
#     teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     class_n = models.ForeignKey(Class_table ,on_delete=models.CASCADE)
#     over_view = models.TextField()
#     video = models.FileField()
#     date_of_record = models.DateTimeField(default=timezone.now)

#######################################################################################

class Subject_taught(models.Model):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Topics_name(models.Model):
    subject = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    topic_name = models.CharField( max_length=30)
    date_of_record = models.DateTimeField(default=timezone.now)
    #teacher = models.ForeignKey(Teacher_apply)
    #class_n = models.ForeignKey(Class_table ,on_delete=models.CASCADE)

    def __str__(self):
        return self.topic_name

class Subjects_overview(models.Model):
    #duration
    subject = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    class_n = models.ForeignKey(Class_table,on_delete=models.CASCADE)
    teacher =models.ForeignKey(Teacher_apply ,on_delete=models.CASCADE)
    over_view = models.TextField()
    video = models.FileField()
    duration = models.DurationField()
    date_of_record = models.DateTimeField(default=timezone.now)
    price = models.IntegerField()

    def __str__(self):
        return "%s -- %s" % (self.teacher, self.subject)
        #return self.current_school
    
    def get_absolute_url(self):
        return reverse("e_learning:subject_overview", args=[str(self.pk)
        ])

class Subject_class_topic(models.Model):
    subject = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    class_n = models.ForeignKey(Class_table,on_delete=models.CASCADE)
    topic = models.ForeignKey(Topics_name,on_delete=models.CASCADE)

class Subscription(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    subject_overview = models.ForeignKey(Subjects_overview ,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher_apply ,on_delete=models.CASCADE)
    Amount = models.IntegerField()
    date_of_subscription = models.DateTimeField(default=timezone.now)
    date_of_expiry = models.DateTimeField()
    

class S1_Class(models.Model):
    overview = models.ForeignKey(Subjects_overview ,on_delete=models.CASCADE)
    topic = models.ForeignKey(Topics ,on_delete=models.CASCADE)
    content = RichTextUploadingField()
    videos = models.FileField()
    attached_file = models.FileField()

class S2_Class(models.Model):
    overview = models.ForeignKey(Subjects_overview ,on_delete=models.CASCADE)
    topic = models.ForeignKey(Topics ,on_delete=models.CASCADE)
    content = RichTextUploadingField()
    videos = models.FileField()
    attached_file = models.FileField()

class S3_Class(models.Model):
    overview = models.ForeignKey(Subjects_overview ,on_delete=models.CASCADE)
    topic = models.ForeignKey(Topics ,on_delete=models.CASCADE)
    content = RichTextUploadingField()
    videos = models.FileField()
    attached_file = models.FileField()

class S4_Class(models.Model):
    overview = models.ForeignKey(Subjects_overview ,on_delete=models.CASCADE)
    topic = models.ForeignKey(Topics ,on_delete=models.CASCADE)
    content = RichTextUploadingField()
    videos = models.FileField()
    attached_file = models.FileField()

class S5_Class(models.Model):
    overview = models.ForeignKey(Subjects_overview ,on_delete=models.CASCADE)
    topic = models.ForeignKey(Topics ,on_delete=models.CASCADE)
    content = RichTextUploadingField()
    videos = models.FileField()
    attached_file = models.FileField()

class S6_Class(models.Model):
    overview = models.ForeignKey(Subjects_overview ,on_delete=models.CASCADE)
    topic = models.ForeignKey(Topics ,on_delete=models.CASCADE)
    content = RichTextUploadingField()
    videos = models.FileField()
    attached_file = models.FileField()


