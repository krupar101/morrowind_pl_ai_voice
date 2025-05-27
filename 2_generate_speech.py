import os
import json
from pathlib import Path
from TTS.api import TTS

# === CONFIG ===
original_vov_root = Path("/home/krupar/.var/app/org.openmw.OpenMW/data/openmw/Mods/VoV/Sound/Vo/AIV")
output_root = Path("/home/krupar/Dokumenty/python_projects/morrowind_pl_dialogue/morrowind/creating polish from scratch/Sound/Vo/AIV")
json_path = Path("Polish_VoiceDialogue_Mod.json")
tts_model_name = "tts_models/pl/mai_female/vits"

# === Load Dialogue JSON ===
with open(json_path, encoding="utf-8") as f:
    mod_data = json.load(f)

id_to_text = {
    str(entry["id"]): entry["text"]
    for entry in mod_data if entry.get("type") == "DialogueInfo" and "text" in entry
}

# === Load TTS model ONCE
print(f"🔊 Loading TTS model: {tts_model_name}")
tts = TTS(tts_model_name, gpu=True)

processed, skipped = 0, 0
missing_log = []

# === Process each original .mp3 ===
for mp3_path in original_vov_root.rglob("*.mp3"):
    file_id = mp3_path.stem

    if file_id not in id_to_text:
        relative_path = mp3_path.relative_to(original_vov_root)
        print(f"⚠️  Skipping {relative_path} — no matching ID {file_id}")
        missing_log.append(str(relative_path))
        skipped += 1
        continue

    text = id_to_text[file_id]

    # Prepare output path
    relative_path = mp3_path.relative_to(original_vov_root)
    output_path = output_root / relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate MP3 directly via Python API
    try:
        tts.tts_to_file(text=text, file_path=str(output_path))
        print(f"✅ Generated: {output_path}")
        processed += 1
    except Exception as e:
        print(f"❌ Error generating {file_id}: {e}")
        skipped += 1
        missing_log.append(f"{file_id} (generation error)")

# Save skipped list
if missing_log:
    with open("skipped_ids.log", "w", encoding="utf-8") as f:
        f.write("\n".join(missing_log))

# Summary
print(f"\n✅ Done.")
print(f"🟢 Generated: {processed}")
print(f"🟡 Skipped: {skipped}")
if skipped:
    print(f"📄 Skipped paths saved to: skipped_ids.log")

