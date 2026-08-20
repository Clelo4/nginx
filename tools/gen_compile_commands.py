#!/usr/bin/env python3
"""
Generate compile_commands.json for NGINX from dry-run make output.
Ensures 100% IDE parity with CMake/Clangd/VS Code C/C++ Extension.
"""

import subprocess
import json
import os
import sys

def main():
    workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(workspace)

    if not os.path.exists("objs/Makefile"):
        print("objs/Makefile not found! Please run ./auto/configure first.", file=sys.stderr)
        sys.exit(1)

    print("Running make -n -B to extract compiler flags...")
    res = subprocess.run(["make", "-n", "-B"], capture_output=True, text=True, check=True)
    raw_output = res.stdout

    # Concatenate lines ending with backslash
    merged_lines = []
    current_line = ""
    for line in raw_output.splitlines():
        if line.endswith("\\"):
            current_line += line[:-1].strip() + " "
        else:
            current_line += line.strip()
            if current_line:
                merged_lines.append(current_line)
            current_line = ""

    commands = []
    for line in merged_lines:
        if line.startswith("cc -c ") or line.startswith("gcc -c ") or line.startswith("clang -c "):
            parts = line.split()
            src_file = parts[-1]
            if os.path.exists(src_file):
                abs_src = os.path.abspath(src_file)
                commands.append({
                    "directory": workspace,
                    "command": line,
                    "file": abs_src
                })

    out_file = os.path.join(workspace, "compile_commands.json")
    with open(out_file, "w") as f:
        json.dump(commands, f, indent=2)

    print(f"Successfully generated {out_file} with {len(commands)} translation units.")

if __name__ == "__main__":
    main()
