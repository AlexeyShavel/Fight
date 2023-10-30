import random
import copy
import math
from colorama import just_fix_windows_console, Fore, Style
from termcolor import colored
import time
from pprint import pprint
import sys

# use Colorama to make Termcolor work on Windows too
just_fix_windows_console()


def log(mas,colors={},pause=0):
    c = [Fore.CYAN, Fore.LIGHTRED_EX, Fore.BLACK, Fore.LIGHTGREEN_EX,
        Fore.LIGHTMAGENTA_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTBLACK_EX]

    string = ""

    if len(mas) > 100000:
        return
    for i in range(len(mas)):
        if i in colors.keys():
            string = string + c[colors[i]]
        else:
            string = string + Fore.WHITE

        string = string + str(mas[i])

    if pause > 0:
        for line in string.split("\n"):
            print(line, end="", flush=True)
            time.sleep(pause)
        print("")
    else:
        print(string)
    string += '\n'



class PlayerDiedException(Exception):
    pass


class Player:
    def __init__(
        self,
        index):
        self.index = index
        self.name = ["Warrior", "Wizard"][self.index]
        self.maxHp = 100
        self.dmg = 10
        self.critCh = 0.2
        self.critMult = 2
        self.state = None

        self.alive = True
        self.stunned = False
        self.protected = False
        self.enemy = self

        self.hp = self.maxHp
        self.perks = []
        self.statuses = []
        self.damageComment = ""

    def setState(
        self,
        state,
        index,
        enemy):
        self.state = state
        self.index = index
        self.enemy = enemy
        for p in self.perks:
            p.state = state
            p.enemy = enemy
        for s in self.statuses:
            s.state = state
            s.enemy = enemy

    def die(
        self):
        self.alive = False
        log([self.name, " just died!"], {0:self.index})
        raise PlayerDiedException()

    def addPerk(
        self,
        classPerk):
        for i in self.perks:
            if type(i) == classPerk:
                return
        self.perks.append(classPerk(self))

    def addStatus(
        self,
        status):
        self.limitStatusOnTurnCount += 1
        if self.limitStatusOnTurnCount > 30:
            return

        foundCopy = False
        for s in self.statuses:
            if s.name == status.name:
                return

        self.statuses.append(status)

    def startGame(
        self):
        self.hp = self.maxHp
        for perk in self.perks:
            perk.startGame()

        for status in self.statuses:
            status.startGame()

    def takeDamage(
        self,
        dmg,
        sourceName):

        damage = round(abs(dmg))
        self.hp -= damage

        log([sourceName, " dealt ", damage, " damage to ", self.name, ". ",
             str(self.hp), "/", str(self.maxHp), " hp left. ",
             self.damageComment],
            {
                0: (1 - self.index),
                4: self.index,
                6: self.index,
                7: self.index,
                8: self.index
            })

        self.damageComment = ""

        if self.hp <= 0:
            self.die()

    def everyStartTurn(
        self):
        log([str(status) for status in self.statuses])
        self.limitStatusOnTurnCount = 0


        for perk in self.perks:
                perk.everyStartTurn()

        for status in self.statuses:
            status.everyStartTurn()
            status.cooldownCheck()

    def prehit(
        self):
        for perk in self.perks:
            perk.prehit()
        for status in self.statuses:
            status.prehit()

    def e_prehit(
        self):
        for perk in self.perks:
            perk.e_prehit()
        for status in self.statuses:
            status.e_prehit()


def showHealth(
    player):
    hpPercent = max(0, player.hp / player.maxHp)
    hpBar = int(hpPercent * 50) * "▓"
    tail = int(max(50 - len(hpBar), 0)) * "-"
    shift = int(max(15 - len(player.name), 0)) * "_"

    log([player.name, shift, " hp: [", hpBar, tail, "]"],
        {
            0:player.index,
            1:2,
            2:player.index,
            3:player.index,
            4:player.index,
            5:player.index
        })

class State:
    def __init__(
        self):
        self.iAttacker = 0
        self.damage = 0
        self.isCrit = False
        self.iTurn = 0
        self.Players = [Player(0), Player(1)]
        for i in range(len(self.Players)):
            self.Players[i].setState(self, i, self.Players[1 - i])

    def attack(
        self):
        self.isCrit = False
        if random.random() < self.Players[self.iAttacker].critCh:
            self.isCrit = True

        # prehit phase

        self.Players[self.iAttacker].prehit()
        self.Players[1 - self.iAttacker].e_prehit()

        self.damage = self.Players[self.iAttacker].dmg
        if not self.Players[self.iAttacker].stunned and not self.Players[1 - self.iAttacker].protected:
            self.hit()

    def hit(
        self):
        if (self.isCrit):
            self.damage *= self.Players[self.iAttacker].critMult
            self.Players[1 - self.iAttacker].damageComment += "Critical hit! "

        self.Players[1 - self.iAttacker].takeDamage(self.damage,
            self.Players[self.iAttacker].name)
        if (self.isCrit):
            self.damage /= self.Players[self.iAttacker].critMult

    def Game(
        self,
        result):
        self.iAttacker = random.randrange(0, 2)
        log(["================================="])
        log(["=========== NEW GAME ============"])
        log(["================================="])
        log([""])

        showHealth(self.Players[0])
        showHealth(self.Players[1])

        try:

            for player in self.Players:
                player.startGame()
            while True:
                self.iTurn += 1

                log([""])


                self.iAttacker = 1 - self.iAttacker
                log(["≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡ Turn ", str(self.iTurn), " - ",
                    self.Players[self.iAttacker].name, " ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡"],
                    {
                        0:self.iAttacker,
                        1:self.iAttacker,
                        2:self.iAttacker,
                        3:self.iAttacker,
                        4:self.iAttacker
                    })

                self.evaded = False
                for player in self.Players:
                    player.everyStartTurn()

                self.attack()

                showHealth(self.Players[0])
                showHealth(self.Players[1])


        except PlayerDiedException:
            assert self.Players[0].alive or self.Players[1].alive
            showHealth(self.Players[0])
            showHealth(self.Players[1])
            if self.Players[0].alive:
                result[0] += 1
            else:
                result[1] += 1
