# main.py
from dotenv import load_dotenv  # 加载 .env 文件中的环境变量
import os  # 用于访问操作系统的环境变量
from engine import complete_reasoning_task  # 导入推理任务执行模块
from mixture import ensemble  # 导入代理组合模块（可能用于多模型推理）
import chain_store  # 导入推理链存储模块

# 加载环境变量
load_dotenv()

# 从环境变量中获取必要的 API 密钥
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")  # 模型访问 API
JINA_API_KEY = os.environ.get("JINA_API_KEY")  # 网页内容提取服务 API
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")  # 用于推理链学习的 API

def save_chain_prompt() -> bool:
    """
    提示用户是否要保存推理链。
    返回值：
        True  - 用户选择保存
        False - 用户选择不保存
    """
    while True:
        # 循环提示用户输入
        response = input("\nWould you like to save this reasoning chain for future reference? (y/n): ").lower()
        if response in ['y', 'yes']:
            return True  # 用户同意保存
        elif response in ['n', 'no']:
            return False  # 用户选择不保存
        print("Please answer 'y' or 'n'")  # 提示用户输入有效选项

def main():
    # 初始化推理链存储系统
    chain_store.init_store()

    # 定义任务描述
    task = """
    实现一个 Python 红黑树（Red-Black Tree）的数据结构，包括以下操作：
    1. 插入节点
    2. 删除节点
    3. 查找节点
    4. 中序打印树结构

    确保实现的红黑树满足以下性质：
    - 每个节点要么是红色，要么是黑色
    - 根节点是黑色
    - 所有叶子节点（NIL 节点）是黑色
    - 如果一个节点是红色，那么它的两个子节点必须是黑色
    - 从根节点到所有叶子节点的路径中，黑色节点数量必须相等

    测试该实现的步骤：
    1. 插入以下数字：[7, 3, 18, 10, 22, 8, 11, 26, 2, 6, 13]
    2. 打印树的结构，并显示节点颜色
    3. 删除节点 18 和 11
    4. 打印最终的树结构
    5. 搜索既存在又不存在的值，验证查找功能

    使用 Python 解释器工具完成上述实现和测试。
    """

    # 指定模型名称和 API 地址
    model = "anthropic/claude-3.5-sonnet"
    api_url = "https://openrouter.ai/api/v1/chat/completions"

    # 执行推理任务
    response, conversation_history, thinking_tools, output_tools = complete_reasoning_task(
        task=task,  # 任务描述
        api_key=OPENROUTER_API_KEY,  # 模型访问的 API 密钥
        model=model,  # 使用的语言模型
        api_url=api_url,  # 模型 API 地址
        verbose=True,  # 是否输出详细日志
        use_planning=False,  # 是否启用计划模式（此处关闭）
        jina_api_key=JINA_API_KEY  # 网页内容提取 API 密钥
    )

    # 检查运行是否成功（确保响应中没有错误）
    if isinstance(response, dict) and not response.get('error'):
        # 提示用户是否保存推理链
        if save_chain_prompt():
            try:
                # 保存成功的推理链
                chain_store.save_successful_chain(
                    task=task,  # 当前任务
                    conversation_history=conversation_history,  # 对话历史
                    final_response=response,  # 最终响应内容
                    cohere_api_key=COHERE_API_KEY,  # 用于学习推理链的 API
                    thinking_tools=thinking_tools,  # 使用的思考工具记录
                    output_tools=output_tools,  # 输出工具记录
                    metadata={"model": model, "api_url": api_url}  # 附加元数据
                )
                print("Chain saved successfully!")  # 成功保存提示
            except Exception as e:
                # 捕获保存过程中可能出现的错误
                print(f"Error saving chain: {str(e)}")
    else:
        # 如果运行过程中出现错误，跳过保存
        print("Run contained errors - skipping chain save prompt")

    # 返回结果
    return response, conversation_history, thinking_tools, output_tools

# 程序入口点
if __name__ == "__main__":
    main()