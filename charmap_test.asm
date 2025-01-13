
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

test_data:
    db   @MZ700:" !\"#$%&'()*+,-./0123456789:;<=>?",0xff
    db   @MZ700:"@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]",0xff
    db   @MZ700:" abcdefghijklmnopqrstuvwxyz",0xff
    db   @MZ700:"ぁぃぅぇぉ　あいうえお　かきくけこ　さしすせそ",0xff
    db   @MZ700:"ァィゥェォ　アイウエオ　カキクケコ　サシスセソ",0xff
    db   @MZ700:"たちつてと　なにぬねの　はひふへほ　まみむめも",0xff
    db   @MZ700:"タチツテト　ナニヌネノ　ハヒフヘホ　マミムメモ",0xff
    db   @MZ700:"やゆよわを　んゃゅょゔ　ぱぴぷぺぽ",0xff
    db   @MZ700:"ヤユヨワヲ　ンャュョヴ　パピプペポ",0xff
    db   @MZ700:"がぎぐげご　ざじずぜぞ",0xff
    db   @MZ700:"ガギグゲゴ　ザジズゼゾ",0xff
    db   @MZ700:"だぢづでど　ばびぶべぼ",0xff
    db   @MZ700:"ダヂヅデド　バビブベボ",0xff
    db   @MZ700:"「」・。．",0xff
    db   @MZ700:"←→↑↓■●◆♥♠♣▩",0xff
    db   @MZ700:"┏━┳━┓  ┌─┬─┐",0xff
    db   @MZ700:"┃→┃↓┃  │♣│◆│",0xff
    db   @MZ700:"┣━╋━┫  ├─┼─┤",0xff
    db   @MZ700:"┃↑┃←┃  │♥│♠│",0xff
    db   @MZ700:"┗━┻━┛  └─┴─┘",0xff
    db   0xff
