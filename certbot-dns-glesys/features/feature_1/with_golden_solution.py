```
class DomainParts(NamedTuple):
    domain: str
    subdomain: str = None

    def iter_variants(self):
        sub_parts = []
        if self.subdomain is not None:
            sub_parts = self.subdomain.split(".")

        parts = self.domain.split(".")
        for i in range(len(parts)):
            yield DomainParts(
                ".".join(parts[i:]),
                ".".join(sub_parts + parts[:i]) or None,
            )
```