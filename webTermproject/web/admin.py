from django.contrib import admin
from web.models import Student,Professor,Grade_Table,Professor_Table,Course_Table,Course
# Register your models here.

admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Grade_Table)
admin.site.register(Professor_Table)
admin.site.register(Course_Table)
admin.site.register(Course)