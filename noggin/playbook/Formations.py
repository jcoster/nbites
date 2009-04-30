

from . import Roles
from . import SubRoles
from . import PBConstants

def fNoFieldPlayers(team):
    '''when only the goalie is active'''
    if team.isGoalie():
        return [PBConstants.NO_FIELD_PLAYERS] + Roles.rGoalie(team)
    else:
        return [PBConstants.NO_FIELD_PLAYERS, PBConstants.INIT_ROLE,
            PBConstants.INIT_SUB_ROLE, [0,0] ]

def fOneDown(team):
    """
    Formation for one missing field player
    """
    if team.isGoalie():
        return [PBConstants.ONE_DOWN] + Roles.rGoalie(team)
    # gets teammate that is chaser (could be me)
    chaser_mate = team.determineChaser()
    # if i am chaser
    if chaser_mate.playerNumber == team.brain.my.playerNumber:
        #team.me.role = PBConstants.CHASER
        return [PBConstants.ONE_DOWN] + Roles.rChaser(team)
    else:
        #team.me.role = PBConstants.DEFENDER
        return [PBConstants.ONE_DOWN] + Roles.rDefender(team)

def fSpread(team):
    if team.isGoalie():
        return [PBConstants.SPREAD] + Roles.rGoalie(team)
    # gets teammate that is chaser (could be me)
    chaser_mate = team.determineChaser()
    chaser_mate.role = PBConstants.CHASER

    # if i am chaser
    if chaser_mate.playerNumber == team.brain.my.playerNumber:
        return [PBConstants.SPREAD] + Roles.rChaser(team)
    # Get where the defender should be
    else:
        defInfo = Roles.rDefender(team)
        return [PBConstants.SPREAD] + defInfo

def fDubD(team):
    if team.isGoalie():
        return [PBConstants.DUB_D] + Roles.rGoalie(team)
    # If we're down a player, use different positions
    if team.numInactiveMates == 0:

        # Figure out who isn't penalized with you
        other_teammate = team.getOtherActiveTeammate()

        # Determine if we should have two defenders or a defender 
        # and a middie dependent on score differential
        pos1 = PBConstants.LEFT_DEEP_BACK_POS
        pos2 = PBConstants.RIGHT_DEEP_BACK_POS
        role = PBConstants.DEFENDER

        # Figure out who should go to which position
        pos = team.getLeastWeightPosition((pos1,pos2), other_teammate)
        if pos == PBConstants.LEFT_DEEP_BACK_POS:
            role = PBConstants.DEFENDER
            subRole = PBConstants.LEFT_DEEP_BACK

        elif pos == PBConstants.RIGHT_DEEP_BACK_POS:
            role = PBConstants.DEFENDER
            subRole = PBConstants.RIGHT_DEEP_BACK

        else:
            role = PBConstants.OFFENDER
            subRole = PBConstants.DUBD_OFFENDER

    # If we are the only player, become the sweeper
    elif team.numInactiveMates == 1:
        pos = (PBConstants.SWEEPER_X, PBConstants.SWEEPER_Y)
        role = PBConstants.DEFENDER
        subRole = PBConstants.SWEEPER

    # position setting
    return [PBConstants.DUB_D, role, subRole, pos]

def fFinder(team):
    '''no one knows where the ball is'''
    if team.isGoalie():
        return [PBConstants.FINDER] + Roles.rGoalie(team)
    #team.me.role = PBConstants.SEARCHER
    return [PBConstants.FINDER] + Roles.rSearcher(team)

def fKickoffPlay(team):
    '''time immediately after kickoff'''
    if team.isGoalie():
        return [PBConstants.KICKOFF_PLAY] + Roles.rGoalie(team)
    if team.brain.my.playerNumber == 2:
        return [PBConstants.KICKOFF_PLAY, PBConstants.DEFENDER] + \
            SubRoles.pKickoffPlaySweeper(team)
    elif team.brain.my.playerNumber == 3:
        return [PBConstants.KICKOFF_PLAY] + Roles.rChaser(team)

def fKickoff(team):
    '''time immediately after kickoff'''
    if team.isGoalie():
        return [PBConstants.KICKOFF] + Roles.rGoalie(team)
    if team.me.playerNumber == 2:
        #team.me.role = PBConstants.DEFENDER
        return [PBConstants.KICKOFF,PBConstants.DEFENDER] + \
            SubRoles.pKickoffSweeper(team)
    elif team.me.playerNumber == 3:
        #team.me.role = PBConstants.CHASER
        return [PBConstants.KICKOFF] + Roles.rChaser(team)

def fOneKickoff(team):
    """
    kickoff for only having one field player
    """
    if team.isGoalie():
        return [PBConstants.ONE_KICKOFF] + Roles.rGoalie(team)
    #team.me.role = PBConstants.CHASER
    return [PBConstants.ONE_KICKOFF] + Roles.rChaser(team)

def fReady(team):
    '''kickoff positions'''
    if team.isGoalie():
        return [PBConstants.READY] + Roles.rGoalie(team)
    # ready state depends on number of players alive
    num_inactive_teammates = len(team.inactiveMates)

    # if two dogs alive, position normally
    if num_inactive_teammates == 0:
        if team.me.playerNumber == 2:
            return [PBConstants.READY, PBConstants.DEFENDER] + \
                SubRoles.pReadyDefender(team)

        elif team.me.playerNumber == 3:
            return [PBConstants.READY, PBConstants.CHASER] + \
                SubRoles.pReadyChaser(team)

    # one dogs alive, alter positions a bit
    elif num_inactive_teammates == 1:
        return [PBConstants.READY, PBConstants.CHASER] + \
            SubRoles.pReadyChaser(team)

# Formations for testing roles
def fTestDefender(team):
    return [PBConstants.TEST_DEFEND] + Roles.rDefender(team)
def fTestOffender(team):
    return [PBConstants.TEST_OFFEND] + Roles.rOffender(team)
def fTestChaser(team):
    return [PBConstants.TEST_CHASE] + Roles.rChaser(team)
