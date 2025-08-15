import json
import argparse
import subprocess

# Function to load and debug the manifest file
def load_manifest(filename):
    try:
        with open(filename, 'r') as file:
            manifest = json.load(file)
            print("Loaded manifest:")
            print(json.dumps(manifest, indent=2))  # Pretty print the JSON
            return manifest
    except FileNotFoundError:
        print("Error: The specified manifest file was not found!")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode the manifest JSON!")
        return []

# Function to filter the manifest based on provided phases and modules
def filter_manifest(manifest, phases, modules):
    filtered = []
    for entry in manifest:
        print(f"Processing entry: {entry}")  # Debugging line to show each entry being processed

        # If the entry is a string, attempt to parse it as a JSON object
        if isinstance(entry, str):
            try:
                entry = json.loads(entry)  # Try to parse string to JSON
                print(f"Successfully parsed string: {entry}")  # Debug parsed entry
            except json.JSONDecodeError:
                print(f"Error decoding string entry: {entry}")
                continue  # Skip invalid JSON strings

        if isinstance(entry, dict):
            entry_phase = entry.get('Phase') or entry.get('PhaseNumber') or entry.get('phase')
            entry_module = entry.get('Module') or entry.get('module')
            print(f"Entry Phase: {entry_phase}, Entry Module: {entry_module}")  # Debug output

            if entry_phase in phases and entry_module in modules:
                filtered.append(entry)
        else:
            print(f"Skipping non-dictionary entry: {entry}")
    
    return filtered

# Main function to handle the manifest processing
def main():
    # Argument parsing setup
    parser = argparse.ArgumentParser(description="Process a phase manifest.")
    parser.add_argument('--manifest', required=True, help="Path to the manifest JSON file")
    parser.add_argument('--phases', required=True, nargs='+', help="List of phases to filter by")
    parser.add_argument('--modules', required=True, nargs='+', help="List of modules to filter by")
    parser.add_argument('--dry-run', action='store_true', help="Dry run without making changes")
    
    args = parser.parse_args()

    # Load the manifest from the provided file
    manifest = load_manifest(args.manifest)

    # Get the phases and modules from the arguments
    phases = args.phases
    modules = args.modules

    # If dry-run is specified, just print the filtered scripts
    if args.dry_run:
        print(f"Dry run enabled. Filtering the manifest based on phases {phases} and modules {modules}.")
        filtered_scripts = filter_manifest(manifest, phases, modules)
        print(f"Filtered scripts: {filtered_scripts}")
    else:
        # Process and execute the necessary actions on the filtered scripts
        filtered_scripts = filter_manifest(manifest, phases, modules)
        
        if not filtered_scripts:
            print("No matching entries found in manifest. Nothing to run.")
        else:
            print(f"Filtered scripts: {filtered_scripts}")
            for script in filtered_scripts:
                print(f"Executing {script['Filename']}...")
                # Add your execution logic here (e.g., running scripts or handling files)
                # Example:
                try:
                    # Example: Run each Python script (you can adapt this part based on your needs)
                    result = subprocess.run(['python', script['Filename']], check=True)
                    print(f"Script {script['Filename']} executed successfully!")
                except subprocess.CalledProcessError as e:
                    print(f"Error executing script {script['Filename']}: {e}")

# Run the script if this is the main module
if __name__ == "__main__":
    main()
