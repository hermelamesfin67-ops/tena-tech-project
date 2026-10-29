from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = "user", "User"
        PHARMACIST = "pharmacist", "Pharmacist"
        ADMIN = "admin", "Administrator"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    native_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.native_name


class Category(models.Model):
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class CategoryTranslation(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="translations",
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["category", "language"],
                name="unique_category_translation",
            )
        ]


class Drug(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    generic_name = models.CharField(max_length=255, db_index=True)
    brand_name = models.CharField(max_length=255, blank=True)
    strength = models.CharField(max_length=100, blank=True)
    dosage_form = models.CharField(max_length=100, blank=True)

    categories = models.ManyToManyField(
        Category,
        related_name="drugs",
        blank=True,
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.generic_name} {self.strength}".strip()


class DrugTranslation(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        REVIEWED = "reviewed", "Reviewed"
        PUBLISHED = "published", "Published"
        REJECTED = "rejected", "Rejected"

    drug = models.ForeignKey(
        Drug,
        on_delete=models.CASCADE,
        related_name="translations",
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        related_name="drug_translations",
    )

    display_name = models.CharField(max_length=255)
    short_description = models.TextField(blank=True)
    what_it_treats = models.TextField(blank=True)
    how_to_use = models.TextField(blank=True)
    when_to_use = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)
    warnings = models.TextField(blank=True)
    storage_instructions = models.TextField(blank=True)

    review_status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    rejection_reason = models.TextField(
        blank=True,
        default="",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["drug", "language"],
                name="unique_drug_translation",
            )
        ]

    def __str__(self):
        return f"{self.display_name} ({self.language.code})"


class DrugInteraction(models.Model):
    """Represents a possible interaction between two different drugs."""

    class Severity(models.TextChoices):
        MINOR = "minor", "Minor"
        MODERATE = "moderate", "Moderate"
        MAJOR = "major", "Major"
        CONTRAINDICATED = "contraindicated", "Contraindicated"
        UNKNOWN = "unknown", "Unknown"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        REVIEWED = "reviewed", "Reviewed"
        PUBLISHED = "published", "Published"
        REJECTED = "rejected", "Rejected"

    drug_a = models.ForeignKey(
        Drug,
        on_delete=models.PROTECT,
        related_name="interactions_as_a",
    )
    drug_b = models.ForeignKey(
        Drug,
        on_delete=models.PROTECT,
        related_name="interactions_as_b",
    )

    severity = models.CharField(
        max_length=20,
        choices=Severity.choices,
        default=Severity.UNKNOWN,
    )
    review_status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    rejection_reason = models.TextField(
        blank=True,
        default="",
    )
    sources = models.ManyToManyField(
        "DrugSource",
        related_name="interactions",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.drug_a_id and self.drug_b_id:
            if self.drug_a_id == self.drug_b_id:
                raise ValidationError(
                    "A drug cannot interact with itself."
                )

    def save(self, *args, **kwargs):
        if self.drug_a_id and self.drug_b_id:
            if self.drug_a_id == self.drug_b_id:
                raise ValidationError(
                    "A drug cannot interact with itself."
                )
            if str(self.drug_a_id) > str(self.drug_b_id):
                self.drug_a_id, self.drug_b_id = (
                    self.drug_b_id,
                    self.drug_a_id,
                )
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["drug_a", "drug_b"],
                name="unique_drug_interaction_pair",
            ),
            models.CheckConstraint(
                condition=~models.Q(drug_a=models.F("drug_b")),
                name="different_drugs_in_interaction",
            ),
        ]

    def __str__(self):
        return f"{self.drug_a} + {self.drug_b}"


class DrugInteractionTranslation(models.Model):
    """Stores interaction explanations in individual languages."""

    interaction = models.ForeignKey(
        DrugInteraction,
        on_delete=models.CASCADE,
        related_name="translations",
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        related_name="interaction_translations",
    )

    explanation = models.TextField()
    recommended_action = models.TextField(blank=True)

    review_status = models.CharField(
        max_length=20,
        choices=DrugInteraction.Status.choices,
        default=DrugInteraction.Status.DRAFT,
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_interaction_translations",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["interaction", "language"],
                name="unique_interaction_translation",
            )
        ]

    def __str__(self):
        return (
            f"{self.interaction} - "
            f"{self.language.code}"
        )


class DrugWarning(models.Model):
    """Stores a specific warning associated with a drug."""

    class WarningType(models.TextChoices):
        CONTRAINDICATION = "contraindication", "Contraindication"
        PRECAUTION = "precaution", "Precaution"
        ALLERGY = "allergy", "Allergy"
        PREGNANCY = "pregnancy", "Pregnancy"
        BREASTFEEDING = "breastfeeding", "Breastfeeding"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        REVIEWED = "reviewed", "Reviewed"
        PUBLISHED = "published", "Published"
        REJECTED = "rejected", "Rejected"

    drug = models.ForeignKey(
        Drug,
        on_delete=models.PROTECT,
        related_name="drug_warnings",
    )
    warning_type = models.CharField(
        max_length=30,
        choices=WarningType.choices,
    )
    sources = models.ManyToManyField(
        "DrugSource",
        related_name="warnings",
        blank=True,
    )
    review_status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    rejection_reason = models.TextField(
        blank=True,
        default="",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.drug} - {self.get_warning_type_display()}"


class DrugWarningTranslation(models.Model):
    """Stores warning details in individual languages."""

    warning = models.ForeignKey(
        DrugWarning,
        on_delete=models.CASCADE,
        related_name="translations",
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        related_name="warning_translations",
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    recommended_action = models.TextField(blank=True)

    review_status = models.CharField(
        max_length=20,
        choices=DrugWarning.Status.choices,
        default=DrugWarning.Status.DRAFT,
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_warning_translations",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["warning", "language"],
                name="unique_warning_translation",
            )
        ]

    def __str__(self):
        return f"{self.title} ({self.language.code})"


class DrugSource(models.Model):
    """Records references used to support medicine information."""

    class SourceType(models.TextChoices):
        OFFICIAL_LABEL = "official_label", "Official product label"
        GOVERNMENT = "government", "Government health source"
        MEDICAL_REFERENCE = "medical_reference", "Medical reference"
        GUIDELINE = "guideline", "Clinical guideline"
        OTHER = "other", "Other"

    title = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, blank=True)
    url = models.URLField(max_length=1000, blank=True)
    source_type = models.CharField(
        max_length=30,
        choices=SourceType.choices,
        default=SourceType.OTHER,
    )
    publication_date = models.DateField(null=True, blank=True)
    accessed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title
