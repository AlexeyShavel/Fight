from Common import *
from Effects import *


class Perk:
    def __init__(
        self,
        owner):
        self.owner = owner
        self.state = owner.state
        self.iOwner = owner.index
        self.enemy = self.owner.enemy
        self.works_in_stun = False

    def prehit(
        self):
        pass

    def e_prehit(
        self):
        pass

    def startGame(
        self):
        pass

    def everyStartTurn(
        self):
        pass

    def activate(
        self):
        pass


class PerkWithCooldown(Perk):
    cooldown = 0
    current_cooldown = 0

    def startGame(
        self):
        self.current_cooldown = 0

    def everyStartTurn(
        self):
        if self.state.iAttacker == self.owner.index:
            self.current_cooldown -= 1

    def prehit(
        self):
        if self.current_cooldown <= 0:
            self.current_cooldown = self.cooldown
            if not self.owner.stunned or self.works_in_stun:
                self.activate()



class PerkCritDagger(Perk):
    name = "PerkCritDagger"
    critChanceMult = 0.1
    critDmgMult = 1.2

    def startGame(
        self):
        self.owner.critCh += self.critChanceMult
        self.owner.critMult += self.critDmgMult


class PerkCat(PerkWithCooldown):
    name = "PerkPetCat"
    cooldown = 3
    catDamage = 5

    def __init__(
        self,
        owner):
        super().__init__(owner)
        self.works_in_stun = True

    def activate(
        self):
        self.enemy.takeDamage(self.catDamage, self.owner.name + "'s cat")
        self.status = StatusBleeding(self.enemy)


class PerkWeaken(PerkWithCooldown):
    name = "PerkWeaken"
    cooldown = 2


    def activate(
        self):
        self.status = StatusWeaken(self.enemy)


class PerkPistol(PerkWithCooldown):
    name = "PerkPistol"
    cooldown = 4
    Damage = 7

    def startGame(
        self):
        self.current_cooldown = 3

    def activate(
        self):

        self.status = StatusStun(self.enemy)
        self.enemy.takeDamage(self.Damage, self.owner.name + "'s pistol")

class PerkFireBall(PerkWithCooldown):
    name = "PerkFireBall"
    cooldown = 5
    Damage = 6

    def __init__(
        self,
        owner):
        super().__init__(owner)
        self.works_in_stun = False

    def activate(
        self):
            self.enemy.takeDamage(self.Damage, self.owner.name + "'s FireBall")
            self.status = StatusOnFire(self.enemy)

class PerkCounterattack(PerkWithCooldown):
    name = "PerkCounterattack"
    cooldown = 4


    def activate(
        self):
        self.status = StatusCounterattack(self.owner)


class PerkShield(PerkWithCooldown):
    name = "PerkShield"
    cooldown = 3


    def activate(
        self):
        self.status = StatusProtected(self.owner)


allPerks = [
    PerkCritDagger,  # 0
    PerkCat,  # 1
    PerkWeaken,  # 2
    PerkPistol,  # 3
    PerkFireBall, # 4
    PerkShield, # 5
    PerkCounterattack, # 6
]
