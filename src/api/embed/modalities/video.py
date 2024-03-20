# import torch
# from PIL import Image
# from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize
# from transformers import CLIPProcessor, CLIPModel
# import cv2
# import numpy as np


# class VideoEmbeddingService:
#     def __init__(self, model):
#         self.processor = CLIPProcessor.from_pretrained(model)
#         self.model = CLIPModel.from_pretrained(model)

#     def frame_embeddings(self, video_path):
#         # Initialize a video capture object
#         cap = cv2.VideoCapture(video_path)
#         frame_embeddings = []

#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             # Convert the color space from BGR to RGB, then convert to PIL Image
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             pil_image = Image.fromarray(frame)

#             # Preprocess the image
#             inputs = self.processor(images=pil_image, return_tensors="pt", padding=True)

#             # Move to CPU and get the image embedding
#             inputs = {k: v.to("cpu") for k, v in inputs.items()}
#             with torch.no_grad():
#                 frame_features = self.model.get_image_features(**inputs)

#             frame_embeddings.append(frame_features)

#         cap.release()
#         return torch.stack(frame_embeddings)

#     def encode(self, file_stream):
#         # Assume file_stream is a path for simplicity; adapt as necessary for actual streams
#         embeddings = self.frame_embeddings(file_stream)
#         # Aggregate embeddings, e.g., by averaging
#         video_embedding = embeddings.mean(dim=0)
#         # Normalize the embeddings
#         normalized_embedding = torch.nn.functional.normalize(
#             video_embedding, p=2, dim=1
#         )
#         return normalized_embedding

#     def get_dimensions(self):
#         return self.model.config.visual_projection.out_features

#     def get_token_size(self):
#         # Not applicable for videos, similar to audio and images
#         return None
