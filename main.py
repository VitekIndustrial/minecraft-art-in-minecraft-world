from mcpi.minecraft import Minecraft
import render, setheight
mine = Minecraft.create()
height = setheight.height

fileimg = '31.jpg'      #фото которое будет сгенерировано в мире

#функция определения направления взгляда игрового персонажа
def opr(rot):
    if ((rot > 0 and rot < 45) or (rot > 315 and rot < 360)) or ((rot < 0 and rot > -45) or (rot < -315 and rot > -360)):
        return '+z'
    elif (rot < 315 and rot > 225) or (rot > -135 and rot < -45):
        return '+x'
    elif (rot > 135 and rot < 225) or (rot < -135 and rot > -225):
        return('-z')
    elif (rot > 45 and rot < 135) or (rot < -225 and rot > -315):
        return('-x')

#------------------------------------Функции построения изображения в соответствие с направлением взгляда-----
def pz(posp, imaga):
    posp = (posp.x - (len(imaga[0])//2), posp.y, posp.z + 2) #в первом аргументе находим середину изображения
    imaga.reverse()
    for y in range(len(imaga)):
        for x in range(len(imaga[0])):
            mine.setBlock(x + posp[0], y + posp[1], posp[2], imaga[y][x][0], imaga[y][x][1])

def mz(posp, imaga):
    posp = (posp.x - (len(imaga[0])//2), posp.y, posp.z - 2)
    imaga.reverse()
    for y in range(len(imaga)):
        for x in range(len(imaga[0])):
            mine.setBlock(x + posp[0], y + posp[1], posp[2], imaga[y][x][0], imaga[y][x][1])
def px(posp, imaga):
    posp = (posp.x + 2, posp.y, posp.z + (len(imaga[0])//2))
    imaga.reverse()
    for y in range(len(imaga)):
        for x in range(len(imaga[0])):
            mine.setBlock(posp[0], y + posp[1], posp[2] - x, imaga[y][x][0], imaga[y][x][1])
def mx(posp, imaga):
    posp = (posp.x - 2, posp.y, posp.z + (len(imaga[0])//2))
    imaga.reverse()
    for y in range(len(imaga)):
        for x in range(len(imaga[0])):
            mine.setBlock(posp[0], y + posp[1], posp[2] - x, imaga[y][x][0], imaga[y][x][1])
#------------------------------------Функции построения изображения в соответствие с направлением взгляда-----


while True:          #Бесконечный цикл, ожидающий любого сообщения в чате игры для начала построения изображения
    if mine.events.pollChatPosts():
        ppos = mine.player.getTilePos()
        rt = mine.player.getRotation()
        if opr(rt) == '+z':
            pz(ppos, render.export_for_API_mine(render.loadimg(fileimg, height), 'new_db_learn8'))
        elif opr(rt) == '-z':
            mz(ppos, render.export_for_API_mine(render.loadimg(fileimg, height), 'new_db_learn8'))
        elif opr(rt) == '+x':
            px(ppos, render.export_for_API_mine(render.loadimg(fileimg, height), 'new_db_learn8'))
        elif opr(rt) == '-x':
            mx(ppos, render.export_for_API_mine(render.loadimg(fileimg, height), 'new_db_learn8'))