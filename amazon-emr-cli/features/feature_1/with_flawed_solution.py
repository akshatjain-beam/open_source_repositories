```
    def _parse_bucket_uri(self, uri: str) -> List[str]:
        parsed_uri = urlparse(uri)
        return [parsed_uri.netloc, parsed_uri.path.lstrip("/")]
```
