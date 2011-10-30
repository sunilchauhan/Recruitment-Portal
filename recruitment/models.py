from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save

media_url=settings.MEDIA_URL


fs = FileSystemStorage()

"""Model to store Job details

"""
class job_detail(models.Model):
    job_title = models.CharField(max_length=30,blank=True,default=None)
    department=models.CharField(max_length=30,blank=False)
    designation=models.CharField(max_length=30,blank=False)
    opening_date=models.DateField()
    closing_date=models.DateField()
    number_of_positions=models.CharField(max_length=30,blank=False)
    job_opening_status=models.CharField(max_length=30,blank=False)
    country=models.CharField(max_length=30,blank=True,default=None)
    location_name=models.CharField(max_length=30,blank=True,default=None)
    min_experience=models.CharField(max_length=30,blank=True,default=None)
    max_experience=models.CharField(max_length=30,blank=True,default=None)
    skill_set=models.TextField(blank=True,default=None)
    roles_and_responsibilities=models.TextField(blank=True,default=None)
    job_type=models.CharField(max_length=30,blank=False)
    validity=models.CharField(max_length=30,blank=True,default=None)
    
"""Model to store Candidate information.

"""
class candidate_detail(models.Model):
    first_name=models.CharField(max_length=30,blank=False)
    last_name=models.CharField(max_length=30,blank=False)
    contact_number=models.CharField(max_length=30,blank=False)
    email_address=models.EmailField(blank=False)
    applied_for=models.CharField(max_length=30,blank=False)
    passport_number=models.CharField(max_length=30,null=True,default='None')
    contact_address=models.TextField(null=True,default='None')
    hr_name=models.CharField(max_length=30,null=True,default='None')
    reference_type=models.CharField(max_length=30,null=True,default='None')
    referral_name=models.CharField(max_length=30,null=True,default='None')
    work_experience_years=models.CharField(max_length=30,null=True,default='None')
    work_experience_months=models.CharField(max_length=30,null=True,default='None')
    current_ctc=models.CharField(max_length=30,null=True,default='None')
    expected_ctc=models.CharField(max_length=30,null=True,default='None')
    qualification=models.CharField(max_length=30,null=True,default='None')
    institute_name=models.CharField(max_length=40,null=True,default='None')
    year_of_passing=models.CharField(max_length=30,null=True,default='None')
    percentage=models.CharField(max_length=30,null=True,default='None')
    special_achievement=models.CharField(max_length=40,null=True,default='None')
    resume=models.FileField(upload_to='resume') 
    skill_set=models.TextField(null=True,default='None')
    validity=models.CharField(max_length=30,null=True,default='None')
    stage=models.CharField(max_length=30)
    status=models.CharField(max_length=30)
    level1_interviewer=models.CharField(max_length=30)
    level2_interviewer=models.CharField(max_length=30)
    level3_interviewer=models.CharField(max_length=30)
    level4_interviewer=models.CharField(max_length=30)
   
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    department=models.CharField(max_length=40,null=True,default='None')
    def __str__(self):  
        return "%s's profile" % self.user 
    
    def save(self, *args, **kwargs):
        try:
            existing = UserProfile.objects.get(user=self.user)
            self.id = existing.id 
        except UserProfile.DoesNotExist:
            pass 
        models.Model.save(self, *args, **kwargs)
        
def create_user_profile(sender, instance, created, **kwargs):  
    if created:
        created = UserProfile.objects.get_or_create(user=instance)
post_save.connect(create_user_profile, sender=User) 


    
class FeedBack(models.Model):
    candidate_id=models.IntegerField()
    level1_feedback=models.CharField(max_length=5000,null=True,default='None')
    level2_feedback=models.CharField(max_length=5000,null=True,default='None')
    level3_feedback=models.CharField(max_length=5000,null=True,default='None')
    level4_feedback=models.CharField(max_length=5000,null=True,default='None')
   
    
        
        
