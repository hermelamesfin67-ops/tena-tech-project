
from .models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import (
    Language,
    Category,
    CategoryTranslation,
    Drug,
    DrugTranslation,
    DrugWarning,
    DrugWarningTranslation,
    DrugInteraction,
    DrugInteractionTranslation,
    DrugSource,
)
from django.contrib.auth.models import Group
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class PharmacistCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return User.objects.create_user(
            **validated_data,
            role="pharmacist"
        )


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "role": (
                "superuser"
                if self.user.is_superuser
                else self.user.role
            )
        }
        return data


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = [
            "id",
            "code",
            "name",
            "native_name",
            "is_active",
        ]
        read_only_fields = ["id"]


class CategoryTranslationSerializer(serializers.ModelSerializer):
    language_code = serializers.CharField(
        source="language.code",
        read_only=True,
    )

    class Meta:
        model = CategoryTranslation
        fields = [
            "id",
            "language",
            "language_code",
            "category",
            "name",
            "description",
        ]
        read_only_fields = ["id"]


class CategorySerializer(serializers.ModelSerializer):
    translations = CategoryTranslationSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Category
        fields = [
            "id",
            "slug",
            "translations",
        ]
        read_only_fields = ["id"]


class DrugTranslationSerializer(serializers.ModelSerializer):
    language_code = serializers.CharField(
        source="language.code",
        read_only=True,
    )

    class Meta:
        model = DrugTranslation
        fields = [
            "id",
            "drug",
            "language",
            "language_code",
            "display_name",
            "short_description",
            "what_it_treats",
            "how_to_use",
            "when_to_use",
            "side_effects",
            "storage_instructions",
            "review_status",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "review_status",
            "updated_at",
        ]


class DrugSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        required=False,
    )

    translations = DrugTranslationSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Drug
        fields = [
            "id",
            "generic_name",
            "brand_name",
            "strength",
            "dosage_form",
            "categories",
            "translations",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "translations",
            "created_at",
            "updated_at",
        ]


class DrugSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugSource
        fields = [
            "id",
            "title",
            "organization",
            "url",
            "source_type",
            "publication_date",
            "accessed_at",
            "notes",
        ]
        read_only_fields = ["id"]


class DrugWarningTranslationSerializer(
        serializers.ModelSerializer):
    language_code = serializers.CharField(
        source="language.code",
        read_only=True,
    )

    class Meta:
        model = DrugWarningTranslation
        fields = [
            "id",
            "warning",
            "language",
            "language_code",
            "title",
            "description",
            "recommended_action",
            "review_status",
            "reviewed_by",
            "reviewed_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "review_status",
            "reviewed_by",
            "reviewed_at",
            "updated_at",
        ]


class DrugWarningSerializer(serializers.ModelSerializer):
    translations = DrugWarningTranslationSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = DrugWarning
        fields = [
            "id",
            "drug",
            "warning_type",
            "sources",
            "review_status",
            "translations",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "review_status",
            "translations",
            "created_at",
            "updated_at",
        ]


class DrugInteractionTranslationSerializer(
    serializers.ModelSerializer
):
    language_code = serializers.CharField(
        source="language.code",
        read_only=True,
    )

    class Meta:
        model = DrugInteractionTranslation
        fields = [
            "id",
            "interaction",
            "language",
            "language_code",
            "explanation",
            "recommended_action",
            "review_status",
            "reviewed_by",
            "reviewed_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "review_status",
            "reviewed_by",
            "reviewed_at",
            "updated_at",
        ]


class DrugInteractionSerializer(serializers.ModelSerializer):
    drug_a_name = serializers.CharField(
        source="drug_a.generic_name",
        read_only=True,
    )
    drug_b_name = serializers.CharField(
        source="drug_b.generic_name",
        read_only=True,
    )
    translations = DrugInteractionTranslationSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = DrugInteraction
        fields = [
            "id",
            "drug_a",
            "drug_a_name",
            "drug_b",
            "drug_b_name",
            "severity",
            "sources",
            "review_status",
            "translations",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "review_status",
            "translations",
            "created_at",
            "updated_at",
        ]

    def get_translations(self, obj):
        published_translations = obj.translations.filter(
            review_status=DrugInteraction.Status.PUBLISHED
        )
        return DrugInteractionTranslationSerializer(
            published_translations,
            many=True,
            context=self.context,
        ).data

    def validate(self, attrs):
        drug_a = attrs.get(
            "drug_a",
            getattr(self.instance, "drug_a", None),
        )
        drug_b = attrs.get(
            "drug_b",
            getattr(self.instance, "drug_b", None),
        )

        if drug_a and drug_b and drug_a.pk == drug_b.pk:
            raise serializers.ValidationError({
                "drug_b": "A drug cannot interact with itself."
            })

        return attrs
