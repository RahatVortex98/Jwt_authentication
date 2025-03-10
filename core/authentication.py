from rest_framework_simplejwt.authentication import JWTAuthentication

class CookiesJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get the access token from cookies
        access_token = request.COOKIES.get('access_token')

        # If there's no token in cookies, return None (unauthenticated)
        if not access_token:
            return None

        # Validate the access token (checks if it's expired or invalid)
        validated_token = self.get_validated_token(access_token)

        try:
            # Get the user from the validated token
            user = self.get_user(validated_token)
        except:
            # If there's an error (e.g., user not found), return None (unauthenticated)
            return None

        # If everything is fine, return the user and the validated token
        return (user, validated_token)
