import webuiapi

class WebUIApiClient:
    def __init__(self, host='127.0.0.1', port=7861):
        self.api = webuiapi.WebUIApi(host=host, port=port)
        self.models = self.api.util_get_model_names()
        self.is_generating = False
    
    def get_models(self):
        return self.models
    
    def generate_image(self, prompt, negative_prompt, model, enable_hr=False ,steps=60, seed=-1, cfg_scale=7, sampler_index='DDIM', is_resize = False):
        if self.is_generating:
            return None
        
        self.is_generating = True

        try:
            self.api.util_set_model(model)
            result = self.api.txt2img(
                prompt=prompt,
                negative_prompt=negative_prompt,
                seed=seed,
                cfg_scale=cfg_scale,
                sampler_index=sampler_index,
                steps=steps,
                firstphase_height=512,
                firstphase_width=512,
                enable_hr=enable_hr,
                hr_scale=2,
                hr_upscaler=webuiapi.HiResUpscaler.Latent,
                hr_second_pass_steps=20,
                # hr_resize_x=1024,
                # hr_resize_y=1024,
                hr_resize_x=768,
                hr_resize_y=768,
                # hr_resize_x=2048,
                # hr_resize_y=2048,
                denoising_strength=0.8,
                restore_faces=True,
            )
            
            if is_resize != True:
                return result

            result = self.api.extra_single_image(image=result.image,
                                 upscaler_1="ESRGAN_4x",
                                 upscaling_resize=2)
            
            return result
            
        finally:
            self.is_generating = False
    
    def save_image(self, image, filename):
        image.save(filename)

    def is_generating(self):
        return self.is_generating




