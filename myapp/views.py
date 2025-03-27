from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from django. contrib import messages
from django.contrib.auth import authenticate, login,logout
from .form import *
from. models import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.shortcuts import redirect, render

# Create your views here.
def index(request):
    return render(request, "index.html")


def gallery(request):
    gallery=Gallarey.objects.all()
    return render(request, "gallery.html",locals())




def login_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if the user is a staff (admin)
            if user.is_staff:
                # If the user is an admin, log them in
                login(request, user)
                messages.success(request, 'Login successful!')

                # Redirect to the admin dashboard (index_admin)
                return redirect('index_admin')
            else:
                # If the user is not staff (admin), show an error message
                messages.error(request, 'You do not have admin privileges.')
                return redirect('login_admin')  # Redirect back to the login page
        else:
            # If authentication fails, show an error message
            messages.error(request, 'Invalid username or password.')
            return redirect('login_admin')  # Redirect back to the login page
    else:
        # If the request is GET, render the login page
        return render(request, 'login-admin.html')



def login_donor(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Check if the user is a Donor
            try:
                donor = Donor.objects.get(user=user)
                # If this is a donor, log them in
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('index_donor')
            except Donor.DoesNotExist:
                messages.error(request, 'You are not registered as a donor.')
                return redirect('login_donor')  # Stay on the donor login page

        else:
            messages.error(request, 'Wrong username or password combination')
            return redirect('login_donor')
    else:
        return render(request, 'login-donor.html')
    


def login_volunteer(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Check if the user is a Volunteer
            try:
                volunteer = Volunteer.objects.get(user=user)
                # If this is a volunteer, log them in
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('index_volunteer')
            except Volunteer.DoesNotExist:
                messages.error(request, 'You are not registered as a volunteer.')
                return redirect('login_volunteer')  # Stay on the volunteer login page

        else:
            messages.error(request, 'Wrong username or password combination')
            return redirect('login_volunteer')
    else:
        return render(request, 'login-volunteer.html')
    
    



class signup_donor(View):
    def get(self, request):
        form1 = UserForm()
        form2 = DonorForm()
        return render(request, "signup_donor.html", {"form1": form1, "form2": form2})

    def post(self, request):
        form1 = UserForm(request.POST)
        form2 = DonorForm(request.POST, request.FILES)

        # Check if the username already exists
        if User.objects.filter(username=form1.data['username']).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
            return render(request, "signup_donor.html", {"form1": form1, "form2": form2})

        if form1.is_valid() and form2.is_valid():
            # Process the forms if both are valid
            user = form1.save(commit=False)
            user.set_password(form1.cleaned_data['password'])
            user.save()

            donor = form2.save(commit=False)
            donor.user = user
            donor.save()

            # Success message
            messages.success(request, 'Donor registration successful! You can now log in.')
            return redirect('login_donor')

        else:
            # Error message if forms are invalid
            messages.error(request, 'There was an error with your submission. Please check the fields below.')
        
        return render(request, "signup_donor.html", {"form1": form1, "form2": form2})



class signup_volunter(View):
    def get(self, request):
        form1 = UserForm()
        form2 = VolunteerForm()
        return render(request, "signup_volunteer.html", {"form1": form1, "form2": form2})

    def post(self, request):
        form1 = UserForm(request.POST)
        form2 = VolunteerForm(request.POST, request.FILES)

        # Check if the username already exists
        if User.objects.filter(username=form1.data['username']).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
            return render(request, "signup_volunteer.html", {"form1": form1, "form2": form2})

        if form1.is_valid() and form2.is_valid():
            # Process the forms if both are valid
            user = form1.save(commit=False)
            user.set_password(form1.cleaned_data['password'])
            user.save()

            # Set status to "pending" before saving the volunteer
            volunteer = form2.save(commit=False)
            volunteer.user = user
            volunteer.status = 'pending'  # Set the default status to "pending"
            volunteer.save()

            # Success message
            messages.success(request, 'Donor registration successful! You can now log in.')
            return redirect('login_volunteer')

        else:
            # Error message if forms are invalid
            messages.error(request, 'There was an error with your submission. Please check the fields below.')

        return render(request, "signup_volunteer.html", {"form1": form1, "form2": form2})

def index_admin(request):
    totaldonation=Donation.objects.all().count()
    totaldonors=Donor.objects.all().count()
    totalvolunteer=Volunteer.objects.all().count()
    totalpendingdon=Donation.objects.filter(status='pending').count()
    totalacceptedon=Donation.objects.filter(status='accept').count()
    totaldeliverdon=Donation.objects.filter(status='Donation Delivered Successfully').count()
    totaldonarea=DonationArea.objects.all().count()
    
    return render(request, "index-admin.html",locals())


# admin dashboard
def pending_donation(request):
    donation=Donation.objects.filter(status='pending')
    return render(request, "pending-donation.html",locals())


def accepted_donation(request):
    donation=Donation.objects.filter(status='accept')
    return render(request, "accepted-donation.html",locals())


def rejected_donation(request):
    donation=Donation.objects.filter(status='reject')
    return render(request, "rejected-donation.html",locals())


def volunteerallocated_donation(request):
    donation=Donation.objects.filter(status='Volunteer Allocated')
    return render(request, "volunteerallocated-donation.html",locals())


def donationrec_admin(request):
    donation=Donation.objects.filter(status='Donation Received')
    return render(request, "donationrec-admin.html",locals())


def donationnotrec_admin(request):
    donation=Donation.objects.filter(status='Donation Not Received')
    return render(request, "donationnotrec-admin.html",locals())


def donationdelivered_admin(request):
    donation=Donation.objects.filter(status='Donation Delivered Successfully')
    return render(request, "donationdelivered-admin.html",locals())

def delete_donation(request,pk):
    donation=Donation.objects.get(id=pk)
    donation.delete()
    return redirect('all_donations')

def delete_volunteer(request,pk):
    volunteer=Volunteer.objects.get(id=pk)
    volunteer.delete()
    return redirect('all_volunteer')

def delete_area(request,pid):
    area=DonationArea.objects.get(id=pid)
    area.delete()
    return redirect('manage_area')

def delete_donor(request,pid):
    user=User.objects.get(id=pid)
    user.delete()
    return redirect('manage_donor')




def all_donations(request):
    donation=Donation.objects.all()
    return render(request, "all-donations.html",locals())


def manage_donor(request):
    donor=Donor.objects.all()
    return render(request, "manage-donor.html",locals())


def new_volunteer(request):
    volunteer=Volunteer.objects.filter(status='pending')
    return render(request, "new-volunteer.html",locals())


def accepted_volunteer(request):
    volunteer=Volunteer.objects.filter(status='accept')
    return render(request, "accepted-volunteer.html",locals())


def rejected_volunteer(request):
    volunteer=Volunteer.objects.filter(status='reject')
    return render(request, "rejected-volunteer.html",locals())


def all_volunteer(request):
    volunteer=Volunteer.objects.all()
    return render(request, "all-volunteer.html",locals())


class add_area(View):
    def get(self, request):
        form=DonationAreaForm()
        return render(request, "add-area.html",locals())
    def post(self, request):
        form = DonationAreaForm(request.POST)
        if form.is_valid():
            # Use the form's cleaned data to access the values
            arename = form.cleaned_data['arename']
            description = form.cleaned_data['description']
            try:
                # Create a new DonationArea object using the cleaned data
                DonationArea.objects.create(arename=arename, description=description)
                messages.success(request, 'Area added successfully')
                return redirect('index_admin')
            except Exception as e:
                messages.error(request, f'Area addition failed: {str(e)}')
        else:
            messages.error(request, 'Form is invalid')
        return render(request, "add-area.html", {'form': form})
    
     

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View


class edit_area(View):
    def get(self, request, pid):
        # Fetch the existing donation area object
        area = get_object_or_404(DonationArea, pk=pid)
        # Populate the form with the existing data
        form = DonationAreaForm(instance=area)
        return render(request, "edit-area.html", {'form': form, 'area': area})

    def post(self, request, pid):
        # Fetch the existing donation area object
        area = get_object_or_404(DonationArea, pk=pid)
        # Populate the form with POST data (to update)
        form = DonationAreaForm(request.POST, instance=area)
        
        if form.is_valid():
            # Save the updated form data
            form.save()
            messages.success(request, 'Area updated successfully')
            return redirect('manage_area')  # Redirect to the area management page
        else:
            # If the form is invalid, render the same page with error messages
            messages.error(request, 'Area not updated. Please try again.')
            return render(request, "edit-area.html", {'form': form, 'area': area})

    
    


def manage_area(request):
    donationarea=DonationArea.objects.all()
    return render(request, "manage-area.html",locals())


def changepwd_admin(request, user_id=None):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Admin privilege check: If no user_id, it is the logged-in user, otherwise it’s an admin changing another user's password
        if user_id:
            # Only admin can change password for another user
            if not request.user.is_staff:
                messages.error(request, 'You are not authorized to change other users\' passwords.')
                return redirect('somewhere')  # Redirect to a safe location if the user is not admin
            try:
                # Get the user whose password is being changed
                user_to_change = User.objects.get(id=user_id)
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
                return redirect('somewhere')  # Redirect if the user doesn't exist
        else:
            user_to_change = request.user  # Default to the logged-in user

        # Handle the form submission
        if request.method == 'POST':
            form = ChangePasswordForm(user=user_to_change, data=request.POST)
            
            if form.is_valid():
                new_password = form.cleaned_data.get('new_password1')
                confirm_password = form.cleaned_data.get('new_password2')

                if new_password != confirm_password:
                    form.add_error('new_password2', 'The new password and confirmation do not match.')
                    messages.error(request, 'The new password and confirmation do not match.')
                else:
                    # Save the new password
                    form.save()
                    if user_to_change == request.user:
                        # If the logged-in user is changing their own password, update the session hash
                        update_session_auth_hash(request, form.user)
                    messages.success(request, 'The password has been updated successfully!')
                    return redirect('changepwd_admin', user_id=user_to_change.id)  # Redirect back to the change password page
            else:
                messages.error(request, 'Please correct the error above so that you can change the password.')
        else:
            form = ChangePasswordForm(user=user_to_change)

        return render(request, 'changepwd-admin.html', {'form': form, 'user_to_change': user_to_change})
    
    else:
        messages.error(request, 'You must login first to access the page')
        return redirect('login_admin')
    
def logout_user(request):
    logout(request)
    messages.success(request, 'you have log out............')
    return redirect('index') 


# admin view details
from django.shortcuts import render, get_object_or_404


class accepted_donationdetail(View):
    def get(self, request, pid):
        donation = get_object_or_404(Donation, id=pid)
        donationarea = DonationArea.objects.all()
        volunteer = Volunteer.objects.filter(status='accept')

        return render(request, "accepted-donationdetail.html", locals())

    def post(self, request, pid):
        donation = get_object_or_404(Donation, id=pid)
        
        # Ensure correct access to POST data
        donationareaid = request.POST['donationareaid']
        volunteerid = request.POST['volunteerid']
        adminremark = request.POST['adminremark']
        
        # Fetch the corresponding DonationArea and Volunteer
        try:
            da = DonationArea.objects.get(id=donationareaid)
            v = Volunteer.objects.get(id=volunteerid)

            # Update donation with allocated volunteer and other details
            donation.donationarea = da
            donation.volunteer = v
            donation.adminremark = adminremark
            donation.status = "Volunteer Allocated"
            donation.volunteerremark = "Not updated yet"
            donation.updationdate = date.today()
            donation.save()

            messages.success(request, 'Volunteer Allocated Successfully')
        except DonationArea.DoesNotExist:
            messages.error(request, 'Donation Area not found')
        except Volunteer.DoesNotExist:
            messages.error(request, 'Volunteer not found')
        except Exception as e:
            messages.error(request, f'Failed to allocate volunteer: {str(e)}')
        
        return render(request, "accepted-donationdetail.html", locals())

            


class view_volunteerdetail(View):
    def get(self, request, pid):
        # Correct the query to use .get() to fetch a single object by id
        try:
            volunteer = Volunteer.objects.get(id=pid)  # Use get() instead of (id=id)
        except Volunteer.DoesNotExist:
            volunteer = None  # Handle the case where the volunteer doesn't exist
        
        return render(request, "view-volunteerdetail.html", locals())
    
    def post(self, request, pid):
        try:
            volunteer = Volunteer.objects.get(id=pid)  # Use .get() for fetching by id
            status = request.POST['status']
            adminremark = request.POST['adminremark']

            # Update the volunteer's details
            volunteer.adminremark = adminremark
            volunteer.status = status
            volunteer.updationdate = date.today()
            volunteer.save()
            messages.success(request, 'Volunteer updated successfully')
        except Volunteer.DoesNotExist:
            messages.error(request, 'Volunteer not found')
        except Exception as e:
            messages.error(request, f'Failed to update volunteer: {e}')
        
        return render(request, "view-volunteerdetail.html", locals())



def view_donordetail(request, pid):
    donor=Donor.objects.get(id=pid)
    return render(request, "view-donordetail.html",locals())


from django.shortcuts import render, get_object_or_404
from datetime import date

class view_donationdetail(View):
    # Handle GET request to display donation details
    def get(self, request, pid):
        # Fetch donation details by its ID (pid)
        donation = get_object_or_404(Donation, id=pid)
        return render(request, "view-donationdetail.html", {'donation': donation})

    # Handle POST request to update admin remarks and donation status
    def post(self, request, pid):
        donation = get_object_or_404(Donation, id=pid)
        status = request.POST.get('status')
        adminremark = request.POST.get('adminremark')

        try:
            donation.adminremark = adminremark
            donation.status = status
            donation.updationdate = date.today()
            donation.save()
            messages.success(request, 'Admin remark updated successfully')
            return render(request, "view-donationdetail.html", {'donation': donation})

        except Exception as e:
            messages.error(request, f'Update failed: {str(e)}')
            return render(request, "view-donationdetail.html", {'donation': donation})


# donor dashboard
def index_donor(request):
    user=request.user
    donor=Donor.objects.get(user=user)
    donationcount=Donation.objects.filter(donor=donor).count()

    acceptedcount=Donation.objects.filter(donor=donor,status='accept').count()
    rejectedcount=Donation.objects.filter(donor=donor,status='reject').count()
    pendingcount=Donation.objects.filter(donor=donor,status='pending').count()
    delivercount=Donation.objects.filter(donor=donor,status='Donation Delivered Successfully').count()
    return render(request, "index-donor.html",locals())

from datetime import date 
def donate_now(request):
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)

        # Get the Donor instance for the logged-in user
        try:
            donor = Donor.objects.get(user=request.user)
        except Donor.DoesNotExist:
            messages.error(request, "You need to be registered as a donor first.")
            return redirect('donor_login')  # Redirect to the donor registration page

        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = donor  # Assign the Donor instance, not the User instance
            donation.donationdate = date.today()  # Set donation date to today's date
            donation.status = 'pending'  # Set default status to 'pending'
            donation.save()
            messages.success(request, 'Donation has been created successfully!')
            return redirect('donate_now')  # Redirect to a donation success page
        else:
            messages.error(request, 'Please correct the errors in the form.')

    else:
        form = DonationForm()

    return render(request, 'donate-now.html', {'form': form})

    


def donation_history(request):
    donation= Donation.objects.all()
    return render(request, "donation-history.html",{'donation':donation})


class profile_donor(View):
    def get(self,request):
        form1=UserForm()
        form2=DonorForm()
        user=request.user
        donor=Donor.objects.get(user=user)
        return render(request, "profile-donor.html",locals())
     
    def post(self,request):
        form1=UserForm(request.POST)
        form1=DonorForm(request.POST)
        user=request.user
        donor=Donor.objects.get(user=user)
        fn=request.POST['firstname']
        ln=request.POST['lastname']
        contact=request.POST['contact']
        address=request.POST['address']

        donor.user.first_name=fn
        donor.user.last_name=ln
        donor.user.contact=contact
        donor.user.address=address

        try:
            userpic=request.FILES['userpic']
            donor.userpic=userpic
            donor.save()
            donor.user.save()
            messages.success(request,'donorprofile updatedsuccesfully')
        except:
            messages.error(request, 'profileupdation failed')
        return render(request,'profile-donor.html',locals()) 





def changepwd_donor(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangePasswordForm(user=request.user, data=request.POST)
            
            if form.is_valid():
                # Check if the new password and confirmation match (handled by Django forms)
                new_password = form.cleaned_data.get('new_password1')
                confirm_password = form.cleaned_data.get('new_password2')

                if new_password != confirm_password:
                    form.add_error('new_password2', 'The new password and confirmation do not match.')
                    messages.error(request, 'The new password and confirmation do not match.')
                else:
                    # Save the new password
                    form.save()
                    update_session_auth_hash(request, form.user)  # Important to keep the user logged in
                    messages.success(request, 'Your password has been updated successfully!')
                    return redirect('changepwd_donor')  # Redirect to the profile page or another appropriate page
            else:
                messages.error(request, 'Please correct the error above so that you can change password.')
        else:
            form = ChangePasswordForm(user=request.user)
        
        return render(request, 'changepwd-donor.html', {'form': form})
    else:
        messages.error(request, 'You must login first to access the page')
        return redirect('login-donor')

# volunteer dashboard
def index_volunteer(request):
    user=request.user
    volunteer=Volunteer.objects.get(user=user)
    totaldelivered=Donation.objects.filter(volunteer=volunteer, status='Donation Delivered Successfully').count()

    totalcollectionreq=Donation.objects.filter(volunteer=volunteer,status='Volunteer Allocated').count()
    totalrecd=Donation.objects.filter(volunteer=volunteer,status='Donation Received').count()
    totalnotrecd=Donation.objects.filter(volunteer=volunteer,status='Donation Not Received').count()
    return render(request, "index-volunteer.html",locals())



def collection_req(request):
    user = request.user
    volunteer = Volunteer.objects.get(user=user)  # Fixed typo from volunter to volunteer
    donation = Donation.objects.filter(volunteer=volunteer, status='Volunteer Allocated')  # Corrected query

    return render(request, "collection-req.html", {'donation': donation}) 


def donationrec_volunteer(request):
    user = request.user
    volunteer = Volunteer.objects.get(user=user)  # Fixed typo from volunter to volunteer
    donation = Donation.objects.filter(volunteer=volunteer, status='Donation Received')  # Corrected query

    return render(request,"donationrec-volunteer.html", {'donation': donation})
    


def donationnotrec_volunteer(request):
     user = request.user
     volunteer = Volunteer.objects.get(user=user)  # Fixed typo from volunter to volunteer
     donation = Donation.objects.filter(volunteer=volunteer, status='Donation Not Recieved')
     return render(request, "donationnotrec-volunteer.html",{'donation': donation})


def donationdelivered_volunteer(request):
    user = request.user
    volunteer = Volunteer.objects.get(user=user)  # Fixed typo from volunter to volunteer
    donation = Donation.objects.filter(volunteer=volunteer, status='Donation Delivered Successfully')
    return render(request, "donationdelivered-volunteer.html",{'donation': donation})



from django.contrib import messages
from django.shortcuts import render
from django.views import View
from .form import UserForm, VolunteerForm
from .models import Volunteer

class profile_volunteer(View):
    def get(self, request):
        form1 = UserForm()
        form2 = VolunteerForm()
        user = request.user
        try:
            volunteer = Volunteer.objects.get(user=user)
        except Volunteer.DoesNotExist:
            volunteer = None

        return render(request, "profile-volunteer.html", {'form1': form1, 'form2': form2, 'volunteer': volunteer})

    def post(self, request):
        form1 = UserForm(request.POST)
        form2 = VolunteerForm(request.POST, request.FILES)

        user = request.user
        try:
            volunteer = Volunteer.objects.get(user=user)
        except Volunteer.DoesNotExist:
            volunteer = None
        
        if form1.is_valid() and form2.is_valid():
            fn = form1.cleaned_data['first_name']
            ln = form1.cleaned_data['last_name']
            username = form1.cleaned_data['username']  # Get the username from the form
            contact = form2.cleaned_data['contact']
            address = form2.cleaned_data['address']
            aboutme = form2.cleaned_data['aboutme']

            # Update user details and volunteer details
            volunteer.user.first_name = fn
            volunteer.user.last_name = ln
            volunteer.user.username = username  # Save the updated username
            volunteer.contact = contact
            volunteer.address = address
            volunteer.aboutme = aboutme

            try:
                if 'userpic' in request.FILES:
                    volunteer.userpic = request.FILES['userpic']
                if 'idpic' in request.FILES:
                    volunteer.idpic = request.FILES['idpic']
                
                volunteer.save()
                volunteer.user.save()

                messages.success(request, 'Volunteer profile updated successfully.')
            except Exception as e:
                messages.error(request, f'Error while updating profile: {e}')

            return render(request, 'profile-volunteer.html', {'form1': form1, 'form2': form2, 'volunteer': volunteer})
        else:
            messages.error(request, 'Form validation failed. Please check the inputs.')
            return render(request, 'profile-volunteer.html', {'form1': form1, 'form2': form2, 'volunteer': volunteer})

def changepwd_volunteer(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangePasswordForm(user=request.user, data=request.POST)
            
            if form.is_valid():
                # Save the new password
                form.save()
                update_session_auth_hash(request, form.user)  # Important to keep the user logged in
                messages.success(request, 'Your password has been updated successfully!')
                return redirect('changepwd_volunteer')  # Redirect to the profile page or another appropriate page
            else:
                messages.error(request, 'Please correct the error above so that you can change password.')
        else:
            form = ChangePasswordForm(user=request.user)
        
        return render(request, 'changepwd-volunteer.html', {'form': form})
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login_volunteer')


# view details
def donationdetail_donor(request, pid):
    donation=Donation.objects.get(id=pid)
    return render(request, "donationdetail-donor.html",{'donation':donation})


class donationcollection_detail(View):
    def get(self,request,pid):
        donation=Donation.objects.get(id=pid)
    
        return render(request, "donationcollection-detail.html",locals())
    def post(self,request,pid):
        donation=Donation.objects.get(id=pid)
        status=request.POST['status']
        volunteerremark=request.POST['volunteerremark']
        try:
            donation.status=status
            donation.volunteerremark=volunteerremark
            donation.updationdate=date.today()
            donation.save()
            messages.success(request, 'Volunteer status and remark updated successfully')
        except:
            messages.error(request,'volunteer status and remark failed to update')
        return render(request, "donationcollection-detail.html",locals())


class donationrec_detail(View):
    def get(self, request, pid):
        donation = Donation.objects.get(id=pid)
        return render(request, "donationrec-detail.html", {'donation': donation})

    def post(self, request, pid):
        donation = Donation.objects.get(id=pid)
        status = request.POST['status']
        deliverypic = request.FILES['deliverypic']
        
        try:
            donation.status = status
            donation.updationdate = date.today()
            donation.save()
            Gallarey.objects.create(donation=donation, deliverypic=deliverypic)
            messages.success(request, 'Donation delivered successfully')
            return redirect('donationrec_detail', pid=donation.id)  # Redirect after successful POST
        except:
            messages.error(request, 'Failed to deliver donation')
            return render(request, "donationrec-detail.html", {'donation': donation})
        
    

