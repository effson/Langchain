import warnings
warnings.filterwarnings("ignore", message="Core Pydantic V1 functionality isn't compatible with Python 3.14")

from langchain_core.prompts import load_prompt

template1 = load_prompt("prompt.json", encoding="utf-8")
print(template1.format(name="张三", what="搞笑的"))

# 方式2：外部加载Prompt,将 prompt 保存为 yaml

template2 = load_prompt("prompt.yaml", encoding="utf-8")
print(template2.format(name="年轻人", what="滑稽"))
