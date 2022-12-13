import torch, os, time, datetime, colab, postprocessor, progress, importlib
from IPython.display import Image
from IPython.display import display

import requests
from PIL import Image
from io import BytesIO
importlib.reload(progress)
importlib.reload(postprocessor)
def process(ShouldSave, ShouldPreview = True):
    colab.prepare("img2img")
    timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
    if colab.save_settings: postprocessor.save_settings(timestamp, mode="img2img")
    num_iterations = colab.settings['Iterations']
    display("Iterations: 0/%d" % num_iterations, display_id="iterations")
    # Load image
    response = requests.get(colab.settings['InitialImageURL'])
    init_image = Image.open(BytesIO(response.content)).convert('RGB')
    init_image.thumbnail((colab.settings['Width'], colab.settings['Height']))
    display(init_image)
    # Process image
    for i in range(num_iterations):
        colab.image_id = i # needed for progress.py
        generator = torch.Generator("cuda").manual_seed(colab.settings['InitialSeed'] + i)
        start = time.time()
        image = colab.img2img(
            prompt=colab.settings['Prompt'],
            image=init_image,
            negative_prompt=colab.settings['NegativePrompt'],
            guidance_scale=colab.settings['GuidanceScale'],
            strength=colab.settings['Strength'],
            num_inference_steps=colab.settings['Steps'],
            generator=generator,
            callback=progress.callback if ShouldPreview else None,
            callback_steps=1).images[0]
        end = time.time()
        print("Execution time: %fs" % (end - start))
        if ShouldPreview:
            display(image, display_id=colab.get_current_image_uid())
        if ShouldSave:
            imageName = "%d_%d" % (timestamp, i)
            path = postprocessor.save_gdrive(image, imageName)
            print("Saved to " + path)
            postprocessor.post_process(image, imageName)
        display("Iterations: %d/%d" % (i + 1,  num_iterations), display_id="iterations")