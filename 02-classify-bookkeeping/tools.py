import datetime

def get_current_time():
    return datetime.datetime.now().strftime("%Y:%m:%d %H:%M:%S")

tools_desc = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取今天的日期，格式YYYY-MM-DD。当用户输入的时间需要推算时，必须调用这个函数拿到基准日期再进行日期推算",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            }
        }
    }
]

tools_map = {
    "get_current_time": get_current_time,
}

if __name__ == "__main__":
    print(get_current_time())