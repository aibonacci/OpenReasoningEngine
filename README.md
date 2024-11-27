以下是翻译后的内容：

<div align="center">


OpenReasoningEngine

当AI实验室正在悄悄构建封闭的推理系统时，
我们可以在开源的环境中一起创造更强大的东西。

</div>


这个仓库是一个模块化、开源的测试时计算引擎——欢迎社区中的任何人添加能够提升模型能力的有用想法到系统中。随着方法的增加，这个系统将允许用户将这些方法组合起来，大幅提升整体能力。

随着时间的推移，用户保存的成功推理链将帮助我们训练能够充分利用该系统的模型。

该引擎支持任何兼容OpenAI的接口/模型，支持函数调用，是构建各种推理系统的绝佳基础。

	⚠️ 重要提示

	我们将非常严格地选择添加到系统中的方法。如果某种方法无法明确提升系统能力，我们将不会采纳。

🚀 初始系统

核心功能

🔹 逐步推理
    通过集成工具逐步执行推理：
	•	Python解释器
	•	网络搜索（通过SerpAPI）
	•	Wolfram Alpha集成
	•	全网页内容读取（通过Jina）

🔹 基于记忆的规划
    从过去的经验中持续学习和适应

🔹 MoA
    实现了代理组合决策（Mixture of Agents）——已可用，但需进一步测试

🔹 束搜索（Beam Search）
    每一步推理时采样多个候选步骤，并选择最佳选项（即将更新为支持分叉Python解释器，大幅提升系统性能）

🔹 自我反思
    强制AI在思考时验证推理步骤

🔹 灵活的模型支持
    模型无关的API，支持任何兼容OpenAI的服务商（如OpenAI、Anthropic等）

🔹 丰富的输入/输出
    支持图片输入、函数调用和多轮对话

⚙️ 安装

1. 克隆并安装

git clone https://github.com/mshumer/OpenReasoningEngine.git
cd OpenReasoningEngine
pip install -r requirements.txt

2. 配置API

获取以下服务的API密钥：
	•	OpenRouter - 模型访问
	•	E2B - 执行Python代码
	•	SerpAPI - 网络搜索
	•	Jina（可选）- 网页内容提取
	•	Wolfram Alpha（可选）- 计算/科学查询
	•	Cohere（可选）- 学习推理链

创建一个 .env 文件：

E2B_API_KEY="your_e2b_key_here"
OPENROUTER_API_KEY="your_openrouter_key_here"
SERPAPI_API_KEY="your_serpapi_key_here"
JINA_API_KEY="your_jina_key_here"  # 可选
WOLFRAM_APP_ID="your_wolfram_key_here"  # 可选
COHERE_API_KEY="your_cohere_key_here"  # 可选

3. 加载环境变量

source .env

🛠️ 使用

运行引擎

提供两种运行方式：
	•	直接执行：python main.py
	•	启动API服务：python api.py（启动一个Flask API端点）

配置选项

代码默认设置即可运行——这些默认参数经过合理选择。如果需要定制系统推理方式，可以运行代码时调整相关参数。

工具系统

1. 内部工具

	•	在推理过程中使用
	•	默认配置包括：
	•	Python解释器（指导LLM添加断言、打印等功能，以提升性能并捕捉问题）
	•	网络搜索（SerpAPI）
	•	网页内容提取（Jina，可选）
	•	Wolfram Alpha（可选）
	•	可根据需要自定义

2. 输出工具

	•	标准AI API输出工具
	•	推理完成后调用
	•	可根据用例进行配置

🧮 学习系统

记忆管理

OpenReasoningEngine的一个主要目标是实现从经验中学习的能力。初始实现较为简单，未来会持续迭代以优化效果。

启用持续学习的步骤：

	1.	从 Cohere 获取API密钥
	2.	保存成功的推理链：

chain_store.save_successful_chain(
    task=task,
    conversation_history=history,
    final_response=response,
    cohere_api_key=cohere_api_key,
    thinking_tools=thinking_tools,
    output_tools=output_tools,
    metadata={"model": model, "api_url": api_url}
)

系统中包含了successful_chains.json作为初始推理链示例。

欢迎社区贡献此数据库，但需经过验证。如果您希望将某个链条添加到数据库中，请在这里提议。社区将对其进行投票，若结果为正面评价，将被加入下一个数据库版本（版本管理允许用户看到稳定的性能提升）。

如果您有关于简化和扩展此流程的想法，请联系我！

📊 性能说明

	•	性能可能因记忆库中的具体推理链而异（不同链条可能带来显著不同的效果）

📝 日志记录

详细模式

当verbose=True时，引擎会显示：
	•	🔄 API交互
	•	🛠️ 工具使用和结果
	•	📋 步骤推理进展

这有助于了解系统内部运行情况并诊断问题。

🧪 基准测试

我已开源了一个非常简单的LLM评估工具，可与本仓库配合使用，用于测试不同设置并了解方法效果。我还提供了一些示例评估数据集供您参考。若想尝试不同的OpenReasoningEngine设置，只需替换您自己的评估数据并调整推理参数，直到达到理想效果！

在这里尝试

🤝 贡献

欢迎任何能：
	•	✨ 显著提升系统能力
	•	📈 包含清晰性能指标的贡献

质量提升型的改进也非常受欢迎。

致谢

感谢以下人员提供的建议、反馈、创意，以及帮助我实现和测试OpenReasoningEngine初版：
	•	Steve Ickman
	•	Vasek Mlejnsky
	•	Josh Bickett
	•	Aidan Gomez
	•	Alec Velikanov（Alex，个人非常欣赏）

关注我，了解有关此项目和其他AI研究的更多更新。

OpenReasoningEngine根据MIT许可证发布。详细信息请参见LICENSE。