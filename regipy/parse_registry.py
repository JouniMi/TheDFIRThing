import os
from regipy.registry import RegistryHive
import regipy.recovery
import json
import time
from regipy import cli

RegistryDataFolder = "/tmp/evidence"
outputfolder = "/tmp/output/"

def find_reg_files_recover_with_regipy(directory, exact_name):
    """
    Recursively find all files with the exact name in the specified directory.
    Additionally, check if files with the same name but with .log1 and .log2 extensions exist in the same folder 
    (case-insensitive). Perform Regipy Recovery if transaction logs found and they are not empty. Return dict of found/recovered paths.

    :param directory: The root directory to start the search.
    :param exact_name: The exact file name to search for (e.g., 'example.txt').
    :return: None
    """
    exact_name_lower = exact_name.lower()
    FoundFiles = {}
    FoundFiles[exact_name] = {}
    counter = 1
    for root, _, files in os.walk(directory):
        lower_files = [f.lower() for f in files]
        for file in files:
            if file.lower() == exact_name_lower:
                base_name = os.path.splitext(file)[0]
                log1_file = base_name + '.LOG1'
                log2_file = base_name + '.LOG2'
                ntuser_log1_file = base_name.lower() + '.dat.LOG1'
                ntuser_log2_file = base_name.lower() + '.dat.LOG2'

                if log1_file.lower() in lower_files and log2_file.lower() in lower_files:
                    # Action if both .log1 and .log2 files exist
                    print(f"Both .log1 and .log2 files exist for: {os.path.join(root, file)}")
                    # Check if log files are empty
                    log1_empty = os.path.getsize(os.path.join(root, log1_file)) == 0
                    log2_empty = os.path.getsize(os.path.join(root, log2_file)) == 0
                    if not log1_empty and not log2_empty:
                        # Action if both .log1 and .log2 files exist and are not empty
                        print(f"Both .log1 and .log2 files exist and are not empty for: {os.path.join(root, file)}")
                        # Add your action here
                        fileloc = root.replace("/","_")
                        fileloc = fileloc.replace(".","")
                        hivefile=(os.path.join(root, file))
                        logfilepath1=(os.path.join(root, log1_file))
                        logfilepath2=(os.path.join(root, log2_file))
                        timestamp = int(time.time())
                        RevorededPath = f"{outputfolder}Recovered-{base_name}_{timestamp}"
                        output_path = outputfolder + base_name + fileloc + ".json"
                        output_path_dump = outputfolder + "FULL_" + base_name + fileloc + ".json"
                        output_path_dump = output_path_dump.replace(" ","")
                        regipy.recovery.apply_transaction_logs(hivefile, logfilepath1, logfilepath2,RevorededPath)
                        FoundFiles[exact_name][output_path] = RevorededPath
                        counter += 1
                    else:
                        # Action if either .log1 or .log2 file is empty
                        print(f"One or both log files are empty for: {os.path.join(root, file)}")
                        fileloc = root.replace("/","_")
                        fileloc = fileloc.replace(".","")
                        output_path = outputfolder + base_name + fileloc + ".json"
                        output_path_dump = outputfolder + "FULL_" + base_name + fileloc + ".json"
                        output_path_dump = output_path_dump.replace(" ","")
                        hivefile=(os.path.join(root, file))
                        FoundFiles[exact_name][output_path] = hivefile
                        counter += 1

                elif ntuser_log1_file.lower() in lower_files and ntuser_log2_file.lower() in lower_files:
                    # Action if both .log1 and .log2 files exist
                    print(f"Both .dat.log1 and .dat.log2 files exist for: {os.path.join(root, file)}")
                    # Check if log files are empty
                    try:
                        ntuser_log1_file_empty = os.path.getsize(os.path.join(root, ntuser_log1_file)) == 0
                        ntuser_log2_file_empty = os.path.getsize(os.path.join(root, ntuser_log2_file)) == 0
                        logfilepath1=(os.path.join(root, ntuser_log1_file))
                        logfilepath2=(os.path.join(root, ntuser_log2_file))
                    except Exception:
                        print(Exception)
                    try:
                        ntuser_log1_file_empty = os.path.getsize(os.path.join(root, ntuser_log1_file.upper())) == 0
                        ntuser_log2_file_empty = os.path.getsize(os.path.join(root, ntuser_log2_file.upper())) == 0
                        logfilepath1=(os.path.join(root, ntuser_log1_file.upper()))
                        logfilepath2=(os.path.join(root, ntuser_log2_file.upper()))
                    except Exception:
                        print(Exception)
                    
                    if not ntuser_log1_file_empty and not ntuser_log2_file_empty:
                        # Action if both .dat.log1 and .dat.log2 files exist
                        print(f"Both .dat.log1 and .dat.log2 files exist for: {os.path.join(root, file)}")
                        fileloc = root.replace("/","_")
                        fileloc = fileloc.replace(".","")
                        hivefile=(os.path.join(root, file))
                        timestamp = int(time.time())
                        RevorededPath = f"{outputfolder}Recovered-{base_name}_{timestamp}"
                        output_path = outputfolder + base_name + fileloc + ".json"
                        output_path_dump = outputfolder + "FULL_" + base_name + fileloc + ".json"
                        output_path_dump = output_path_dump.replace(" ","")
                        regipy.recovery.apply_transaction_logs(hivefile, logfilepath1, logfilepath2,RevorededPath)
                        FoundFiles[exact_name][output_path] = RevorededPath
                        counter += 1
                    else:
                        # Action if either .log1 or .log2 file is empty
                        print(f"One or both log files are empty for: {os.path.join(root, file)}")
                        fileloc = root.replace("/","_")
                        fileloc = fileloc.replace(".","")
                        output_path = outputfolder + base_name + fileloc + ".json"
                        output_path_dump = outputfolder + "FULL_" + base_name + fileloc + ".json"
                        output_path_dump = output_path_dump.replace(" ","")
                        hivefile=(os.path.join(root, file))
                        FoundFiles[exact_name][output_path] = hivefile
                        counter += 1
                else:
                    # Action if either .log1 or .log2 file does not exist
                    print(f"Missing .log1 or .log2 file for: {os.path.join(root, file)}")
                    print(f"Not replaying logs.")
                    fileloc = root.replace("/","_")
                    fileloc = fileloc.replace(".","")
                    output_path = outputfolder + base_name + fileloc + ".json"
                    output_path_dump = outputfolder + "FULL_" + base_name + fileloc + ".json"
                    output_path_dump = output_path_dump.replace(" ","")
                    hivefile=(os.path.join(root, file))

                    FoundFiles[exact_name][output_path] = hivefile
                    counter += 1
    return FoundFiles

def convert_values_to_string_and_lists_to_dict(d):
    if isinstance(d, dict):
        return {k: convert_values_to_string_and_lists_to_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        # Convert list to dict with indices as keys
        return {str(i): convert_values_to_string_and_lists_to_dict(v) for i, v in enumerate(d)}
    else:
        return str(d)


FilesToProcess = {}
# SYSTEM
FilesToProcess.update(find_reg_files_recover_with_regipy(RegistryDataFolder, 'SYSTEM'))

# SECURITY
FilesToProcess.update(find_reg_files_recover_with_regipy(RegistryDataFolder, 'SECURITY'))

# SAM
FilesToProcess.update(find_reg_files_recover_with_regipy(RegistryDataFolder, 'SAM'))

# SOFTWARE
FilesToProcess.update(find_reg_files_recover_with_regipy(RegistryDataFolder, 'SOFTWARE'))

# NTUSER
FilesToProcess.update(find_reg_files_recover_with_regipy(RegistryDataFolder, 'NTUSER.DAT'))

for e in FilesToProcess:
    timestamp = int(time.time())
    for a in FilesToProcess[e]:
        print("Starting to process file: ",FilesToProcess[e][a])
        RunPlugins = regipy.plugins.utils.run_relevant_plugins(RegistryHive(FilesToProcess[e][a]), as_json=True)
        converted_dict = convert_values_to_string_and_lists_to_dict(RunPlugins)
        with open(a, 'w') as f:
            f.write(json.dumps(converted_dict, indent=4))
