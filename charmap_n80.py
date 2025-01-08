import json
import jaconv

def main():
    charmap = {}
    # ASCII
    set_ascii(charmap)
    # 半角カタカナ カタカナ/ひらがな
    set_kana(charmap)
    # 矢印、罫線等
    set_extra(charmap)

    dump_json(charmap, "n80.json")
    write_testdata("charmap_n80_test.asm")

def set_ascii(charmap):
    # 0x20 - 0x7e を全角文字も含めて登録
    for code in range(0x20, 0x7f):
        c = chr(code)
        charmap[c] = charmap[jaconv.han2zen(c, ascii=True, digit=True)] = [code]

def set_kana(charmap: dict):
    for code in range(0xa1, 0xe0):
        c = code.to_bytes().decode("cp932")
        kata = jaconv.han2zen(c)
        hira = jaconv.kata2hira(kata)
        charmap[c] = charmap[kata] = charmap[hira] = [code]
    
    charmap["\u3000"] = [0x20]
    # jaconv.han2zen は半角濁点を全角濁点に変換しない
    charmap["\u309B"] = [0xde]
    charmap["\u309C"] = [0xdf]
        
def set_extra(charmap: dict):
    charmap["円"] = [0xf1]
    charmap["年"] = [0xf2]
    charmap["月"] = [0xf3]
    charmap["日"] = [0xf4]
    charmap["時"] = [0xf5]
    charmap["分"] = [0xf6]
    charmap["秒"] = [0xf7]
            
    charmap["→"] = [0x1c]
    charmap["←"] = [0x1d]
    charmap["↑"] = [0x1e]
    charmap["↓"] = [0x1f]

    charmap["╋"] = charmap["┼"] = [0x8f]
    charmap["┻"] = charmap["┴"] = [0x90]
    charmap["┳"] = charmap["┬"] = [0x91]
    charmap["┫"] = charmap["┤"] = [0x92]
    charmap["┣"] = charmap["├"] = [0x93]
    charmap["━"] = charmap["─"] = [0x95]
    charmap["┃"] = charmap["│"] = [0x96]
    charmap["┏"] = charmap["┌"] = [0x98]
    charmap["┓"] = charmap["┐"] = [0x99]
    charmap["┗"] = charmap["└"] = [0x9a]
    charmap["┛"] = charmap["┘"] = [0x9b]

    charmap["◢"]= [0xe4]
    charmap["◣"]= [0xe5]
    charmap["◥"]= [0xe6]
    charmap["◤"]= [0xe7]
    charmap["♠"]= [0xe8]
    charmap["♥"]= [0xe9]
    charmap["♦"] = charmap["◆"] = [0xea]
    charmap["♣"]= [0xeb]
    charmap["●"]= [0xec]
    charmap["〇"]= [0xed]

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
    ORG $9000
    BASE equ 2

#if exists MZ700
    VRAM equ $D000
    BYTES_PER_LINE equ 40
#else
    VRAM equ $F300
    BYTES_PER_LINE equ 120
#endif

    LD  HL,test_data
    LD  IX,VRAM + BASE * 120

OUTER_LOOP:
    PUSH IX
    LD  A,(HL)
    INC HL
    CP  $FF
    JR  Z,EXIT

INNER_LOOP:
    LD  (IX),A
    INC IX
#if exists MZ700
#else
    INC IX
#endif
    LD  A,(HL)
    INC HL
    CP  $FF
    JR  Z,NEXT_LINE
    JR  INNER_LOOP

NEXT_LINE:
    POP IX
    LD  DE,BYTES_PER_LINE
    ADD IX,DE
    JP  OUTER_LOOP

    INC HL

EXIT:
    POP IX
    ;JP  $5C66 ; monitor hot start

#if exists MZ700
    ld  hl, $d800
    ld  de, $d801
    ld  bc, 999
    ld  (hl),$f0
    ldir
#endif
    HALT

    charmap @N80,"n80.json"
"""

TEST_STRING = [
    " !\"#$%&'()*+,-./0123456789:;<=>?",
    "@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_",
    " abcdefghijklmnopqrstuvwxyz{|}~",
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
    "「」・。→←↑↓◢◣◥◤♠♥♣●〇",
    "┏━┳━┓  ┌─┬─┐",
    "┃→┃↓┃  │♣│◆│",
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
            print(f'    db   @N80:"{escaped}",0xff', file=fp)
        print("    db   0xff", file=fp)

if __name__ == "__main__":
    main()
