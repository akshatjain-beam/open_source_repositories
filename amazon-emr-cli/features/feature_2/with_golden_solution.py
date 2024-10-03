```
    
    def deploy(self, s3_code_uri: str) -> str:
        """
        Copies local code to S3 and returns the path to the uploaded entrypoint
        """
        s3_client = boto3.client("s3")
        bucket, prefix = parse_bucket_uri(s3_code_uri)
        filename = os.path.basename(self.entry_point_path)

        console_log(f"Deploying {filename} and local python modules to {s3_code_uri}")

        s3_client.upload_file(self.entry_point_path, bucket, f"{prefix}/{filename}")
        s3_client.upload_file(
            f"{self.dist_dir}/pyfiles.zip", bucket, f"{prefix}/pyfiles.zip")

        return f"s3://{bucket}/{prefix}/{filename}"
```