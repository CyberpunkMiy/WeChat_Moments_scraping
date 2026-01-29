import ollama

def use_ollama(image_path):
    response = ollama.chat(
        model='llama3.2-vision',
        messages=[{
            'role': 'user',
            'content': '请具体描述这张图片内容，用中文告诉我',
            'images': [image_path]
        }]
    )

    image_description = response.message.content

    print(image_description)
    return image_description
