from django.contrib import admin
from .models import Modelnames,CustomUser,Projects
from dynamic_models.models import ModelSchema


admin.site.register(CustomUser)
admin.site.register(Projects)
admin.site.register(Modelnames)

try:

    models = Modelnames.objects.all()
    for model in models:
        try:
            reg_model = ModelSchema.objects.get(name=model.modelname).as_model()
            admin.site.register(reg_model)
        except Exception as e:
            print("error :  " ,model.modelname ,e)
except Exception as e:
    print("error in admin file : ", e)
