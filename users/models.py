from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

UPLOAD_TO_DIR = 'profilepics/'
FILE_SIZE = 5242880  # 5MB
FILE_TYPE = '.jpg'
GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
)


class Profile(models.Model):

    def validate_file_type(value):
        import os
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.jpg', '.JPG']
        if not ext in valid_extensions:
            raise ValidationError(u'Image type must be jpg file!')

    def validate_file_size(value):
        if value.size > FILE_SIZE:
            raise ValidationError(u'Image size should not exceed 5 MB!')

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birth_date = models.DateField(default='')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    college_name = models.CharField(max_length=50)
    year_of_study = models.PositiveIntegerField(validators=[MaxValueValidator(10)],
                                                choices=[(x, x) for x in range(1, 8)])
    about_me = models.TextField(max_length=250, null=True, blank=True, default='')
    friends = models.ManyToManyField("profile", blank=True)
    profile_pic = models.ImageField(upload_to=UPLOAD_TO_DIR, default='',
                                    validators=[validate_file_type, validate_file_size],
                                    null=True)

    def __str__(self):
        return str(self.user)

    # def save(self, **kwargs):


'''
def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass


post_save.connect(post_save_user_model_receiver, sender=User)
'''


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.course_name


class Degree(models.Model):
    degree_id = models.AutoField(primary_key=True)
    degree_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.degree_name


class UserCourses(models.Model):
    user_id = models.OneToOneField(Profile, on_delete=models.CASCADE)
    course_id = models.ManyToManyField(Course)

    def __str__(self):
        return '{0} courses'.format(str(self.user_id))

    # class Meta:
    #     unique_together = ('user_id', 'course_id',)


class UserDegrees(models.Model):
    user_id = models.OneToOneField(Profile, on_delete=models.CASCADE)
    degree_id = models.ForeignKey(Degree, on_delete=models.CASCADE)

    def __str__(self):
        return '{0}, {1}'.format(str(self.user_id), str(self.degree_id))

    # class Meta:
    #     unique_together = ('user_id', 'degree_id',)


class Privacy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    privacy_first_name = models.BooleanField(default=True)
    privacy_last_name = models.BooleanField(default=True)
    privacy_email = models.BooleanField(default=True)
    privacy_birth_date = models.BooleanField(default=True)
    privacy_gender = models.BooleanField(default=True)
    privacy_college_name = models.BooleanField(default=True)
    privacy_year_of_study = models.BooleanField(default=True)
    privacy_about_me = models.BooleanField(default=True)

    def __str__(self):
        return "privacy {}".format(self.user.username)


class FriendRequest(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')

    def __str__(self):
        return "From {}, To {}".format(self.from_user.username, self.to_user.username)


class Rules(models.Model):
    text_rules = models.TextField(max_length=50000, default="Undefined")

    def __str__(self):
        return '{0}'.format(str(self.text_rules))

