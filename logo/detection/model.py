#!/usr/bin/python

import sys
import torch
from PIL import Image, ImageDraw
from PIL import ImageFilter
from torchvision import transforms

assert len(sys.argv) == 5

model_path = sys.argv[1]
mode = sys.argv[2]
image_from_path = sys.argv[3]
image_to_path = sys.argv[4]

assert mode in ["-bl", "-bb", "-fl"]

image = Image.open(image_from_path).convert('RGB')
model = torch.load(model_path, map_location=torch.device('cpu'))
model.eval()

score_filter = 0.7
prediction = model([transforms.ToTensor()(image)])[0]
predict_boxes = prediction['boxes']
predict_scores = prediction['scores']

draw = ImageDraw.Draw(image)

for i, box in enumerate(predict_boxes):
    if predict_scores[i] < score_filter:
      break

    if mode=="-bl":
        ib = (int(box[0]), int(box[1]), int(box[2]), int(box[3]))
        ic = image.crop(ib)
        for i in range(20):
            ic = ic.filter(ImageFilter.GaussianBlur())
        image.paste(ic, ib)
    elif mode=="-bb":
        draw.rectangle([(box[0], box[1]), (box[2], box[3])], outline=(255, 0, 0))
    elif mode=="-fl":
        draw.rectangle([(box[0], box[1]), (box[2], box[3])], fill=(255, 0, 0))

del draw

image.save(image_to_path, "PNG")