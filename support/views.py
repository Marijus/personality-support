import logging

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic import FormView, TemplateView

from common.external_services.brevo.client import BrevoClient
from support.forms import SupportForm


class SupportView(FormView):
    template_name = "support.html"
    form_class = SupportForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')

        email_html = render_to_string(
            "emails/support_request.html",
            context=form.cleaned_data,
        )

        try:
            BrevoClient(api_key=settings.BREVO_API_KEY).send_email(
                from_email=settings.BREVO_FROM_EMAIL,
                emails=[settings.BREVO_FROM_EMAIL],
                subject=f"URGENT: {email} refund request",
                email_html=email_html,
                reply_to=email,
            )
        except Exception:
            logging.exception("Failed to send support email for %s", email)
            messages.error(self.request, "Something went wrong. Please try again later.")
            return redirect('support')

        logging.info("Support request received. domain: %s, data: %s", self.request.get_host(), form.cleaned_data)
        return redirect('thank-you')


class ThankYouView(TemplateView):
    template_name = "thank_you.html"
