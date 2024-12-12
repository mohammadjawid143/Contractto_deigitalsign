from django.db import models
from django.contrib.auth.models import User

class Contract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_contracts")
    recipient_email = models.EmailField()
    full_name = models.CharField(max_length=100, default="Default Name")
    envelope_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, default="draft")  # Can be 'draft', 'sent', 'signed', etc.
    contract_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contract by {self.user.username} for {self.recipient_email}"
