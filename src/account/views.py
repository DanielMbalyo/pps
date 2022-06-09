import string, random
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordChangeView, PasswordResetConfirmView, PasswordResetView)
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.utils.safestring import mark_safe
from django.views.generic import FormView, TemplateView, UpdateView, CreateView

from .forms import (ActivateForm, ChangePassForm, LoginForm, ResetPassForm,
                    SetPassForm, UserForm, RegistrationForm)
from .models import EmailActivation

User = get_user_model()

class RegisterView(FormView):
    form_class = RegistrationForm
    template_name = 'account/register.html'

    def get_success_url(self):
        return reverse('account:login')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Create Account'
        return context

    def post(self, form):
        email = self.request.POST.get("email")
        type = self.request.POST.get("type")
        self.request.session['email'] = email
        self.request.session['type'] = type
        if type == 'client':
            return redirect(reverse('client:policy'))
        else:
            return redirect(reverse('shop:policy'))

class AdminActivateView(TemplateView):
    template_name = 'accounts/resend_activation.html'
    key = None

    def get(self, request, *args, key=None, **kwargs):
        self.key = key
        if key is not None:
            if request.user.staff:
                qs = User.objects.filter(uid__iexact=key)
                if qs.count() > 0:
                    temp = EmailActivation.objects.create(user=qs.first(), email=qs.first().email)
                    temp.send_activation()
                    messages.success(request, "Account Is Now Activated.")
                    if qs.first().staff:
                        return redirect('manager:list')
                    elif qs.first().business:
                        return redirect('shop:list')
                    else:
                        return redirect('client:list')
            else:
                messages.success(request, "Account Is Not Activated.")
                return redirect('account:login')
        else:
            messages.success(request, "Account Is Not Activated.")
            return redirect('client:list')

class EmailActivateView(FormView):
    form_class = ActivateForm
    template_name = 'accounts/resend_activation.html'
    key = None

    def get_success_url(self):
        return reverse('account:login')

    def get(self, request, *args, key=None, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                form = ActivateForm(initial={'email' : obj.email})
                messages.success(
                    request, "Your email has been confirmed. Please change password to finalize.")
                context = {'form': form, 'key': key,}
                return render(request, 'account/activate_acc.html', context)
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse('account:password_reset')
                    msg = """Your email has already been confirmed
                    Do you need to <a href="{link}">reset your password</a>?
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect('account:login')
        return redirect('account:login')

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        pass2 = form.cleaned_data.get("password2")
        u = User.objects.get(email=email)
        u.set_password(pass2)
        u.save()
        messages.success(self.request, """Activation completed please login to continue.""")
        return redirect('account:login')

    def form_invalid(self, form):
        context = {'form': form, "key": self.key}
        return render(self.request, 'account/activate_acc.html', context)

class DeactivateView(TemplateView):
    template_name = 'accounts/resend_activation.html'
    key = None

    def get(self, request, *args, key=None, **kwargs):
        self.key = key
        if key is not None:
            qs = User.objects.get(uid=key)
            if qs.is_active == True:
                qs.is_active=False
                qs.save()
                messages.success(request, "User is Deactivated.")
            if qs.staff:
                return redirect('manager:list')
            else:
                return redirect('client:list')

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'

    # def get(self, *args, **kwargs):
    #     if self.request.user.is_authenticated and not self.request.user.is_admin:
    #         return redirect(self.request.user.get_absolute_url())
    #     return render(self.request, 'account/login.html', {'form': self.get_form()})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(request=self.request)
        return kwargs

    def form_valid(self, form):
        email = self.request.POST.get("email")
        password = self.request.POST.get("password")
        remember_me = self.request.POST.get('remember_me')
        qs = User.objects.filter(email=email)
        if qs.exists():
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                link = reverse('account:resend_activation')
                reconfirm_msg = """Go to <a href='{resend_link}'>
                resend confirmation email</a>.
                """.format(resend_link=link)
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    msg1 = """Please check your email to confirm your
                    account or """ + reconfirm_msg.lower()
                    messages.success(self.request, mark_safe(msg1))
                    return redirect('account:login')
                email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists:
                    msg2 = "Email not confirmed. " + reconfirm_msg
                    messages.success(self.request, mark_safe(msg2))
                    return redirect('account:login')
                if not is_confirmable and not email_confirm_exists:
                    messages.success(self.request, "This user is inactive.")
                    return redirect('account:login')
            user = authenticate(self.request, username=email, password=password)
            if user is None:
                messages.success(self.request, "Invalid credentials")
                return redirect('account:login')
            else: 
                login(self.request, user)
                if remember_me:
                    self.request.session.set_expiry(1209600)
                return redirect(user.get_absolute_url())
        messages.success(self.request, "Invalid user")
        return redirect('account:login')

    def form_invalid(self, form):
        context = {'form': form,}
        return render(self.request, 'account/login.html', context)

class SettingView(LoginRequiredMixin, TemplateView):
    template_name = 'account/settings_account.html'

    def get_context_data(self, **kwargs):
        context = super(SettingView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.staff:
            manager = user.manager_set.all().first()
            context["acc_form"] = ManagerForm(self.request.POST or None, instance=manager)
        else:
            client = user.client_set.all().first()
            address = Address.objects.filter(client=client).first()
            context["acc_form"] = ClientForm(self.request.POST or None, instance=client)
            context["address_form"] = AddressForm(self.request.POST or None, instance=address)
        context["user_form"] = UserForm(self.request.POST or None, instance=self.request.user)
        context['pass_form'] = ChangePassForm(self.request.POST or None,)
        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm

    def get_success_url(self):
        return reverse('account:setting')

class ChangePassView(LoginRequiredMixin, PasswordChangeView):
    form_class = ChangePassForm

    def form_valid(self):
        messages.success(self.request, '''Your password has been set. You may go ahead and log in now.''')
        reverse('account:login')

class ResetPassView(PasswordResetView):
    form_class = ResetPassForm
    template_name = 'account/reset_pass.html'
    email_template_name = 'account/emails/reset_email.html'

    def get_success_url(self):
        return reverse('account:login')

    def form_valid(self):
        messages.success(self.request, '''We\'ve emailed you instructions for setting your password,
            if an account exists with the email you entered. You should receive them shortly.\n
            If you don't receive an email, please make sure you've entered the address you registered with,
            and check your spam folder.''')
        reverse('account:login')

class ResetPassConfirmView(PasswordResetConfirmView):
    form_class = SetPassForm
    template_name = 'account/reset_pass_confirm.html'

    def form_valid(self):
        messages.success(self.request, 'Your password has been set. You may go ahead and log in now.')
        return reverse('account:login')
