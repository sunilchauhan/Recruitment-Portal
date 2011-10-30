# Recruitment Tracking Portal - To track the Applicant end-to-end hiring process
# Copyright (C) 2011 Sunil R. Chauhan <sunil.chauhan45@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Recruitment Portal is end-to-end Applicant tracking web application. It has the following features:
1. Consolidated information about Candidate and Job at one place in Grid format using Jquery Datatable plugins.
2. Search facility on table-level and column level.
3. Dynamic column management facility of Grid for HR team
4. Interviewer level-wise feedback entry and display. e.g. Level-1 interviewer can't see feedback of level-2 interviewer but level-2 interviewer can see the 	 	feedback of level-1.
5. Column autofill facility
6. HR admins can create new user for HR department and other department.
7. Employees other than HR have limited access to information. HR employee have full control over the behaviour of portal i.e. can add/update/delete any of the   	 information.
8. Lightbox window for entering feedback about the candidate. Feedback once provided can not be updated by anyone except HR department.
9. in-place check for User existance in database while making entry through username, emailid, contact number and passport number.
10. Direct HTML table export in CSV,XLS and PDF. Apart from whole table, searched result can also be exported in CSV, XLS and PDF format.
11. Download and update resume directly from the datatable.

"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.conf import settings
from django.http import HttpResponse
import xlwt
from django.utils import simplejson
from django.contrib.auth.models import User
from django.template import RequestContext
import datetime
from portal.recruitment.models import job_detail,candidate_detail,UserProfile,FeedBack


"""media url to be used to provide media path in the template"""
media_url=settings.MEDIA_URL




@login_required
def baseview(request):
    """This module display the first page for login to the user.
	 
    """
    context_instance = RequestContext(request)
    template_values = {'MEDIA_URL': media_url, 'user_request': context_instance}
    return render_to_response("firstpage.html", template_values)
	
@login_required
def recruit_index(request):
    """This module is Module responsible for displaying the first job detail page.
	   Here level variable is used to display the level of the interviewer.  On the basis of level, candidate feedback is displayed.
	
    """
    job_details = job_detail.objects.all().order_by('opening_date')
    context_instance = RequestContext(request)
    candidate_details = candidate_detail.objects.all()
    profile_info = request.user.get_profile().department
    level1 = 1
    level2 = 2
    level3 = 3
    level4 = 4
    
    template_values = {'MEDIA_URL': media_url, 'level1': level1, 'level2': level2, 'level3': level3, 'level4': level4, 'department': profile_info, 'job_result': job_details, 'candidate_result': candidate_details, 'user_request': context_instance}
    return render_to_response("recruit_index.html",template_values)


@login_required
def enter_feedback(request):
    """Display the feedback form in lightbox.
	
    """
    req_data=request.POST.copy()
    candidate_id = req_data['candidate_id']
    template_values = {'MEDIA_URL': media_url, 'candidate_id': candidate_id}
    return render_to_response('feedback_form.html', template_values) 




@login_required
def add_candidate(request):
    """Display candidate add form.
    
    """
    all_posting_detail_result = job_detail.objects.values('job_title').distinct()
    all_job_id_result = job_detail.objects.values('id').distinct()
    context_instance = RequestContext(request)
    users_list = User.objects.all()
    template_values={'MEDIA_URL':  media_url, 'allusers': users_list, 'job_result': all_posting_detail_result, 'all_job_id_result': all_job_id_result, 'username': context_instance}
    return render_to_response("candidate_details.html", template_values)


@login_required
def candidate_added(request):
    """Display candidate successfully added form.
    
    """
    template_values = {'MEDIA_URL': media_url}
    return render_to_response("candidate_added.html", template_values)


@login_required
def update_candidate_detail(request):
    """Display update candidate page.
    
    """
    candidate_id = request.GET['candidate_id']
    db_result = candidate_detail.objects.filter(id=candidate_id)
    all_posting_detail_result = job_detail.objects.values('job_title').distinct()
    template_values = {'MEDIA_URL': media_url, 'db_result': db_result, 'posting_result': all_posting_detail_result }
    return render_to_response('update_candidate_page.html', template_values)


@login_required
def candidate_update_done(request):
    """Gets the updated candidate information from candidate update page and update the database for particular candidate.
    
    """
    template_values = {'MEDIA_URL': media_url}
    req_data = request.POST.copy()
    req_data.update(request.FILES)
    candidate_id = req_data['candidate_id']
    candidate_table = candidate_detail.objects.get(id = candidate_id)
    candidate_table.first_name = req_data['first_name']
    candidate_table.last_name = req_data['last_name']
    candidate_table.contact_number = req_data['contact_number']
    candidate_table.email_address = req_data['email_address']
    candidate_table.applied_for = req_data['job_title']
    candidate_table.passport_number = req_data['passport_number']
    candidate_table.contact_address = req_data['address']
    candidate_table.hr_name = req_data['hr_name']
    candidate_table.reference_type = req_data['reference_type']
    candidate_table.referral_name = req_data['referal_name']
    candidate_table.work_experience_years = req_data['experience_yrs']
    candidate_table.work_experience_months = req_data['experience_mnths']
    candidate_table.current_ctc = req_data['current_ctc']
    candidate_table.expected_ctc = req_data['expected_ctc']
    candidate_table.qualification = req_data['qualification']
    candidate_table.institute_name = req_data['institute_name']
    candidate_table.year_of_passing = req_data['year_of_passing']
    candidate_table.percentage = req_data['percentage']
    candidate_table.special_achievement = req_data['special_achievements']
    candidate_table.skill_set = req_data['skill_set']
    candidate_table.validity = req_data['validity']
    candidate_table.stage = req_data['stage']
    candidate_table.status = req_data['status']
    candidate_table.level1_interviewer = req_data['interviewer1']
    candidate_table.level2_interviewer = req_data['interviewer2']
    candidate_table.level3_interviewer = req_data['interviewer3']
    candidate_table.level4_interviewer = req_data['interviewer4']
    candidate_table.save()
    return render_to_response("form_submitted.html", template_values)


@login_required
def add_job(request):
    """Display job first page.
    
    """
    template_values = {'MEDIA_URL':media_url}
    return render_to_response("recruitment_form.html", template_values)


@login_required
def update_job(request):
    """display update job page.
    
    """
    req_data = request.POST.copy()
    job_id = req_data['job_id']
    db_result = job_detail.objects.filter(id=job_id)
    template_values = {'MEDIA_URL': media_url, 'db_result': db_result}
    return render_to_response('update_job_page.html', template_values) 


@login_required
def job_update_done(request):
    """Gets the updated information from job update page and update the database for particular job.
    
    """
    template_values = {'MEDIA_URL': media_url}
    req_data=request.POST.copy()
    candidate_id = req_data['candidate_id']
    job_table = job_detail.objects.get(id=candidate_id)
    job_table.job_title = req_data['job_title']
    job_table.department = req_data['department']
    job_table.designation = req_data['designation']
    job_table.roles_and_responsibilities = req_data['roles']
    job_table.opened_date = req_data['open_date']
    job_table.opened_month = req_data['open_month']
    job_table.opened_year = req_data['open_year']
    job_table.closing_date = req_data['close_date']
    job_table.closing_month = req_data['close_month']
    job_table.closing_year = req_data['close_year']
    job_table.number_of_positions = req_data['No_of_pos']
    job_table.job_opening_status = req_data['job_opening_status']
    job_table.job_type = req_data['job_type']
    job_table.location_name = req_data['location']
    job_table.country = req_data['country']
    job_table.skill_set = req_data['skill']
    job_table.work_experience = req_data['work_experience']
    job_table.validity = req_data['validity']
    job_table.save()
    return render_to_response("form_submitted.html", template_values)


@login_required
def create_user(request):
    """Create user page for user having admin access(superuser).
    
    """
    template_values = {'MEDIA_URL': media_url}
    return render_to_response("registration/create_user_form.html", template_values)


@login_required
def create_login(request):
    """Module responsible for creating new user.
    
    """
    template_values = {'MEDIA_URL': media_url}
    if request.method == 'POST':
        data=request.POST.copy()
        User.username = data['user_name']
        first_name = data['first_name']
        last_name = data['last_name']
        User.email = data['email_address']
        User.password = data['password']
        name = User.username
        
        try:
            user = User.objects.get(username=name)
            return render_to_response("registration/user_exist.html", template_values)
        except User.DoesNotExist:
            user = User.objects.create_user(name,User.email,User.password)
            user.first_name =  first_name
            user.last_name = last_name
            user.save()
            userprofile = UserProfile()
            userprofile.user = user
            userprofile.department = data['dept']
            userprofile.save()
    return render_to_response("registration/create_successful.html", template_values)


@login_required
def submit_recruit_form(request):
    """Module responsible for new job opening entry.
    
    """
    import datetime;
    template_values = {'MEDIA_URL': media_url}
    data=request.POST.copy()
    job_table = job_detail()
   
    job_table.job_title = data['job_title']
    job_table.department = data['department']
    job_table.designation = data['designation']
    job_table.opening_date = datetime.datetime.strptime(data['open_date'], "%m/%d/%Y")
    job_table.closing_date = datetime.datetime.strptime(data['close_date'], "%m/%d/%Y")
    job_table.number_of_positions = data['No_of_pos']
    job_table.job_opening_status = data['job_opening_status']
    job_table.country = data['country']
    

    job_table.location_name = data['location']
    job_table.min_experience = data['minwork_experience']
    job_table.max_experience = data['maxwork_experience']
    job_table.skill_set = data['skill']
    job_table.roles_and_responsibilities = data['roles']
    job_table.job_type = data['job_type']
    job_table.validity = data['validity']
    job_table.save()
    return render_to_response("form_submitted.html",  template_values)

@login_required

def submit_candidate_form(request):
    """Module responsible for new candidate entry.
    
    """
    template_values = {'MEDIA_URL': media_url}
    res_data = request.POST.copy()
    res_data.update(request.FILES)
    
    if res_data['special_achievements'] == '':    #If no achievement is provided in form, then default value
        achivement = 'No Special Achievement'
    else:
        achivement = res_data['special_achievements']
    
    if res_data['highest_qualification'] == 'other':
        qualification = res_data['other qualification']
    else:
        qualification = res_data['highest_qualification']
 
    candidate_table = candidate_detail()
    candidate_table.first_name = res_data['first_name']
    candidate_table.last_name = res_data['last_name']
    candidate_table.contact_number = res_data['contact_number']
    candidate_table.email_address = res_data['email_address']
    candidate_table.applied_for = res_data['job_title']
    candidate_table.passport_number = res_data['passport_number']
    candidate_table.contact_address = res_data['address']
    candidate_table.hr_name = res_data['hr_name']
    candidate_table.reference_type = res_data['reference_type']
    candidate_table.referral_name = res_data['referral_name']
    candidate_table.work_experience_years = res_data['experience_yrs']
    candidate_table.work_experience_months = res_data['experience_mnths']
    candidate_table.current_ctc = res_data['current_ctc']
    candidate_table.expected_ctc = res_data['expected_ctc']
    candidate_table.qualification = qualification
    candidate_table.institute_name = res_data['institute_name']
    candidate_table.year_of_passing = res_data['year_of_passing']
    candidate_table.percentage = res_data['percentage']
    candidate_table.special_achievement = achivement
    candidate_table.resume = res_data['resume']
    candidate_table.skill_set = res_data['skill_set']
    candidate_table.validity = res_data['validity']
    candidate_table.stage = res_data['stage']
    candidate_table.status = res_data['status']
    candidate_table.level1_interviewer = res_data['interviewer1']
    candidate_table.level2_interviewer = res_data['interviewer2']
    candidate_table.level3_interviewer = res_data['interviewer3']
    candidate_table.level4_interviewer = res_data['interviewer4']
    candidate_table.save()
    return render_to_response("form_submitted.html", template_values)

@login_required
def update_resume(request):
    """Update resume for particular candidate
    
    """
    candidate_id = request.GET['candidate_id']
    db_result = candidate_detail.objects.get(id=candidate_id)
    template_values = {'MEDIA_URL': media_url, 'candidate_result': db_result}
    return render_to_response("update_resume_done.html", template_values)

@login_required
def update_resume_done(request):
    """Resume update form submitted
    
    """
    template_values = {'MEDIA_URL': media_url}
    res_data = request.POST.copy()
    res_data.update(request.FILES)
    candidate_id = res_data['candidate_id']
    candidate_result = candidate_detail.objects.get(id=candidate_id)
    candidate_result.resume = res_data['new_resume'] 
    candidate_result.save()
    return render_to_response("form_submitted.html", template_values)



def  check_email(request):
    """module to check existing email address on Ajax request.
     
    """
    email = request.POST.get('email',False)
    email_existed = candidate_detail.objects.filter(email_address=email).count()
    
    if email:
        if email_existed != 0:
            res = "<html><body><font color='red'>Already In Use</font></body></html>"
        else:
            res = "<html><body><font color='green'></font></body></html>"
    else:
        res = ""

    return HttpResponse('%s' % res)


@login_required
def feedback_updated(request):
    """Module to control feedback entry about candidate
    
    """
    req_data = request.POST.copy()
    res_feedback = req_data['candidate_feedback']
    res_id = req_data['candidate_id']
    user = request.user
    today_date = datetime.date.today()
    my_date = today_date.strftime("%d/%m/%y")
    
    user_level = candidate_detail.objects.get(id=res_id)
    try:
        show_feedback = FeedBack.objects.get(candidate_id=res_id)
    except:
        show_feedback = False
    
    if show_feedback == False:
        if user_level.level1_interviewer == str(user):
            feedback = FeedBack()
            feedback.user = request.user
            feedback.candidate_id = res_id
            feedback.level1_feedback = 'On '+ my_date +': <br>'+ res_feedback
            feedback.level2_feedback = None
            feedback.level3_feedback = None
            feedback.level4_feedback = None
            feedback.save()
        
        
        if user_level.level2_interviewer == str(user):
            feedback = FeedBack()
            feedback.user = request.user
            feedback.candidate_id = res_id
            feedback.level1_feedback = None
            feedback.level2_feedback = 'On '+ my_date +': <br>'+ res_feedback
            feedback.level3_feedback = None
            feedback.level4_feedback = None
            feedback.save()
    
        if user_level.level3_interviewer == str(user):
            feedback = FeedBack()
            feedback.user = request.user
            feedback.candidate_id = res_id
            feedback.level1_feedback = None
            feedback.level2_feedback = None
            feedback.level3_feedback = 'On '+ my_date +': <br>'+ res_feedback
            feedback.level4_feedback = None
            feedback.save()
        
        if user_level.level4_interviewer == str(user):
            feedback = FeedBack()
            feedback.user = request.user
            feedback.candidate_id = res_id
            feedback.level1_feedback = None
            feedback.level2_feedback = None
            feedback.level3_feedback = None
            feedback.level4_feedback = 'On '+ my_date +': <br>'+ res_feedback
            feedback.save()
            
    else:
        
        feedback = FeedBack.objects.get(candidate_id=res_id)
        if user_level.level1_interviewer == str(user):
            feedback.level1_feedback = 'On '+ my_date +': <br>'+ res_feedback
            feedback.save()
        elif user_level.level2_interviewer == str(user):
            feedback.level2_feedback = 'On '+ my_date +': <br>'+ res_feedback
            feedback.save()
        elif user_level.level3_interviewer == str(user):
            feedback.level3_feedback = 'On ' + my_date +': <br>'+ res_feedback
            feedback.save()
        else:
            feedback.level4_feedback = 'On '+ my_date +': <br>'+ res_feedback
            feedback.save()
    job_details = job_detail.objects.all().order_by('opening_date')
    context_instance = RequestContext(request)
    candidate_details = candidate_detail.objects.all()
    profile_info = request.user.get_profile().department
    template_values={'MEDIA_URL': media_url, 'department': profile_info, 'job_result': job_details, 'candidate_result': candidate_details, 'user_request': context_instance }
    return render_to_response("recruit_index.html", template_values)
   
    

def  check_feedback(request):
    level = request.GET['level']
    candidate_id = request.GET['candidate_id']
    try:
        candidate_result = FeedBack.objects.get(candidate_id=candidate_id)
    except:
        pass
    
    if candidate_result:
        level1_feedback = candidate_result.level1_feedback
        level2_feedback = candidate_result.level2_feedback
        level3_feedback = candidate_result.level3_feedback
        level4_feedback = candidate_result.level4_feedback
        
        if level == "1":
            if level1_feedback != None:
                status = 1
            else:
                status = 0
        
        if level == "2":
            if level2_feedback != None:
                status = 1
            else:
                status = 0
      
        if level == "3":
            if level3_feedback !=None:
                status = 1
            else:
                status = 0
            
        if level == "4":
            if level4_feedback != None:
                status = 1
            else:
                status = 0
    else:
        status = 0

       
    return HttpResponse(simplejson.dumps(status),mimetype="application/json")



def  viewable_feedback(request):
    """Display feedback on the basis of level of current user.
    
    """
    level = request.GET["level"]
    candidate_id = request.GET["candidate_id"]

    all_feedback = FeedBack.objects.get(candidate_id=candidate_id)
    candidate_result = candidate_detail.objects.get(id=candidate_id)
    
    if level == "1":
        if all_feedback.level1_feedback:
            user_feedback1 = candidate_result.level1_interviewer.capitalize() + '&nbspSaid&nbsp;' + all_feedback.level1_feedback
        else:
            user_feedback1 =  ""
        user_feedback2 = ""
        user_feedback3 = ""
        user_feedback4 = ""
        
    if level == "2":
        if all_feedback.level1_feedback:
            user_feedback1 = candidate_result.level1_interviewer.capitalize() + '&nbspSaid&nbsp;' + all_feedback.level1_feedback
        else:
            user_feedback1 = ""
        
        if all_feedback.level2_feedback:
            user_feedback2 = '<br><br>' + candidate_result.level2_interviewer.capitalize() + '&nbspSaid&nbsp;' + all_feedback.level2_feedback
        else:
            user_feedback2 = ""
            
        user_feedback3 = ""
        user_feedback4 = ""
        
    if level == "3":
        
        if all_feedback.level1_feedback:
            user_feedback1 = candidate_result.level1_interviewer.capitalize() + '&nbspSaid&nbsp;' + all_feedback.level1_feedback
        else:
            user_feedback1 = ""
        
        if all_feedback.level2_feedback:
            user_feedback2 = '<br><br>' + candidate_result.level2_interviewer.capitalize() + '&nbspSaid&nbsp;' + all_feedback.level2_feedback
        else:
            user_feedback2 = ""
        
        if all_feedback.level3_feedback:
            user_feedback3 = '<br><br>'+candidate_result.level3_interviewer.capitalize() + '&nbspSaid&nbsp;'  + all_feedback.level3_feedback
        else:
            user_feedback3 = ""
        user_feedback4 = ""
        
    if level == "4":
        if all_feedback.level1_feedback:
            user_feedback1 = candidate_result.level1_interviewer.capitalize() + '&nbspSaid&nbsp;' + all_feedback.level1_feedback
        else:
            user_feedback1 = ""
        
        if all_feedback.level2_feedback:
            user_feedback2 = '<br><br>' + candidate_result.level2_interviewer.capitalize() + '&nbspSaid&nbsp;' + all_feedback.level2_feedback
        else:
            user_feedback2 = ""
            
        if all_feedback.level3_feedback:  
            user_feedback3 = '<br><br>' + candidate_result.level3_interviewer.capitalize() + '&nbspSaid&nbsp;' + all_feedback.level3_feedback
        else:
            user_feedback3 = ""
            
        if all_feedback.level4_feedback:
            user_feedback4 = '<br><br>' + candidate_result.level4_interviewer.capitalize() + '&nbspSaid&nbsp;' + all_feedback.level4_feedback
        else:
            user_feedback4 = ""
            
    user_feedback = user_feedback1 + user_feedback2 + user_feedback3 + user_feedback4
    
    user_feedback = user_feedback.lstrip(",")
    user_feedback = user_feedback.strip()
    user_feedback = str(user_feedback)
    
    return HttpResponse(simplejson.dumps(user_feedback), mimetype="application/json")
 
   
def viewable_HRfeedback(request):
    """Feedback tooltip displayed to HR members.
    
    """
    candidate_id = request.GET['candidate_id']
    
    all_feedback = FeedBack.objects.get(candidate_id=candidate_id)
    candidate_result = candidate_detail.objects.get(id=candidate_id)
    
    if all_feedback.level1_feedback:
        user_feedback1 = candidate_result.level1_interviewer.capitalize() + '&nbspSaid&nbsp;' + all_feedback.level1_feedback
    else:
        user_feedback1 = candidate_result.level1_interviewer.capitalize() + '&nbspSaid&nbsp;' + "Has not given feedback yet."
        
    if all_feedback.level2_feedback:
        user_feedback2 = '|<br><br>' + candidate_result.level2_interviewer.capitalize() + '&nbspSaid&nbsp;' + all_feedback.level2_feedback
    else:
        user_feedback2 = '|<br><br>' + candidate_result.level2_interviewer.capitalize() + '&nbspSaid&nbsp;' + "Has not given feedback yet."
            
    if all_feedback.level3_feedback:  
        user_feedback3 = '|<br><br>'+candidate_result.level3_interviewer.capitalize() + '&nbspSaid&nbsp;' + all_feedback.level3_feedback
    else:
        user_feedback3 = '|<br><br>' + candidate_result.level3_interviewer.capitalize() + '&nbspSaid&nbsp;' + "Has not given feedback yet."
            
    if all_feedback.level4_feedback:
        user_feedback4 = '|<br><br>' + candidate_result.level4_interviewer.capitalize() + '&nbspSaid&nbsp;' + all_feedback.level4_feedback
    else:
        user_feedback4 = '|<br><br>' + candidate_result.level4_interviewer.capitalize() + '&nbspSaid&nbsp;' + "Has not given feedback yet."
            
    user_feedback = user_feedback1+user_feedback2+user_feedback3+user_feedback4
    
    user_feedback = user_feedback.lstrip(",")
    user_feedback = user_feedback.strip()
    user_feedback = str(user_feedback)
    return HttpResponse(simplejson.dumps(user_feedback), mimetype="application/json")
 
  
      
def hr_feedback_update(request):
    candidate_id = request.GET['candidate_id']
    all_feedback = FeedBack.objects.get(candidate_id=candidate_id)
    
    template_values = {'MEDIA_URL': media_url, 'all_feedback': all_feedback, 'candidate_id': candidate_id}
    return render_to_response("HR_feedback_update_form.html", template_values)


def hr_feedback_updated(request):
    res_data = request.POST.copy()
    feedback1 = res_data['feedback1']
    feedback2 = res_data['feedback2']
    feedback3 = res_data['feedback3']
    feedback4 = res_data['feedback4']
    candidate_id = res_data['candidate_id']
    
    feedback_table = FeedBack.objects.get(candidate_id=candidate_id)
    
    if feedback1:
        feedback_table.level1_feedback = feedback1
        feedback_table.save()
    
    if feedback2:
        feedback_table.level2_feedback = feedback2
        feedback_table.save()
    
    if feedback3:
        feedback_table.level3_feedback = feedback3
        feedback_table.save()
        
    if feedback4:
        feedback_table.level4_feedback = feedback4
        feedback_table.save()
    
    template_values = {'MEDIA_URL': media_url}
    return render_to_response("form_submitted.html", template_values)


def  check_contact_number(request):
    my_number = request.POST.get('contact_number',False)
    contact_number = candidate_detail.objects.filter(contact_number=my_number).count()

    if contact_number:
        if contact_number != 0:
            res = "<html><body><font color='red'>Already In Use</font></body></html>"
        else:
            res = "<html><body><font color='green'>Ok</font></body></html>"
    else:
        res = ""

    return HttpResponse('%s' % res)

    

def  check_passport_number(request):
    """Check updated passport number on Ajax request.
    
    """
    my_passport_number = request.POST.get('passport_number',False)
    passport_number = candidate_detail.objects.filter(passport_number=my_passport_number).count()

    if passport_number:
        if passport_number != 0:
            res = "<html><body><font color='red'>Already In Use</font></body></html>"
        else:
            res = "<html><body><font color='green'>Ok</font></body></html>"
    else:
        res = ""

    return HttpResponse('%s' % res)


def checkusername(request):
    """Check existing username.Give warning in case user already exist.
    
    """
    user_name = request.POST.get('user_name', False)
    if user_name:
        user_name_exist = User.objects.filter(username=user_name).count()
        if user_name_exist != 0:
            res = "<html><body><font color='red'>Already In Use</font></body></html>"
        else:
            res = "<html><body><font color='green'>OK</font></body></html>"
    else:
        res = ""

    return HttpResponse('%s' % res)



def check_location(request):
    """Check existing location for the job.Helpful in autofill of the field.
    
    """
    location = job_detail.objects.values_list('location_name').distinct()
    location = list(location)
    return HttpResponse(simplejson.dumps(location), mimetype="application/json")
    

def check_title(request):
    """Check the availability of new job title.Helpful in autofill of the field.
    
    """
    title = job_detail.objects.values_list('job_title').distinct()
    title = list(title)
    return HttpResponse(simplejson.dumps(title), mimetype="application/json")


def check_skill_set(request):
    """Check the availability of skill set.Helpful in autofill of the skill set field of Add candidate form.
    
    """
    skill_set = job_detail.objects.values_list('skill_set').distinct()
    skill_set = list(skill_set)
    return HttpResponse(simplejson.dumps(skill_set), mimetype="application/json") 


def all_users(request):
    """Give the list of all users while making entry for level-wise interviewer in candidate form.Helpful in autofill of the interviewer field.
    
    """
    all_users = User.objects.values_list('username').distinct()
    all_users = list(all_users)
    return HttpResponse(simplejson.dumps(all_users), mimetype="application/json") 


def check_roles(request):
    """Provide all the roles and responsibilities while filling Add candidate form. Helpful in autofill of the Roles and Responsibility field.
    
    """
    roles = job_detail.objects.values_list('roles_and_responsibilities').distinct()
    roles = list(roles)
    return HttpResponse(simplejson.dumps(roles), mimetype="application/json") 


def check_referral(request):
    """Provide the referral name for candidate form.Helpful in autofill of the referral field in Add candidate form.
    
    """
    referral = candidate_detail.objects.values_list('referral_name').distinct()
    referral = list(referral)
    return HttpResponse(simplejson.dumps(referral), mimetype="application/json") 
