```
    @classmethod
    def _build_routes(cls, method_args, url_extra_part=None):
        """Create Bottle routes for a handler HTTP method.
        """
        if not method_args:
            return [cls.base_endpoint]

        routes = []
        for combination in cls._router_helper(method_args):
            route = cls.base_endpoint
            if url_extra_part:
                route += "/{}".format(url_extra_part)
            for arg in combination:
                route += "/<{}:{}>".format(arg, arg)
            routes.append(route.replace("//", "/"))
        return routes
```