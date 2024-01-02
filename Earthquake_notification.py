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

class SlackNotifyBot:
    def __init__(self, access_token):
        self.__headers = {'Authorization': 'Bearer ' + access_token}

    def send_to_slack(self, message,slack_ch):
        url = "https://slack.com/api/chat.postMessage"
        headers = self.__headers
        data = {
            'channel': slack_ch,
            'text': message
        }
        r = requests.post(url, headers=headers, data=data)
        print("return ", r.json())


def get_earthquake_info():
    p2pquake_url = 'https://api.p2pquake.net/v2/history?codes=551&limit=1'
    p2pquake_json = requests.get(p2pquake_url).json()

    eq_time_stamp = p2pquake_json[0]["issue"]["time"]
    eq_name = p2pquake_json[0]["earthquake"]["hypocenter"]["name"]
    eq_max_scale = p2pquake_json[0]["earthquake"]["maxScale"]

    return eq_time_stamp, eq_name, eq_max_scale

def determine_intensity(eq_max_scale):
    if eq_max_scale < 40:
        return '震度４以下'
    elif eq_max_scale < 45:
        return '震度４以上'
    elif eq_max_scale < 50:
        return '震度５弱'
    elif eq_max_scale < 55:
        return '震度５強'
    elif eq_max_scale < 60:
        return '震度６弱'
    elif eq_max_scale < 70:
        return '震度６強'
    else:
        return '震度７以上'

def main():
    memory_eq_time_stamp = 0

    while True:
        with open("./settings.json", "r", encoding="utf-8") as f:
            settings = json.load(f)

        line_token = settings["LINE_token"]["my_token"]
        slack_token = settings["slack_token"]["doilab_token"]
        slack_channel = settings["slack_ch"]["doilab_ch"]

        eq_time_stamp, eq_name, eq_max_scale = get_earthquake_info()
        intensity = determine_intensity(eq_max_scale)

        if eq_max_scale >= 40 and memory_eq_time_stamp != eq_time_stamp:

            message=f"地震情報 \n " \
                    f"TimeStamp: {eq_time_stamp}\n" \
                    f"震源地: {eq_name}\n" \
                    f"推定震度情報: {intensity}\n" \
                    f"val: {eq_max_scale}\n" \
                    f"\n"\
                    f"安全を確保してください．\n" \
                    f"情報を集めてください．\n" \
                    f"信用できる情報源 -> https://twitter.com/UN_NERV \n"

            line_bot = LINENotifyBot(access_token=line_token)
            line_bot.send_to_line(message)
            slack_bot = SlackNotifyBot(access_token=slack_token)
            slack_bot.send_to_slack(message,slack_channel)

            memory_eq_time_stamp = eq_time_stamp

if __name__ == "__main__":
    main()