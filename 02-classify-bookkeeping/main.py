from openai import OpenAI
import config as cfg
import tools

myBaseUrl = cfg.CONFIG_BASE_URL
myApiKey = cfg.CONFIG_API_KEY
myModelName = cfg.CONFIG_MODEL_NAME

client = OpenAI(
    api_key=myApiKey,
    base_url=myBaseUrl,
)

consumeTypes = ["聚餐", "饮食", "购物", "日用", "交通", "买菜", "水果", "零食", "运动", "娱乐", "通讯", "服饰", "美容", "住房",
                "孩子", "长辈", "社交", "旅行", "烟酒", "数码", "汽车", "医疗", "学习", "宠物", "礼金"]
exampleDatas = [
    {
        "input": "刚吃早餐花了30块",
        "output": {
            "time": "2026-10-09 14:54:18",
            "consume_type": "饮食",
            "cost": "30"
        }
    },
    {
        "input": "昨晚9点请朋友吃饭花了188",
        "output": {
            "time": "2026-10-08 21:00:00",
            "consume_type": "聚餐",
            "cost": "188"
        }
    },
    {
        "input": "10月1日给红十字会捐款500块",
        "output": {
            "time": "2026-10-01 08:00:00",
            "consume_type": "未知类型",
            "cost": "500"
        }
    },
]
systemPrompt = f"""
    你是一个专业的记账分类员，请根据用户的输入，提取出时间、消费类型以及花费这三个信息。
    日期&时间规则:
        - 输出格式: YYYY-MM-DD HH:MM:SS（24小时制）
        - 用户输入中，有具体日期和时间的，取用户输入的日期和时间
        日期规则:
            - 用户输入中，没有日期信息，取当前时间的日期
            - 用户输入中，有相对日期信息，如今天、昨天、本周一、上周天等，先调用工具查询当前时间的日期，然后进行推算，用户的日期是哪天
            - 日期一定要严谨，不要自己乱猜，不确定可以反问用户
        时间规则：
            - 用户输入中，只有日期，没有时间点的，取早上8点整
            - 用户输入中，只有日期，时间点是模糊的，比如说晚上，吃午饭等，时间点取值如下
                - 凌晨，取3点整
                - 早上，取8点整
                - 上午，取10点整
                - 中午，取12点整
                - 下午，取15点整
                - 晚上，取20点整
                - 深夜，取23点整
    分类规则：
        - 所有分类: {consumeTypes}
        - 根据用户描述，从所有分类中，选取最贴近的一个分类，要合理，不贴近的不要强行归纳
        - 如果在素有分类中找不到合适的，则输出"未知类型"
        - 聚餐和饮食分类说明: 在外面吃大餐，分类为聚餐，一日三餐，分类为饮食
    输出规则:
        - 请描述出思考过程
        - 最终输出为json格式，时间、消费类型、花费的key分别为: time、consume_type、cost
    """
userInput = [
    "昨天买足彩花了1600",
    "今天吃午饭花了20",
]
messages = [
    {
        "role": "system",
        "content": systemPrompt,
    },
]

for temp in exampleDatas:
    messages.append(
        {
            "role": "user",
            "content": temp["input"],
        }
    )

    messages.append(
        {
            "role": "assistant",
            "content": str(temp["output"]),
        }
    )

for q in userInput:
    print("=================================== start ===================================")
    curMessages = messages[:]
    curMessages.append(
        {
            "role": "user",
            "content": q,
        }
    )

    stream = client.chat.completions.create(
        model=myModelName,
        messages=curMessages,
        tools=tools.tools_desc,
        tool_choice="auto",
        stream=True
    )

    # ---- 累积器 ----
    assistant_text = ""  # 累积文本内容
    tool_calls_buffer = {}  # {index: {"id": ..., "name": ..., "arguments": ...}}

    # ---- 逐 chunk 处理 ----
    for chunk in stream:
        delta = chunk.choices[0].delta

        # 1) 文本内容：直接打印，实现流式输出
        if delta.content:
            assistant_text += delta.content
            print(delta.content, end="", flush=True)

        # 2) 工具调用分片：累积
        if delta.tool_calls:
            for tc in delta.tool_calls:
                idx = tc.index
                if idx not in tool_calls_buffer:
                    tool_calls_buffer[idx] = {
                        "id": "",
                        "name": "",
                        "arguments": "",
                    }
                if tc.id:
                    tool_calls_buffer[idx]["id"] = tc.id
                if tc.function:
                    if tc.function.name:
                        tool_calls_buffer[idx]["name"] += tc.function.name
                    if tc.function.arguments:
                        tool_calls_buffer[idx]["arguments"] += tc.function.arguments

    # ---- 本轮结束，处理工具调用 ----
    if not tool_calls_buffer:
        # 没有工具调用，纯文本回答，结束
        # return assistant_text
        curMessages.append(
            {
                "role": "assistant",
                "content": assistant_text,
            }
        )

    # 构建 assistant 消息（包含 tool_calls）
    tool_calls_list = []
    for idx in sorted(tool_calls_buffer.keys()):
        tc = tool_calls_buffer[idx]
        tool_calls_list.append({
            "id": tc["id"],
            "type": "function",
            "function": {
                "name": tc["name"],
                "arguments": tc["arguments"],
            },
        })

    messages.append({
        "role": "assistant",
        "content": assistant_text or None,
        "tool_calls": tool_calls_list,
    })

    # 执行每个工具，并把结果追加到消息历史
    for tc in tool_calls_list:
        name = tc["function"]["name"]
        try:
            args = json.loads(tc["function"]["arguments"])
        except json.JSONDecodeError:
            args = {}

        fn = TOOL_IMPL.get(name)
        result = fn(**args) if fn else {"error": f"未知工具: {name}"}

        print(f"\n🔧 调用工具: {name}({args}) → {result}")

        messages.append({
            "role": "tool",
            "tool_call_id": tc["id"],
            "content": json.dumps(result, ensure_ascii=False),
        })

    # for chunk in stream:
    #     delta = chunk.choices[0].delta if chunk.choices else None
    #     if delta is not None and delta.content is not None:
    #         print(delta.content, flush=True, end='')

    print("=================================== end ===================================")