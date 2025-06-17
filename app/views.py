from django.shortcuts import render,redirect,get_object_or_404
from .models import Testimonials,Course,Join,Team,Contact,AboutCourse,Profile,Transaction
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import re
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import uuid
from django.contrib import messages
from django_esewa import EsewaPayment
from django_esewa import generate_signature
from django.conf import settings

# Create your views here.
def home(request):
    testimonials=Testimonials.objects.all()
    course=Course.objects.all()
    join=Join.objects.all()
    
    return render(request,"index.html",{
        'test':testimonials,'course':course,'join':join
    })


def about(request):
    team=Team.objects.all()
    return render(request,"about.html",{
        'team':team
    })

def contact(request):
    if request.method=="POST":
        data=request.POST
        name=data['name']
        contact=data['contact']
        email=data['email']
        message=data['message']
        contact=Contact.objects.create(name=name,contact=contact,email=email,message=message)
        contact.save()
        subject="New Contact Form Submission - Saraswatinagar Institute"
        message=render_to_string("message.html",{
            "name":name
        })
        from_email=settings.EMAIL_HOST_USER
        recipient_list=[email]

        em=EmailMessage(subject,message,from_email,recipient_list)
        em.send(fail_silently=True)
        messages.success(request, "Thank you for contacting us! We will get back to you soon.")
        return redirect("contact")
    return render(request,"contact.html")


def register(request):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,}$'
    has_error=False
    if request.method=="POST":
        data=request.POST
        fname=data['firstname']
        username=data['username']
        lname=data['lastname']
        email=data['email']
        password=data['password']
        cpassword=data['cpassword']
        if User.objects.filter(email=email):
            messages.error(request,"email already exists")
            has_error=True
        if password != cpassword:
            messages.error(request,"password doesnot match")
            has_error=True
        if not re.match(pattern,password):
            messages.error(request,"Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, and one special character.")
            has_error=True
        if has_error == True:
            return redirect('register')
        User.objects.create_user(first_name=fname,username=username,last_name=lname,email=email,password=password)
    return render(request,"register.html")

def signin(request):
    if request.method=="POST":
        data=request.POST
        username=data['username']
        password=data['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"incorrect credentials!!!!!")
    return render(request,'login.html')
    


def log_out(request):
    logout(request)
    return redirect('signin')

def course(request):
    course=Course.objects.all()
    return render(request,"courses.html",{
        'course':course
    })


def description(request,id):
    aboutcourse=AboutCourse.objects.filter(id=id)
    course=Course.objects.filter(id=id)
    return render(request,"description.html",{
        "aboutcourse":aboutcourse,
        "course":course
    })


# def profile(request):
    # if request.user in request.user.profile.user:###since request.user.profile.user is not iterable it a single object hence error 
    #   pro=request.user.profile
    
    #   if request.method=="POST":
    #         data=request.POST
    #         user=data['user']
    #         profile=request.FILES.get('profile_image',pro.profile)
    #         pro.save()
    #         return redirect('home')
    # else:
    #     if request.method=="POST":
    #         user=request.user
    #         profile_image=request.FILES.get('profile_image')
    #         profile=Profile.objects.create(user=user,profile_image=profile_image)
    #         return redirect('home')
    # return render(request,"profile.html")
def profile(request):
    user = request.user

    # Check if profile exists
    try:
        pro = user.profile
        profile_exists = True
    except:
        pro = None
        profile_exists = False

    if request.method == "POST":
        profile_image = request.FILES.get('profile_image')

        if profile_exists:
            # Update existing profile image only if new image uploaded
            if profile_image:
                pro.profile = profile_image  # replace 'profile' with your image field name
            pro.save()
        else:
            # Create profile if none exists
            Profile.objects.create(user=user, profile=profile_image)

        return redirect('home')

    return render(request, "profile.html")

def profile_update(request):
    user = request.user
    pro = user.profile

    if request.method == "POST":
        data = request.POST
        files = request.FILES

        # Use get() to avoid KeyError if fields are missing
        username = data.get('username', user.username)
        first_name = data.get('first_name', user.first_name)
        last_name = data.get('last_name', user.last_name)

        # Check for uploaded file safely
        profile_image = files.get('profile_image', pro.profile)

        # Update user and profile objects
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        pro.profile = profile_image
        user.save()
        pro.save()

        return redirect('Profile')

    return render(request, "profile_update.html")



# def pay(request, id):

#     course = get_object_or_404(Course, id=id)
    
 
#     uid = str(uuid.uuid4())


#     payment = EsewaPayment(
#         product_code="EPAYTEST", 
#         amount=course.fee, 
#         tax_amount=0,
#         total_amount=course.fee,
#         product_delivery_charge=0,
#         product_service_charge=0,
#         transaction_uuid=uid,
#         success_url=f'http://localhost:8000/success/{uid}/',
#         failure_url=f'http://localhost:8000/failure/{uid}/',
#         secret_key=settings.secret_key 
#     )

   
#     signature = payment.create_signature()

  
#     form = payment.generate_form()

 
#     return render(request, "description.html", {
#         'form': form
#     })
def pay(request, id):
    course = get_object_or_404(Course, id=id)
    print("Course:", course.name, "| Fee:", course.fee)  # 👈 prints to terminal

    uid = str(uuid.uuid4())
    print("Generated UUID:", uid)  # 👈 prints the UUID

    transaction = Transaction.objects.create(
        course=course,
        transaction_uuid=uid,
        transaction_amount=course.fee,
        transaction_status='pending'
    )
    print("Transaction created:", transaction)

    payment = EsewaPayment(
        product_code="EPAYTEST",
        amount=course.fee,
        tax_amount=0,
        total_amount=course.fee,
        product_delivery_charge=0,
        product_service_charge=0,
        transaction_uuid=uid,
        success_url=f'http://localhost:8000/success/{transaction.id}/',
        failure_url=f'http://localhost:8000/failure/{transaction.id}/',
        secret_key=settings.esewa_secret_key,
    )

    signature = payment.create_signature()
    print("Signature:", signature)

    form = payment.generate_form()
    print("Form HTML:", form)

    return render(request, "description.html", {
        'form': form,
        'transaction': transaction,
        'course': course
    })


def success(request,id):
    return render(request,"success.html")

def failure(request,id):
    return render(request,"failure.html")






