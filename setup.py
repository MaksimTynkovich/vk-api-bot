from urllib import request
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import randint
from requests import *
import requests
from io import BytesIO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import urllib.request
import random

group_id = '00000'
postID = '00000'
tokenGroup = '0000000'
accessToken = '000000'

def main():
    vkcomment = vk_api.VkApi(token=tokenGroup)
    vk_session = vk_api.VkApi(token=accessToken)
    vk = vk_session.get_api()

    longpoll = VkBotLongPoll(vk_session, group_id)
    textcomment = 'хочу в космос'
    textcomment2 = 'хочу в космос!'
    textcomment3 = 'хочу в космос)'
    for event in longpoll.listen():
        if event.type == VkBotEventType.WALL_REPLY_NEW and str(event.object.from_id) != group_id and event.object.post_id == postID and str(event.object.text).lower() == textcomment or str(event.object.text).lower() == textcomment2 or str(event.object.text).lower() == textcomment3:
            repostArray = vk.wall.getReposts(owner_id = -group_id, post_id=postID, offset=0)
            likeArray = vk.wall.getLikes(owner_id = -group_id, post_id=postID, offset=0)
            def repost(id):
                for i in range(len(repostArray['items'])):
                    if repostArray['items'][i]['from_id'] == id:
                        return True

            def like(id):
                for i in range(len(likeArray['users'])):
                    if (likeArray['users'][i]['uid']) == id:
                        return True

            def checkID(userID):
                with open("ids.txt", "r") as file:
                    for line in file:
                        if str(userID) in line:
                            file.close()
                            return True

            vk_session = vk_api.VkApi(token=accessToken)
            vk = vk_session.get_api()
            if vk.groups.isMember(group_id = group_id,user_id = event.object['from_id']) and repost(event.object['from_id']) == True and like(event.object['from_id']) == True:
                if checkID(event.object['from_id']) == True:
                    wall_post_id = str(event.object.post_id)
                    comment_id = str(event.object.id)
                    vkcomment.method('wall.createComment',{
                    'post_id': wall_post_id,
                    'owner_id': -group_id,
                    'reply_to_comment': comment_id,
                    'message': 'Вы уже получили свой билет'})
                else:
                    session = vk_api.VkApi(token=accessToken)
                    user = session.method("users.get", {"user_ids": event.object.from_id})
                    last_name = user[0]['last_name']
                    first_name = user[0]['first_name']
                    images = ["1.png", "2.png"]
                    img = Image.open(images[random.randint(0, 1)])
                    draw = ImageDraw.Draw(img)
                    fontLastName = ImageFont.truetype('consolas.ttf', 71)
                    fontname = ImageFont.truetype('consolab.ttf', 62)
                    draw.text((122, 250), last_name,font=fontLastName, fill=(0, 0, 0, 128))
                    draw.text((128, 340), first_name,font=fontname, fill=(0, 0, 0, 128))
                    bio = BytesIO()
                    bio.name = 'image.jpeg'
                    img.save(bio, 'jpeg')
                    bio.getvalue()
                    image_name = "photo{}.png".format(str(event.object.from_id))
                    server = session.method('photos.getWallUploadServer', {'group_id': group_id})
                    req = requests.post(server['upload_url'], files={'photo': (image_name, bio.getvalue())}).json()
                    photo = session.method('photos.saveWallPhoto', {'group_id': group_id, 'photo': req['photo'], 'server': req['server'], 'hash': req['hash']})
                    wall_post_id = str(event.object.post_id)
                    comment_id = str(event.object.id)
                    session.method('wall.createComment',{'owner_id': -group_id, 'post_id': wall_post_id, 'reply_to_comment': comment_id, 'from_group': group_id, 'attachments': f"photo{photo[0]['owner_id']}_{photo[0]['id']}"})
                    fullname = user[0]['last_name'] + ' ' + user[0]['first_name']
                    nameArray = [fullname]
                    nameID = str(event.object['from_id'])
                    idsArray = [nameID]
                    with open(r"list.txt", "a") as file:
                        for line in nameArray:
                            file.write(line + '\n')
                            file.close()
                    nameArray.clear()
                    with open(r"ids.txt", "a") as file:
                        for line in idsArray:
                            file.write(line + '\n')
                            file.close()
                    idsArray.clear()
            else:
                wall_post_id = str(event.object.post_id)
                comment_id = str(event.object.id)
                vkcomment.method('wall.createComment',{
                'post_id': wall_post_id,
                'owner_id': -group_id,
                'reply_to_comment': comment_id,
                'message': 'Ошибка! Одно из условий не выполнено.'})

if __name__ == '__main__':
    main()