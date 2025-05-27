import json
from pathlib import Path

# Paths to input JSON files
input_files = [
    "morrowind_pl.json",
    "tribunal_pl.json",
    "bloodmoon_pl.json"
]

# Output path
output_file = "Polish_VoiceDialogue_Mod.json"

# Function to split a long ID into diagInfoID1/2/3
def generate_diaginfo_script(info_id_str):
    try:
        full_id = int(info_id_str)
        part1 = int(str(full_id)[:7])
        part2 = int(str(full_id)[7:13])
        part3 = int(str(full_id)[13:])
        return f"Set diagInfoID1 to {part1}\nSet diagInfoID2 to {part2}\nSet diagInfoID3 to {part3}"
    except Exception:
        return ""

# Header block for ESP compatibility
header = {
    "type": "Header",
    "flags": "",
    "version": 1.3,
    "file_type": "Esp",
    "author": "Polish Voice Mod Generator",
    "description": "Polish dialogue mod with diagInfoID injected.",
    "num_objects": 0,
    "masters": [
        ["Morrowind.esm", 79837557],
        ["Tribunal.esm", 4554200],
        ["Bloodmoon.esm", 9627056]
    ]
}

# Load and process all files
all_entries = [header]
updated_count = 0

for file_path in input_files:
    print(f"🔄 Processing: {file_path}")
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)
        for entry in data:
            if entry.get("type") in ("Dialogue", "DialogueInfo"):
                if entry["type"] == "DialogueInfo":
                    info_id = str(entry.get("id", ""))
                    diag_script = generate_diaginfo_script(info_id)
                    if diag_script:
                        existing_script = entry.get("script_text", "").strip()
                        combined_script = (existing_script + "\n" + diag_script) if existing_script else diag_script
                        entry["script_text"] = combined_script.strip()
                        updated_count += 1
                all_entries.append(entry)

# Update header with correct object count
all_entries[0]["num_objects"] = len(all_entries) - 1

# Save final result
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_entries, f, ensure_ascii=False, indent=2)

print(f"\n✅ Injected diagInfoID into {updated_count} DialogueInfo entries.")
print(f"💾 Output saved to: {output_file}")

