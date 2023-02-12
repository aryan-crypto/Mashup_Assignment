
import streamlit as st
import moviepy.editor as mp
import os
import sys
from pytube import YouTube
import streamlit as st
import smtplib
import zipfile
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email.utils import COMMASPACE, formatdate
import shutil
import subprocess


def func(singer,N,Y,outputfile):

# Create a YouTube object with the URL of the video you want to download
    from youtubesearchpython import VideosSearch

    videosSearch = VideosSearch(singer, limit = N)

    data=videosSearch.result()

    result = data["result"]
    links = []
    for item in result:
        link = item.get("link")
        if link:
            links.append(link)
            YouTube(link).streams.get_highest_resolution().download("videos")
    print(links)


    import os

    def get_filenames_in_folder(folder_path):
        filenames = []
        for filename in os.listdir(folder_path):
            filenames.append(filename)
        return filenames

    folder_path = 'videos'
    filenames = get_filenames_in_folder(folder_path)
    print(filenames)

    video_files=[]
    for file in filenames:
        video_files.append('videos/'+file)


    import moviepy.editor as mp

    def extract_audio(video_file, audio_file):
        video = mp.VideoFileClip(video_file)
        audio = video.audio
        audio.write_audiofile(audio_file)

#video_files = ['videos\Shawn Mendes - Stitches (Official Music Video).mp4']

    for video_file in video_files:
        audio_file = video_file.split('.')[0] + '.mp3'
        extract_audio(video_file, audio_file)

    print('Audio extraction complete!')


    def cut_audio(filename, start_time, end_time):
        audio = mp.AudioFileClip(filename)
        audio_cut = audio.subclip(start_time, end_time)
        audio_cut.write_audiofile('videos/audio'+file+'.mp3')

    cutaudio=[]
    for file in filenames:
        cutaudio.append(file.replace(".mp4",""))

    cutaudio

# List of audio files
#files = ["videos\Shawn Mendes - Stitches (Official Music Video).mp3"]

# Cut the first Y seconds of each audio file
   # Y = int(sys.argv[3])
    for file in cutaudio:
        cut_audio('videos/'+file+'.mp3', 0, Y)
#cut_audio('videos\Shawn Mendes - Stitches (Official Music Video).mp3', 0, Y)

    def merge_audios(filenames, output_filename):
        audios = [mp.AudioFileClip(filename) for filename in filenames]
        final_audio = mp.concatenate_audioclips(audios)
        final_audio.write_audiofile(output_filename)


    filena=[]
    for file in cutaudio:
        filena.append('videos/'+'audio'+file+'.mp3')
    filena

    merge_audios(filena,outputfile)



st.title("Streamlit Input Example")

input_1 = st.text_input("Enter Singer:")
input_2 = st.text_input("Enter Number of Videos:")
input_3 = st.text_input("Enter trim seconds:")
input_4 = st.text_input("Enter Output file name:")
email = st.text_input("Enter your email address:")
if st.button("Submit"):
 if input_1 and input_2 and input_3 and input_4:
    num=int(input_2)
    trim=int(input_3)
    print(type(input_1))
    print(type(input_2))
    name=input_1
    out=input_4
    func(name,num,trim,out)
    try:
        import zipfile

        def package_audio_file(audio_file_path, zip_file_path):
            with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
                zip_file.write(audio_file_path)

        package_audio_file(out, 'audio.zip')

        def send_email(to, subject, text, files=[]):
            msg = MIMEMultipart()
            msg['From'] = "forestrandom71@gmail.com"
            msg['To'] = COMMASPACE.join(to)
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = subject

            msg.attach(MIMEText(text))

            for path in files:
                with open(path, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                part.add_header("Content-Disposition",
                        "attachment; filename={}".format(path))
                msg.attach(part)

            smtp = smtplib.SMTP("smtp.gmail.com", 587)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login("forestrandom71@gmail.com","szhgkywzdvjinxms")
            smtp.sendmail("forestrandom71@gmail.com", to, msg.as_string())
            smtp.close()

        send_email([email], "Subject", "Text", ["audio.zip"])
        print('Mail Sent')
        st.write("You have recieved an email from forestrandom71@gmail.com")
        
    except:
        st.error("Failed to send result.")

#if os.path.exists("videos"):
#    shutil.rmtree("videos")
#if os.path.exists("audio.zip"):
#    os.remove("audio.zip")
    