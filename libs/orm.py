class ModelToDictMixin():
    def to_dic(self,exclued=None):
        if exclued is None:
            exclued = []
        attr_dict={}
        fields = self._meta.fields

        for field in fields:
            if field not in exclued:
                field_name= field.attname
                attr_dict[field_name] = getattr(self,field_name)
        return attr_dict