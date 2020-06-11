# for 今日の運勢


import random


def unsei():
    unsei = ["大吉", "中吉", "吉", "小吉", "末吉",
             "凶", "大凶", "超凶", "中凶", "末凶"]

    hitokoto = ["やったね！", "やべぇ！", "はーまじかよ…",
                "もう人生薔薇色だわ！☆", "ぷぇぇ、、つらたにえん、、、",
                "＼(^o^)／ｵﾜﾀ", "ふ、こんなもんか…"]

    colors = ["白", "黒", "赤", "青", "黄色",
              "緑", "紫", "オレンジ", "ピンク",
              "空色", "黄緑", "茶色", "赤紫", "青紫",
              "紅", "朱",
              "透明", "レインボー", "俺"]

    items = ["バッグ", "ティッシュ", "けーたい", "えんぴつ", "イヤホン", "マフラー",
             "スカート", "スウェット", "タンクトップ", "どんぐり", "蛍光ペン", "腕時計",
             "筋肉", "ダンベル", "ヘアバンド", "筆", "消しゴム", "財布",
             "ハンカチ", "メガネ", "眼帯", "筆箱", "折り紙", "ビー玉",
             "お野菜", "ジーンズ", "流れ星", "CD", "ろうそく", "ブックケース"]

    n_unsei = random.randint(0, len(unsei) - 1)
    n_hitokoto = random.randint(0, len(hitokoto) - 1)
    n_colors = random.randint(0, len(colors) - 1)
    n_items = random.randint(0, len(items) - 1)

    output = f"あなたは{unsei[n_unsei]}！{hitokoto[n_hitokoto]}\n" \
             f"そんなあなたには{colors[n_colors]}の{items[n_items]}！"
    return output
