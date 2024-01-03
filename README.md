# 概要
[民間の情報・システム](https://www.p2pquake.net)を利用しているので，精度は保証できませんが，
石川で被災された方も県外の方も，情報を得る１つの手段としてご利用ください．  
地震発生から情報が届くまで，長いときは3分ほどかかります．

# settings.josnの例
settings.josnの例を示します．
[JSON の操作](https://developer.mozilla.org/ja/docs/Learn/JavaScript/Objects/JSON)を参考に，自身の環境に合わせて設定してください．

```
{
    "LINE_token":{

        "my_token":"*******************************************",
        },
    "slack_token":{
        "ws_token":"********************************************************"
    },
    "slack_ch":{
        "ws_ch":"general"
    }
}
```

# 参考
- [slackに通知させる方法　(slack API 入門 (1) - Pythonによるメッセージ送信)](https://note.com/npaka/n/n4bcb38a1ea74)
- [LINEに通知させる方法  (PythonでLINE Notifyへ通知を送る)](https://qiita.com/akeome/items/e1e0fecf2e754436afc8)
- [Pythonで地震情報を取得する](https://qiita.com/Ri-chan041213/items/b8db38b485fea960e905)
- [JSON API v2 仕様 (WebSocket API 含む)](https://www.p2pquake.net/develop/json_api_v2/)
- [JSON の操作](https://developer.mozilla.org/ja/docs/Learn/JavaScript/Objects/JSON)