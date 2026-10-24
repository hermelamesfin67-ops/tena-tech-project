from django.urls import path
from .views import (DrugListView, DrugDetailView, DrugCreateView, LanguageListView, CategoryListView
                    , LanguageCreateView, CategoryCreateView, CategoryTranslationCreateView
                    , CategoryTranslationListView,DrugTranslationListView,
                    DrugTranslationCreateView,DrugWarningListView, DrugWarningCreateView,home,
                    DrugInteractionListView, DrugInteractionCreateView,DrugInteractionTranslationCreateView
                    ,DrugWarningTranslationCreateView, DrugWarningTranslationListView,
                    DrugInteractionTranslationListView,DrugSourceCreateView, DrugSourceListView)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns=[
  
  path("", home, name="home"),
  path("login/,", TokenObtainPairView.as_view(), name="token_obtain_pair"),
  path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
  path("drugs/",DrugListView.as_view(),name="drug-list"),
  path("drugs/<uuid:id>/", DrugDetailView.as_view(), name="drug-detail"),
  path("drugs/create/", DrugCreateView.as_view(), name="drug-create"),
  path("languages/", LanguageListView.as_view(), name="language-list"),
  path("categories/", CategoryListView.as_view(), name="category-list"),
  path("languages/create/", LanguageCreateView.as_view(), name="language-create"),
  path("categories/create/", CategoryCreateView.as_view(), name="category-create"),
  path("categories/translations/create/", CategoryTranslationCreateView.as_view(), name="category-translation-create"),
  path("categories/translations/", CategoryTranslationListView.as_view(), name="category-translation-list"),
  path("drugs/translations/", DrugTranslationListView.as_view(), name="drug-translation-list"),
  path("drugs/translations/create/", DrugTranslationCreateView.as_view(), name="drug-translation-create"),
  path("drugs/warnings/", DrugWarningListView.as_view(), name="drug-warning-list"),
  path("drugs/warnings/create/", DrugWarningCreateView.as_view(), name="drug-warning-create"),
  path("drugs/warnings/translations/create/", DrugWarningTranslationCreateView.as_view(), name="drug-warning-translation-create"),
  path("drugs/warnings/translations/", DrugWarningTranslationListView.as_view(), name="drug-warning-translation-list"),
  path("drugs/interactions/", DrugInteractionListView.as_view(), name="drug-interaction-list"),
  path("drugs/interactions/create/", DrugInteractionCreateView.as_view(), name="drug-interaction-create"),
  path("drugs/interactions/translations/", DrugInteractionTranslationListView.as_view(), name="drug-interaction-translation-list"),
  path("drugs/interactions/translations/create/", DrugInteractionTranslationCreateView.as_view(), name="drug-interaction-translation-create"),
  path("drugs/sources/create/", DrugSourceCreateView.as_view(), name="drug-source-create"),
  path("drugs/sources/", DrugSourceListView.as_view(), name="drug-source-list"),
]