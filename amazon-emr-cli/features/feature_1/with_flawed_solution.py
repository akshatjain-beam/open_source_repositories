```
    def _parse_bucket_uri(self, uri: str) -> List[str]:
        parts = uri[5:].split("/", 1)
        bucket = parts[0]
        prefix = parts[1] if len(parts) > 1 else ""
        return [bucket, prefix]
```
