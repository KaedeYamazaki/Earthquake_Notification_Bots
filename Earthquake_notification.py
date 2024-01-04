import json
import time
import requests

class LINENotifyBot(object):
    API_URL = 'https://notify-api.line.me/api/notify'

    def __init__(self, access_token):
        self.__headers = {'Authorization': 'Bearer ' + access_token}

    def send_to_line(self, message, image=None, sticker_package_id=None, sticker_id=None):
        payload = {
            'message': message,
            'stickerPackageId': sticker_package_id,
            'stickerId': sticker_id,
        }
        files = {'imageFile': open(image, 'rb')} if image else {}
        requests.post(
            LINENotifyBot.API_URL,
            headers=self.__headers,
            data=payload,
            files=files,
        )



class SlackNotifyBot(object):
    def __init__(self, access_token):
        self.__headers = {'Authorization': 'Bearer ' + access_token}

    def send_to_slack(self, message,slack_ch):
        API_URL = "https://slack.com/api/chat.postMessage"
        headers = self.__headers
        data = {
            'channel': slack_ch,
            'text': message
        }
        r = requests.post(API_URL, headers=headers, data=data)



def get_earthquake_info():
    p2pquake_url = 'https://api.p2pquake.net/v2/history?codes=551&limit=1'
    p2pquake_json = requests.get(p2pquake_url).json()

    eq_info = p2pquake_json[0]
    eq_time_stamp = eq_info["issue"]["time"]
    eq_Tsunami_info = eq_info["earthquake"]["domesticTsunami"]
    eq_depth = eq_info["earthquake"]["hypocenter"]["depth"]
    eq_magnitude = eq_info["earthquake"]["hypocenter"]["magnitude"]
    eq_name = eq_info["earthquake"]["hypocenter"]["name"]
    eq_max_scale = eq_info["earthquake"]["maxScale"]
    intensity = determine_intensity(eq_max_scale)

    dict2str = json.dumps(p2pquake_json)
    json_data = json.loads(dict2str)

    message = ""

    if eq_magnitude == -1 :
        message =  (f"地震速報 \n "
                    f"TimeStamp: {eq_time_stamp}\n"
                    f"推定最大震度: {intensity}\n"
                    f"Eq_max_scale: {eq_max_scale}\n"
                    f"直ちに身の安全を確保してください．\n")

    elif eq_max_scale >= 0 :
        message =  (f"地震情報 \n "
                    f"TimeStamp: {eq_time_stamp}\n"
                    f"震源地: {eq_name}\n"
                    f"津波の有無: {eq_Tsunami_info}\n"
                    f"推定最大震度: {intensity}\n"
                    f"マグニチュード: {eq_magnitude}\n"
                    f"震源の深さ[km]: {eq_depth}\n"
                    f"Eq_max_scale: {eq_max_scale}\n"
                    f"\n"
                    f"\n"
                    f"各地点の震度一覧\n")

        # "points"の各要素から"addr"と"scale"を抽出してメッセージに追加
        for i, point in enumerate(json_data[0]["points"][:4]):
            addr = point["addr"]
            addr_intensity = determine_intensity(point["scale"])
            message += f"地点: {addr}, 推定震度: {addr_intensity}\n"

            # 上限を超えたらループを抜ける
            if i == 5:
                break

        message += (f"\n"
                    f"身の安全を確保してください．\n"
                    f"落ち着いたら，情報を集め，必要に応じて避難してください．\n"
                    f"\n"
                    f"信用できる情報源 -> https://twitter.com/UN_NERV \n")

    return message,eq_time_stamp,eq_max_scale,eq_magnitude,eq_name




def determine_intensity(eq_max_scale):
    if eq_max_scale <= 10:
        return '震度１'
    elif eq_max_scale <= 20:
        return '震度２'
    elif eq_max_scale <= 30:
        return '震度３'
    if eq_max_scale <= 40:
        return '震度４以下'
    elif eq_max_scale <= 45:
        return '震度４以上'
    elif eq_max_scale <= 50:
        return '震度５弱'
    elif eq_max_scale <= 55:
        return '震度５強'
    elif eq_max_scale <= 60:
        return '震度６弱'
    elif eq_max_scale <= 70:
        return '震度６強'
    else:
        return '震度７以上'




def main():
    memory_eq_time_stamp = 0

    with open("./settings.json", "r", encoding="utf-8") as f:
        settings = json.load(f)
    line_token = settings["LINE_token"]["my_token"]
    slack_token = settings["slack_token"]["doilab_token"]
    slack_channel = settings["slack_ch"]["doilab_ch"]
    debug_channel = settings["slack_ch"]["debug"]

    slack_bot = SlackNotifyBot(access_token=slack_token)
    line_bot = LINENotifyBot(access_token=line_token)

    line_bot.send_to_line("Bot restart")
    slack_bot.send_to_slack("Bot restart",debug_channel)

    while True:
        message,eq_time_stamp,eq_max_scale,eq_magnitude,eq_name = get_earthquake_info()

        # 推定震度4以上で通知．推定震度の参考元： https://www.p2pquake.net/develop/json_api_v2
        # 震源地の深さについて単位の情報なし．[km]と思われる．また離散的にスケーリングされているように思われる．
        if memory_eq_time_stamp != eq_time_stamp:
            if eq_magnitude == -1 :
                line_bot.send_to_line(message)
                slack_bot.send_to_slack(message,slack_channel)
            elif eq_max_scale > 0 :
                line_bot.send_to_line(message)
                slack_bot.send_to_slack(message,debug_channel)
            elif eq_max_scale >= 40 :
                line_bot.send_to_line(message)
                slack_bot.send_to_slack(message,slack_channel)

            print(f"Time_stamp: {eq_time_stamp},震源地:{eq_name},eq_max_scale:{eq_max_scale}\n")
            memory_eq_time_stamp = eq_time_stamp

if __name__ == "__main__":
    print("動作開始")
    main()