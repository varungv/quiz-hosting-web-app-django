from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.UserExtensionTable)
admin.site.register(models.BatchTable)
admin.site.register(models.SubjectsTable)
admin.site.register(models.TestTable)
admin.site.register(models.TestBatchJunction)
admin.site.register(models.QuestionsTable)
admin.site.register(models.UserTestJunction)
admin.site.register(models.TestSubjectTable)
admin.site.register(models.UserTestQuestionJunction)
admin.site.register(models.BookmarksTable)