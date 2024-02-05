import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from urllib.request import urlopen
from PIL import Image
import numpy as np
import json
import sys
import time

def predict(url):
    try:
        print("Classifying image ",url)
        #img = Image.open(urlopen(url))
        img = Image.open(url)
        print(img)
        model = models.resnet18(pretrained=True)

        model.eval()
        img_tensor = transforms.ToTensor()(img).unsqueeze_(0)
        outputs = model(img_tensor)
        _, predicted = torch.max(outputs.data, 1)

        with open('./imagenet-labels.json') as f:
            labels = json.load(f)
        result = labels[np.array(predicted)[0]]
        key = url.split("/")[-1].split(".")[0]
        return key, f"{key}, {result}"
    
    except Exception as error:
        print("Error while classifing image ",url," ", error)
    return url,""
