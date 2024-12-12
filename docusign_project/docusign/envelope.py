import os
from datetime import date, datetime
from docusign_esign import (
    EnvelopesApi,
    EnvelopeDefinition,
    TemplateRole,
    RecipientPhoneNumber,
    RecipientAdditionalNotification,
    RecipientViewRequest,
    Tabs,
    Text,
    Email
)
from .ds_client import DsClient

class Envelope:

    @staticmethod
    def send(session, envelope_definition):
        """
        Sending an envelope
        """
        api_client = DsClient.get_configured_instance(
            access_token=session["access_token"]
        )
        envelopes_api = EnvelopesApi(api_client)
        envelope = envelopes_api.create_envelope(
            account_id=session["account_id"],
            envelope_definition=envelope_definition
        )
        return envelope.envelope_id

    @staticmethod
    def create_request_contract_definition(args):
        """
        Creates envelope definition for request medical records endpoint
        """
        #Update template tabs
        email = Email(
          tab_label="email", value=args["email"]
        )

        tabs = Tabs(
          email_tabs=[email]
        )

        # create the envelope definition
        envelope_definition = EnvelopeDefinition(
            status="sent",  # requests that the envelope be created and sent.
            template_id=args["template_id"],
            email_subject="Please sign this document"
        )
        # Create template role elements to connect the signer and cc recipients
        # to the template
        signer = TemplateRole(
            email=args["email"],
            name=args["name"],
            role_name="signer",
            tabs=tabs
        )

        # Add the TemplateRole objects to the envelope object
        envelope_definition.template_roles = [signer]
        return envelope_definition

    @staticmethod
    def get_view_url(session, envelope_id, args):
        """
        Get the recipient view
        """

        # Create the recipient view request object
        recipient_view_request = RecipientViewRequest(
            authentication_method="None",
            client_user_id="1000",
            recipient_id="1",
            return_url=args["return_url"],
            user_name=f'{args["first_name"]} {args["last_name"]}',
            email=args["email"],
            frame_ancestors=[os.environ.get('REACT_APP_DS_RETURN_URL'), "https://apps-d.docusign.com"],
            message_origins=["https://apps-d.docusign.com"]
        )
        # Obtain the recipient view URL for the signing ceremony
        # Exceptions will be caught by the calling function
        ds_client = DsClient.get_configured_instance(session.get('access_token'))

        envelope_api = EnvelopesApi(ds_client)
        recipient_view = envelope_api.create_recipient_view(
            session.get('account_id'),
            envelope_id,
            recipient_view_request=recipient_view_request
        )
        return recipient_view.url
