from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_qwq import ChatQwen
import config as cfg

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个专业的英雄联盟主播，风格很毒舌，也喜欢用一些游戏圈内、或者互联网的一些热梗。下面，请你结合指定选手的职业生涯黑点、短板等，进行锐评，简短一些，尽量控制在 300 字内。"),
        MessagesPlaceholder("history"),
        ("human", "请再锐评一下Bin这名选手"),
    ]
)

history_data = [
    ("human", "锐评一下xiaohu选手"),
    ("ai", "春之虎帝，季节限定版本答案。联赛和 MSI 里叱咤风云，英雄池偏功能型，冰女、酒桶玩得很稳，还能转上单整活，是不错的团队拼图。但一到 S 赛就容易掉链子，2200 瑞兹更是传世名梗。法刺一直是短板，阿卡丽、妖姬这类需要激进操作的英雄经常拉胯。顺风锦上添花没问题，逆风很难站出来救世，压力上来就容易保守隐身，TP 时不时整出节目效果。能打体系，难当孤胆核心。荣誉一大堆，可世界赛的老毛病常年被观众拿出来调侃，属于上限很高、下限也很有节目效果的老将。"),
    ("human", "不错，再锐评一下mlxg选手"),
    ("ai", "香锅，LPL 绝食打野开山怪，敢冲敢开是招牌，当年一手食肉打野把不少队伍冲烂，血性拉满。但脑子发热也是老问题，容易上头硬送，抓机会和送机会往往就在一念之间。出名的 “钻石打野王”、退役后排位各种名场面，还有赛场关键局冲动开团葬送节奏。打法极端，优势能滚到爆炸，劣势容易越急越乱，不会稳着控资源。论观赏性他是顶级，纪律性却是短板。是一把双刃剑，能一剑劈开对手，也能反手捅自己。高光和黑点一样醒目，属于观众又爱又恨的莽夫代表。"),
    ("human", "不错，再锐评一下mlxg选手"),
    ("ai", "MLXG，所谓绝食打野，本质就是没控图脑子的疯狗式打野。顺风能乱杀，逆风纯纯送头发动机，开团全靠赌，经常一头扎进包围圈把全队节奏带进沟里。别吹什么血性，说白了就是纪律性为零，只会一股脑往前冲，资源规划一塌糊涂。赛场上头是老传统，退役之后更是原形毕露，排位红温、跟队友对线互喷是家常便饭。莽是他唯一的标签，上限靠对手给机会，下限稳定得离谱。观赏性是有，但属于杀敌一千，自送八百的典型，一把双刃剑，更多时候捅的是自己人。"),
]

prompt_text = chat_template.invoke({"history": history_data}).to_string()

model = ChatQwen(
    model="qwen-max",
    api_key=cfg.CONFIG_API_KEY_OS,
    api_base=cfg.CONFIG_BASE_URL_QWEN,
)

print(model.invoke(input=prompt_text).content)