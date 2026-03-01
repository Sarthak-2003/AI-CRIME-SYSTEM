import os
import sys
import pandas as pd
from datetime import datetime
import pyttsx3
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import ImageClip, AudioFileClip, ColorClip, CompositeVideoClip
import difflib

sys.stdout.reconfigure(encoding='utf-8')

# =========================================================
# PATH CONFIGURATION (100% SAFE)
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

DATASET_PATH = os.path.join(BASE_DIR, "crime_dataset_india.csv")

if not os.path.isfile(DATASET_PATH):
    print("Dataset file not found at:", DATASET_PATH)
    sys.exit(1)

df = pd.read_csv(DATASET_PATH)
df.fillna("NULL", inplace=True)

# =========================================================
# CRIME LAW DATABASE
# =========================================================

crime_ipc_crpc_mapping = {
    "murder": ("IPC 302", "CRPC 154", "Death penalty or life imprisonment"),
    "homicide": ("IPC 302", "CRPC 174", "Life imprisonment or death"),
    "killing": ("IPC 302", "CRPC 154", "Death penalty or life imprisonment"),
    "kidnapping": ("IPC 363", "CRPC 98", "Up to 7 years and fine"),
    "burglary": ("IPC 454, IPC 380", "CRPC 154", "Up to 10 years and fine"),
    "vandalism": ("IPC 427", "CRPC 107", "Up to 2 years or fine or both"),
    "assault": ("IPC 351", "CRPC 107", "Up to 3 months or fine or both"),
    "robbery": ("IPC 392", "CRPC 154", "Up to 10 years and fine"),
    "fraud": ("IPC 420", "CRPC 154", "Up to 7 years and fine"),
    "sexual assault": ("IPC 354, IPC 376", "CRPC 154", "7 years to life imprisonment"),
    "rape": ("IPC 376", "CRPC 154", "7 years to life imprisonment"),
    "arson": ("IPC 435, IPC 436", "CRPC 154", "Up to life imprisonment"),
    "cybercrime": ("IT Act Sections", "CRPC 154", "Up to 3 years and/or fine"),
}

# =========================================================
# INPUT VALIDATION
# =========================================================

if len(sys.argv) < 2:
    print("Please provide crime description")
    sys.exit(1)

crime_text = " ".join(sys.argv[1:]).lower()

# =========================================================
# ADVANCED FUZZY MATCHING
# =========================================================

def find_best_match(text, keywords):
    # Full sentence matching
    best = difflib.get_close_matches(text, keywords, n=1, cutoff=0.5)
    if best:
        return best[0]

    # Word-by-word matching
    for word in text.split():
        best = difflib.get_close_matches(word, keywords, n=1, cutoff=0.6)
        if best:
            return best[0]

    return None


ipc = "Section to be determined"
crpc = "Section to be determined"
punishment = "Punishment to be determined"

matched_keyword = find_best_match(crime_text, crime_ipc_crpc_mapping.keys())

if matched_keyword:
    ipc, crpc, punishment = crime_ipc_crpc_mapping[matched_keyword]

# =========================================================
# OUTPUT DIRECTORY
# =========================================================

output_dir = os.path.join(PROJECT_ROOT, "outputs")
os.makedirs(output_dir, exist_ok=True)

case_id = "CASE_" + datetime.now().strftime("%Y%m%d_%H%M%S")
case_folder = os.path.join(output_dir, case_id)
os.makedirs(case_folder, exist_ok=True)

# =========================================================
# REPORT GENERATION
# =========================================================

report_text = f"""
एआई अपराध विश्लेषण रिपोर्ट

अपराध विवरण:
{crime_text}

लागू आईपीसी धारा:
{ipc}

लागू सीआरपीसी धारा:
{crpc}

दंड:
{punishment}
"""

report_path = os.path.join(case_folder, "case_summary.txt")

with open(report_path, "w", encoding="utf-8") as f:
    f.write(report_text)

# =========================================================
# HINDI FEMALE VOICE
# =========================================================

engine = pyttsx3.init()
engine.setProperty("rate", 140)

voices = engine.getProperty("voices")
selected_voice = None

# Priority Hindi Female
for voice in voices:
    if "heera" in voice.name.lower() or "kalpana" in voice.name.lower():
        selected_voice = voice.id
        break

# Any Hindi
if not selected_voice:
    for voice in voices:
        if "hindi" in voice.name.lower():
            selected_voice = voice.id
            break

# English Female fallback
if not selected_voice:
    for voice in voices:
        if "zira" in voice.name.lower():
            selected_voice = voice.id
            break

if selected_voice:
    engine.setProperty("voice", selected_voice)
    print("Voice Selected:", selected_voice)
else:
    print("Using default voice")

audio_path = os.path.join(case_folder, "incident_audio.mp3")

engine.save_to_file(report_text, audio_path)
engine.runAndWait()

# =========================================================
# VIDEO GENERATION
# =========================================================

audio_clip = AudioFileClip(audio_path)

background = ColorClip(
    size=(1280, 720),
    color=(15, 15, 15),
    duration=audio_clip.duration
)

img = Image.new("RGB", (1200, 600), color="black")
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("arial.ttf", 42)
except:
    font = ImageFont.load_default()

video_text = f"IPC: {ipc}\nCRPC: {crpc}\n\nPunishment:\n{punishment}"

draw.multiline_text((100, 200), video_text, fill="white", font=font)

np_img = np.array(img)
text_clip = ImageClip(np_img).set_duration(audio_clip.duration)

final_video = CompositeVideoClip([background, text_clip])
final_video = final_video.set_audio(audio_clip)

video_path = os.path.join(case_folder, "incident_video.mp4")

final_video.write_videofile(
    video_path,
    fps=24,
    codec="libx264",
    audio_codec="aac"
)

print("\n[SUCCESS] Execution Successful")
print("Saved at:", case_folder)