from docusign_esign import TemplatesApi, Recipients, EnvelopeTemplate

from docusign.ds_client import DsClient
from docusign.document import create_document

from .templates.make_request_Contract_signer import make_request_Contract_signer

class Template:

    @staticmethod
    def get_existing(templates_api, account_id, template_request_object):
        """
        Returns the ID of the template if such a template already exists
        """
        templates = templates_api.list_templates(account_id)
        for template in templates.envelope_templates:
            if template.name == template_request_object.name:
                return template.template_id
        return None

    @classmethod
    def create(cls, session, template_request_object):
        """
        Create a template
        """
        api_client = DsClient.get_configured_instance(
            access_token=session["access_token"]
        )
        templates_api = TemplatesApi(api_client)
        account_id=session["account_id"]

        existing_template_id = cls.get_existing(templates_api, account_id, template_request_object)
        if existing_template_id is not None:
            return existing_template_id

        template = templates_api.create_template(
            account_id=account_id,
            envelope_template=template_request_object
        )
        return template.template_id

    @staticmethod
    def make_request(template_name, document, signer):
        """
        Make a template request
        """
        return EnvelopeTemplate(
            documents=[document],
            email_subject="Please sign this document",
            recipients=Recipients(signers=[signer]),
            description="Example template created via the MyHealthcare App",
            name=template_name,
            shared="false",
            status="sent"
        )

    @classmethod
    def make_request_Contract_signer(cls, workflow_id, args):
        """
        Make template_request for request_medical_records endpoint
        """
        template_name = "RequestContractSignTemplate"
        document = create_document("Cntract_release_form.pdf")
        signer = make_request_Contract_signer(workflow_id, args)

        return cls.make_request(template_name, document, signer)
