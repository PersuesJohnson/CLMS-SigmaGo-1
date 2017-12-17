from __future__ import unicode_literals
from Main.models import *
# Create your views here.
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage, VoiceMessage, ImageMessage, \
    VideoMessage, LinkMessage, LocationMessage, EventMessage
from secret import Secret
import os



wechat_instance = WechatBasic(
    token=Secret.SECRET_TOKEN,
    appid=Secret.APP_ID,
    appsecret=Secret.ENCODING_AES_KEY)
home_url = Secret.HOME_URL


@csrf_exempt
def wechat(request):
    if request.method == 'GET':  # verifycation
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        if not wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            return HTTPResponseBadRequest('Verify Failed')
        return HttpResponse(request.GET.get('echostr', ''), content_type="text/plain")

    # parse the XML
    try:
        wechat_instance.parse_data(data=request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')

    message = wechat_instance.get_message()
    user_info = wechat_instance.get_user_info(message.source)

    if isinstance(message, TextMessage):
        content = message.content.strip()
        if content == 'Competition' or content == '竞赛':
            return HttpResponse(wechat_instance.response_news(get_new_comps(request)), content_type="application/xml")
        elif content == 'Lecture' or content == '讲座':
            return HttpResponse(wechat_instance.response_news(get_new_lecs(request)), content_type="application/xml")
        elif content == 'Tags' or content == '订阅标签':
            TagList = Tag.objects.all()
            reply_text = ''
            for tag in TagList:
                reply_text += '回复“tag:' + tag + '“查看该标签下最新动态\n'
            if not reply_text:
                reply_text += 'no tag'
            response = wechat_instance.response_text(content=reply_text)
            return HttpResponse(response, content_type="application/xml")
        elif content[:4] == 'tag:':
            tag = content[4:]
            return HttpResponse(wechat_instance.response_news(tagProcess(tag)), content_type="application/xml")

        elif content == '查看微信订阅':
            pass
        elif content == '添加微信订阅':
            pass



        elif content == 'function' or '功能':
            reply_text = ('回复Competition或‘竞赛’查看最新竞赛信息\n' + '回复Tags或‘订阅标签’查看可订阅标签信息'
                          '回复Lecture或‘讲座’查看最新讲座信息\n')
            response = wechat_instance.response_text(content=reply_text)
            return HttpResponse(response, content_type="application/xml")
        # elif content:
        #     pass
        else:
            reply_text = ('回复Competition或‘竞赛’查看最新竞赛信息\n' + '回复Tags或‘订阅标签’查看可订阅标签信息'
                          '回复Lecture或‘讲座’查看最新讲座信息\n')
            response = wechat_instance.response_text(content=reply_text)
            return HttpResponse(response, content_type="application/xml")
    else:
        if isinstance(message, VoiceMessage) or isinstance(message, ImageMessage):
            reply_text = ('回复Competition或‘竞赛’查看最新竞赛信息\n' + '回复Tags或‘订阅标签’查看可订阅标签信息'
                          '回复Lecture或‘讲座’查看最新讲座信息\n')
        elif isinstance(message, VideoMessage) or isinstance(message, LinkMessage):
            reply_text = ('回复Competition或‘竞赛’查看最新竞赛信息\n' + '回复Tags或‘订阅标签’查看可订阅标签信息'
                          '回复Lecture或‘讲座’查看最新讲座信息\n')
        elif isinstance(message, LocationMessage):
            reply_text = ('回复Competition或‘竞赛’查看最新竞赛信息\n' + '回复Tags或‘订阅标签’查看可订阅标签信息'
                          '回复Lecture或‘讲座’查看最新讲座信息\n')
        elif isinstance(message, EventMessage):
            if message.type == 'subscribe':
                reply_text = '感谢您的到来!回复“功能”返回使用指南'
                open_id = user_info['openid']
                isRegist = wechat_new_user(open_id)
                if isRegist:
                    reply_text += 'Welcome' + open_id
            elif message.type == 'unsubscribe':
                reply_text = '取消关注事件'
            elif message.type == 'scan':
                reply_text = '已关注用户扫描二维码！'
            elif message.type == 'location':
                reply_text = '上报地理位置'
            elif message.type == 'click':
                reply_text = '自定义菜单点击'
            elif message.type == 'view':
                reply_text = '自定义菜单跳转链接'
            elif message.type == 'templatesendjobfinish':
                reply_text = '模板消息'
            else:
                reply_text = ('回复Competition或‘竞赛’查看最新竞赛信息\n' + '回复Tags或‘订阅标签’查看可订阅标签信息'
                          '回复Lecture或‘讲座’查看最新讲座信息\n')

        response = wechat_instance.response_text(content=reply_text)
        return HttpResponse(response, content_type="application/xml")


def get_new_comps(request):
    listLen = 4
    competition_list = Competition.objects.all()
    if len(competition_list) > listLen:
        competitionList = competition_list[0:listLen - 1]
    return comp_to_array(competition_list)


def comp_to_array(comp_list):
    response = []
    for comp in comp_list:
        response.append({
            'title': comp.title,
            'picurl': os.path.join(home_url, comp.thumb_path),
            'description': comp.intro,
            'url': home_url + '/' + 'competition' + '/' + str(comp.id) + '/'
        })
    if not response:
        response.append({
            'title': "home",
            'picurl': "",
            'description': "home",
            'url': home_url
        })
    return response


def get_new_lecs(request):
    listLen = 4
    lectureList = Lecture.objects.all()
    if len(lectureList) > listLen:
        lectureList = lectureList[0:listLen - 1]
    return lec_to_array(lectureList)


def lec_to_array(lecs_list):
    response = []
    for lec in lecs_list:
        response.append({
            'title': lec.title,
            'picurl': os.path.join(home_url, lec.thumb_path),
            'description': lec.intro,
            'url': home_url + '/' + 'lecture' + '/' + str(lec.id) + '/'
        })
    if not response:
        response.append({
            'title': "home",
            'picurl': "",
            'description': "home",
            'url': home_url
        })
    return response


def tagProcess(tag):
    try:
        CompetitionList = Competition.objects.filter(tag__name=tag)
    except Competition.DoesNotExist:
        reply_text = "Content does not exit, try again please!"
        response = wechat_instance.response_text(content=reply_text)
        return HttpResponse(response, content_type="application/xml")
    try:
        LectureList = Lecture.objects.filter(tag__name=tag)
    except Lecture.DoesNotExist:
        reply_text = "Content does not exit, try again please!"
        response = wechat_instance.response_text(content=reply_text)
        return HttpResponse(response, content_type="application/xml")
    listLen = 2
    response = []
    if len(CompetitionList) <= listLen:
        for comp in CompetitionList:
            response.append({
                'title' : comp.title,
                'picurl' : os.path.join(home_url, comp.thumb_path),
                'description' : comp.intro,
                'url' : home_url + '/' + 'competition' + '/' + str(comp.id) + '/'
            })
    else:
        for comp in CompetitionList[:listLen]:
            response.append({
                'title' : comp.title,
                'picurl' : os.path.join(home_url, comp.thumb_path),
                'description' : comp.intro,
                'url' : home_url + '/' + 'competition' + '/' + str(comp.id) + '/'
            })
    if  len(LectureList) <= listLen:
        for lec in LectureList:
            response.append({
                'title' : lec.title,
                'picurl' : os.path.join(home_url, lec.thumb_path),
                'description' : lec.intro,
                'url' : home_url + '/' + 'competition' + '/' + str(lec.id) + '/'
                })
    else:
        for lec in LectureList[:listLen]:
            response.append({
                'title' : lec.title,
                'picurl' : os.path.join(home_url, lec.thumb_path),
                'description' : lec.intro,
                'url' : home_url + '/' + 'competition' + '/' + str(lec.id) + '/'
                })
    if not response:
        response.append({
            'title': "home",
            'picurl': "",
            'description': "home",
            'url': home_url
        })
    return response
    # return HttpResponse(wechat_instance.response_news(response), content_type="application/xml")


def wechat_new_user(open_id):
    registAdd = User.objects.create(
                    username=open_id)
    if registAdd:
        return True
    return False
