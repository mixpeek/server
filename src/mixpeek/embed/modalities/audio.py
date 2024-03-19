# from transformers import Wav2Vec2Processor, Wav2Vec2Model
# import torch
# import librosa
# import numpy as np
# import io

# class AudioEmbeddingService:
#     def __init__(self, model):
#         self.processor = Wav2Vec2Processor.from_pretrained(model)
#         self.model = Wav2Vec2Model.from_pretrained(model)

#     def encode(self, file_stream):
#         # Load the audio file
#         audio_input, sr = librosa.load(io.BytesIO(file_stream), sr=16000)

#         # Process audio
#         inputs = self.processor(audio_input, return_tensors="pt", sampling_rate=sr)

#         # Move to CPU
#         inputs = {k: v.to("cpu") for k, v in inputs.items()}

#         # Get the audio embedding
#         with torch.no_grad():
#             audio_features = self.model(**inputs).last_hidden_state

#         # Mean pooling the embeddings across the time dimension
#         embeddings = audio_features.mean(dim=1)

#         # Normalize the embeddings
#         normalized_embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

#         return normalized_embeddings

#     def get_dimensions(self):
#         return self.model.config.hidden_size

#     def get_token_size(self):
#         # Similar to images, token size isn't directly applicable to audio
#         return None
