from itertools import chain
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.shortcuts import redirect, render, reverse, get_object_or_404

from src.support.forms import ContactForm, NewsLetterForm
from src.support.models import Contact
from src.project.models import Project

class HomeView(TemplateView):
    template_name = 'base/home.html'
    form_class = NewsLetterForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['testimony'] = Testimony.objects.all()
        context['project'] = Project.objects.all()[:3]
        context['gallery'] = Gallery.objects.all()[:6]
        context['form'] = NewsLetterForm
        return context