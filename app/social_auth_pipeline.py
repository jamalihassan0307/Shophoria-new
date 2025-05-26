from social_core.pipeline.user import get_username
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Customer

def save_google_user_details(backend, user, response, *args, **kwargs):
    """
    Pipeline function to save additional user details from Google OAuth2
    """
    if backend.name == 'google-oauth2':
        # Get user details from Google response
        email = response.get('email', '')
        first_name = response.get('given_name', '')
        last_name = response.get('family_name', '')
        
        # Update user details if they exist
        if email:
            user.email = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        
        # Save the user
        user.save()
        
        # Check if user has a complete profile
        try:
            customer = Customer.objects.get(user=user)
            # If customer exists but has incomplete profile, set a flag in the session
            if not all([customer.name, customer.locality, customer.city, customer.zipcode, customer.state]):
                kwargs['request'].session['needs_profile_completion'] = True
        except Customer.DoesNotExist:
            # Create a basic customer profile with just the name
            customer = Customer.objects.create(
                user=user,
                name=f"{first_name} {last_name}".strip() or user.username,
                locality="",  # Empty string instead of null
                city="",     # Empty string instead of null
                zipcode=0,   # Default value instead of null
                state="Punjab"  # Default state
            )
            # Set flag in session to indicate profile completion is needed
            kwargs['request'].session['needs_profile_completion'] = True
    
    return None 