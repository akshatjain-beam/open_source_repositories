import os
import zipfile

import boto3

from src.emr_cli.deployments.emr_serverless import DeploymentPackage
from src.emr_cli.utils import console_log, find_files, mkdir, parse_bucket_uri


class PythonFilesProject(DeploymentPackage):
    """
    A PythonFilesProject is a simple project that includes multiple `.py` files.

    This is a simple project that has no external dependencies and requires no
    additional packaging. The files in the project are simply zipped up.
    """

    def build(self):
        """
        Zip all the files except for the entrypoint file.
        """
        py_files = find_files(os.getcwd(), [".venv"], ".py")
        py_files.remove(os.path.abspath(self.entry_point_path))
        cwd = os.getcwd()
        mkdir(self.dist_dir)
        with zipfile.ZipFile(f"{self.dist_dir}/pyfiles.zip", "w") as zf:
            for file in py_files:
                relpath = os.path.relpath(file, cwd)
                zf.write(file, relpath)

    """
    Create a function `deploy` that uploads the local entry point code and related Python modules to an Amazon S3 bucket.

    This function takes an S3 URI and copies the specified entry point file along with
    a ZIP file of local Python modules to the designated S3 location.

    Parameters:
    s3_code_uri : str
        The S3 URI where the code will be uploaded, formatted as 
        's3://bucket-name/prefix'.

    Returns:
    str
        The S3 URI of the uploaded entry point, formatted as 
        's3://bucket-name/prefix/filename'.

    """
    $PlaceHolder$

    def spark_submit_parameters(self) -> str:
        zip_path = os.path.join(self.s3_uri_base, "pyfiles.zip")
        return f"--conf spark.submit.pyFiles={zip_path}"
