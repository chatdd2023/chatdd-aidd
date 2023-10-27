import torch
import torchvision.transforms as transforms
from PIL import Image

# 加载模型
model = torch.load("model.pth")
model.eval()  # 设置模型为评估模式，这将关闭dropout等影响结果的因素

# 数据预处理
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),  # 根据你的模型要求调整大小
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # 根据你的模型要求调整标准化参数
])


def predict(image_path):
    # 加载图像
    image = Image.open(image_path)
    image = preprocess(image)
    image = image.unsqueeze(0)  # 添加batch维度，因为模型期望的是batch输入

    # 进行推理
    with torch.no_grad():
        output = model(image)





