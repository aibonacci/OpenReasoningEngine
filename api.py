from flask import Flask, request, jsonify
from engine import complete_reasoning_task  # 执行单模型推理的核心逻辑
from mixture import ensemble  # 执行多模型协作推理的核心逻辑
import traceback  # 用于捕获和返回错误堆栈信息

app = Flask(__name__)  # 创建 Flask 应用

@app.route('/reason', methods=['POST'])
def reason():
    """
    单模型推理接口
    
    接受 JSON 格式的请求数据，执行单个模型的推理任务。
    
    请求参数（JSON 格式）：
    - 必填：
      - task: 任务描述
      - api_key: 模型访问所需的 API 密钥
      - model: 模型名称
      - api_url: 模型的 API 地址
    - 可选：
      - temperature, top_p, max_tokens: 模型的生成参数
      - verbose: 是否输出详细日志
      - chain_store_api_key, wolfram_app_id: 相关工具的 API 密钥
      - max_reasoning_steps: 最大推理步骤数
      - image: 输入图像（URL 或 Base64 编码）
      - output_tools: 输出工具描述
      - reflection_mode: 是否开启反思模式
      - previous_chains: 上一次对话的推理链
      - jina_api_key: Jina 工具的 API 密钥

    返回：
    - response: 推理结果
    - reasoning_chain: 推理步骤记录
    - thinking_tools: 使用的工具记录
    - output_tools: 输出工具的返回信息
    """
    try:
        # 获取请求数据
        data = request.get_json()

        # 检查必填参数
        task = data.get('task')
        api_key = data.get('api_key')
        model = data.get('model')
        api_url = data.get('api_url')

        if not all([task, api_key, model, api_url]):
            return jsonify({'error': '缺少必填参数：task, api_key, model, api_url'}), 400

        # 获取可选参数，设置默认值
        temperature = data.get('temperature', 0.7)
        top_p = data.get('top_p', 1.0)
        max_tokens = data.get('max_tokens', 500)
        verbose = data.get('verbose', False)
        chain_store_api_key = data.get('chain_store_api_key')
        wolfram_app_id = data.get('wolfram_app_id')
        max_reasoning_steps = data.get('max_reasoning_steps', 10)
        image = data.get('image')
        output_tools = data.get('output_tools', [])
        reflection_mode = data.get('reflection_mode', False)
        previous_chains = data.get('previous_chains', [])
        num_candidates = data.get('num_candidates', 1)
        beam_search_enabled = data.get('beam_search_enabled', False)
        use_planning = data.get('use_planning', False)
        use_jeremy_planning = data.get('use_jeremy_planning', False)
        jina_api_key = data.get('jina_api_key')

        # 执行单模型推理任务
        response, history, thinking_tools, output_tools = complete_reasoning_task(
            task=task,
            api_key=api_key,
            model=model,
            api_url=api_url,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            verbose=verbose,
            chain_store_api_key=chain_store_api_key,
            wolfram_app_id=wolfram_app_id,
            max_reasoning_steps=max_reasoning_steps,
            image=image,
            output_tools=output_tools,
            reflection_mode=reflection_mode,
            previous_chains=previous_chains,
            num_candidates=num_candidates,
            beam_search_enabled=beam_search_enabled,
            use_planning=use_planning,
            use_jeremy_planning=use_jeremy_planning,
            jina_api_key=jina_api_key
        )

        # 返回推理结果
        return jsonify({
            'response': response,
            'reasoning_chain': history,
            'thinking_tools': thinking_tools,
            'output_tools': output_tools
        })

    except Exception as e:
        # 捕获异常并返回错误堆栈
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500


@app.route('/ensemble', methods=['POST'])
def run_ensemble():
    """
    集成推理接口
    
    接受 JSON 格式的请求数据，协调多个模型协同完成任务。
    
    请求参数（JSON 格式）：
    - 必填：
      - task: 任务描述
      - agents: 代理模型列表，每个代理需包含 model, api_key, api_url, temperature 等信息
      - coordinator: 协调模型信息
    - 可选：
      - verbose: 是否输出详细日志
      - chain_store_api_key: 推理链存储工具 API 密钥
      - max_workers: 并发任务数
      - return_reasoning: 是否返回推理链
      - max_reasoning_steps: 每个代理的最大推理步骤数
      - coordinator_max_steps: 协调模型的最大步骤数
      - temperature, top_p, max_tokens: 模型生成参数
      - reflection_mode: 是否启用反思模式

    返回：
    - response: 协调模型的结果
    - agent_results: 每个代理的推理详情（可选）
    """
    try:
        # 获取请求数据
        data = request.get_json()

        # 检查必填参数
        task = data.get('task')
        agents = data.get('agents')
        coordinator = data.get('coordinator')

        if not all([task, agents, coordinator]):
            return jsonify({'error': '缺少必填参数：task, agents, coordinator'}), 400

        # 获取可选参数，设置默认值
        verbose = data.get('verbose', False)
        chain_store_api_key = data.get('chain_store_api_key')
        max_workers = data.get('max_workers', 3)
        return_reasoning = data.get('return_reasoning', False)
        max_reasoning_steps = data.get('max_reasoning_steps', 10)
        coordinator_max_steps = data.get('coordinator_max_steps', 5)
        wolfram_app_id = data.get('wolfram_app_id')
        temperature = data.get('temperature', 0.7)
        top_p = data.get('top_p', 1.0)
        max_tokens = data.get('max_tokens', 500)
        reflection_mode = data.get('reflection_mode', False)

        # 执行集成推理任务
        result = ensemble(
            task=task,
            agents=agents,
            coordinator=coordinator,
            verbose=verbose,
            chain_store_api_key=chain_store_api_key,
            max_workers=max_workers,
            return_reasoning=return_reasoning,
            max_reasoning_steps=max_reasoning_steps,
            coordinator_max_steps=coordinator_max_steps,
            wolfram_app_id=wolfram_app_id,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            reflection_mode=reflection_mode
        )

        # 如果需要返回推理链，格式化响应
        if return_reasoning:
            coordinator_response, agent_results = result
            return jsonify({
                'response': coordinator_response,
                'agent_results': [
                    {
                        'model': config['model'],
                        'response': response,
                        'reasoning_chain': history,
                        'thinking_tools': thinking_tools,
                        'output_tools': output_tools
                    }
                    for config, response, history, thinking_tools, output_tools in agent_results
                ]
            })

        # 仅返回推理结果
        return jsonify({'response': result})

    except Exception as e:
        # 捕获异常并返回错误堆栈
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500


if __name__ == '__main__':
    # 启动服务，监听 5050 端口
    app.run(host='0.0.0.0', port=5050)