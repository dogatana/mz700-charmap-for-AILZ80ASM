
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

test_data:
    db   @N80:" !\"#$%&'()*+,-./0123456789:;<=>?",0xff
    db   @N80:"@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_",0xff
    db   @N80:" abcdefghijklmnopqrstuvwxyz{|}~",0xff
    db   @N80:"ぁぃぅぇぉ　あいうえお　かきくけこ　さしすせそ",0xff
    db   @N80:"ァィゥェォ　アイウエオ　カキクケコ　サシスセソ",0xff
    db   @N80:"たちつてと　なにぬねの　はひふへほ　まみむめも",0xff
    db   @N80:"タチツテト　ナニヌネノ　ハヒフヘホ　マミムメモ",0xff
    db   @N80:"やゆよわを　んゃゅょゔ　ぱぴぷぺぽ",0xff
    db   @N80:"ヤユヨワヲ　ンャュョヴ　パピプペポ",0xff
    db   @N80:"がぎぐげご　ざじずぜぞ",0xff
    db   @N80:"ガギグゲゴ　ザジズゼゾ",0xff
    db   @N80:"だぢづでど　ばびぶべぼ",0xff
    db   @N80:"ダヂヅデド　バビブベボ",0xff
    db   @N80:"「」・。→←↑↓◢◣◥◤♠♥♣●〇",0xff
    db   @N80:"┏━┳━┓  ┌─┬─┐",0xff
    db   @N80:"┃→┃↓┃  │♣│◆│",0xff
    db   @N80:"┣━╋━┫  ├─┼─┤",0xff
    db   @N80:"┃↑┃←┃  │♥│♠│",0xff
    db   @N80:"┗━┻━┛  └─┴─┘",0xff
    db   0xff
