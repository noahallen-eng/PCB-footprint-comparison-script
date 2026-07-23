# © 2025 Noah Allen. All rights reserved.
# This script is proprietary and confidential. Unauthorized use, reproduction, or distribution is prohibited.

import zipfile
import os

def find_part_number_in_zips(part_number, zip_directory, output_filename="search_results.txt"):
    """
    Searches for a given part number within .txt files inside zip archives
    in a specified directory.

    Args:
        part_number (str): The part number to search for.
        zip_directory (str): The path to the directory containing the zip files.
        output_filename (str): The name of the file to write search results to.
    """
    if not os.path.isdir(zip_directory):
        print(f"Error: Directory not found: {zip_directory}")
        return 0, []

    search_term_bytes = part_number.encode('utf-8')
    matches_found = 0
    zips_with_matches = set()
    results_lines = []

    for zip_filename in os.listdir(zip_directory):
        if zip_filename.endswith(".zip"):
            zip_path = os.path.join(zip_directory, zip_filename)

            try:
                with zipfile.ZipFile(zip_path, 'r') as z:
                    for filename in z.namelist():
                        if filename.endswith(".txt"):
                            try:
                                with z.open(filename) as f:
                                    for i, line in enumerate(f):
                                        if search_term_bytes in line:
                                            try:
                                                line_text = line.decode('utf-8').strip()
                                                results_lines.append(f"{zip_filename} -> {filename}, line {i+1}: {line_text}")
                                                matches_found += 1
                                                zips_with_matches.add(zip_filename)
                                            except UnicodeDecodeError:
                                                results_lines.append(f"{zip_filename} -> {filename}, line {i+1}: <Could not decode line>")
                                                matches_found += 1
                            except Exception as e:
                                known_errors = (
                                    "Bad magic number for file header",
                                    "Bad CRC-32 for file",
                                    "encrypted",
                                    "password required",
                                )
                                if not any(err in str(e) for err in known_errors):
                                    print(f"An unexpected error occurred while processing {filename} in {zip_filename}: {e}")
            except zipfile.BadZipFile:
                continue
            except Exception as e:
                if "Bad magic number" not in str(e):
                    print(f"An unexpected error occurred while processing {zip_filename}: {e}")

    # Write to output file
    with open(output_filename, "w", encoding='utf-8') as output_file:
        if matches_found == 0:
            output_file.write("No matching part numbers found.\n")
        else:
            output_file.write("Detailed Matches:\n")
            output_file.write("\n".join(results_lines))
            output_file.write("\n\n-----------------------\n")
            output_file.write("Summary of ZIP matches:\n")
            output_file.write("-----------------------\n")
            for zip_name in sorted(zips_with_matches):
                output_file.write(f"- {zip_name}\n")

    return matches_found, sorted(zips_with_matches)

# --- Interactive Prompt Execution ---
if __name__ == "__main__":
    import sys

    print("=" * 60)
    print(" " * 15 + "DL DESIGNS - NOAH ALLEN")
    print("=" * 60)
    print("© 2025 Noah Allen. All rights reserved.")
    print("This script is proprietary and confidential.")
    print()

    print("Part Number Search Tool")
    part_number = input("Enter the part number to search for: ").strip()
    if not part_number:
        print("No part number entered. Exiting.")
        input("\nPress Enter to close.")
        sys.exit()

    print("\nPlease wait... The search may take a few minutes...\n")

    zip_directory = r"T:\GERBER"  # Change if needed
    output_file = "search_results.txt"

    match_count, matching_zips = find_part_number_in_zips(part_number, zip_directory, output_file)

    print("\n" + "-" * 60)
    if match_count:
        print(f"Search complete. {match_count} matching line(s) found.")
        print("Search results file is complete.")
        print(f"Output saved to: {os.path.abspath(output_file)}")

        if matching_zips:
            print("\nZIP files that contain matches:")
            for zip_name in matching_zips:
                print(f"- {zip_name}")
    else:
        print("Search complete. No part number found.")
        print(f"Output saved to: {os.path.abspath(output_file)}")
    print("-" * 60)

    input("\nPress Enter to close.")
