import moviepy.editor as mp

def add_audio_to_video(video_path, audio_path, output_path):
    video = mp.VideoFileClip(video_path)
    
    audio = mp.AudioFileClip(audio_path)
    
    video_duration = video.duration
    audio_duration = audio.duration
    
    if audio_duration > video_duration:
        audio = audio.subclip(0, video_duration)
    elif video_duration > audio_duration:
        video = video.subclip(0, audio_duration)
    
    video_with_audio = video.set_audio(audio)
    
    video_with_audio.write_videofile(output_path, codec='libx264', audio_codec='aac')

video_path = ""
audio_path = ""
output_path = "/home/user_201/nerf/video_with_audio.mp4"

# Appeler la fonction pour ajouter l'audio à la vidéo
add_audio_to_video(video_path, audio_path, output_path)

