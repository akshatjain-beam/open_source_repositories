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
    Create a function `deploy` which uploads the local entry point script and associated Python modules to an S3 bucket.

    This method takes a specified S3 URI, uploads the entry point script and 
    a zip file containing local Python modules to the corresponding S3 bucket and 
    returns the S3 path of the uploaded entry point script.
    
    The filename of the entry point script is derived from the entry point path 
    specified in the instance variable. 

    Parameters:
        s3_code_uri (str): The S3 URI where the code will be uploaded. 
                            It should be in the format 's3://bucket-name/prefix/'.

    Returns:
        str: The S3 path of the uploaded entry point script.
                It should formatted as 's3://bucket-name/prefix/filename'.
    """
    $PlaceHolder$

    def spark_submit_parameters(self) -> str:
        zip_path = os.path.join(self.s3_uri_base, "pyfiles.zip")
        return f"--conf spark.submit.pyFiles={zip_path}"