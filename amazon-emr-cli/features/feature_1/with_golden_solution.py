```
    def _parse_bucket_uri(self, uri: str) -> List[str]:
        result = urlparse(uri, allow_fragments=False)
        return [result.netloc, result.path.strip("/")]
```