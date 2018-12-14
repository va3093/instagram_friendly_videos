
import argparse
from moviepy.editor import VideoFileClip
import subprocess
import os


def prefix_file_name(path, prefix):
    directory = os.path.dirname(path)
    filename = os.path.basename(path)
    return directory + '/' + prefix + filename


def make_clip(*, file_prefix, start_clip, end_clip):
    clipped_path_name = prefix_file_name(video_path, file_prefix)
    bordered_clipped_path_name = prefix_file_name(
        clipped_path_name, "bordered_")
    subprocess.call(
        f'ffmpeg -i {video_path} -ss {start_clip} '
        f'-t {end_clip}  {clipped_path_name}',
        shell=True)
    subprocess.call(
        f'ffmpeg -i {clipped_path_name} -filter_complex '
        f'"[0:v]pad=iw:ih+{remainding_height}:0:(oh-ih)/2:color=white" '
        f'{bordered_clipped_path_name}',
        shell=True)


ap = argparse.ArgumentParser()
ap.add_argument(
    "-p", "--path", required=True,
    help="The path of the file to clip")
args = vars(ap.parse_args())

video_path = args['path']
if not os.path.isabs(video_path):
    video_path = os.getcwd() + '/' + video_path

CLIP_DURATION = 55
clip = VideoFileClip(video_path)
clips, remainder = divmod(clip.duration, CLIP_DURATION)
remainding_height = clip.size[0] - clip.size[1]

print(f'Clipping {video_path}')
print(f'{clips} clips will be made each of length {CLIP_DURATION}')
print(f'The last clip wil be of length {remainder}')

for index in range(int(clips)):
    make_clip(
        file_prefix=str(index) + "_", start_clip=index * CLIP_DURATION,
        end_clip=(index + 1) * CLIP_DURATION)

remainder_index = int(clips) + 1
make_clip(
    file_prefix=str(remainder_index) + "_",
    start_clip=remainder_index * CLIP_DURATION,
    end_clip=(remainder_index + 1) * remainder)
