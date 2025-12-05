'''
This script lets you caption all images in a local folder using the BLIP model.
Just provide the folder path and it will process each image, saving the results to a text file.
'''

# import libraries
import glob
import gradio as gr
from PIL import Image
import os
from transformers import AutoProcessor, BlipForConditionalGeneration

# loading processor and model
auto_processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def caption_images_in_folder(images_directory:str, image_extentions:list=["jpg", "jpeg", "png"], output_path:str="outputs/local_img_captions.txt"):
    """
    Generate captions for all images in a specified local directory using BLIP model.
    
    Args:
        images_directory (str): Path to the directory containing images.
        image_extentions (list): List of image file extensions to consider.
        output_path (str): Path to save the image captions.
    """
    # correct if extentions are not given as list
    if isinstance(image_extentions, str):
        image_extentions = [ext.strip() for ext in image_extentions.split(",")]

    # write path and caption in a txt file
    with open(output_path, "w") as img_captions:
        
        for img_ext in image_extentions:
            for img_dir in glob.glob(os.path.join(images_directory, f"*.{img_ext}")):

                # convert PIL Image and required format for processor
                img_for_processor = Image.open(img_dir).convert("RGB")

                # get input image by appling AutoProcessor
                input_img = auto_processor(images=img_for_processor, text="This is an image of ", return_tensors="pt")

                # get output from model
                output_img = model.generate(**input_img, max_length=100)

                # decode output using Auto Processor to get caption
                img_caption = auto_processor.decode(output_img[0], skip_special_tokens=True)

                img_captions.write(f"{os.path.basename(img_dir)}: {img_caption}\n")

        return f"Captions saved to {output_path}"
    
_ui = gr.Interface(
    fn=caption_images_in_folder,
    inputs=[
        gr.Textbox(label="Images Directory", value="example_images/"),
        gr.Textbox(label="Image Extensions (comma separated)", value="jpg,jpeg,png"),
        gr.Textbox(label="Output Path", value="outputs/local_img_captions.txt")
    ],
    outputs="text",
    title="Local Folder Image Captioning",
    description="Enter a local folder path to generate captions for all images using the BLIP model."
)
    
_ui.launch(server_name="127.0.0.1", server_port=7862, inbrowser=True)
