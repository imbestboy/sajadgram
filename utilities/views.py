from django.http import HttpResponse, Http404
from django.core.exceptions import ImproperlyConfigured
from django.views import generic


class DoUndoWithAjaxView(generic.View):
    model = None
    check_dict = None
    create_dict = None

    def post(self, request):
        if request.is_ajax():
            model = self.get_model()
            try:
                self.do_model_instance = model.objects.get(**self.get_check_dict())
                self.do_model_instance.is_active, is_do = (
                    (False, False) if self.do_model_instance.is_active else (True, True)
                )
                self.do_model_instance.save()
            except model.DoesNotExist:
                model.objects.create(
                    **self.get_create_dict(),
                )
                is_do = True

            return HttpResponse(str(is_do))
        else:
            raise Http404

    def get_model(self, model=None):
        if model:
            self.model = model
        elif self.model is None:
            raise ImproperlyConfigured(
                "%(cls)s is missing a model. Define "
                "%(cls)s.model, or override "
                "%(cls)s.get_model()." % {"cls": self.__class__.__name__}
            )
        return self.model

    def get_check_dict(self, check_dict=None):
        if check_dict:
            self.check_dict = check_dict
        elif self.check_dict is None:
            raise ImproperlyConfigured(
                "%(cls)s is missing a check dict. Define "
                "%(cls)s.check_dict, or override "
                "%(cls)s.get_check_dict()." % {"cls": self.__class__.__name__}
            )

        return self.check_dict

    def get_create_dict(self, create_dict=None):
        if create_dict:
            self.create_dict = create_dict
        elif self.create_dict is None:
            raise ImproperlyConfigured(
                "%(cls)s is missing a create dict. Define "
                "%(cls)s.create_dict, or override "
                "%(cls)s.get_create_dict()." % {"cls": self.__class__.__name__}
            )

        return self.create_dict
