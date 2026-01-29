from pathlib import Path
from main import use_ollama


name_id = "小沈"

# 设置路径
base_path = Path(r'C:\Users\15815\Desktop\data_pyq')
txt_file = base_path / f'{name_id}的朋友圈.txt'

# 图片张数
n = 9

def main():
    # 读取原文本
    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 处理每张图片并替换文本
    for i in range(1, n+1):
        image_path = base_path / f'image_description{i}.jpg'
        if image_path.exists():
            # 获取图片描述
            description = use_ollama(image_path)
            # 替换文本中的标记
            content = content.replace(f'<image_description{i}>', description)
        else:
            print("error")

    # 保存更新后的文本
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    main()