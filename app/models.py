from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name
    
class Document(models.Model):
    title = models.CharField(
        max_length=512,
        validators=[MinLengthValidator(1)],
        db_index=True,
    )
    content = models.TextField(validators=[MinLengthValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(
        Tag,
        related_name='documents',
        blank=True,
    )
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Document"
        verbose_name_plural = "Documents"
      
    def __str__(self):
        return self.title
        
class Query(models.Model):
    question = models.TextField(validators=[MinLengthValidator(1)])
    answer = models.TextField(blank=True)
    related_docs = models.ManyToManyField(Document,
                                          related_name="queries",
                                          blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    processing_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'), 
        ],
        default='pending',
        db_index=True
    )
    confidence_score = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Query"
        verbose_name_plural = "Queries"

    def __str__(self):
        return self.question[:80]
    
    def mark_as_completed(self):
        self.processing_status = "completed"
        self.save(update_fields=["processing_status", "updated_at"])

    def has_answer(self):
        return bool(self.answer)