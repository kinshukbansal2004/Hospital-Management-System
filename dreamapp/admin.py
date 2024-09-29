from django.contrib import admin
from dreamapp.models import * 
# Register your models here.
admin.site.register(Feedback)
admin.site.register(Patient)
admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Rooms)
admin.site.register(Appointment)
admin.site.register(Admit)
admin.site.register(Discharge)