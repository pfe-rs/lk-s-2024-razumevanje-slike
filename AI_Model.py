from transformers import AutoModelForCausalLM, AutoProcessor
import numpy as np
from PIL import Image

class AI_Model:
    def __init__(self, model_id=None, model=None, processor=None, generation_args=None):
        if model_id is None:
            model_id = "microsoft/Phi-3-vision-128k-instruct" 
        self.model_id = model_id
        if model is None:
            model = AutoModelForCausalLM.from_pretrained(model_id,
                                                         cache_dir="/notebooks/my_models/phi_3_vision",
                                                         device_map="cuda",
                                                         trust_remote_code=True,
                                                         torch_dtype="auto",
                                                         _attn_implementation="eager") 
        self.model = model
        if processor is None:
            processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True) 
        self.processor = processor
        if generation_args is None:
            generation_args = {
                "max_new_tokens": 1024,
                "temperature": 0.0,
                "do_sample": False,
            } 
        self.generation_args = generation_args
    
    def get_response(self, message, image):
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)

        context = [
            {"role": "user", "content": "<|image_1|>\n" + message}
        ]
        prompt = self.processor.tokenizer.apply_chat_template(context, tokenize=False, add_generation_prompt=True)
        inputs = self.processor(prompt, [image], return_tensors="pt").to("cuda:0")
        
        generate_ids = self.model.generate(**inputs, eos_token_id=self.processor.tokenizer.eos_token_id, **self.generation_args)
        generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]
        response = self.processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        return response