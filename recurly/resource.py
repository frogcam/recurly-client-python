from pydoc import locate

class Resource:

    @staticmethod
    def cast(properties):
        if 'object' not in properties:
            return properties

        name_parts = properties['object'].split('_')
        class_name = ''.join(x.title() for x in name_parts)
        klass = locate("recurly.resources.%s" % class_name)

        if klass is None:
            return properties

        del properties['object']
        for k, v in properties.items():
            if isinstance(v, dict):
                properties[k] = Resource.cast(v)
            elif isinstance(v, list):
                for i in range(len(v)):
                    if isinstance(v[i], dict):
                        v[i] = Resource.cast(v[i])

        return klass(properties)

    def __init__(self, properties):
        vars(self).update(properties)
