import pygame
import sys
import os
import gc


from Environment import Environment
from Player import Player
from Mind import Mind
from Background import Stars
import Color

gc.collect()

pygame.init()
pygame.event.get()
pygame.mouse.get_rel()


# draw a graphical bar like health or shields
def draw_bar(bar_w, pos, color, value, high, desc):
    pygame.draw.rect(env.getScreen(), Color.BLACK, (0, 5 + 15 * pos, bar_w, 10))
    pygame.draw.rect(env.getScreen(), color, (0, 5 + 15 * pos, bar_w, 10), 1)
    val = (bar_w - 1) / (high + .000001) * value
    if val < 0:
        val = 0
    if val > 298:
        val = 298
    pygame.draw.rect(Environment.getScreen(), color, (1, 6 + 15 * pos, val, 8))
    myfont.set_bold(True)
    font_text = myfont.render(str(value) + "/" + str(high), 1, (255, 255, 0))
    screen.blit(font_text, (bar_w, 1 + 15 * pos))
    screen.blit(myfont.render(desc, 1, (255, 255, 255)), (0, 1 + 15 * pos))
    myfont.set_bold(False)


# draw an entity, not used yet
def draw_ent(pos, ent, width, height, pad):
    height = height + pad
    st = ent.state
    lncol = (40, 40, 40)
    bxcol = lncol
    if st == Mind.ATTACK or st == Mind.BERZERK or st == Mind.FIRE:
        lncol = Color.RED
        bxcol = lncol
    if st == Mind.ROAM:
        lncol = (16, 38, 14)
        bxcol = (0, 255, 0)
    x, y = ent.creature.projectedPos(Player.player.get_cam ())
    x2, y2 = width, 5 + height * pos + (height + 2) / 2
    if x >= x2:
        pygame.draw.line(env.getScreen(), lncol, (x, y), (x2, y2))

    y = 5 + (height * pos) + pos + 2
    pygame.draw.rect(env.getScreen (), Color.BLACK, (0, y, width, height + 2 - pad))
    pygame.draw.rect(env.getScreen (), bxcol, (0, y, width, height + 2 - pad), 1)
    screen.blit(ent.creature.img, (0, y + 1))
    myfont.set_bold(True)
    label = myfont.render(ent.statement, 1, (255, 255, 0))
    screen.blit(label, (32, y))
    myfont.set_bold(False)


def draw_obj(pos, ent, width, height, pad):
    height = height + pad
    # st = ent.state
    # lncol = (40, 40, 40)
    # bxcol = lncol

    lncol = (16, 38, 14)
    bxcol = (0, 255, 0)
    pp = ent.pos.projectedPos(Player.player.get_cam())
    x2, y2 = Environment.screen_width - (width + 1), 5 + height * pos + (height + 2) / 2
    if x2 >= pp[1].x() and pp[0]:
        pygame.draw.line(env.getScreen(), lncol, (x2, y2), pp[1].p2D())

    y = 5 + (height * pos) + pos + 2
    pygame.draw.rect(env.getScreen (), Color.BLACK, (x2, y, width + 2, height + 2 - pad))
    pygame.draw.rect(env.getScreen (), bxcol, (x2, y, width + 2, height + 2 - pad), 1)
    screen.blit(ent.img, (Environment.screen_width - width, y + 1))
    # myfont.set_bold(True)
    # label = myfont.render(ent.statement, 1, (255, 255, 0))
    # screen.blit(label, (Environment.screen_width-width, y))
    # myfont.set_bold(False)


pitch, yaw, roll = 0, 1, 2
lens = 10

# sw, sh = 800, 600  # screen width & height
os.environ['SDL_VIDEO_CENTERED'] = '1'
env = Environment()
player = Player()
Environment.player = player
bkg = Stars.init(player.cam)

# dm = dungeonGenerator.genCaveRoom(1, 40, 40)
# dm = dungeonGenerator.genSpiderRooms(1,40, 40)
# dm = dungeonGenerator.genRooms(1,40, 40)
# print ("Dungeon processed")
# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
myfont = pygame.font.SysFont("consolas", 15)

screen = env.getScreen()
screen.set_alpha(None)
pygame.display.set_caption('Test game')
clock = pygame.time.Clock()
FPS = 1000

player.set_cam_pos(0, -10, -5)

crashed = False
lscv = 0

mbd = False
start_timer = 0
shotType = 0
deltaTime2 = 1
mouseRel = False
while not crashed:

    # do fps calculations
    pygame.display.set_caption(('FPS: ' + str ("%.2f" % (1000.0 / deltaTime2))))

    # do delta time stuff
    deltaTime2 = clock.tick(FPS)
    deltaTime = deltaTime2 / 1000.0

    # I forget what this is for, probably debuging
    Environment.interact = False

    # do event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                crashed = True
            if event.key == pygame.K_SPACE:
                mouseRel = not mouseRel
                if mouseRel:
                    pygame.mouse.set_visible(1)
                    pygame.event.set_grab(0)
                else:
                    pygame.mouse.set_visible(0)
                    pygame.event.set_grab(1)
            if event.key == pygame.K_p:
                Environment.interact = True

        player.get_cam().events(event)

    Environment.updateGlobalPosition(player.cam.pos)
    Environment.update(player.cam)

    if player.inship:
        # draw_bar (300, 0, Color.BLUE, player.ship.stats.xp, player.ship.stats.nxtlvlxp, "XP")
        draw_bar(300, 0, Color.RED, 100 - player.ship.weapon.getTemp(), 100, "Energy")
        draw_bar(300, 1, Color.GREEN, player.ship.stats.getHP(), player.ship.stats.getHTH(), "Condition")
    else:
        # draw_bar (300, 0, Color.BLUE, player.creature.stats.xp, player.creature.stats.nxtlvlxp, "XP")
        draw_bar(300, 0, Color.RED, 100-player.creature.weapon.getTemp (), 100, "Energy")
        draw_bar(300, 1, Color.GREEN, player.creature.stats.getHP(), player.creature.stats.getHTH(), "Health")

    for i, e in enumerate (Environment.visible_creatures):
        draw_ent(2 + i, e, 150, 32, 2)

    #    for i, e in enumerate(Environment.visible_objects):
    #        drawObj(2+i, e, 32, 32, 3)

    label = myfont.render("FPS:" + str ("%.2f" % (1000.0 / deltaTime2)) + "   " + str(
        "%.2f" % player.cam.pos.length()) + "   gPos:" + str(Environment.gpos), 1, (255, 255, 255))

    screen.blit(label,(0, 1 + 15 * 4))
    pygame.display.flip()

    key = pygame.key.get_pressed()

    player.get_cam().update(deltaTime, key)

pygame.quit()
sys.exit()
