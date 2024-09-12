from django.contrib import admin
# import your models here
from .models import Cat
from .models import Feeding
from .models import Toy

# Register your models here
admin.site.register(Cat)
# register the new Feeding Model 
admin.site.register(Feeding)
# register the new Toy Model
admin.site.register(Toy)