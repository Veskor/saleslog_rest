import json

def create_sub_model(serializer):
    def _method_wrapper(function):
        def _arguments_wrapper(self, *args, **kwargs):
            obj_data = {}
            for item in self.request.POST:
                if serializer.Meta.model.__name__.lower() in item:
                    field = item.split('.')[1]
                    obj_data.update({field:self.request.POST[item]})

            obj = serializer(data=obj_data)

            if obj.is_valid():
                obj.save()
            else:
                obj = None
            return function(self, self.request, obj, *args, **kwargs)

        return _arguments_wrapper
    return _method_wrapper

def create_sub_model_on_detail(serializer):
    def _method_wrapper(function):
        def _arguments_wrapper(self, *args, **kwargs):
            obj_data = {}
            for item in self.request.data:
                if serializer.Meta.model.__name__.lower() in item:
                    field = item.split('.')[1]
                    obj_data.update({field:self.request.data[item]})

            obj = serializer(data=obj_data)

            if obj.is_valid():
                obj.save()
            else:
                obj = None
            return function(self, self.request, obj)

        return _arguments_wrapper
    return _method_wrapper
