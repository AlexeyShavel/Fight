from Common import log

# all cooldowns should be +=1

class StatusEffect:
    # Базовый класс, от него наследуются все бафы, дебафы. В нём только логика
    # появления, снятия, кулдауны
    def __init__(
        self,
        name,
        owner,
        cooldown):
        self.iOwner = owner.index
        self.name = name
        self.owner = owner
        self.enemy = owner.enemy
        self.state = owner.state
        self.cooldown = cooldown
        self.current_cooldown = cooldown
        owner.addStatus(self)

    def cooldownCheck(
        self):
        self.current_cooldown -= 1
        if self.current_cooldown <= 0:
            self.destroy()

    def destroy(
        self):
        self.owner.statuses.remove(self)

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


class StatusBleeding(StatusEffect):
    name = "StatusBleeding"
    cooldown = 3
    Damage = 3

    def __init__(
        self,
        owner):
        super().__init__(self.name, owner, self.cooldown)
        log([self.owner.name, " bleeds for ", str(self.cooldown), " turns!"],
            {0:self.owner.index})

    def everyStartTurn(
        self):
        self.owner.takeDamage(self.Damage, "bleeding")


class StatusWeaken(StatusEffect):
    name = "StatusWeaken"
    cooldown = 2
    coef = 0.35

    def __init__(
        self,
        owner):
        super().__init__(self.name, owner, self.cooldown)
        self.owner.dmg *= self.coef

        log([self.owner.name, " weakened for ", str(self.cooldown), " turns!"],
            {0:self.owner.index})

    def destroy(
        self):
        # if dmg gets increased, this will bug
        self.owner.dmg /= self.coef  #may bug if the damage was increased by a buff
        super().destroy()


class StatusStun(StatusEffect):
    name = "StatusStun"
    cooldown = 2

    def __init__(
        self,
        owner):
        super().__init__(self.name, owner, self.cooldown)
        owner.stunned=True

        log([self.owner.name, " stunned for ", str(self.cooldown/2),
            " turns!"],
            {0:self.owner.index})

    def destroy(
        self):
        self.owner.stunned=False
        super().destroy()

class StatusOnFire(StatusEffect):
    name = "StatusOnFire"
    cooldown = 3
    Damage = 4

    def __init__(
        self,
        owner):
        super().__init__(self.name, owner, self.cooldown)
        log([self.owner.name, " Burn for ", str(self.cooldown), " turns!"],
            {0:self.owner.index})

    def everyStartTurn(
        self):
        self.owner.takeDamage(self.Damage, "burning")

class StatusCounterattack(StatusEffect):
    name = "StatusCounterattack"
    cooldown = 3
    Damage = 10


    def __init__(
        self,
        owner):
        super().__init__(self.name, owner, self.cooldown)
        log([self.owner.name, " will counterattack ", str(self.cooldown), " turns!"],
            {0:self.owner.index})

    def e_prehit(
        self):
        self.enemy.takeDamage(self.Damage, "Warrior is counterattack")

class StatusProtected(StatusEffect):
    name = "StatusProtected"
    cooldown = 2

    def __init__(
        self,
        owner):
        super().__init__(self.name, owner, self.cooldown)
        owner.protected = True


        log([self.owner.name, " protected for ", str(self.cooldown),
            " turns!"],
            {0:self.owner.index})

    def e_prehit(
            self):
        self.owner.protected = True

    def destroy(
        self):
        self.owner.protected=False
        super().destroy()
