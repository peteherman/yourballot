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

from yourballot.api.router import (all_question_router, candidate_router, voter_candidate_router, voter_opinions_router,
                                   voter_question_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/", include(all_question_router.urls)),
    path("v1/voter/", include(voter_question_router.urls)),
    path("v1/voter/", include(voter_candidate_router.urls)),
    path("v1/voter/opinions/", include(voter_opinions_router.urls)),
    path("v1/candidate/", include(candidate_router.urls))
]
