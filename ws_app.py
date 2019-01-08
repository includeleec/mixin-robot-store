"""
Mixin Robot Store
code by Lee.c
"""
from lib.mixin_ws_api import MIXIN_WS_API
from lib.mixin_api import MIXIN_API
import config.mixin

from model.robots import Robots
from model.mixin_session import MixinSession
from model.rating_map import RatingMap

import json
from io import BytesIO
import base64
import gzip

try:
    import thread
except ImportError:
    import _thread as thread

def on_message(ws, message):

    inbuffer = BytesIO(message)

    f = gzip.GzipFile(mode="rb", fileobj=inbuffer)
    rdata_injson = f.read()
    rdata_obj = json.loads(rdata_injson)
    action = rdata_obj["action"]

    if action not in ["ACKNOWLEDGE_MESSAGE_RECEIPT", "CREATE_MESSAGE", "LIST_PENDING_MESSAGES"]:
        print("unknow action")
        return

    if action == "ACKNOWLEDGE_MESSAGE_RECEIPT":
        return


    if action == "CREATE_MESSAGE":

        data = rdata_obj["data"]
        msgid = data["message_id"]
        typeindata = data["type"]
        categoryindata = data["category"]
        userId = data["user_id"]
        conversationId = data["conversation_id"]
        dataindata = data["data"]
        created_at = data["created_at"]
        updated_at = data["updated_at"]

        realData = base64.b64decode(dataindata)

        MIXIN_WS_API.replayMessage(ws, msgid)


        if 'error' in rdata_obj:
            return

        if categoryindata not in ["SYSTEM_ACCOUNT_SNAPSHOT", "PLAIN_TEXT", "SYSTEM_CONVERSATION", "PLAIN_STICKER", "PLAIN_IMAGE", "PLAIN_CONTACT"]:
            return

        if categoryindata == "PLAIN_TEXT" and typeindata == "message":
            realData = realData.decode('utf-8')

            introductionContent = """Mixin Robot Store
you can reply [..] these below:

[hot] most popular mixin robots
[new] the latest submission mixin robots
[top] top rating mixin robots
[search] find a mixin robot by name/tag/description
[code] return a mixin robot by code (star with '7000')
[rate] rating mixin robot
[submit] submit a new mixin robot
[help] if you have other problems..."""

            robot_str_tmp = "\n" + "-" * 30
            robot_str_tmp += '\nName:{name}\nScore:{score}\nCode:{app_code}\nTags:{tags}\nDescription:{desc}'
            reply_robot_code = '\nReply {Code} will send you Robot Contact Card'

            if MixinSession.isInAction(user_id=userId, action_in='app_code'):
                print(userId + ' in action: app_code, keyword:' + realData)
                r = Robots.find(app_code=realData)
                if r is not None:
                    Robots.searched(r)
                    MIXIN_WS_API.sendUserContactCard(ws, conversationId, userId, r.app_id)
                else:
                    reply_str = 'Mixin Robot Code:' + realData + ' is not exist'
                    MIXIN_WS_API.sendUserText(ws, conversationId, userId, reply_str)
                return


            if MixinSession.isInAction(user_id=userId, action_in='rate_find'):
                print(userId + ' in action: rate_find, keyword:' + realData)
                r = Robots.find(app_code=realData)
                if r is not None:
                    reply_str = 'You want to rating this Mixin Robot, Reply 0~5 integer score\n'

                    rating_num = r.rating_num
                    if rating_num > 0:
                        score = round(r.score_avg, 1)
                    else:
                        score = 'None'

                    reply_str += robot_str_tmp.format(name=r.name, score=score, app_code=r.app_code,
                                                      tags=r.tags, desc=r.desc)
                    MIXIN_WS_API.sendUserText(ws, conversationId, userId, reply_str)
                    MixinSession.inAction(user_id=userId, action_in='rate_score', app_id=r.app_id)

                else:
                    reply_str = 'Mixin Robot Code:' + realData + ' is not exist'
                    MIXIN_WS_API.sendUserText(ws, conversationId, userId, reply_str)
                return

            if MixinSession.isInAction(user_id=userId, action_in='rate_score'):

                app_id = MixinSession.get_app_id(user_id=userId, action_in='rate_score')
                if app_id:
                    print(userId + ' in action: rate_score, keyword:' + realData + ' robot id:'+app_id)
                else:
                    print("can't find robot app id")
                    return

                if realData in ['0', '1', '2', '3', '4', '5']:
                    RatingMap.rating(user_id=userId, app_id=app_id, score=int(realData))
                    reply_str = 'score success,thank you'
                else:
                    reply_str = 'You Must Reply 0~5 integer score\n'

                MIXIN_WS_API.sendUserText(ws, conversationId, userId, reply_str)
                return



            if MixinSession.isInAction(user_id=userId, action_in='search'):
                print(userId + ' in action: search, keyword:' + realData)
                s_list = Robots.search(keyword=realData)

                reply_str = 'Mixin Robots Search Results : ' + realData + reply_robot_code

                print(reply_str)

                if len(s_list) == 0:
                    reply_str = 'Mixin Robot Search Results :' + realData + ' is not exist'
                    MIXIN_WS_API.sendUserText(ws, conversationId, userId, reply_str)
                    return

                for r in s_list:
                    rating_num = round(r.get('rating_num'), 1)
                    if rating_num > 0:
                        score = r.get('score_avg')
                    else:
                        score = 'None'
                    reply_str += robot_str_tmp.format(name=r.get('name'), score=score, app_code=r.get('app_code'),
                                                      tags=r.get('tags'), desc=r.get('desc'))

                print(reply_str)
                MIXIN_WS_API.sendUserText(ws, conversationId, userId, reply_str)
                MixinSession.inAction(user_id=userId, action_in='app_code')

                return

            print('normal mode')

            if realData.lower() in ['hot', 'new', 'top']:
                robots_list_func = getattr(Robots, realData)
                reply_str = 'Mixin Robots Top 10: ' + realData.upper() + reply_robot_code

                MixinSession.inAction(user_id=userId, action_in='app_code')

                print(reply_str)

                for r in robots_list_func():
                    rating_num = r.rating_num
                    if rating_num > 0:
                        score = round(r.score_avg, 1)
                    else:
                        score = 'None'

                    reply_str += robot_str_tmp.format(name=r.name, score=score, app_code=r.app_code, tags=r.tags, desc=r.desc)

                print(reply_str)

                MIXIN_WS_API.sendUserText(ws, conversationId, userId, reply_str)
                return

            if 'search' == realData.lower():
                reply_str = "Reply Mixin Robot's name/tag/description, we will show you related results"

                MIXIN_WS_API.sendUserText(ws, conversationId, userId, reply_str)
                MixinSession.inAction(user_id=userId, action_in='search')
                return

            if 'code' == realData.lower():
                reply_str = "Reply Mixin Robot's Code(star with '7000'), we will return the robot"

                MIXIN_WS_API.sendUserText(ws, conversationId, userId, reply_str)
                MixinSession.inAction(user_id=userId, action_in='app_code')
                return

            if 'rate' == realData.lower():
                reply_str = "Rating mixin robot, Reply the mixin robot code which you want to rating"
                MIXIN_WS_API.sendUserText(ws, conversationId, userId, reply_str)
                MixinSession.inAction(user_id=userId, action_in='rate_find')
                return

            if 'submit' == realData.lower():
                MIXIN_WS_API.sendUserAppButton(ws, conversationId, userId,
                                               "http://m3blockchain.mikecrm.com/A95F8m4",
                                               "Submit a new mixin robot", colorOfLink="#267dc5")
                return

            if 'help' == realData.lower():
                reply_str = "If you have any problem or advice, you can send email to: includeleec@gmail.com or add my wechat:leec121"

                MIXIN_WS_API.sendUserText(ws, conversationId, userId, reply_str)
                return

            else:

                MIXIN_WS_API.sendUserText(ws, conversationId, userId, introductionContent)
                return

        elif categoryindata == "PLAIN_TEXT":
            print("PLAIN_TEXT but unkonw:")



if __name__ == "__main__":

    # mixin_api = MIXIN_API(config.mixin)
    mixin_ws = MIXIN_WS_API(on_message=on_message)
    mixin_ws.run()

