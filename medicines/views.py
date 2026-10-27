from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Prefetch
from rest_framework import generics
from rest_framework.filters import SearchFilter
from django.db.models import Q, Prefetch
from .models import (Drug, DrugTranslation, Language, Category,
                     CategoryTranslation, DrugWarning, DrugInteraction,
                     DrugInteractionTranslation, DrugWarningTranslation,
                     DrugSource,User)
from .serializers import (
    DrugSerializer,
    LanguageSerializer,
    CategorySerializer,
    CategoryTranslationSerializer,
    DrugTranslationSerializer,
    DrugWarningSerializer,
    DrugInteractionSerializer,
    DrugInteractionTranslationSerializer,
    DrugWarningTranslationSerializer,
    DrugSourceSerializer,
    PharmacistCreateSerializer,
    MyTokenObtainPairSerializer
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .pagination import DrugPagination, CategoryPagination
from .permissions import IsSuperuserOnly, IsPharmacist


@api_view(["GET"])
def home(request):
    return Response({
        "message": "Welcome to Tenatech API",
        "status": "running",
        "endpoints": {
            "drugs": "/drugs/",
            "languages": "/languages/",
            "categories": "/categories/",
            "drug_warnings": "/drugs/warnings/",
        }
    })


class PharmacistListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsSuperuserOnly]
    serializer_class = PharmacistCreateSerializer

    def get_queryset(self):
        return User.objects.filter(role="pharmacist")


class PharmacistDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperuserOnly]
    serializer_class = PharmacistCreateSerializer
    def get_queryset(self):
         return User.objects.filter(role="pharmacist")

class MyLogin(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class DrugListView(generics.ListAPIView):
    serializer_class = DrugSerializer
    pagination_class = DrugPagination


    search_fields = [
        "generic_name",
        "brand_name",
        "translations__display_name",
    ]

    def get_queryset(self):
        queryset = Drug.objects.filter(
            is_active=True
        ).prefetch_related(
            Prefetch(
                "translations",
                queryset=DrugTranslation.objects.filter(
                    review_status=DrugTranslation.Status.PUBLISHED
                ).select_related("language"),
            )
        )

        search = self.request.query_params.get(
            "search", ""
        ).strip()

        if search:
            queryset = queryset.filter(
                Q(generic_name__istartswith=search)
                | Q(brand_name__istartswith=search)
                | Q(
                    translations__display_name__istartswith=search,
                    translations__review_status=(
                        DrugTranslation.Status.PUBLISHED
                    ),
                )
                | Q(
                    categories__translations__name__icontains=search,
                    categories__translations__language__is_active=True,
                )
            )

        category = self.request.query_params.get(
            "category", ""
        ).strip()
        if category:
            queryset = queryset.filter(
                categories__slug=category
            )

        return queryset.order_by("id").distinct()


class DrugDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DrugSerializer
    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    lookup_field = "id"

    def get_queryset(self):
        return Drug.objects.filter(
            is_active=True
        ).prefetch_related(
            Prefetch(
                "translations",
                queryset=DrugTranslation.objects.filter(
                    review_status=DrugTranslation.Status.PUBLISHED
                ),
            )
        )

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.save()

        return Response(
            {"message": "Drug deactivated successfully."},
            status=status.HTTP_200_OK
        )


class DrugCreateView(generics.CreateAPIView):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    permission_classes=[IsSuperuserOnly]


class LanguageListView(generics.ListAPIView):
    serializer_class = LanguageSerializer

    def get_queryset(self):
        return Language.objects.filter(is_active=True)
class LanguageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = CategoryPagination

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    
    queryset=Category.objects.all()
    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

class LanguageCreateView(generics.CreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes=[IsSuperuserOnly]


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes=[IsSuperuserOnly]


class CategoryTranslationCreateView(generics.CreateAPIView):
    queryset = CategoryTranslation.objects.all()
    serializer_class = CategoryTranslationSerializer
    permission_classes = [IsSuperuserOnly]


class CategoryTranslationListView(generics.ListAPIView):
    serializer_class = CategoryTranslationSerializer

    def get_queryset(self):
        queryset = CategoryTranslation.objects.all()

        language_code = self.request.query_params.get("language")

        if language_code:
            queryset = queryset.filter(
                language__code=language_code
            )

        return queryset


class DrugTranslationCreateView(generics.CreateAPIView):
    queryset = DrugTranslation.objects.all()
    serializer_class = DrugTranslationSerializer
    permission_classes = [IsSuperuserOnly]



class DrugTranslationListView(generics.ListAPIView):
    serializer_class = DrugTranslationSerializer

    def get_queryset(self):
        queryset = DrugTranslation.objects.all()

        language_code = self.request.query_params.get("language")

        if language_code:
            queryset = queryset.filter(
                language__code=language_code
            )

        return queryset


class DrugWarningCreateView(generics.CreateAPIView):
    queryset = DrugWarning.objects.all()
    serializer_class = DrugWarningSerializer
    permission_classes = [IsSuperuserOnly]

class DrugWarningListView(generics.ListAPIView):
    serializer_class = DrugWarningSerializer

    def get_queryset(self):
        queryset = DrugWarning.objects.all()

        drug_id = self.request.query_params.get("drug")

        if drug_id:
            queryset = queryset.filter(drug_id=drug_id)

        return queryset


class DrugInteractionListView(generics.ListAPIView):
    """List published drug interactions."""

    serializer_class = DrugInteractionSerializer

    def get_queryset(self):
        queryset = DrugInteraction.objects.filter(
            review_status=DrugInteraction.Status.PUBLISHED
        )

        drug_id = self.request.query_params.get("drug_id")

        if drug_id:
            queryset = queryset.filter(
                Q(drug_a_id=drug_id)
                | Q(drug_b_id=drug_id)
            )

        return queryset.select_related(
            "drug_a",
            "drug_b",
        ).prefetch_related(
            "sources",
            "translations",
        ).order_by("id")


class DrugInteractionCreateView(generics.CreateAPIView):
    serializer_class = DrugInteractionSerializer
    permission_classes = [IsSuperuserOnly]



class DrugInteractionTranslationListView(generics.ListAPIView):
    serializer_class = DrugInteractionTranslationSerializer

    def get_queryset(self):
        queryset = DrugInteractionTranslation.objects.all()

        language_code = self.request.query_params.get("language")

        if language_code:
            queryset = queryset.filter(
                language__code=language_code
            )

        return queryset


class DrugInteractionTranslationCreateView(generics.CreateAPIView):
    queryset = DrugInteractionTranslation.objects.all()
    serializer_class = DrugInteractionTranslationSerializer
    permission_classes = [IsSuperuserOnly]



class DrugWarningTranslationCreateView(generics.CreateAPIView):
    queryset = DrugWarningTranslation.objects.all()
    serializer_class = DrugWarningTranslationSerializer
    permission_classes = [IsSuperuserOnly]


class DrugWarningTranslationListView(generics.ListAPIView):
    serializer_class = DrugWarningTranslationSerializer

    def get_queryset(self):
        queryset = DrugWarningTranslation.objects.all()

        language_code = self.request.query_params.get("language")

        if language_code:
            queryset = queryset.filter(
                language__code=language_code
            )

        return queryset


class DrugSourceListView(generics.ListAPIView):
    serializer_class = DrugSourceSerializer

    def get_queryset(self):
        return DrugSource.objects.all()


class DrugSourceCreateView(generics.CreateAPIView):
    queryset = DrugSource.objects.all()
    serializer_class = DrugSourceSerializer
    permission_classes = [IsSuperuserOnly]
