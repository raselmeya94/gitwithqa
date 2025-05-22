# import re
# import os

# # Input merged file path
# input_file = '/Users/ainiton/Rasel_data_scientist/GIT WITH QA/gitingest/tmp/90b10cbd-a201-4e94-aa03-02286ba39186/raselmeya94-RAGpedia.txt'

# # Output directory
# base_dir = os.path.dirname(input_file)

# # Read the merged file content
# with open(input_file, 'r', encoding='utf-8') as f:
#     merged_text = f.read()

# # Regex pattern to match file blocks
# pattern = r"={48}\nFile: (.+?)\n={48}\n([\s\S]*?)(?=(={48}\nFile: )|$)"
# matches = re.findall(pattern, merged_text)

# for filename, content, *_ in matches:
#     # Sanitize filename: replace slashes, remove leading `/`, and change extension to `.txt`
#     sanitized_filename = filename.strip("/").replace("/", "__") + ".txt"
#     output_path = os.path.join(base_dir, sanitized_filename)

#     # Write content to new .txt file
#     with open(output_path, 'w', encoding='utf-8') as out_file:
#         out_file.write(content.strip())

#     print(f"✅ Saved: {output_path}")

# print(f"\n🎉 Done! Total files extracted and saved as .txt: {len(matches)}")
