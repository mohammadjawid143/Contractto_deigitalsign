from rest_framework.serializers import ModelSerializer, CharField, EmailField
from .models import Contract


class RequestContratSerializer(ModelSerializer):
    full_name = CharField(required=True)
    recipient_email = EmailField(required=True)
    contract_text = CharField(required=True)

    class Meta:
        model = Contract
        fields = ['full_name', 'recipient_email', 'contract_text']
