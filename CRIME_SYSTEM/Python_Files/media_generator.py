import os
from moviepy.editor import AudioFileClip, ColorClip, TextClip
import os
import pyttsx3


def generate_audio(text, output_folder):
    audio_path = os.path.join(output_folder, "incident_audio.mp3")

    # Offline Text-to-Speech
    engine = pyttsx3.init()
    engine.save_to_file(text, audio_path)
    engine.runAndWait()

    return audio_path


def generate_video(text, audio_path, output_folder):
    video_path = os.path.join(output_folder, "incident_video.mp4")

    audio_clip = AudioFileClip(audio_path)

    # Create plain black background
    background = ColorClip(size=(1280, 720), color=(0, 0, 0))
    background = background.set_duration(audio_clip.duration)

    final_clip = background.set_audio(audio_clip)

    final_clip.write_videofile(video_path, fps=24)

    return video_path