# from transformers import CLIPProcessor, CLIPModel
# import torch
# import io
# from PIL import Image


# class ImageEmbeddingService:
#     def __init__(self, model):
#         self.processor = CLIPProcessor.from_pretrained(model)
#         self.model = CLIPModel.from_pretrained(model)

#     def encode(self, file_stream):
#         # Load the image
#         image = Image.open(io.BytesIO(file_stream))

#         # Process image
#         inputs = self.processor(images=image, return_tensors="pt")

#         # Move to CPU
#         inputs = {k: v.to("cpu") for k, v in inputs.items()}

#         # Get the image embedding
#         with torch.no_grad():
#             image_features = self.model.get_image_features(**inputs)

#         # Normalize the embeddings
#         image_embeddings = torch.nn.functional.normalize(image_features, p=2, dim=1)

#         return image_embeddings

#     def get_dimensions(self):
#         # CLIP's image and text embeddings are of the same size
#         return self.model.config.text_config.hidden_size

#     def get_token_size(self):
#         # This method isn't directly applicable to images as it is to text
#         # Returning None or a default value could be more appropriate
#         return None
