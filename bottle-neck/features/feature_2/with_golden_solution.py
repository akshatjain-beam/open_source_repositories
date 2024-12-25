```
    @classmethod
    def _build_routes(cls, method_args, url_extra_part=None):
        """Create bottle route for a handler http method."""

        prefix = '/{}'.format(url_extra_part) if url_extra_part else ''

        endpoint = cls.base_endpoint + prefix

        if not method_args:
            return [endpoint]

        endpoints = []

        for args_list in cls._router_helper(method_args):
            prefix = '/:' if args_list else ''
            endpoints.append((endpoint + prefix + '/:'.join(args_list)).replace("//", '/'))

        return endpoints
```