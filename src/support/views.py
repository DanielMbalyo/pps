from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db.models import Q
from django.http import Http404
from django.shortcuts import (get_object_or_404,  # render_to_response,
                              redirect, render, reverse)
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, UpdateView, View)
from django.views.generic.edit import FormMixin

from .forms import (ContactForm, NewsLetterForm, SingleMailForm,
                    SubscriptionForm)
from .models import Contact, NewsLetter


class ContactListView(LoginRequiredMixin, ListView):
    template_name = 'support/contact_list.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return Contact.objects.all()

    
class ContactView(LoginRequiredMixin, FormMixin, DetailView):
    model = Contact
    form_class = SingleMailForm
    template_name = 'support/contact_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        # create form to post comments
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        c_type = form.cleaned_data.get("content_type")
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")

        Faq.objects.get_or_create(
            user=self.request.user,
            object_id=obj_id,
            content=content_data,
        )
        return super(ContactView, self).form_valid(form)

    def form_invalid(self, form):
        return super(ContactView, self).form_invalid(form)

class MailPrefView(LoginRequiredMixin, UpdateView):
    form_class = SubscriptionForm
    template_name = 'base/forms.html' # yeah create this

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated():
            return redirect("/login/?next=/settings/email/") # HttpResponse("Not allowed", status=400)
        return super(MailPrefView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MailPrefView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Email Preferences'
        return context

    def get_object(self):
        user = self.request.user
        obj, created = NewsLetter.objects.get_or_create(user=user) # get_absolute_url
        return obj

class SingleMailView(LoginRequiredMixin, DetailView, FormMixin):
    model = Contact
    form_class = SingleMailForm
    template_name = 'support/contact_mail.html'

    def get_context_data(self, **kwargs):
        context = super(SingleMailView, self).get_context_data(**kwargs)
        package = self.request.session.get('package_id')
        package = Package.objects.get(id=package)
        initial_data = {    
			"subject": self.object.subject,
			"recipient": self.object.email,
        }
        context.update({
            'form': SingleMailForm(initial=initial_data),
            'package' : package,
        })
        return context

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        sender = form.cleaned_data['sender']
        cc_myself = form.cleaned_data['cc_myself']
        recipients = [form.cleaned_data['recipient']]
        if cc_myself:
            recipients.append(sender)
        send_mail(subject, message, sender, recipients)
        return super(SingleMailView, self).form_valid(form)
