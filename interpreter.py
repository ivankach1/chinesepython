from pydub import AudioSegment
from pydub.playback import play
import threading


def run_code(cmd):
    translations = {
        "print": "印刷",
        "(": "左括号",
        ")": "右括号",
        "input": "输入",
        "=": "转让",
        "if": "如果",
        "else": "否则",
        "elif": "否则如果",
        "for": "为",
        "while": "再见",
        "break": "中止",
        "continue": "继续",
        "return": "返回",
        "def": "定义",
        "class": "类",
        "import": "进口",
        "from": "来自",
        "as": "如何",
        "try": "尝试",
        "except": "例外",
        "finally": "终于",
        "with": "与",
        "pass": "跳过",
        "global": "全球",
        "nonlocal": "非本地",
        "and": "和",
        "or": "或",
        "not": "不是",
        "in": "在",
        "is": "是",
        "True": "真的",
        "False": "假",
        "None": "没什么"
    }



    for value in translations.values():
        cmd = cmd.replace(value, "")

    for key, value in translations.items():
        cmd = cmd.replace(key, value)

    try:
        exec(cmd)
    except Exception as e:
        print("лох")

def soundtrack():

    sound = AudioSegment.from_mp3("sound.mp3")
    t = threading.Thread(target=play, args=(sound,))
    t.start()

if name == "main":
    soundtrack()
    while True:
        cmd = input(">>> ")

        if cmd == "выход":
            break

        run_code(cmd)
