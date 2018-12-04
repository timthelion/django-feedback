#!/usr/bin/env python
from django import forms
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from feedback.models import Feedback

class FeedbackForm(forms.ModelForm):
    '''The form shown when giving feedback'''
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.captchas = getattr(settings, 'FEEDBACK_CAPTCHAS', {})
        if self.captchas:
            self.fields['captchaquestion'] = forms.CharField()
            self.fields['captcha'] = forms.CharField()

    def clean_captcha(self):
       for question, answers in self.captchas:
           if self.cleaned_data['captchaquestion'] == question and self.cleaned_data['captcha'] in answers:
               return self.cleaned_data['captcha']
       if self.captchas:
           raise forms.ValidationError(_("Captcha incorrect"))
       return self.cleaned_data['captcha']

    class Meta:
        model = Feedback
        fields = "__all__"
        #exclude = ('site', 'url')

# vim: et sw=4 sts=4
