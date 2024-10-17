import os
import subprocess
import sys
from pathlib import Path
from typing import List
from urllib.parse import urlparse

import boto3

from src.emr_cli.deployments.emr_serverless import DeploymentPackage
from src.emr_cli.utils import console_log, copy_template


class PythonPoetryProject(DeploymentPackage):
    def initialize(self, target_dir: str = os.getcwd()):
        """
        Initializes a poetry-based pyspark project in the provided directory.
        - Creates a basic poetry project
        - Creates a pyproject.toml file
        - Creates a Dockerfile
        """
        console_log(f"Initializing project in {target_dir}")
        copy_template("pyspark", target_dir)
        copy_template("poetry", target_dir)
        console_log("Project initialized.")

    def build(self):
        if not Path("poetry.lock").exists():
            print("Error: No poetry.lock present, please setup your poetry project.")
            sys.exit(1)

        console_log(f"Packaging assets into {self.dist_dir}/")
        # TODO: Add an option for --force-local-build
        self._run_docker_build(self.dist_dir)

    def _run_local_build(self, output_dir: str = "dist"):
        subprocess.run(
            ["poetry", "bundle", "venv" "poeticemrbundle" "--without" "dev"], check=True
        )

    def _run_docker_build(self, output_dir: str):
        subprocess.run(
            [
                "docker",
                "build",
                "--target",
                "export-poetry",
                "--output",
                output_dir,
                "--file",
                self._dockerfile_path(),
                ".",
            ],
            check=True,
            env=dict(os.environ, DOCKER_BUILDKIT="1"),
        )

    def _dockerfile_path(self) -> str:
        if Path("Dockerfile").is_file():
            return "Dockerfile"

        templates = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "templates", "pyspark")
        )
        return os.path.join(templates, "Dockerfile")

    def deploy(self, s3_code_uri: str) -> str:
        """
        Copies local code to S3 and returns the path to the uploaded entrypoint
        """
        s3_client = boto3.client("s3")
        bucket, prefix = self._parse_bucket_uri(s3_code_uri)
        filename = os.path.basename(self.entry_point_path)

        console_log(f"Deploying {filename} and dependencies to {s3_code_uri}")

        s3_client.upload_file(
            self.entry_point_path, bucket, os.path.join(prefix, filename)
        )
        s3_client.upload_file(
            os.path.join(self.dist_dir, "pyspark_deps.tar.gz"),
            bucket,
            os.path.join(prefix, "pyspark_deps.tar.gz"),
        )

        return f"s3://{bucket}/{prefix}/{filename}"

    def spark_submit_parameters(self) -> str:
        tar_path = os.path.join(self.s3_uri_base, "pyspark_deps.tar.gz")
        return f"--conf spark.archives={tar_path}#environment --conf spark.emr-serverless.driverEnv.PYSPARK_DRIVER_PYTHON=./environment/bin/python --conf spark.emr-serverless.driverEnv.PYSPARK_PYTHON=./environment/bin/python --conf spark.executorEnv.PYSPARK_PYTHON=./environment/bin/python"  # noqa: E501

    """
    Create a function `_parse_bucket_uri` that Extracts the bucket name and prefix from a given S3 URI.

    This method takes an S3 URI 
    and returns the bucket name and the path prefix as a list.
    Parameters:
    uri : str
        The S3 URI to parse.

    Returns:
    List[str]
        A list where the first element is the bucket name and the 
        second element is the path prefix.

    Note: 
        -  The URI may contain leading and trailing slashes that need to be discarded.
        -  There is no need to check the validity of the URI being an S3 URI.
        -  Fragment identifiers shouldn't be considered.

    """
    $PlaceHolder$

