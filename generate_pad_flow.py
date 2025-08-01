import os
import zipfile
import json

# Output zip file path
OUTPUT_ZIP = "FileRouter_Magic_Flow.zip"

# Flow name
FLOW_NAME = "FileRouter_Magic"

# CSV path used in flow - update if needed
CSV_PATH = "D:\\Fulfinal_File_CLEANED.csv"

# Flow JSON structure (simplified)
FLOW_JSON = {
  "name": FLOW_NAME,
  "actions": [
    {
      "type": "ReadCsvFile",
      "inputs": {
        "filePath": CSV_PATH,
        "outputVariable": "CSVTable"
      }
    },
    {
      "type": "ForEach",
      "inputs": {
        "input": "%CSVTable%",
        "currentItem": "CurrentItem"
      },
      "actions": [
        {"type": "SetVariable", "inputs": {"name": "PhaseNumber", "value": "%CurrentItem.Phase%"}},
        {"type": "SetVariable", "inputs": {"name": "ModuleName", "value": "%CurrentItem.Module%"}},
        {"type": "SetVariable", "inputs": {"name": "OriginalPath", "value": "%CurrentItem.Original Path%"}},
        {"type": "SetVariable", "inputs": {"name": "FileName", "value": "%CurrentItem.Filename%"}},
        {
          "type": "CreateFolder",
          "inputs": {"folderPath": "D:\\MAGIC\\scripts\\phase%PhaseNumber%"}
        },
        {
          "type": "CreateFolder",
          "inputs": {"folderPath": "D:\\MAGIC\\scripts\\phase%PhaseNumber%\\module_%ModuleName%"}
        },
        {
          "type": "MoveFile",
          "inputs": {
            "sourceFilePath": "%OriginalPath%",
            "destinationFilePath": "D:\\MAGIC\\scripts\\phase%PhaseNumber%\\module_%ModuleName%\\%FileName%",
            "overwrite": True
          }
        }
      ]
    }
  ]
}

def create_flow_json_file():
    os.makedirs("flow_export", exist_ok=True)
    with open("flow_export/flow.json", "w", encoding="utf-8") as f:
        json.dump(FLOW_JSON, f, indent=2)
    print("Created flow_export/flow.json")

def create_manifest_file():
    manifest = {
        "package": FLOW_NAME,
        "version": "1.0",
        "author": "ChatGPT Assistant",
        "description": "File routing automation flow for MAGIC project"
    }
    with open("flow_export/manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print("Created flow_export/manifest.json")

def create_zip():
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zipf:
        for foldername, _, filenames in os.walk("flow_export"):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                arcname = os.path.relpath(filepath, "flow_export")
                zipf.write(filepath, arcname)
    print(f"Created {OUTPUT_ZIP}")

def main():
    create_flow_json_file()
    create_manifest_file()
    create_zip()

if __name__ == "__main__":
    main()
