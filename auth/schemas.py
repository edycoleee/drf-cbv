from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from auth.serializers import (
    RegisterSerializer,
    UpdatePasswordSerializer,
    UserOutputSerializer
)

register_schema = extend_schema(
    request=RegisterSerializer,
    responses={201: UserOutputSerializer},
    examples=[
        OpenApiExample(
            "Register Example",
            value={"username": "user1", "password": "123456"},
        )
    ],
    description="Register a new user.",
)

update_password_schema = extend_schema(
    request=UpdatePasswordSerializer,
    responses={200: OpenApiResponse(description="Password updated")},
    examples=[
        OpenApiExample(
            "Update Password Example",
            value={"new_password": "newpass123"},
        )
    ],
    description="Update password. Requires authentication.",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            type=str,
            location=OpenApiParameter.HEADER,
            required=True,
            description='JWT access token. Format: Bearer <access_token>'
        )
    ]
)

logout_schema = extend_schema(
    responses={200: OpenApiResponse(description="Logout successful")},
    description="Logout current user. Requires authentication.",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            type=str,
            location=OpenApiParameter.HEADER,
            required=True,
            description='JWT access token. Format: Bearer <access_token>'
        )
    ]
)
