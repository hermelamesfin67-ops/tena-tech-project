
from django.db.models import Prefetch
from rest_framework import generics
from rest_framework.filters import SearchFilter
from django.db.models import Q, Prefetch
from .models import (Drug, DrugTranslation, Language, Category, 
                     CategoryTranslation, DrugWarning)
from .serializers import (
    DrugSerializer,
    LanguageSerializer,
    CategorySerializer,
    CategoryTranslationSerializer,
    DrugTranslationSerializer,
    DrugWarningSerializer,
    DrugInteractionSerializer,

)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .pagination import DrugPagination, CategoryPagination

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


class DrugListView(generics.ListAPIView):
    serializer_class = DrugSerializer
    pagination_class = DrugPagination

    filter_backends = [SearchFilter]

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
                    categories__translations__name__istartswith=search,
                    categories__translations__language__is_active=True,
                )
            )

        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(
                categories__slug=category
            )


        return queryset.order_by("id").distinct()

class DrugDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DrugSerializer
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


class LanguageListView(generics.ListAPIView):
    serializer_class = LanguageSerializer

    def get_queryset(self):
        return Language.objects.filter(is_active=True)


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = CategoryPagination

class LanguageCreateView(generics.CreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryTranslationCreateView(generics.CreateAPIView):
    queryset = CategoryTranslation.objects.all()
    serializer_class = CategoryTranslationSerializer


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

    serializer_class=DrugInteractionSerializer
     