import os

import boto3

from src.emr_cli.deployments.emr_serverless import DeploymentPackage
from src.emr_cli.utils import console_log, parse_bucket_uri


class SimpleProject(DeploymentPackage):
    """
    A simple project only has a single entry point file.
    This can be a pyspark file or packaged jar file.
    """

    def build(self):
        pass

    def deploy(self, s3_code_uri: str) -> str:
        """
        Copies local code to S3 and returns the path to the uploaded entrypoint
        """
        s3_client = boto3.client("s3")
        bucket, prefix = parse_bucket_uri(s3_code_uri)
        filename = os.path.basename(self.entry_point_path)

        console_log(f"Deploying {filename} to {s3_code_uri}")

        s3_client.upload_file(self.entry_point_path, bucket, f"{prefix}/{filename}")

        return f"s3://{bucket}/{prefix}/{filename}"
