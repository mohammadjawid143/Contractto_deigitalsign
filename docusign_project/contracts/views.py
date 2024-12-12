from django.shortcuts import render, redirect, get_object_or_404
from .models import Contract
from docusign.envelope import Envelope
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from docusign.template import Template
from docusign.workflow import get_idv_workflow, is_sms_workflow
from .serializers import RequestContratSerializer
from docusign_project.utils import error_processing

def home(request):
    return render(request, 'contracts/index.html')


@login_required
@api_view(['POST'])
@error_processing
def request_contact_sign(request):
    access_token = request.session.get('access_token')
    if not access_token:
        return Response({"error": "Access token not found. Please log in again."}, status=401)
    
    serializer = RequestContratSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    args = serializer.validated_data.copy()

    workflow_id = get_idv_workflow(request.session)
    if not workflow_id:
        return Response({"error": "IDV is not enabled in your account."}, status=400)

    try:
        template_request = Template.make_request_Contract_signer(workflow_id, args)
        template_id = Template.create(request.session, template_request)

        args["template_id"] = template_id
        envelope_definition = Envelope.create_request_contract_definition(args)
        envelope_id = Envelope.send(request.session, envelope_definition)

        return Response({"message": "Successfully sent request", "envelope_id": envelope_id})
    except Exception as e:
        return Response({"error": str(e)}, status=500)

# @login_required
# def create_contract(request):
#     # Authenticate with DocuSign if the session is missing required keys
#     if "access_token" not in request.session:
#         auth_data = authenticate_with_docusign()
#         if auth_data is None:
#             return render(request, "contracts/error.html", {"message": "Failed to authenticate with DocuSign."})
#         request.session["access_token"] = auth_data["access_token"]
#         request.session["account_id"] = auth_data["account_id"]

#     if request.method == 'POST':
#         form = ContractForm(request.POST, request.FILES)
#         if form.is_valid():
#             contract = form.save(commit=False)
#             contract.user = request.user  # Associate the contract with the logged-in user
#             contract.save()

#             # Create DocuSign envelope definition using the contract
#             envelope_definition = Envelope.create_contract_envelope_definition(contract)

#             # Send the envelope and get the envelope ID
#             envelope_id = Envelope.send(
#                 session=request.session, 
#                 envelope_definition=envelope_definition
#             )

#             # Save the envelope ID and status to the contract
#             contract.envelope_id = envelope_id
#             contract.status = 'sent'
#             contract.save()

#             # Redirect the user to the contract details page
#             return redirect('contract_detail', contract_id=contract.id)

#     else:
#         form = ContractForm()

#     return render(request, 'contracts/create_contract.html', {'form': form})

def contract_detail(request, contract_id):
    contract = Contract.objects.get(id=contract_id)
    if contract.status == 'sent':
        view_url = Envelope.get_view_url(request.session, contract.envelope_id, contract)
        return redirect(view_url)

    return render(request, 'contracts/contract_detail.html', {'contract': contract})

def all_contract(request):
    contract = Contract.objects.all()
    context ={
        "contract": contract
    }
    return render(request,"contracts/contract_all.html",context)

@login_required
def contract_delete(request, contract_id):
    
    contract = get_object_or_404(Contract, id=contract_id)
    
    # # Ensure only the creator can delete the contract
    # if request.user != contract.user:
    #     return HttpResponseForbidden("You are not authorized to delete this contract.")
    
    # Handle deletion for POST requests
    if request.method == "POST":
        contract.delete()
        return redirect('contracts_all')  # Redirect to the homepage or contract list after deletion


def contract_detail(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    return render(request, 'contracts/contract_detail.html', {'contract': contract})
