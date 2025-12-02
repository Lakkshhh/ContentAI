#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from autogram import get_openai_key
import sys
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
from autogram.crew import Autogram

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def merge_two_videos(video1_path: str, video2_path: str, output_path: str = "outputs/final_reel.mp4"):

    os.makedirs("outputs", exist_ok=True)

    clip1 = VideoFileClip(video1_path)
    clip2 = VideoFileClip(video2_path)

    final = concatenate_videoclips([clip1, clip2], method="compose")
    final = final.crossfadein(0.5).crossfadeout(0.5)
    final = final.resize(height=1920).set_fps(30)

    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        bitrate="8000k",
        threads=6,
        logger=None
    )

    print(f"Successfully merged → {output_path}")
    clip1.close()
    clip2.close()
    final.close()
    return output_path


def run():

    inputs = {
        'current_year': str(datetime.now().year)
    }

    if not get_openai_key():
        print("Warning: OPENAI_API_KEY not set. Some agents may fail.")

    print("Starting CrewAI neuroscience reel generation...")
    try:
        Autogram().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"Crew failed: {e}")

    video1 = "outputs/part1.mp4"   # dummy vids for now, replace with generated vids path
    video2 = "outputs/part2.mp4"

    if os.path.exists(video1) and os.path.exists(video2):
        final_video = merge_two_videos(video1, video2, "outputs/final_reel.mp4")
        print(f"FINAL REEL READY: {final_video}")
        print("Next step: Upload via Instagram Graph API")
    else:
        print("ERROR: Could not find one or both video parts.")
        print(f"Looking for:\n  {video1}\n  {video2}")
        print("Check your Google Veo output paths/filenames.")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        Autogram().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Autogram().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        Autogram().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
      run()