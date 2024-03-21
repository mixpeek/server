# import os
# import boto3
# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# from _exceptions import InternalServerError


# class VideoService:
#     def __init__(self, file_path, s3_bucket, chunk_length):
#         self.file_path = file_path
#         self.s3_bucket = s3_bucket
#         self.chunk_length = chunk_length
#         self.s3_client = boto3.client("s3")

#     def _chunk(self):
#         chunks = []
#         video_length = int(moviepy.editor.VideoFileClip(self.file_path).duration)
#         for i in range(0, video_length, self.chunk_length):
#             start_time = i
#             end_time = (
#                 i + self.chunk_length
#                 if i + self.chunk_length < video_length
#                 else video_length
#             )
#             chunk_file_path = f"{self.file_path}_chunk_{start_time}_{end_time}.mp4"
#             ffmpeg_extract_subclip(
#                 self.file_path, start_time, end_time, targetname=chunk_file_path
#             )
#             chunks.append(chunk_file_path)
#         return chunks

#     def _upload_to_s3(self, file_path):
#         try:
#             self.s3_client.upload_file(
#                 file_path, self.s3_bucket, os.path.basename(file_path)
#             )
#         except Exception as e:
#             raise InternalServerError({"error": str(e)})

#     def run(self):
#         try:
#             chunks = self._chunk()
#             for chunk in chunks:
#                 self._upload_to_s3(chunk)
#             return chunks
#         except Exception as e:
#             raise InternalServerError({"error": str(e)})
