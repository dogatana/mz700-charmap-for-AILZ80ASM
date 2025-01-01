import json
import jaconv

HANKAKU_KATAKANA = (
    "ﾁｺｿｼｲﾊｷｸﾆﾏﾉﾘﾓﾐﾗ" 
    "ｾﾀｽﾄｶﾅﾋﾃｻﾝﾂﾛｹ｢ｧｬ"
    "ﾜﾇﾌｱｳｴｵﾔﾕﾖﾎﾍﾚﾒﾙﾈ"
    "ﾑ｣ｨｭｦ､ｩｮ\uFF9Fｪ\uFF65ｯ\uFF9E\uFF61ｫｰ"
)

KANJI = "日月火水木金土生年時分秒円"
KIGOU = {
    "←": [0x45],
    "→": [0x40],
    "↑": [0x50],
    "↓": [0x80],
    "■": [0x43],
    "●": [0x47],
    "◆": [0x44],
    "♥": [0x53],
    "♠": [0x41],
    "▩": [0x5A],
    # "／": [0x76],
    # "＼": [0x77],
    "╋": [0x1B], "┼": [0x1B],
    "┗": [0x1C], "└": [0x1C],
    "┛": [0x1D], "┘": [0x1D],
    "┣": [0x1E], "├": [0x1E],
    "┻": [0x1F], "┴": [0x1F],
    "┏": [0x5C], "┌": [0x5C],
    "┓": [0x5D], "┐": [0x5D],
    "┫": [0x5E], "┤": [0x5E],
    "┳": [0x5F], "┬": [0x5F],
    "━": [0x78], "─": [0x78],
    "┃": [0x79], "│": [0x79],
}


def main():
    charmap = {}
    # ASCII
    set_ascii(charmap)
    # 半角カタカナ
    set_kana(charmap)
    # 矢印,記号,罫線
    charmap.update(KIGOU)
    # 濁点/半濁点 カタカナ/ひらがな
    set_extra(charmap)

    dump_json(charmap, "mz700.json")
    write_testdata("charamap_test.asm")

def set_ascii(charmap):
    # 0x20
    charmap[" "] = [0]
    for c in range(ord("!"), ord(")") + 1):
        charmap[chr(c)] = [c + 0x40]
    charmap["*"] = [0x6B]
    charmap["+"] = [0x6A]
    charmap[","] = [0x2F]
    charmap["-"] = [0x2A]
    charmap["."] = [0x2E]
    charmap["/"] = [0x2D]

    # 0x30
    for c in range(ord("0"), ord("9") + 1):
        charmap[chr(c)] = [c - 0x10]
    charmap[":"] = [0x4F]
    charmap[";"] = [0x2C]
    charmap["<"] = [0x51]
    charmap["="] = [0x2B]
    charmap[">"] = [0x57]
    charmap["?"] = [0x49]

    # 0x40
    charmap["@"] = [0x55]
    for c in range(ord("A"), ord("Z") + 1):
        charmap[chr(c)] = [c - 0x40]
    charmap["["] = [0x52]
    charmap["\\"] = [0xDD]
    charmap["]"] = [0x54]

    # a-z を A-Z へ
    for code in range(ord("a"), ord("z") + 1):
        c = chr(code)
        charmap[c] = charmap[c.upper()]


def set_kana(charmap: dict):
    for n, c in enumerate(HANKAKU_KATAKANA, start=0x81):
        charmap[c] = [n]
    
def set_extra(charmap: dict):
    # 日月火水木金土生年時分秒円
    for n, c in enumerate(KANJI, start=0xD0):
        charmap[c] = [n]

    # 全角 " " - "]" 
    for code in range(ord(" "), ord("]") + 1):
        c = chr(code)
        zc = jaconv.han2zen(c, kana=True, ascii=True, digit=True)
        charmap[zc] = charmap[c]

    # カナ、ひらがな
    for c in HANKAKU_KATAKANA:
        kata = jaconv.han2zen(c, kana=True, ascii=True, digit=True)
        hira = jaconv.kata2hira(kata)
        charmap[kata] = charmap[hira] = charmap[c]
    # jaconv.han2zen は半角濁点を全角濁点に変換しない
    charmap["\u309B"] = [0xbc]
    charmap["\u309C"] = [0xb8]

    # 濁点, 半濁点
    charmap["ガ"] = charmap["が"] = charmap["カ"] + charmap["゛"]
    charmap["ギ"] = charmap["ぎ"] = charmap["キ"] + charmap["゛"]
    charmap["グ"] = charmap["ぐ"] = charmap["ク"] + charmap["゛"]
    charmap["ゲ"] = charmap["げ"] = charmap["ケ"] + charmap["゛"]
    charmap["ゴ"] = charmap["ご"] = charmap["コ"] + charmap["゛"]
    charmap["ザ"] = charmap["ざ"] = charmap["サ"] + charmap["゛"]
    charmap["ジ"] = charmap["じ"] = charmap["シ"] + charmap["゛"]
    charmap["ズ"] = charmap["ず"] = charmap["ス"] + charmap["゛"]
    charmap["ゼ"] = charmap["ぜ"] = charmap["セ"] + charmap["゛"]
    charmap["ゾ"] = charmap["ぞ"] = charmap["ソ"] + charmap["゛"]
    charmap["ダ"] = charmap["だ"] = charmap["タ"] + charmap["゛"]
    charmap["ヂ"] = charmap["ぢ"] = charmap["チ"] + charmap["゛"]
    charmap["ヅ"] = charmap["づ"] = charmap["ツ"] + charmap["゛"]
    charmap["デ"] = charmap["で"] = charmap["テ"] + charmap["゛"]
    charmap["ド"] = charmap["ど"] = charmap["ト"] + charmap["゛"]
    charmap["バ"] = charmap["ば"] = charmap["ハ"] + charmap["゛"]
    charmap["ビ"] = charmap["び"] = charmap["ヒ"] + charmap["゛"]
    charmap["ブ"] = charmap["ぶ"] = charmap["フ"] + charmap["゛"]
    charmap["ベ"] = charmap["べ"] = charmap["ヘ"] + charmap["゛"]
    charmap["ボ"] = charmap["ぼ"] = charmap["ホ"] + charmap["゛"]
    charmap["パ"] = charmap["ぱ"] = charmap["ハ"] + charmap["゜"]
    charmap["ピ"] = charmap["ぴ"] = charmap["ヒ"] + charmap["゜"]
    charmap["プ"] = charmap["ぷ"] = charmap["フ"] + charmap["゜"]
    charmap["ペ"] = charmap["ぺ"] = charmap["ヘ"] + charmap["゜"]
    charmap["ポ"] = charmap["ぽ"] = charmap["ホ"] + charmap["゜"]
    charmap["ヴ"] = charmap["ゔ"] = charmap["ウ"] + charmap["゛"]

def dump_json(obj: any, filename: str):
    with open(filename, "w") as fp:
        json.dump(obj, fp)



TEST_ASM = """
    BASE EQU 4

    ORG $1200

    LD  HL,test_data
    LD  IX,$D000 + BASE * 40


OUTER_LOOP:
    PUSH IX
    LD  A,(HL)
    INC HL
    CP  $FF
    JR  Z,EXIT

INNER_LOOP:
    LD  (IX),A
    INC IX
    LD  A,(HL)
    INC HL
    CP  $FF
    JR  Z,NEXT_LINE
    JR  INNER_LOOP

NEXT_LINE:
    POP IX
    LD  DE,40
    ADD IX,DE
    JP  OUTER_LOOP

    INC HL

EXIT:
    POP IX
    JP  $00AD ; monitor hot start

    charmap @MZ700,"mz700.json"
"""

TEST_STRING = [
    " !\"#$%&'()*+,-./0123456789:;<=>?",
    "@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]",
    " abcdefghijklmnopqrstuvwxyz",
    "ぁぃぅぇぉ　あいうえお　かきくけこ　さしすせそ",
    "ァィゥェォ　アイウエオ　カキクケコ　サシスセソ",
    "たちつてと　なにぬねの　はひふへほ　まみむめも",
    "タチツテト　ナニヌネノ　ハヒフヘホ　マミムメモ",
    "やゆよわを　んゃゅょゔ　ぱぴぷぺぽ",
    "ヤユヨワヲ　ンャュョヴ　パピプペポ",
    "がぎぐげご　ざじずぜぞ",
    "ガギグゲゴ　ザジズゼゾ",
    "だぢづでど　ばびぶべぼ",
    "ダヂヅデド　バビブベボ",
    "「」・。．",
    "←→↑↓■●◆♥♠▩",
    "┏━┳━┓  ┌─┬─┐",
    "┃→┃↓┃  │●│◆│",
    "┣━╋━┫  ├─┼─┤",
    "┃↑┃←┃  │♥│♠│",
    "┗━┻━┛  └─┴─┘",
]
def write_testdata(file):
    with open(file, "w", encoding="utf8") as fp:
        print(TEST_ASM, file=fp)
        print("test_data:", file=fp)
        for line in TEST_STRING:
            escaped = line.replace("\\", "\\\\").replace('"', '\\"')
            print(f'    db   @MZ700:"{escaped}",0xff', file=fp)
        print("    db   0xff", file=fp)

if __name__ == "__main__":
    main()
