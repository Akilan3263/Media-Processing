import gradio as gr
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def cut_video(video_file, start1, end1, start2, end2, start3, end3):
    try:
        video = VideoFileClip(video_file.name)
        duration = video.duration

        if start1 >= end1 or start2 >= end2 or start3 >= end3:
            return "Error: Start time must be less than end time.", None, None, None
        if end1 > duration or end2 > duration or end3 > duration:
            return f"Error: One or more cuts exceed the video duration ({duration:.2f} seconds).", None, None, None
        
        cut1, cut2, cut3 = video.subclip(start1, end1), video.subclip(start2, end2), video.subclip(start3, end3)
        filenames = ["cut1.mp4", "cut2.mp4", "cut3.mp4"]
        
        for filename, cut in zip(filenames, [cut1, cut2, cut3]):
            cut.write_videofile(filename, codec='libx264', audio_codec='aac')
        
        return "Cuts successful.", filenames[0], filenames[1], filenames[2]
    except Exception as e:
        return f"Error cutting video: {str(e)}", None, None, None

def merge_videos(video1_file, video2_file, video3_file):
    try:
        if not video1_file or not video2_file or not video3_file:
            return "Error: Please upload all three videos.", None
        
        final_video = concatenate_videoclips([VideoFileClip(f.name) for f in [video1_file, video2_file, video3_file]])
        output_filename = "merged_video.mp4"
        final_video.write_videofile(output_filename, codec='libx264', audio_codec='aac')
        return "Merging successful!", output_filename
    except Exception as e:
        return f"Error merging videos: {str(e)}", None

def change_video_resolution(video_file, quality):
    try:
        video = VideoFileClip(video_file.name)
        resolutions = {"480p": (854, 480), "720p": (1280, 720), "1080p": (1920, 1080), "1440p": (2560, 1440), "4K": (3840, 2160)}
        if quality not in resolutions:
            return "Error: Invalid quality selection.", None
        
        resized_video = video.resize(resolutions[quality])
        output_path = "output_video.mp4"
        resized_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        return output_path
    except Exception as e:
        return f"Error: {str(e)}", None

with gr.Blocks(theme="soft") as demo:
    with gr.TabItem("🏠 Home"):
        gr.Markdown("""
        # 🎬 Welcome to Advanced Video Editor
        **Developed by Akilan JD, Adithya J, and Jayavignesh G**  
        *Engineers Exploring the Future of Media and AI*
        
        ## 🔹 Features:
        - ✂️ **Video Cutter**: Trim multiple parts of a video with ease.
        - 🔗 **Video Merger**: Combine multiple video clips seamlessly.
        - 🎚️ **Resolution Changer**: Convert videos to different resolutions (480p, 720p, 1080p, 1440p, 4K).
        
        🎥 **Enhance your video editing experience with our intuitive and user-friendly interface!**
        """)
    
    with gr.Tabs():
        with gr.TabItem("✂️ Video Cutter"):
            video_input = gr.File(label="Upload Video")
            start1, end1 = gr.Number(label="Start Cut 1"), gr.Number(label="End Cut 1")
            start2, end2 = gr.Number(label="Start Cut 2"), gr.Number(label="End Cut 2")
            start3, end3 = gr.Number(label="Start Cut 3"), gr.Number(label="End Cut 3")
            cut_button = gr.Button("Cut Video")
            status, cut1, cut2, cut3 = gr.Textbox(label="Status"), gr.Video(), gr.Video(), gr.Video()
            cut_button.click(cut_video, inputs=[video_input, start1, end1, start2, end2, start3, end3], outputs=[status, cut1, cut2, cut3])
        
        with gr.TabItem("🔗 Video Merger"):
            vid1, vid2, vid3 = gr.File(label="Upload Video 1"), gr.File(label="Upload Video 2"), gr.File(label="Upload Video 3")
            merge_button = gr.Button("Merge Videos")
            merge_status, final_vid = gr.Textbox(label="Status"), gr.Video()
            merge_button.click(merge_videos, inputs=[vid1, vid2, vid3], outputs=[merge_status, final_vid])
        
        with gr.TabItem("🎚️ Change Resolution"):
            res_video = gr.File(label="Upload Video")
            quality_input = gr.Dropdown(["480p", "720p", "1080p", "1440p", "4K"], label="Select Quality", value="720p")
            convert_button = gr.Button("Convert Quality")
            converted_video = gr.Video()
            convert_button.click(change_video_resolution, inputs=[res_video, quality_input], outputs=converted_video)

demo.launch()
