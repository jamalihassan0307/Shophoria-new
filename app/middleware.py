from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated and needs profile completion
        if request.user.is_authenticated and request.session.get('needs_profile_completion'):
            # Don't redirect if already on profile page to avoid redirect loops
            if not request.path.startswith('/profile/'):
                # Clear the flag and redirect to profile
                del request.session['needs_profile_completion']
                return redirect('profile')
        
        response = self.get_response(request)
        return response 