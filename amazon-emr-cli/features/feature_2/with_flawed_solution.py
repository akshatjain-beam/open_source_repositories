```
    def deploy(self, s3_code_uri: str) -> str:
            console_log(f"Deploying to {s3_code_uri}")
            bucket, prefix = parse_bucket_uri(s3_code_uri)

            s3 = boto3.client("s3")

            # Upload entry point
            s3_entrypoint_uri = os.path.join(prefix, self.entry_point_path)
            s3.upload_file(self.entry_point_path, bucket, s3_entrypoint_uri)
            console_log(
                f"Uploaded entrypoint {self.entry_point_path} to s3://{bucket}/{s3_entrypoint_uri}"
            )

            # Upload zip
            local_zip_path = f"{self.dist_dir}/pyfiles.zip"
            s3_zip_uri = os.path.join(prefix, "pyfiles.zip")
            s3.upload_file(local_zip_path, bucket, s3_zip_uri)
            console_log(f"Uploaded pyfiles.zip to s3://{bucket}/{s3_zip_uri}")

            self.s3_uri_base = s3_code_uri
            return self.entrypoint_uri()
```