from django.urls import path
from .views import (DrugListView, DrugDetailView, DrugCreateView, LanguageListView, CategoryListView, LanguageCreateView, CategoryCreateView, CategoryTranslationCreateView, CategoryTranslationListView, DrugTranslationListView,
                    DrugTranslationCreateView, DrugWarningListView, DrugWarningCreateView, home,
                    DrugInteractionListView, DrugInteractionCreateView, DrugInteractionTranslationCreateView, DrugWarningTranslationCreateView, DrugWarningTranslationListView,
                    DrugInteractionTranslationListView, DrugSourceCreateView, DrugSourceListView, PharmacistDetailView, PharmacistListCreateView,
                    LanguageDetailView, MyLogin, CategoryDetailView, DrugTranslationPublishView, DrugTranslationRejectView,

                    DrugWarningRejectView, DrugWarningPublishView, DrugWarningTranslationPublishView, DrugWarningTranslationRejectView,
                    DrugInteractionRejectView, DrugInteractionDetailView, 
                     DrugInteractionPublishView, 
                    DrugInteractionTranslationRejectView,DrugInteractionTranslationPublishView,
                    DrugTranslationDetailView, CategoryTranslationDetailView, DrugInteractionTranslationDetailView
                    , DrugWarningDetailView, DrugSourceDetailView, DrugWarningTranslationDetailView,
                    DraftDrugTranslationListView, DraftDrugInteractionListView, DraftDrugWarningListView)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("", home, name="home"),
    path("token/", MyLogin.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("create/pharmacist/", PharmacistListCreateView.as_view(),
         name="create_pharmacist"),
    path("pharmacist/detail/<int:pk>/",
         PharmacistDetailView.as_view(), name="detail_view"),
    path("drugs/", DrugListView.as_view(), name="drug-list"),
    path("drugs/<uuid:id>/", DrugDetailView.as_view(), name="drug-detail"),
    path("drugs/create/", DrugCreateView.as_view(), name="drug-create"),
    path("languages/", LanguageListView.as_view(), name="language-list"),
    path("language/<int:pk>/", LanguageDetailView.as_view(), name="language-detail"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/",CategoryDetailView.as_view(),
         name="category-detail"),
    path("languages/create/", LanguageCreateView.as_view(), name="language-create"),
    path("categories/create/", CategoryCreateView.as_view(), name="category-create"),
    path("categories/translations/create/",
         CategoryTranslationCreateView.as_view(), name="category-translation-create"),
    path("categories/translations/", CategoryTranslationListView.as_view(),
         name="category-translation-list"),
    path("drugs/translations/", DrugTranslationListView.as_view(),
         name="drug-translation-list"),
    path("drugs/translations/create/", DrugTranslationCreateView.as_view(),
         name="drug-translation-create"),
    path("drugs/warnings/", DrugWarningListView.as_view(),
         name="drug-warning-list"),
    path("drugs/warnings/create/", DrugWarningCreateView.as_view(),
         name="drug-warning-create"),
    path("drugs/warnings/translations/create/",
         DrugWarningTranslationCreateView.as_view(), name="drug-warning-translation-create"),
    path("drugs/warnings/translations/", DrugWarningTranslationListView.as_view(),
         name="drug-warning-translation-list"),
    path("drugs/interactions/", DrugInteractionListView.as_view(),
         name="drug-interaction-list"),
    path("drugs/interactions/create/", DrugInteractionCreateView.as_view(),
         name="drug-interaction-create"),
    path("drugs/interactions/translations/", DrugInteractionTranslationListView.as_view(),
         name="drug-interaction-translation-list"),
    path("drugs/interactions/translations/create/",
         DrugInteractionTranslationCreateView.as_view(), name="drug-interaction-translation-create"),
    path("drugs/sources/create/", DrugSourceCreateView.as_view(),
         name="drug-source-create"),
    path("drugs/sources/", DrugSourceListView.as_view(), name="drug-source-list"),

    path(
        "drugs/translations/<int:pk>/publish/",
        DrugTranslationPublishView.as_view(),
        name="drug-translation-publish",
    ),
    path(
        "drugs/translations/<int:pk>/reject/",
        DrugTranslationRejectView.as_view(),
        name="drug-translation-reject",
    ),

    path(
        "drugs/warnings/<int:pk>/publish/",
        DrugWarningPublishView.as_view(),
        name="drug-warning-publish",
    ),
    path(
        "drugs/warnings/<int:pk>/reject/",
        DrugWarningRejectView.as_view(),
        name="drug-warning-reject",
    ),

    path(
        "drugs/warnings/translations/<int:pk>/publish/",
        DrugWarningTranslationPublishView.as_view(),
        name="drug-warning-translation-publish",
    ),
    path(
        "drugs/warnings/translations/<int:pk>/reject/",
        DrugWarningTranslationRejectView.as_view(),
        name="drug-warning-translation-reject",
    ),
    path(
        "drugs/interactions/<int:pk>/",
        DrugInteractionDetailView.as_view(),
        name="drug-interaction-detail",
    ),

    path("drugs/interactions/<int:pk>/publish/", DrugInteractionPublishView.as_view(),
         name="drug-interaction-publish"),
    path("drugs/interactions/<int:pk>/reject/", DrugInteractionRejectView.as_view(),
         name="drug-interaction-reject"),
 
    path(
        "drugs/interaction-translations/<int:pk>/publish/",
        DrugInteractionTranslationPublishView.as_view(),
        name="interaction-translation-publish",
    ),
    path(
        "drugs/interaction-translations/<int:pk>/reject/",
        DrugInteractionTranslationRejectView.as_view(),
        name="interaction-translation-reject",
    ),

    path(
        "drug-translations/<int:pk>/",
        DrugTranslationDetailView.as_view(),
        name="drug-translation-detail",
    ),
    path(
        "category-translations/<int:pk>/",
        CategoryTranslationDetailView.as_view(),
        name="category-translation-detail",
    ),
    path(
        "drug-interaction-translations/<int:pk>/",
        DrugInteractionTranslationDetailView.as_view(),
        name="drug-interaction-translation-detail",
    ),
    path(
        "drug-warnings/<int:pk>/",
        DrugWarningDetailView.as_view(),
        name="drug-warning-detail",
    ),
    path(
        "drug-warning-translations/<int:pk>/",
        DrugWarningTranslationDetailView.as_view(),
        name="drug-warning-translation-detail",
    ),
    path(
        "drug-sources/<int:pk>/",
        DrugSourceDetailView.as_view(),
        name="drug-source-detail",
    ),
    path(
        "drug-translations/drafts/",
        DraftDrugTranslationListView.as_view(),
        name="draft-drug-translations",
    ),
    path(
        "drug-warnings/drafts/",
        DraftDrugWarningListView.as_view(),
        name="draft-drug-warnings",
    ),
    path(
        "drug-interactions/drafts/",
        DraftDrugInteractionListView.as_view(),
        name="draft-drug-interactions",
    ),
]
