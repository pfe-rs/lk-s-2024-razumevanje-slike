import numpy as np
from transformers import AutoModelForCausalLM, AutoProcessor
from PIL import Image

class AIModel:
    def __init__(self) -> None:
        # Constructor
        self.model_id = "microsoft/Phi-3-vision-128k-instruct" 
        self.model = AutoModelForCausalLM.from_pretrained(self.model_id,
                                                         cache_dir="/notebooks/my_models/phi_3_vision",
                                                         device_map="cuda",
                                                         trust_remote_code=True,
                                                         torch_dtype="auto",
                                                         _attn_implementation="eager")  
        self.processor = AutoProcessor.from_pretrained(self.model_id, trust_remote_code=True)
        self.generation_args = {
                "max_new_tokens": 2048,
                "temperature": 0.0,
                "do_sample": False,
            }
    
    def get_response(self, message: str, image: Image.Image) -> str:
        # Gets text response from Phi-3-Vision given a message and image

        # Converts image into array
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)

        # Appends message to context
        context = [
            {"role": "user", "content": "<|image_1|>\n" + message}
        ]

        # Tokenizes the context
        prompt = self.processor.tokenizer.apply_chat_template(context, tokenize=False, add_generation_prompt=True)

        # Constructs the embeddings
        inputs = self.processor(prompt, [image], return_tensors="pt").to("cuda:0")
        
        # Generates the output
        generate_ids = self.model.generate(**inputs, eos_token_id=self.processor.tokenizer.eos_token_id, **self.generation_args)

        # Gets rid of the input text
        generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]

        # Decodes the output into a string
        response = self.processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        return response