"""
URL configuration for yourballot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from yourballot.api.router import (all_question_router, candidate_router, guest_match_router, guest_questions_router,
                                   voter_candidate_router, voter_opinions_router, voter_question_router,
                                   voter_register_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/", include(all_question_router.urls)),
    path("v1/voter/", include(voter_question_router.urls)),
    path("v1/voter/", include(voter_candidate_router.urls)),
    path("v1/voter/register/", include(voter_register_router.urls)),
    path("v1/voter/opinions/", include(voter_opinions_router.urls)),
    path("v1/candidate/", include(candidate_router.urls)),
    path("v1/guest/candidates/", include(guest_match_router.urls)),
    path("v1/guest/questions/", include(guest_questions_router.urls)),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
