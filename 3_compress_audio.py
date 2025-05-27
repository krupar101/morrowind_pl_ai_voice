import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# === CONFIG ===
input_root = Path("./Sound")
output_root = Path("./Sound_Compressed")
max_workers = 4  # Adjust based on your CPU

# === Compression Mode ===
use_vbr = True             # Set to False to use CBR instead

# VBR settings
vbr_quality = "7"          # FFmpeg -qscale:a value (2–9), lower = better quality

# CBR settings (ignored if use_vbr=True)
target_bitrate = "32k"     # e.g., "48k", "64k"
target_sample_rate = "22050"

# === Speed Adjustment ===
audio_speed_factor = 1.10   # e.g., 1.0 (normal), 1.05 (5% faster), 1.1 (10% faster)

def compress_mp3(mp3_path):
    relative_path = mp3_path.relative_to(input_root)
    output_path = output_root / relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Build common FFmpeg command
    base_cmd = [
        "ffmpeg", "-y", "-i", str(mp3_path),
        "-filter:a", f"atempo={audio_speed_factor}",
        "-ar", target_sample_rate,
        "-ac", "1",
    ]

    if use_vbr:
        ffmpeg_cmd = base_cmd + ["-qscale:a", vbr_quality, str(output_path)]
    else:
        ffmpeg_cmd = base_cmd + ["-b:a", target_bitrate, str(output_path)]

    try:
        subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return f"✅ {relative_path}", None
    except subprocess.CalledProcessError as e:
        return None, f"❌ Failed: {relative_path} — {e}"

# === Gather and run
all_mp3s = list(input_root.rglob("*.mp3"))
print(f"🎧 Found {len(all_mp3s)} files to compress using {'VBR' if use_vbr else 'CBR'} with speed {audio_speed_factor}x...")

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [executor.submit(compress_mp3, mp3) for mp3 in all_mp3s]
    processed, failed = 0, 0

    for future in as_completed(futures):
        success_msg, error_msg = future.result()
        if success_msg:
            print(success_msg)
            processed += 1
        else:
            print(error_msg)
            failed += 1

# === Summary ===
print(f"\n✅ Done compressing.")
print(f"🟢 Processed: {processed}")
print(f"🔴 Failed: {failed}")

