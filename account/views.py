from django.views.generic import View
from home.views import *
from django.contrib.auth.decorators import login_required
from home.models import *
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.conf import settings
import requests
from django.http.response import JsonResponse


def send_otp(request):
    if request.method == 'POST':
        phone = request.POST.get('phone', None)
        usr_otp = random.randint(100000, 999999)
        OTP.objects.create(phone_number=phone,otp=usr_otp)
        url = "https://www.fast2sms.com/dev/bulk"
        querystring = {
            "authorization": '2UB8HFSGq9Qz0bArckO7otPsMjfuYLR4gTm3n1iNWE5XKZlChD7uRKvnqsmNVU2Ify6dlZ5S8oFAXr13',
            "sender_id": "FSTSMS", "language": "english", "route": "qt", "numbers": phone, "message": 41704,
            "variables": "{BB}", "variables_values": usr_otp}

        headers = {
            'cache-control': "no-cache"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)
        return JsonResponse({'msg':response.json().get('message','')})


def signup(request):
    order = None
    phone_error = ''
    otp_error = ''
    phone = ''
    name = ''
    otp = ''
    pass_error = ''
    form = SignUpForm()
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(profile=request.user.profile, complete=False)
        except ObjectDoesNotExist:
            pass
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        phone = request.POST['phone_number']
        name = request.POST['name']
        otp = request.POST['otp']
        if form.is_valid():

            if User.objects.filter(username=form.cleaned_data['phone_number']).exists():
                phone_error = 'phone number already exists'
            elif not OTP.objects.filter(phone_number=form.cleaned_data['phone_number'],
                                        otp=form.cleaned_data['otp'], verified=False).exists():
                otp_error = "invalid otp"
            else:
                otp = OTP.objects.filter(phone_number=form.cleaned_data['phone_number'],
                                         otp=form.cleaned_data['otp'], verified=False).last()
                otp.verified = True
                otp.save()
                u = User.objects.create(username=form.cleaned_data['phone_number'])
                u.set_password('password1')
                u.save()
                UserProfile.objects.create(user=u, phone_number=u.username, name=form.cleaned_data['name'])
                login(request,u)
                return redirect('home:index')
    all_category = Category.objects.all()
    context={
        'Category':all_category,
        'order':order,
        'form': form,
        'phone_error':phone_error,
        'otp_error':otp_error,
        'phone':phone,
        'name':name,
        'otp':otp,
        'pass_error':pass_error
    }
    return render(request, 'registration/registration.html', context)






def authenticate_user(email, password):
    try:
        try:
            user = User.objects.get(email=email)
        except:
            try:
                user = User.objects.get(username=email)
            except:
                user = User.objects.get(profile__phone_number=email)
    except User.DoesNotExist:
        return None
    if user.check_password(password):
        return user

    return None


class LoginPage(View):
    template_name = 'registration/login.html'

    def get(self, request):
        order = None
        if request.user.is_authenticated:
            logout(request)
            return redirect('home:index')
        login_type = request.GET.get('type',None)
        if login_type == 'otp':
            self.template_name = 'registration/login_with_otp.html'
        all_category = Category.objects.all()
        context = {
            'Category': all_category,
            'order': order
        }
        return render(request, self.template_name, context)

    def post(self, request):
        error_msg = ''
        login_type = request.GET.get('type', None)
        order = None
        if request.user.is_authenticated:
            return redirect('home:index')

        if login_type == 'otp':
            self.template_name = 'registration/login_with_otp.html'
            if not User.objects.filter(username=request.POST['phone_number']).exists():
                error_msg = 'phone number is not registered with us'
            elif not OTP.objects.filter(phone_number=request.POST['phone_number'],
                                        otp=request.POST['otp'], verified=False).exists():
                error_msg = 'invalid otp'
            else:
                u = User.objects.get(username=request.POST['phone_number'])
                login(request, u)
                return redirect('home:index')
        else:
            if not User.objects.filter(username=request.POST['phone_number']).exists():
                error_msg = 'phone number is not registered with us'
            else:
                try:
                    u = User.objects.get(username=request.POST['phone_number'], password=request.POST['pass'])
                    login(request, u)
                    return redirect('home:index')
                except ObjectDoesNotExist:
                    print("here")
                    error_msg = 'phone number or password incorrect'
        context = {
            'Category': Category.objects.all(),
            'order': order,
            'error_msg':error_msg,
            'phone':request.POST['phone_number']
        }
        return render(request, self.template_name, context)


# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('change_password')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'change_password.html', {
#         'form': form
#     })


def resend_otp(request):
    if request.method == 'GET':
        get_phone = request.GET.get('usr_phone')
        print(get_phone)
        # get_phone = request.GET['usr_phone']
        if get_phone:
            print('i')
            try:
                print("-----------------------")
                usr = User.objects.get(profile__phone_number=get_phone)
                print('--------',usr)
            except:
                usr= None
            if usr is not None :
                usr_otp = random.randint(100000, 999999)
                try:
                    otps = UserOTP.objects.get(user = usr)
                    print(otps)
                    otps.otp = usr_otp
                    otps.save()
                except:
                    UserOTP.objects.create(user = usr, otp = usr_otp)
                # UserOTP.objects.create(user = usr, otp = usr_otp)
                url = "https://www.fast2sms.com/dev/bulk"
                querystring = {"authorization":'2UB8HFSGq9Qz0bArckO7otPsMjfuYLR4gTm3n1iNWE5XKZlChD7uRKvnqsmNVU2Ify6dlZ5S8oFAXr13',"sender_id":"FSTSMS","language":"english","route":"qt","numbers":phone,"message":41704,"variables":"{BB}","variables_values":usr_otp}

                headers = {
                    'cache-control': "no-cache"
                    }

                response = requests.request("GET", url, headers=headers, params=querystring)

                print(response.text)
                # url = "https://www.fast2sms.com/dev/bulk"
                #
                #
                # # create a dictionary
                # my_data = {
                #      # Your default Sender ID
                #     'sender_id': 'FSTSMS',
                #
                #      # Put your message here!
                #     'message': ' Your OTP for login is-'+ str(usr_otp),
                #
                #     'language': 'english',
                #     'route': 'p',
                #
                #     # You can send sms to multiple numbers
                #     # separated by comma.
                #     'numbers': get_phone
                # }
                #
                # # create a dictionary
                # headers = {
                #     'authorization': '2UB8HFSGq9Qz0bArckO7otPsMjfuYLR4gTm3n1iNWE5XKZlChD7uRKvnqsmNVU2Ify6dlZ5S8oFAXr13',
                #     'Content-Type': "application/x-www-form-urlencoded",
                #     'Cache-Control': "no-cache"
                # }
                # response = requests.request("POST",
                #         url,
                #         data = my_data,
                #         headers = headers)
                # #
                # # load json data from source
                # returned_msg = json.loads(response.text)
                #
                # # print the send message
                # print(returned_msg['message'])
                return HttpResponse("Resend")

        else:

            get_usr = request.GET.get('usr')
            if User.objects.filter(username = get_usr).exists() and not User.objects.get(username = get_usr).is_active:
                usr = User.objects.get(username=get_usr)
                usr_otp = random.randint(100000, 999999)
                UserOTP.objects.create(user = usr, otp = usr_otp)
                mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

                send_mail(
                    "Welcome to Souvenir Publisher - Verify Your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [usr.email],
                    fail_silently = False
                    )
                return HttpResponse("Resend")

    return HttpResponse("Can't Send ")

@login_required
def profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except:
        profile= None
    try:
        try:
            device = request.COOKIES['device']
            order = Order.objects.get(device=device,complete=False)
            if not order.device:
                order.device = device
            order.save()
        except:
            order = Order.objects.get(profile=profile,complete=False)

        if not order.order_num:
            order.order_num = generate_order_id()
        order.save()
    except:
        order = None
    category = Category.objects.all()
    # print(Category)
    subcate = subcategory.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        states = request.POST.get('states')
        postal_code = request.POST.get('postal_code')
        phone_number = request.POST.get('phone_number')
        country = request.POST.get('country')
        avatar = request.FILES.get('avatar')
        print("avatar=======",avatar)
        profile.name = name
        profile.email = email
        profile.address1 = address1
        profile.address2 = address2
        profile.city = city
        profile.states = states
        profile.postal_code = postal_code
        profile.phone_number = phone_number
        profile.country = country
        if avatar is None:
            pass
        else:
            profile.avatar = avatar
        profile.save()
    context={
    'Category':category,
    'sub':subcate,
    'order':order,
    'profile':profile
    }

    return render(request, 'profile.html',context)
