import os
import subprocess
import sys
from pathlib import Path
from shutil import copy

import boto3

from src.emr_cli.deployments.emr_serverless import DeploymentPackage
from src.emr_cli.utils import console_log, copy_template, parse_bucket_uri


class PythonProject(DeploymentPackage):
    def initialize(self, target_dir: str = os.getcwd()):
        """
        Initializes a pyspark project in the provided directory.
        - Creates a basic project
        - Creates a pyproject.toml file
        - Creates a Dockerfile
        """
        console_log(f"Initializing project in {target_dir}")
        copy_template("pyspark", target_dir)
        console_log("Project initialized.")

    def copy_single_file(self, relative_file_path: str, target_dir: str = os.getcwd()):
        """
        Copies a single file from the template directory to the target directory.
        """
        template_path = (
            Path(__file__).parent.parent / "templates" / "pyspark" / relative_file_path
        )
        target_path = Path(target_dir)
        copy(template_path, target_path)

    def build(self):
        """
        For now, uses a pre-existing Docker file and setuptools
        """
        if not Path("Dockerfile").exists():
            print(
                "Error: No Dockerfile present, use 'emr-cli init --dockerfile' to generate one"  # noqa: E501
            )
            sys.exit(1)
        if not Path("pyproject.toml").exists():
            print("Error: No pyproject.toml present, please set one up before building")
            sys.exit(1)

        console_log(f"Packaging assets into {self.dist_dir}/")
        self._run_docker_build(self.dist_dir)

    def _run_docker_build(self, output_dir: str):
        subprocess.run(
            ["docker", "build", "--output", output_dir, "."],
            check=True,
            env=dict(os.environ, DOCKER_BUILDKIT="1"),
        )

    def deploy(self, s3_code_uri: str) -> str:
        """
        Copies local code to S3 and returns the path to the uploaded entrypoint
        """
        self.s3_uri_base = s3_code_uri
        s3_client = boto3.client("s3")
        bucket, prefix = parse_bucket_uri(self.s3_uri_base)
        filename = os.path.basename(self.entry_point_path)

        console_log(f"Deploying {filename} and dependencies to {self.s3_uri_base}")

        s3_client.upload_file(self.entry_point_path, bucket, f"{prefix}/{filename}")
        s3_client.upload_file(
            f"{self.dist_dir}/pyspark_deps.tar.gz",
            bucket,
            f"{prefix}/pyspark_deps.tar.gz",
        )

        return f"s3://{bucket}/{prefix}/{filename}"

    def spark_submit_parameters(self) -> str:
        tar_path = os.path.join(self.s3_uri_base, "pyspark_deps.tar.gz")
        return f"--conf spark.archives={tar_path}#environment --conf spark.emr-serverless.driverEnv.PYSPARK_DRIVER_PYTHON=./environment/bin/python --conf spark.emr-serverless.driverEnv.PYSPARK_PYTHON=./environment/bin/python --conf spark.executorEnv.PYSPARK_PYTHON=./environment/bin/python"  # noqa: E501
