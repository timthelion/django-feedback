#!/usr/bin/env python

from django.test import TestCase
from django.test.utils import override_settings
try:
    from django.urls import reverse
except ImportError:  # Django<2.0
    from django.core.urlresolvers import reverse

class ViewTestCase(TestCase):
    """Test project views."""

    def test_feedback_view(self):
        """A POST should log the error"""
        post_data = {
        "text": "sample test text",
        }
        response = self.client.post(reverse('feedback', kwargs={'url': 'test_url'}), post_data)
        self.assertEqual(response.content, b"{}")
        self.assertEqual(response.status_code, 200)

    def test_error_view(self):
        """A POST should log the error"""
        response = self.client.post(reverse('feedback', kwargs={'url': 'test_url'}))
        self.assertEqual(response.content, b'{"errors": {"text": ["This field is required."]}}')
        self.assertEqual(response.status_code, 200)


@override_settings(
    FEEDBACK_CAPTCHAS = [("foo", ["bar"])]
)
class ViewWithCaptchasTestCase(TestCase):
    def test_feedback_view_correct_captcha(self):
        post_data = {
        "text": "sample test text",
        "captcha": "bar",
        "captchaquestion": "foo",
        }
        response = self.client.post(reverse('feedback', kwargs={'url': 'test_url'}), post_data)
        self.assertEqual(response.content, b"{}")
        self.assertEqual(response.status_code, 200)

    def test_feedback_view_wrong_captcha(self):
        post_data = {
        "text": "sample test text",
        "captcha": "baz",
        "captchaquestion": "foo",
        }
        response = self.client.post(reverse('feedback', kwargs={'url': 'test_url'}), post_data)
        self.assertEqual(response.content, b'{"errors": {"captcha": ["Captcha incorrect"]}}')
        self.assertEqual(response.status_code, 200)

# vim: et sw=4 sts=4
