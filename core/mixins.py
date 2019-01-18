from django.views.generic.base import TemplateResponseMixin


class RequestFormKwargsMixin(object):

    def get_form_kwargs(self):
        kwargs = super(RequestFormKwargsMixin, self).get_form_kwargs()
        # Update the existing form kwargs dict with the request's user.
        kwargs.update({"request": self.request})
        return kwargs


class RequestKwargModelFormMixin(object):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)  # Pop the request off the passed in kwargs.
        super(RequestKwargModelFormMixin, self).__init__(*args, **kwargs)


# class CustomTemplateResponseMixin(TemplateResponseMixin):

#     def get_template_names(self):
#         """
#         Return a list of template names to be used for the request. Must return
#         a list. May not be called if render_to_response() is overridden.
#         """
#         if self.template_name is None:
#             raise ImproperlyConfigured(
#                 "TemplateResponseMixin requires either a definition of "
#                 "'template_name' or an implementation of 'get_template_names()'")
#         elif request.user.user_type == "BR":
#             return ["buyerdetails.html"]
#         else:
#             return [self.template_name]
