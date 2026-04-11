import warnings
warnings.filterwarnings("ignore", message="Core Pydantic V1 functionality isn't compatible with Python 3.14")

from langchain_core.prompts import load_prompt
from langchain_core.load import loads


template1 = load_prompt("prompt.json", encoding="utf-8")
print(template1.format(name="张三", what="搞笑的"))

"""
base_dir = os.path.dirname(__file__)
with open(os.path.join(base_dir, "prompt_new.json"), "r", encoding="utf-8") as f:
    json_string = f.read()

# 这里的 loads 会尝试将 JSON 映射回 PromptTemplate 对象
template = loads(json_string)

# 只有映射成功，template 才是对象，才能调用 .format
print(template.format(name="年轻人", what="滑稽"))
"""

# 方式2：外部加载Prompt,将 prompt 保存为 yaml

template2 = load_prompt("prompt.yaml", encoding="utf-8")
print(template2.format(name="年轻人", what="滑稽"))
