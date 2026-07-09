import zipfile
import os
from models.interface import Interface
from pathlib import Path

def read_zip(zip_path):
    """
    Reads an SAP CPI ZIP file and returns all files inside it.
    """

    if not os.path.exists(zip_path):
        print(f"File not found: {zip_path}")
        return None

    interface = Interface()

    with zipfile.ZipFile(zip_path, "r") as zip_ref:

        print("\nFiles found inside ZIP:\n")

        for file_name in zip_ref.namelist():

            print(file_name)

            with zip_ref.open(file_name) as file:

                try:
                    content = file.read().decode("utf-8")

                except UnicodeDecodeError:
                    content = file.read()

            lower_name = file_name.lower()

            if lower_name.endswith(".iflw"):
                interface.iflow_xml = content
                interface.name = Path(file_name).stem
                print("✔ Found iFlow:", file_name)

            elif lower_name.endswith(".groovy"):
                interface.resources["groovy"].append({
                    "name": file_name,
                    "path": file_name,
                    "content": content
                })

            elif lower_name.endswith(".mmap"):
                interface.resources["mapping"].append({
                    "name": file_name,
                    "path": file_name,
                    "content": content
                })

            elif lower_name.endswith(".xsd"):
                interface.resources["xsd"].append({
                    "name": file_name,
                    "path": file_name,
                    "content": content
                })

            elif lower_name.endswith(".wsdl"):
                interface.resources["wsdl"].append({
                    "name": file_name,
                    "path": file_name,
                    "content": content
                })

            elif lower_name.endswith(".edmx"):
                interface.resources["edmx"].append({
                    "name": file_name,
                    "path": file_name,
                    "content": content
                })

            elif lower_name.endswith(".prop") or lower_name.endswith(".propdef"):
                interface.resources["properties"].append({
                    "name": file_name,
                    "path": file_name,
                    "content": content
                })

            else:
                interface.resources["other"].append({
                    "name": file_name,
                    "path": file_name
                })

    return interface