from panda3d.core import *
from otp.nametag.NametagGroup import *
from toontown.hood import ZoneUtil
from toontown.toonbase import TTLocalizer, ToontownBattleGlobals, ToontownGlobals
import ToonDNA

QUEST_MOVIE_CLEAR = 0
QUEST_MOVIE_REJECT = 1
QUEST_MOVIE_COMPLETE = 2
QUEST_MOVIE_INCOMPLETE = 3
QUEST_MOVIE_ASSIGN = 4
QUEST_MOVIE_BUSY = 5
QUEST_MOVIE_QUEST_CHOICE = 6
QUEST_MOVIE_QUEST_CHOICE_CANCEL = 7
QUEST_MOVIE_TRACK_CHOICE = 8
QUEST_MOVIE_TRACK_CHOICE_CANCEL = 9
QUEST_MOVIE_TIMEOUT = 10
QUEST_MOVIE_TIER_NOT_DONE = 11
PURCHASE_MOVIE_CLEAR = 0
PURCHASE_MOVIE_START = 1
PURCHASE_MOVIE_START_BROWSE = 9
PURCHASE_MOVIE_START_BROWSE_JBS = 11
PURCHASE_MOVIE_COMPLETE = 2
PURCHASE_MOVIE_NO_MONEY = 3
PURCHASE_MOVIE_TIMEOUT = 8
PURCHASE_MOVIE_START_NOROOM = 10
SELL_MOVIE_CLEAR = 0
SELL_MOVIE_START = 1
SELL_MOVIE_COMPLETE = 2
SELL_MOVIE_NOFISH = 3
SELL_MOVIE_TROPHY = 4
SELL_MOVIE_TIMEOUT = 8
SELL_MOVIE_PETRETURNED = 9
SELL_MOVIE_PETADOPTED = 10
SELL_MOVIE_PETCANCELED = 11
SELL_MOVIE_CHEATER = 15
PARTY_MOVIE_CLEAR = 0
PARTY_MOVIE_START = 1
PARTY_MOVIE_COMPLETE = 2
PARTY_MOVIE_ALREADYHOSTING = 3
PARTY_MOVIE_MAYBENEXTTIME = 4
PARTY_MOVIE_MINCOST = 6
PARTY_MOVIE_TIMEOUT = 7
BLOCKER_MOVIE_CLEAR = 0
BLOCKER_MOVIE_START = 1
BLOCKER_MOVIE_TIMEOUT = 8
NPC_REGULAR = 0
NPC_CLERK = 1
NPC_TAILOR = 2
NPC_HQ = 3
NPC_BLOCKER = 4
NPC_FISHERMAN = 5
NPC_PETCLERK = 6
NPC_KARTCLERK = 7
NPC_PARTYPERSON = 8
NPC_SPECIALQUESTGIVER = 9
NPC_FLIPPYTOONHALL = 10
NPC_SCIENTIST = 11
NPC_GLOVE = 12
NPC_LAFF_RESTOCK = 13
QUEST_COUNTDOWN_TIME = 120
CLERK_COUNTDOWN_TIME = 120
TAILOR_COUNTDOWN_TIME = 300

def getRandomDNA(seed, gender):
    randomDNA = ToonDNA.ToonDNA()
    randomDNA.newToonRandom(seed, gender, 1)
    return randomDNA.asTuple()

def createNPC(air, npcId, desc, zoneId, posIndex = 0, questCallback = None):
    import DistributedNPCToonAI
    import DistributedNPCClerkAI
    import DistributedNPCTailorAI
    import DistributedNPCBlockerAI
    import DistributedNPCFishermanAI
    import DistributedNPCPetclerkAI
    import DistributedNPCKartClerkAI
    import DistributedNPCPartyPersonAI
    import DistributedNPCSpecialQuestGiverAI
    import DistributedNPCFlippyInToonHallAI
    import DistributedNPCScientistAI
    import DistributedNPCGloveAI
    import DistributedNPCLaffRestockAI
    canonicalZoneId, name, dnaType, gender, protected, type = desc
    if type == NPC_REGULAR:
        npc = DistributedNPCToonAI.DistributedNPCToonAI(air, npcId, questCallback=questCallback)
    elif type == NPC_HQ:
        npc = DistributedNPCToonAI.DistributedNPCToonAI(air, npcId, questCallback=questCallback, hq=1)
    elif type == NPC_CLERK:
        npc = DistributedNPCClerkAI.DistributedNPCClerkAI(air, npcId)
    elif type == NPC_TAILOR:
        npc = DistributedNPCTailorAI.DistributedNPCTailorAI(air, npcId)
    elif type == NPC_BLOCKER:
        npc = DistributedNPCBlockerAI.DistributedNPCBlockerAI(air, npcId)
    elif type == NPC_FISHERMAN:
        npc = DistributedNPCFishermanAI.DistributedNPCFishermanAI(air, npcId)
    elif type == NPC_PETCLERK:
        npc = DistributedNPCPetclerkAI.DistributedNPCPetclerkAI(air, npcId)
    elif type == NPC_KARTCLERK:
        npc = DistributedNPCKartClerkAI.DistributedNPCKartClerkAI(air, npcId)
    elif type == NPC_PARTYPERSON:
        npc = DistributedNPCPartyPersonAI.DistributedNPCPartyPersonAI(air, npcId)
    elif type == NPC_SPECIALQUESTGIVER:
        npc = DistributedNPCSpecialQuestGiverAI.DistributedNPCSpecialQuestGiverAI(air, npcId)
    elif type == NPC_FLIPPYTOONHALL:
        npc = DistributedNPCFlippyInToonHallAI.DistributedNPCFlippyInToonHallAI(air, npcId)
    elif type == NPC_SCIENTIST:
        npc = DistributedNPCScientistAI.DistributedNPCScientistAI(air, npcId)
    elif type == NPC_GLOVE:
        npc = DistributedNPCGloveAI.DistributedNPCGloveAI(air, npcId)
    elif type == NPC_LAFF_RESTOCK:
        npc = DistributedNPCLaffRestockAI.DistributedNPCLaffRestockAI(air, npcId)
    else:
        print 'Invalid NPC type: %s' % type
    npc.setName(name)
    dna = ToonDNA.ToonDNA()
    if dnaType == 'r':
        dnaList = getRandomDNA(npcId, gender)
    else:
        dnaList = dnaType
    dna.newToonFromProperties(*dnaList)
    npc.setDNAString(dna.makeNetString())
    npc.setHp(15)
    npc.setMaxHp(15)
    npc.setPositionIndex(posIndex)
    npc.generateWithRequired(zoneId)
    npc.d_setAnimState(npc.getStartAnimState(), 1.0)
    return npc

def createNpcsInZone(air, zoneId):
    npcs = []
    npcIdList = sorted(zone2NpcDict.get(ZoneUtil.getCanonicalZoneId(zoneId), []))

    for i, npcId in enumerate(npcIdList):
        npcDesc = NPCToonDict.get(npcId)

        if npcDesc[5] == NPC_FISHERMAN and not air.wantFishing:
            continue
        elif npcDesc[5] == NPC_PARTYPERSON and not air.wantParties:
            continue

        npcs.append(createNPC(air, npcId, npcDesc, zoneId, posIndex=i))

    return npcs

def createLocalNPC(npcId):
    if npcId not in NPCToonDict:
        return
    import Toon
    desc = NPCToonDict[npcId]
    canonicalZoneId, name, dnaType, gender, protected, type = desc
    npc = Toon.Toon()
    npc.setName(name)
    npc.setPickable(0)
    npc.setPlayerType(NametagGroup.CCNonPlayer)
    dna = ToonDNA.ToonDNA()
    if dnaType == 'r':
        dnaList = getRandomDNA(npcId, gender)
    else:
        dnaList = dnaType
    dna.newToonFromProperties(*dnaList)
    npc.setDNAString(dna.makeNetString())
    npc.animFSM.request('neutral')
    return npc

# Some buildings don't have NPCs, so we need to store their zone IDs here:
badBlocks = [
    2606, 2602, 2708, 2705, 2704, 2701, 2803, 2804, 2809, 2805, 5607, 1707,
    5609, 3605, 3703
]

def isZoneProtected(zoneId):
    if zoneId in badBlocks:
        return 1

    for npcId in zone2NpcDict.get(zoneId, []):
        if NPCToonDict.get(npcId)[4]:
            return 1

    return 0

lnames = TTLocalizer.NPCToonNames
NPCToonDict = {
 20000: (-1, lnames[20000], ('dss', 'ms', 'm', 'm', 7, 0, 7, 7, 2, 6, 2, 6, 2, 16), 'm', 1, NPC_SPECIALQUESTGIVER),
 999: (-1, lnames[999], 'r', 'm', 1, NPC_TAILOR),
 1000: (-1, lnames[1000], 'r', 'm', 1, NPC_HQ),
 20001: (-1, lnames[20001], ('dss', 'ms', 'm', 'm', 17, 0, 17, 17, 3, 3, 3, 3, 7, 2), 'm', 1, NPC_BLOCKER),
 20002: (-1, TTLocalizer.TutorialHQOfficerName, ('dss', 'ms', 'm', 'm', 6, 0, 6, 6, 0, 10, 0, 10, 2, 9), 'm', 1, NPC_SPECIALQUESTGIVER),
 2002: (2514, lnames[2002], ('hss', 'ls', 'l', 'm', 4, 0, 4, 4, 0, 3, 0, 3, 1, 18), 'm', 1, NPC_REGULAR),
 2003: (2516, lnames[2003], ('cll', 'ms', 'l', 'm', 18, 0, 18, 18, 0, 4, 0, 4, 1, 15), 'm', 1, NPC_REGULAR),
 2004: (2521, lnames[2004], ('rll', 'md', 'm', 'f', 15, 0, 5, 7, 3, 5, 3, 5, 0, 3), 'f', 1, NPC_TAILOR),
 2005: (2518, lnames[2005], ('cls', 'ls', 'l', 'm', 4, 0, 4, 4, 0, 4, 0, 4, 1, 9), 'm', 1, NPC_REGULAR),
 2006: (2519, lnames[2006], ('dsl', 'ls', 'l', 'm', 18, 0, 18, 18, 1, 4, 1, 4, 1, 2), 'm', 1, NPC_CLERK),
 2011: (2519, lnames[2011], ('rll', 'ms', 'l', 'f', 2, 0, 2, 2, 1, 9, 1, 9, 23, 27), 'f', 1, NPC_CLERK),
 2007: (2520, lnames[2007], ('dss', 'ms', 'l', 'm', 10, 0, 10, 10, 1, 5, 1, 5, 1, 20), 'm', 1, NPC_HQ),
 2008: (2520, lnames[2008], ('fll', 'ss', 'l', 'm', 3, 0, 3, 3, 1, 5, 1, 5, 1, 17), 'm', 1, NPC_HQ),
 2009: (2520, lnames[2009], ('fsl', 'md', 'l', 'f', 18, 0, 18, 18, 1, 8, 1, 8, 11, 27), 'f', 1, NPC_HQ),
 2010: (2520, lnames[2010], ('fls', 'ls', 'l', 'f', 11, 0, 11, 11, 1, 8, 1, 8, 8, 4), 'f', 1, NPC_HQ),
 2012: (2000, lnames[2012], ('rss', 'ls', 'l', 'm', 17, 0, 17, 17, 1, 6, 1, 6, 1, 1), 'm', 1, NPC_FISHERMAN),
 2013: (2522, lnames[2013], ('rls', 'ms', 'l', 'm', 9, 0, 9, 9, 0, 7, 0, 7, 1, 19), 'm', 1, NPC_PETCLERK),
 2014: (2522, lnames[2014], ('mls', 'ms', 'm', 'f', 2, 0, 2, 2, 0, 12, 0, 12, 1, 0), 'f', 1, NPC_PETCLERK),
 2015: (2522, lnames[2015], ('hsl', 'ls', 'm', 'm', 17, 0, 17, 17, 0, 8, 0, 8, 1, 13), 'm', 1, NPC_PETCLERK),
 2016: (2000, lnames[2016], ('sls', 'ls', 'm', 'm', 10, 0, 9, 9, 0, 3, 0, 3, 0, 18), 'm', 1, NPC_PARTYPERSON),
 2017: (2000, lnames[2017], ('sss', 'ld', 'm', 'f', 10, 0, 9, 9, 0, 23, 0, 23, 0, 5), 'f', 1, NPC_PARTYPERSON),
 2018: (2513, lnames[2019], ('fll', 'ss', 's', 'm', 15, 0, 15, 15, 99, 27, 86, 27, 39, 27), 'm', 1, NPC_SCIENTIST),
 2019: (2513, lnames[2018], ('pls', 'ls', 'l', 'm', 9, 0, 9, 9, 98, 27, 86, 27, 38, 27), 'm', 1, NPC_SCIENTIST),
 2020: (2513, lnames[2020], ('hss', 'ms', 'm', 'm', 20, 0, 20, 20, 97, 27, 86, 27, 37, 27), 'm', 1, NPC_SCIENTIST),
 2021: (2000, lnames[2021], ('dss', 'ls', 's', 'm', 13, 0, 13, 13, 1, 6, 1, 6, 0, 18), 'm', 1, NPC_GLOVE),
 2101: (2601, lnames[2101], ('rll', 'ms', 'l', 'm', 15, 0, 15, 15, 0, 9, 0, 9, 0, 6), 'm', 1, NPC_REGULAR),
 2102: (2619, lnames[2102], 'r', 'f', 0, NPC_REGULAR),
 2103: (2616, lnames[2103], ('csl', 'ss', 's', 'm', 9, 0, 8, 5, 0, 11, 0, 11, 2, 10), 'm', 0, NPC_REGULAR),
 2104: (2671, lnames[2104], ('mls', 'ms', 'm', 'm', 15, 0, 15, 15, 1, 10, 1, 10, 0, 16), 'm', 1, NPC_HQ),
 2105: (2671, lnames[2105], ('hsl', 'ss', 'm', 'm', 7, 0, 7, 7, 1, 10, 1, 10, 0, 13), 'm', 1, NPC_HQ),
 2106: (2671, lnames[2106], ('hss', 'ld', 'm', 'f', 23, 0, 23, 23, 1, 23, 1, 23, 24, 27), 'f', 1, NPC_HQ),
 2107: (2671, lnames[2107], ('cll', 'sd', 'm', 'f', 14, 0, 14, 14, 1, 24, 1, 24, 7, 4), 'f', 1, NPC_HQ),
 2108: (2603, lnames[2108], ('csl', 'ms', 'm', 'f', 7, 0, 7, 7, 1, 24, 1, 24, 3, 2), 'f', 1, NPC_REGULAR),
 2109: (2604, lnames[2109], 'r', 'm', 1, NPC_REGULAR),
 2110: (2605, lnames[2110], ('dll', 'ls', 'm', 'm', 14, 0, 14, 14, 0, 27, 0, 27, 0, 15), 'm', 0, NPC_REGULAR),
 2111: (2607, lnames[2111], 'r', 'm', 1, NPC_REGULAR),
 2112: (2610, lnames[2112], ('fll', 'ss', 'm', 'm', 20, 0, 20, 20, 0, 27, 0, 27, 0, 9), 'm', 1, NPC_REGULAR),
 2113: (2617, lnames[2113], ('fsl', 'ls', 'm', 'm', 14, 0, 14, 14, 0, 0, 0, 0, 0, 2), 'm', 0, NPC_REGULAR),
 2114: (2618, lnames[2114], ('fls', 'sd', 'm', 'f', 6, 0, 6, 6, 0, 0, 0, 0, 23, 27), 'f', 0, NPC_REGULAR),
 2115: (2621, lnames[2115], ('rll', 'ms', 'l', 'f', 22, 0, 22, 22, 1, 1, 1, 1, 26, 27), 'f', 0, NPC_REGULAR),
 2116: (2624, lnames[2116], ('rss', 'ls', 'l', 'm', 13, 0, 13, 13, 1, 1, 1, 1, 1, 14), 'm', 0, NPC_REGULAR),
 2117: (2625, lnames[2117], ('rls', 'sd', 'l', 'f', 6, 0, 6, 6, 1, 2, 1, 2, 25, 27), 'f', 0, NPC_REGULAR),
 2118: (2626, lnames[2118], ('mls', 'ss', 'l', 'm', 20, 0, 20, 20, 1, 1, 1, 1, 1, 6), 'm', 0, NPC_REGULAR),
 2119: (2629, lnames[2119], ('hll', 'ss', 'l', 'f', 13, 0, 13, 13, 1, 3, 1, 3, 19, 27), 'f', 1, NPC_REGULAR),
 2120: (2632, lnames[2120], ('hss', 'ls', 'l', 'm', 5, 0, 5, 5, 1, 2, 1, 2, 1, 19), 'm', 0, NPC_REGULAR),
 2121: (2633, lnames[2121], ('cll', 'ls', 'l', 'f', 21, 0, 21, 21, 0, 4, 0, 4, 4, 4), 'f', 0, NPC_REGULAR),
 2122: (2639, lnames[2122], ('csl', 'ss', 'l', 'm', 13, 0, 13, 13, 0, 3, 0, 3, 1, 13), 'm', 0, NPC_REGULAR),
 2123: (2643, lnames[2123], ('cls', 'md', 'l', 'f', 4, 0, 4, 4, 0, 5, 0, 5, 14, 27), 'f', 0, NPC_REGULAR),
 2124: (2644, lnames[2124], ('dll', 'sd', 'l', 'f', 21, 0, 21, 21, 0, 5, 0, 5, 8, 21), 'f', 0, NPC_REGULAR),
 2125: (2649, lnames[2125], ('dss', 'ss', 'l', 'm', 12, 0, 12, 12, 0, 4, 0, 4, 1, 0), 'm', 0, NPC_REGULAR),
 2126: (2654, lnames[2126], ('dls', 'ld', 'l', 'f', 4, 0, 4, 4, 0, 6, 0, 6, 3, 7), 'f', 1, NPC_REGULAR),
 2127: (2655, lnames[2127], ('fsl', 'ms', 'l', 'm', 19, 0, 19, 19, 0, 5, 0, 5, 1, 15), 'm', 1, NPC_REGULAR),
 2128: (2656, lnames[2128], ('fss', 'ss', 'l', 'm', 12, 0, 12, 12, 1, 5, 1, 5, 1, 12), 'm', 1, NPC_REGULAR),
 2129: (2657, lnames[2129], ('rll', 'ss', 'l', 'm', 4, 0, 4, 4, 1, 5, 1, 5, 1, 9), 'm', 0, NPC_REGULAR),
 2130: (2659, lnames[2130], ('rss', 'md', 'l', 'f', 19, 0, 19, 19, 1, 8, 1, 8, 7, 7), 'f', 0, NPC_REGULAR),
 2131: (2660, lnames[2131], ('rls', 'ls', 'l', 'f', 12, 0, 12, 12, 1, 8, 1, 8, 1, 26), 'f', 1, NPC_REGULAR),
 2132: (2661, lnames[2132], ('mls', 'ss', 'l', 'm', 4, 0, 4, 4, 1, 6, 1, 6, 1, 17), 'm', 0, NPC_REGULAR),
 2133: (2662, lnames[2133], ('hll', 'ls', 'l', 'm', 18, 0, 18, 18, 1, 6, 1, 6, 1, 14), 'm', 0, NPC_REGULAR),
 2134: (2664, lnames[2134], 'r', 'f', 0, NPC_REGULAR),
 2135: (2665, lnames[2135], ('hls', 'ms', 'l', 'f', 3, 0, 3, 3, 0, 12, 0, 12, 2, 26), 'f', 1, NPC_REGULAR),
 2136: (2666, lnames[2136], ('csl', 'ls', 'l', 'm', 18, 0, 18, 18, 0, 8, 0, 8, 1, 1), 'm', 0, NPC_REGULAR),
 2137: (2667, lnames[2137], ('css', 'sd', 'l', 'f', 11, 0, 11, 11, 0, 21, 0, 21, 24, 27), 'f', 0, NPC_REGULAR),
 2138: (2669, lnames[2138], ('dll', 'ss', 'l', 'm', 3, 0, 3, 3, 0, 9, 0, 9, 1, 16), 'm', 0, NPC_REGULAR),
 2139: (2670, lnames[2139], 'r', 'm', 0, NPC_REGULAR),
 2140: (2156, lnames[2140], ('dls', 'ls', 'l', 'm', 10, 0, 10, 10, 1, 9, 1, 9, 1, 10), 'm', 0, NPC_FISHERMAN),
 2201: (2711, lnames[2201], ('dss', 'ss', 'l', 'm', 13, 0, 13, 13, 1, 6, 1, 6, 0, 17), 'm', 1, NPC_REGULAR),
 2202: (2718, lnames[2202], 'r', 'f', 1, NPC_REGULAR),
 2203: (2742, lnames[2203], ('fss', 'ms', 's', 'm', 19, 0, 19, 19, 0, 7, 0, 7, 0, 11), 'm', 1, NPC_HQ),
 2204: (2742, lnames[2204], ('fls', 'ss', 's', 'm', 13, 0, 13, 13, 0, 7, 0, 7, 0, 6), 'm', 1, NPC_HQ),
 2205: (2742, lnames[2205], ('rsl', 'md', 's', 'f', 4, 0, 4, 4, 0, 11, 0, 11, 16, 27), 'f', 1, NPC_HQ),
 2206: (2742, lnames[2206], ('rss', 'sd', 's', 'f', 21, 0, 21, 21, 0, 12, 0, 12, 0, 8), 'f', 1, NPC_HQ),
 2207: (2705, lnames[2207], ('mss', 'ss', 's', 'm', 12, 0, 12, 12, 0, 8, 0, 8, 0, 16), 'm', 1, NPC_REGULAR),
 2208: (2708, lnames[2208], ('mls', 'ls', 's', 'm', 4, 0, 4, 4, 1, 8, 1, 8, 0, 13), 'm', 1, NPC_REGULAR),
 2209: (2712, lnames[2209], ('hsl', 'ms', 's', 'm', 19, 0, 19, 19, 1, 8, 1, 8, 0, 10), 'm', 1, NPC_REGULAR),
 2210: (2713, lnames[2210], ('hss', 'ms', 's', 'f', 12, 0, 12, 12, 1, 21, 1, 21, 1, 24), 'f', 1, NPC_REGULAR),
 2211: (2716, lnames[2211], ('cll', 'ss', 's', 'f', 3, 0, 3, 3, 1, 22, 1, 22, 25, 27), 'f', 1, NPC_REGULAR),
 2212: (2717, lnames[2212], ('css', 'ls', 's', 'm', 18, 0, 18, 18, 1, 9, 1, 9, 0, 18), 'm', 0, NPC_REGULAR),
 2213: (2720, lnames[2213], ('cls', 'ls', 's', 'f', 12, 0, 12, 12, 1, 23, 1, 23, 11, 27), 'f', 1, NPC_REGULAR),
 2214: (2723, lnames[2214], 'r', 'm', 0, NPC_REGULAR),
 2215: (2727, lnames[2215], ('dss', 'ls', 'm', 'm', 18, 0, 18, 18, 0, 11, 0, 11, 0, 9), 'm', 0, NPC_REGULAR),
 2216: (2728, lnames[2216], ('fll', 'sd', 'm', 'f', 11, 0, 11, 11, 0, 25, 0, 25, 12, 27), 'f', 0, NPC_REGULAR),
 2217: (2729, lnames[2217], ('fsl', 'ss', 'm', 'm', 4, 0, 4, 4, 0, 12, 0, 12, 0, 20), 'm', 1, NPC_REGULAR),
 2218: (2730, lnames[2218], 'r', 'f', 0, NPC_REGULAR),
 2219: (2732, lnames[2219], ('rll', 'ms', 'm', 'm', 10, 0, 10, 10, 0, 27, 0, 27, 0, 14), 'm', 0, NPC_REGULAR),
 2220: (2733, lnames[2220], ('rss', 'ss', 'm', 'm', 3, 0, 3, 3, 1, 12, 1, 12, 0, 11), 'm', 0, NPC_REGULAR),
 2221: (2734, lnames[2221], 'r', 'f', 0, NPC_REGULAR),
 2222: (2735, lnames[2222], ('mls', 'ls', 'm', 'm', 10, 0, 10, 10, 1, 0, 1, 0, 0, 1), 'm', 0, NPC_REGULAR),
 2223: (2739, lnames[2223], 'r', 'f', 0, NPC_REGULAR),
 2224: (2740, lnames[2224], ('hss', 'ss', 'm', 'm', 17, 0, 17, 17, 1, 1, 1, 1, 0, 16), 'm', 0, NPC_REGULAR),
 2225: (2236, lnames[2225], ('cll', 'ls', 'm', 'm', 9, 0, 9, 9, 1, 1, 1, 1, 0, 13), 'm', 0, NPC_FISHERMAN),
 2301: (2804, lnames[2301], ('cll', 'ms', 'm', 'm', 10, 0, 10, 10, 1, 3, 1, 3, 0, 6), 'm', 1, NPC_REGULAR),
 2302: (2831, lnames[2302], ('css', 'ms', 'm', 'm', 3, 0, 3, 3, 1, 3, 1, 3, 0, 1), 'm', 1, NPC_REGULAR),
 2303: (2834, lnames[2303], 'r', 'f', 0, NPC_REGULAR),
 2304: (2832, lnames[2304], ('dss', 'ss', 'm', 'm', 9, 0, 9, 9, 0, 10, 0, 10, 1, 12), 'm', 1, NPC_HQ),
 2305: (2832, lnames[2305], ('dss', 'ss', 'm', 'm', 8, 0, 8, 8, 1, 0, 1, 0, 1, 9), 'm', 1, NPC_HQ),
 2306: (2832, lnames[2306], ('fll', 'md', 'm', 'f', 24, 0, 24, 24, 1, 0, 1, 0, 16, 27), 'f', 1, NPC_HQ),
 2307: (2832, lnames[2307], ('fsl', 'ls', 'm', 'f', 16, 0, 16, 16, 1, 1, 1, 1, 3, 1), 'f', 1, NPC_HQ),
 2308: (2801, lnames[2308], ('fls', 'ss', 'm', 'f', 8, 0, 8, 8, 1, 1, 1, 1, 14, 27), 'f', 1, NPC_REGULAR),
 2309: (2802, lnames[2309], ('rsl', 'ls', 'm', 'm', 22, 0, 22, 22, 1, 1, 1, 1, 1, 14), 'm', 1, NPC_REGULAR),
 2311: (2809, lnames[2311], ('mss', 'ss', 'm', 'm', 7, 0, 7, 7, 0, 2, 0, 2, 1, 6), 'm', 1, NPC_REGULAR),
 2312: (2837, lnames[2312], ('mls', 'ld', 'm', 'f', 24, 0, 24, 24, 0, 3, 0, 3, 4, 6), 'f', 0, NPC_REGULAR),
 2313: (2817, lnames[2313], 'r', 'f', 0, NPC_REGULAR),
 2314: (2818, lnames[2314], ('hss', 'ms', 'm', 'm', 7, 0, 7, 7, 0, 3, 0, 3, 1, 16), 'm', 0, NPC_REGULAR),
 2315: (2822, lnames[2315], ('cll', 'ss', 'm', 'm', 21, 0, 21, 21, 0, 3, 0, 3, 1, 13), 'm', 0, NPC_REGULAR),
 2316: (2823, lnames[2316], ('csl', 'md', 'l', 'f', 15, 0, 15, 15, 0, 5, 0, 5, 0, 23), 'f', 0, NPC_REGULAR),
 2318: (2829, lnames[2318], ('dsl', 'ss', 'l', 'm', 21, 0, 21, 21, 1, 4, 1, 4, 1, 0), 'm', 0, NPC_REGULAR),
 2319: (2830, lnames[2319], ('dss', 'ls', 'l', 'm', 14, 0, 14, 14, 1, 5, 1, 5, 1, 18), 'm', 0, NPC_REGULAR),
 2320: (2839, lnames[2320], 'r', 'm', 0, NPC_REGULAR),
 2321: (2341, lnames[2321], ('fsl', 'ss', 'l', 'm', 21, 0, 21, 21, 1, 5, 1, 5, 0, 12), 'm', 0, NPC_FISHERMAN),
 1001: (1506, lnames[1001], ('rss', 'ms', 'l', 'm', 10, 0, 10, 10, 0, 11, 0, 11, 0, 0), 'm', 0, NPC_CLERK),
 1002: (1506, lnames[1002], ('mss', 'ss', 'l', 'm', 3, 0, 3, 3, 1, 10, 1, 10, 0, 18), 'm', 0, NPC_CLERK),
 1003: (1507, lnames[1003], ('mls', 'ss', 'l', 'm', 17, 0, 17, 17, 1, 11, 1, 11, 0, 15), 'm', 0, NPC_HQ),
 1004: (1507, lnames[1004], ('hsl', 'md', 'l', 'f', 10, 0, 10, 10, 1, 24, 1, 24, 24, 27), 'f', 0, NPC_HQ),
 1005: (1507, lnames[1005], ('hss', 'ms', 'l', 'm', 3, 0, 3, 3, 1, 11, 1, 11, 0, 9), 'm', 0, NPC_HQ),
 1006: (1507, lnames[1006], ('cll', 'ss', 'l', 'f', 18, 0, 18, 18, 1, 25, 1, 25, 19, 27), 'f', 0, NPC_HQ),
 1007: (1508, lnames[1007], ('csl', 'ls', 'm', 'm', 9, 0, 9, 9, 1, 12, 1, 12, 0, 20), 'm', 0, NPC_TAILOR),
 1008: (1000, lnames[1008], ('cls', 'ms', 'm', 'm', 3, 0, 3, 3, 0, 27, 0, 27, 0, 17), 'm', 0, NPC_FISHERMAN),
 1009: (1510, lnames[1009], ('dsl', 'ss', 'm', 'm', 17, 0, 17, 17, 0, 0, 0, 0, 0, 14), 'm', 0, NPC_PETCLERK),
 1010: (1510, lnames[1010], ('dss', 'ld', 'm', 'f', 10, 0, 10, 10, 0, 0, 0, 0, 26, 27), 'f', 0, NPC_PETCLERK),
 1011: (1510, lnames[1011], ('fll', 'sd', 'm', 'f', 1, 0, 1, 1, 0, 1, 0, 1, 4, 25), 'f', 0, NPC_PETCLERK),
 1012: (1000, lnames[1012], ('fls', 'ms', 'l', 'm', 14, 0, 3, 3, 0, 1, 0, 1, 0, 13), 'm', 1, NPC_PARTYPERSON),
 1013: (1000, lnames[1013], ('fss', 'ms', 'm', 'f', 2, 0, 3, 3, 1, 6, 1, 6, 5, 6), 'f', 1, NPC_PARTYPERSON),
 1101: (1627, lnames[1101], ('fll', 'ls', 'm', 'm', 14, 0, 14, 14, 1, 3, 1, 3, 1, 9), 'm', 0, NPC_REGULAR),
 1102: (1612, lnames[1102], ('fsl', 'ms', 'm', 'm', 7, 0, 7, 7, 1, 3, 1, 3, 1, 2), 'm', 0, NPC_REGULAR),
 1103: (1626, lnames[1103], 'r', 'm', 0, NPC_REGULAR),
 1104: (1617, lnames[1104], 'r', 'm', 0, NPC_REGULAR),
 1105: (1606, lnames[1105], ('rss', 'ms', 'm', 'm', 6, 0, 6, 6, 0, 4, 0, 4, 1, 14), 'm', 1, NPC_REGULAR),
 1106: (1604, lnames[1106], 'r', 'f', 1, NPC_REGULAR),
 1107: (1621, lnames[1107], 'r', 'm', 0, NPC_REGULAR),
 1108: (1629, lnames[1108], ('hsl', 'ls', 'l', 'm', 6, 0, 6, 6, 0, 6, 0, 6, 1, 1), 'm', 0, NPC_HQ),
 1109: (1629, lnames[1109], ('hss', 'ls', 'l', 'f', 22, 0, 22, 22, 0, 8, 0, 8, 14, 27), 'f', 0, NPC_HQ),
 1110: (1629, lnames[1110], ('cll', 'ss', 'l', 'm', 13, 0, 13, 13, 1, 6, 1, 6, 1, 16), 'm', 0, NPC_HQ),
 1111: (1629, lnames[1111], ('csl', 'ld', 'l', 'f', 6, 0, 6, 6, 1, 9, 1, 9, 2, 2), 'f', 0, NPC_HQ),
 1112: (1602, lnames[1112], ('cls', 'ms', 'l', 'm', 20, 0, 20, 20, 1, 7, 1, 7, 1, 10), 'm', 1, NPC_REGULAR),
 1113: (1608, lnames[1113], ('dll', 'ms', 'l', 'f', 13, 0, 13, 13, 1, 11, 1, 11, 0, 27), 'f', 1, NPC_REGULAR),
 1114: (1609, lnames[1114], ('dss', 'ls', 'l', 'm', 5, 0, 5, 5, 1, 7, 1, 7, 1, 0), 'm', 1, NPC_REGULAR),
 1115: (1613, lnames[1115], ('fll', 'sd', 'l', 'f', 21, 0, 21, 21, 1, 12, 1, 12, 25, 27), 'f', 0, NPC_REGULAR),
 1116: (1614, lnames[1116], ('fsl', 'ls', 'l', 'f', 13, 0, 13, 13, 1, 12, 1, 12, 1, 25), 'f', 0, NPC_REGULAR),
 1117: (1615, lnames[1117], ('fls', 'ss', 'l', 'm', 5, 0, 5, 5, 0, 9, 0, 9, 1, 12), 'm', 0, NPC_REGULAR),
 1118: (1616, lnames[1118], ('rll', 'ls', 'l', 'm', 19, 0, 19, 19, 0, 9, 0, 9, 1, 9), 'm', 0, NPC_REGULAR),
 1121: (1619, lnames[1121], 'r', 'f', 0, NPC_REGULAR),
 1122: (1620, lnames[1122], ('hll', 'ms', 'l', 'm', 12, 0, 12, 12, 0, 11, 0, 11, 0, 14), 'm', 0, NPC_REGULAR),
 1123: (1622, lnames[1123], ('hss', 'ms', 'l', 'f', 4, 0, 4, 4, 1, 23, 1, 23, 23, 27), 'f', 0, NPC_REGULAR),
 1124: (1624, lnames[1124], ('cll', 'ls', 'l', 'm', 19, 0, 19, 19, 1, 11, 1, 11, 0, 6), 'm', 0, NPC_REGULAR),
 1125: (1628, lnames[1125], ('csl', 'sd', 'l', 'f', 12, 0, 12, 12, 1, 24, 1, 24, 25, 27), 'f', 0, NPC_REGULAR),
 1126: (1129, lnames[1126], ('cls', 'ms', 'l', 'm', 4, 0, 4, 4, 1, 11, 1, 11, 0, 19), 'm', 0, NPC_FISHERMAN),
 1201: (1710, lnames[1201], ('css', 'ls', 's', 'f', 12, 0, 12, 12, 0, 0, 0, 0, 1, 24), 'f', 0, NPC_REGULAR),
 1202: (1713, lnames[1202], ('cls', 'ss', 's', 'm', 4, 0, 4, 4, 0, 0, 0, 0, 1, 14), 'm', 0, NPC_REGULAR),
 1203: (1725, lnames[1203], 'r', 'm', 0, NPC_REGULAR),
 1204: (1712, lnames[1204], ('dss', 'ms', 's', 'm', 12, 0, 12, 12, 1, 1, 1, 1, 1, 6), 'm', 0, NPC_REGULAR),
 1205: (1729, lnames[1205], ('fll', 'ss', 's', 'm', 4, 0, 4, 4, 1, 1, 1, 1, 1, 1), 'm', 0, NPC_HQ),
 1206: (1729, lnames[1206], ('fss', 'ld', 's', 'f', 19, 0, 19, 19, 1, 2, 1, 2, 7, 11), 'f', 0, NPC_HQ),
 1207: (1729, lnames[1207], ('fls', 'ms', 's', 'm', 12, 0, 12, 12, 1, 2, 1, 2, 1, 16), 'm', 0, NPC_HQ),
 1208: (1729, lnames[1208], ('rsl', 'ls', 'm', 'f', 3, 0, 3, 3, 1, 3, 1, 3, 23, 27), 'f', 0, NPC_HQ),
 1209: (1701, lnames[1209], ('rss', 'ss', 'm', 'f', 19, 0, 19, 19, 0, 4, 0, 4, 17, 27), 'f', 1, NPC_REGULAR),
 1210: (1703, lnames[1210], 'r', 'm', 1, NPC_REGULAR),
 1211: (1705, lnames[1211], ('mls', 'ms', 'm', 'm', 4, 0, 4, 4, 0, 4, 0, 4, 1, 0), 'm', 1, NPC_REGULAR),
 1212: (1706, lnames[1212], ('hsl', 'ss', 'm', 'm', 18, 0, 18, 18, 0, 4, 0, 4, 1, 18), 'm', 1, NPC_REGULAR),
 1213: (1707, lnames[1213], ('hss', 'ls', 'm', 'm', 10, 0, 10, 10, 0, 4, 0, 4, 1, 15), 'm', 1, NPC_REGULAR),
 1214: (1709, lnames[1214], ('cll', 'sd', 'm', 'f', 2, 0, 2, 2, 0, 7, 0, 7, 1, 12), 'f', 1, NPC_REGULAR),
 1215: (1711, lnames[1215], ('css', 'ms', 'm', 'f', 18, 0, 18, 18, 0, 7, 0, 7, 25, 27), 'f', 0, NPC_REGULAR),
 1216: (1714, lnames[1216], ('cls', 'ls', 'm', 'm', 10, 0, 10, 10, 1, 5, 1, 5, 1, 2), 'm', 0, NPC_REGULAR),
 1217: (1716, lnames[1217], 'r', 'f', 0, NPC_REGULAR),
 1218: (1717, lnames[1218], ('dss', 'ms', 'm', 'm', 17, 0, 17, 17, 1, 6, 1, 6, 1, 17), 'm', 0, NPC_REGULAR),
 1219: (1718, lnames[1219], ('fll', 'ss', 'm', 'm', 9, 0, 9, 9, 1, 6, 1, 6, 1, 14), 'm', 0, NPC_REGULAR),
 1220: (1719, lnames[1220], ('fsl', 'md', 'm', 'f', 2, 0, 2, 2, 1, 9, 1, 9, 7, 23), 'f', 0, NPC_REGULAR),
 1221: (1720, lnames[1221], 'r', 'm', 0, NPC_REGULAR),
 1222: (1721, lnames[1222], 'r', 'm', 0, NPC_REGULAR),
 1223: (1723, lnames[1223], ('rss', 'ls', 'l', 'm', 2, 0, 2, 2, 0, 8, 0, 8, 1, 19), 'm', 0, NPC_REGULAR),
 1224: (1724, lnames[1224], ('mss', 'sd', 'l', 'f', 17, 0, 17, 17, 0, 21, 0, 21, 7, 9), 'f', 0, NPC_REGULAR),
 1225: (1726, lnames[1225], ('mls', 'ss', 'l', 'm', 9, 0, 9, 9, 0, 9, 0, 9, 1, 13), 'm', 0, NPC_REGULAR),
 1226: (1727, lnames[1226], ('hsl', 'ls', 'l', 'm', 2, 0, 2, 2, 0, 9, 0, 9, 1, 10), 'm', 0, NPC_REGULAR),
 1227: (1728, lnames[1227], ('hss', 'sd', 'l', 'f', 17, 0, 17, 17, 0, 22, 0, 22, 3, 7), 'f', 0, NPC_REGULAR),
 1228: (1236, lnames[1228], ('cll', 'ms', 'l', 'm', 8, 0, 8, 8, 1, 9, 1, 9, 1, 0), 'm', 0, NPC_FISHERMAN),
 1301: (1828, lnames[1301], ('mls', 'md', 'm', 'f', 16, 0, 16, 16, 1, 8, 1, 8, 14, 27), 'f', 0, NPC_REGULAR),
 1302: (1832, lnames[1302], ('hsl', 'ms', 'm', 'm', 8, 0, 8, 8, 1, 6, 1, 6, 0, 18), 'm', 0, NPC_REGULAR),
 1303: (1826, lnames[1303], ('hls', 'ss', 'm', 'm', 22, 0, 22, 22, 1, 6, 1, 6, 0, 15), 'm', 0, NPC_REGULAR),
 1304: (1804, lnames[1304], ('cll', 'md', 'm', 'f', 15, 0, 15, 15, 1, 9, 1, 9, 23, 27), 'f', 1, NPC_REGULAR),
 1305: (1835, lnames[1305], ('css', 'ms', 'm', 'm', 7, 0, 7, 7, 1, 7, 1, 7, 0, 9), 'm', 0, NPC_HQ),
 1306: (1835, lnames[1306], ('cls', 'ms', 'm', 'f', 24, 0, 24, 24, 0, 12, 0, 12, 0, 7), 'f', 0, NPC_HQ),
 1307: (1835, lnames[1307], ('dsl', 'ls', 'm', 'm', 15, 0, 15, 15, 0, 8, 0, 8, 0, 20), 'm', 0, NPC_HQ),
 1308: (1835, lnames[1308], ('dss', 'sd', 'm', 'f', 8, 0, 8, 8, 0, 21, 0, 21, 4, 5), 'f', 0, NPC_HQ),
 1309: (1802, lnames[1309], ('fll', 'ms', 'l', 'f', 23, 0, 23, 23, 0, 21, 0, 21, 1, 12), 'f', 1, NPC_REGULAR),
 1310: (1805, lnames[1310], ('fsl', 'ss', 'l', 'm', 15, 0, 15, 15, 0, 9, 0, 9, 0, 11), 'm', 1, NPC_REGULAR),
 1311: (1806, lnames[1311], 'r', 'f', 1, NPC_REGULAR),
 1312: (1807, lnames[1312], ('rsl', 'ms', 'l', 'm', 21, 0, 21, 21, 1, 9, 1, 9, 0, 1), 'm', 1, NPC_REGULAR),
 1313: (1808, lnames[1313], ('rss', 'ss', 'l', 'm', 14, 0, 14, 14, 1, 10, 1, 10, 0, 19), 'm', 1, NPC_REGULAR),
 1314: (1809, lnames[1314], ('mss', 'ls', 'l', 'm', 6, 0, 6, 6, 1, 10, 1, 10, 0, 16), 'm', 1, NPC_REGULAR),
 1315: (1810, lnames[1315], 'r', 'f', 0, NPC_REGULAR),
 1316: (1811, lnames[1316], ('hsl', 'ms', 'l', 'f', 14, 0, 14, 14, 1, 24, 1, 24, 7, 7), 'f', 0, NPC_REGULAR),
 1317: (1813, lnames[1317], ('hss', 'ld', 'l', 'f', 7, 0, 7, 7, 1, 25, 1, 25, 26, 27), 'f', 0, NPC_REGULAR),
 1318: (1814, lnames[1318], ('cll', 'ms', 'l', 'm', 20, 0, 20, 20, 0, 12, 0, 12, 0, 0), 'm', 0, NPC_REGULAR),
 1319: (1815, lnames[1319], ('csl', 'ss', 'l', 'm', 14, 0, 14, 14, 0, 27, 0, 27, 0, 18), 'm', 0, NPC_REGULAR),
 1320: (1818, lnames[1320], 'r', 'm', 0, NPC_REGULAR),
 1321: (1819, lnames[1321], ('dsl', 'md', 'l', 'f', 22, 0, 22, 22, 0, 27, 0, 27, 7, 5), 'f', 0, NPC_REGULAR),
 1322: (1820, lnames[1322], ('dss', 'ls', 'm', 'f', 13, 0, 13, 13, 0, 0, 0, 0, 26, 27), 'f', 0, NPC_REGULAR),
 1323: (1821, lnames[1323], ('fll', 'ss', 'm', 'm', 6, 0, 6, 6, 0, 0, 0, 0, 1, 2), 'm', 0, NPC_REGULAR),
 1324: (1823, lnames[1324], ('fsl', 'md', 'm', 'f', 22, 0, 22, 22, 0, 1, 0, 1, 10, 27), 'f', 0, NPC_REGULAR),
 1325: (1824, lnames[1325], 'r', 'm', 0, NPC_REGULAR),
 1326: (1825, lnames[1326], ('rll', 'ms', 'm', 'f', 6, 0, 6, 6, 1, 2, 1, 2, 10, 27), 'f', 0, NPC_REGULAR),
 1327: (1829, lnames[1327], 'r', 'f', 0, NPC_REGULAR),
 1328: (1830, lnames[1328], ('rls', 'ms', 'm', 'm', 13, 0, 13, 13, 1, 2, 1, 2, 1, 6), 'm', 0, NPC_REGULAR),
 1329: (1831, lnames[1329], ('mls', 'ms', 'm', 'f', 4, 0, 4, 4, 1, 3, 1, 3, 25, 27), 'f', 0, NPC_REGULAR),
 1330: (1833, lnames[1330], ('hsl', 'ls', 'm', 'm', 19, 0, 19, 19, 1, 3, 1, 3, 1, 19), 'm', 0, NPC_REGULAR),
 1331: (1834, lnames[1331], ('hss', 'ls', 'm', 'm', 12, 0, 12, 12, 0, 3, 0, 3, 1, 16), 'm', 0, NPC_REGULAR),
 1332: (1330, lnames[1332], ('cll', 'ms', 'm', 'm', 5, 0, 5, 5, 0, 4, 0, 4, 1, 13), 'm', 0, NPC_FISHERMAN),
 3001: (3506, lnames[3001], 'r', 'f', 0, NPC_REGULAR),
 3002: (3508, lnames[3002], ('cls', 'ms', 'm', 'm', 4, 0, 4, 4, 1, 9, 1, 9, 0, 18), 'm', 0, NPC_HQ),
 3003: (3508, lnames[3003], ('dsl', 'ss', 'm', 'f', 19, 0, 19, 19, 1, 22, 1, 22, 25, 27), 'f', 0, NPC_HQ),
 3004: (3508, lnames[3004], ('dss', 'ls', 'm', 'm', 12, 0, 12, 12, 1, 10, 1, 10, 0, 12), 'm', 0, NPC_HQ),
 3005: (3508, lnames[3005], ('fll', 'ms', 'm', 'm', 4, 0, 4, 4, 0, 11, 0, 11, 0, 9), 'm', 0, NPC_HQ),
 3006: (3507, lnames[3006], ('fsl', 'ss', 'm', 'm', 18, 0, 18, 18, 0, 11, 0, 11, 0, 2), 'm', 0, NPC_CLERK),
 3007: (3507, lnames[3007], ('fls', 'ld', 'm', 'f', 12, 0, 12, 12, 0, 25, 0, 25, 8, 5), 'f', 0, NPC_CLERK),
 3008: (3509, lnames[3008], ('rll', 'ms', 'l', 'm', 4, 0, 4, 4, 0, 12, 0, 12, 0, 17), 'm', 0, NPC_TAILOR),
 3009: (3000, lnames[3009], ('rss', 'ls', 'l', 'f', 19, 0, 19, 19, 0, 26, 0, 26, 4, 23), 'f', 0, NPC_FISHERMAN),
 3010: (3511, lnames[3010], ('rls', 'ss', 'l', 'm', 10, 0, 10, 10, 0, 12, 0, 12, 0, 11), 'm', 0, NPC_PETCLERK),
 3011: (3511, lnames[3011], ('mls', 'md', 'l', 'f', 3, 0, 3, 3, 1, 26, 1, 26, 26, 27), 'f', 0, NPC_PETCLERK),
 3012: (3511, lnames[3012], ('hsl', 'ms', 'l', 'm', 18, 0, 18, 18, 1, 12, 1, 12, 0, 1), 'm', 0, NPC_PETCLERK),
 3013: (3000, lnames[3013], ('cls', 'ss', 'm', 'm', 18, 0, 17, 17, 1, 7, 1, 7, 1, 9), 'm', 1, NPC_PARTYPERSON),
 3014: (3000, lnames[3014], ('css', 'sd', 'm', 'f', 17, 0, 16, 16, 0, 24, 0, 24, 0, 9), 'f', 1, NPC_PARTYPERSON),
 3101: (3611, lnames[3101], ('mls', 'ls', 'l', 'm', 16, 0, 16, 16, 1, 1, 1, 1, 1, 6), 'm', 0, NPC_REGULAR),
 3102: (3625, lnames[3102], 'r', 'f', 0, NPC_REGULAR),
 3103: (3641, lnames[3103], 'r', 'm', 0, NPC_REGULAR),
 3104: (3602, lnames[3104], ('cll', 'ss', 'l', 'f', 16, 0, 16, 16, 0, 4, 0, 4, 3, 2), 'f', 1, NPC_REGULAR),
 3105: (3651, lnames[3105], 'r', 'm', 0, NPC_REGULAR),
 3106: (3636, lnames[3106], ('fll', 'ls', 'l', 'm', 8, 2, 8, 8, 10, 27, 0, 27, 7, 11), 'm', 0, NPC_REGULAR),
 3107: (3630, lnames[3107], ('dll', 'ms', 'l', 'f', 15, 0, 15, 15, 0, 5, 0, 5, 4, 4), 'f', 0, NPC_REGULAR),
 3108: (3638, lnames[3108], 'r', 'm', 0, NPC_REGULAR),
 3109: (3637, lnames[3109], ('fll', 'sd', 'm', 'f', 23, 0, 23, 23, 1, 6, 1, 6, 12, 27), 'f', 0, NPC_REGULAR),
 3110: (3629, lnames[3110], ('fss', 'ms', 'l', 'm', 10, 10, 10, 10, 16, 4, 0, 4, 5, 4), 'm', 0, NPC_REGULAR),
 3111: (3627, lnames[3111], ('dsl', 'ls', 's', 'm', 6, 0, 6, 6, 14, 27, 10, 27, 1, 14), 'm', 1, NPC_REGULAR),
 3112: (3607, lnames[3112], ('rll', 'ls', 'm', 'm', 21, 0, 21, 21, 1, 5, 1, 5, 1, 9), 'm', 1, NPC_REGULAR),
 3113: (3618, lnames[3113], ('rss', 'ms', 'm', 'm', 14, 0, 14, 14, 1, 5, 1, 5, 0, 2), 'm', 0, NPC_REGULAR),
 3114: (3620, lnames[3114], ('rls', 'ss', 'm', 'm', 7, 0, 7, 7, 0, 6, 0, 6, 0, 20), 'm', 0, NPC_REGULAR),
 3115: (3654, lnames[3115], ('mls', 'ls', 'm', 'm', 21, 0, 21, 21, 0, 7, 0, 7, 0, 17), 'm', 0, NPC_HQ),
 3116: (3654, lnames[3116], ('hll', 'ls', 'm', 'f', 14, 0, 14, 14, 0, 11, 0, 11, 0, 12), 'f', 0, NPC_HQ),
 3117: (3654, lnames[3117], ('hss', 'ss', 'm', 'm', 6, 0, 6, 6, 0, 7, 0, 7, 0, 11), 'm', 0, NPC_HQ),
 3118: (3654, lnames[3118], ('cll', 'ls', 'm', 'm', 20, 0, 20, 20, 0, 8, 0, 8, 0, 6), 'm', 0, NPC_HQ),
 3119: (3653, lnames[3119], ('csl', 'ms', 'm', 'm', 14, 0, 14, 14, 0, 8, 0, 8, 0, 1), 'm', 0, NPC_REGULAR),
 3120: (3610, lnames[3120], ('cls', 'ss', 'm', 'm', 6, 0, 6, 6, 1, 8, 1, 8, 0, 19), 'm', 0, NPC_REGULAR),
 3121: (3601, lnames[3121], ('dll', 'ls', 'm', 'm', 20, 0, 20, 20, 1, 8, 1, 8, 0, 16), 'm', 1, NPC_REGULAR),
 3122: (3608, lnames[3122], ('dss', 'md', 'l', 'f', 13, 0, 13, 13, 1, 21, 1, 21, 10, 27), 'f', 1, NPC_REGULAR),
 3123: (3612, lnames[3123], ('dls', 'ms', 'l', 'm', 6, 0, 6, 6, 1, 9, 1, 9, 0, 10), 'm', 0, NPC_REGULAR),
 3124: (3613, lnames[3124], ('fsl', 'ss', 'l', 'm', 20, 0, 20, 20, 1, 9, 1, 9, 0, 4), 'm', 0, NPC_REGULAR),
 3125: (3614, lnames[3125], ('fls', 'ls', 'l', 'm', 13, 0, 13, 13, 1, 9, 1, 9, 0, 0), 'm', 0, NPC_REGULAR),
 3126: (3615, lnames[3126], ('rll', 'ls', 'l', 'f', 6, 0, 6, 6, 0, 24, 0, 24, 17, 27), 'f', 0, NPC_REGULAR),
 3127: (3617, lnames[3127], ('rss', 'ms', 'l', 'f', 21, 0, 21, 21, 0, 24, 0, 24, 19, 27), 'f', 0, NPC_REGULAR),
 3128: (3621, lnames[3128], ('rls', 'ls', 'l', 'm', 13, 0, 13, 13, 0, 11, 0, 11, 0, 12), 'm', 0, NPC_REGULAR),
 3129: (3623, lnames[3129], ('mls', 'sd', 'l', 'f', 4, 0, 4, 4, 0, 25, 0, 25, 23, 27), 'f', 0, NPC_REGULAR),
 3130: (3624, lnames[3130], ('hll', 'ms', 'l', 'f', 21, 0, 21, 21, 0, 26, 0, 26, 25, 27), 'f', 0, NPC_REGULAR),
 3131: (3634, lnames[3131], ('hss', 'ls', 'l', 'm', 12, 0, 12, 12, 0, 12, 0, 12, 0, 20), 'm', 0, NPC_REGULAR),
 3132: (3635, lnames[3132], 'r', 'f', 0, NPC_REGULAR),
 3133: (3642, lnames[3133], ('csl', 'ms', 'l', 'm', 19, 0, 19, 19, 1, 12, 1, 12, 0, 14), 'm', 0, NPC_REGULAR),
 3134: (3643, lnames[3134], ('cls', 'ss', 'l', 'm', 12, 0, 12, 12, 1, 0, 1, 0, 0, 11), 'm', 0, NPC_REGULAR),
 3135: (3644, lnames[3135], ('dll', 'md', 'l', 'f', 4, 0, 4, 4, 1, 0, 1, 0, 4, 12), 'f', 0, NPC_REGULAR),
 3136: (3647, lnames[3136], ('dss', 'ls', 'l', 'f', 19, 0, 19, 19, 1, 1, 1, 1, 25, 27), 'f', 0, NPC_REGULAR),
 3137: (3648, lnames[3137], ('dls', 'ss', 'l', 'm', 12, 0, 12, 12, 1, 1, 1, 1, 0, 19), 'm', 0, NPC_REGULAR),
 3138: (3649, lnames[3138], ('fsl', 'ld', 'l', 'f', 3, 0, 3, 3, 1, 2, 1, 2, 26, 27), 'f', 0, NPC_REGULAR),
 3139: (3650, lnames[3139], ('fss', 'sd', 'l', 'f', 19, 0, 19, 19, 0, 2, 0, 2, 16, 27), 'f', 0, NPC_REGULAR),
 3140: (3136, lnames[3140], ('rll', 'ms', 'l', 'f', 11, 0, 11, 11, 0, 3, 0, 3, 12, 27), 'f', 0, NPC_FISHERMAN),
 3201: (3715, lnames[3201], 'r', 'f', 0, NPC_REGULAR),
 3202: (3723, lnames[3202], ('rsl', 'ss', 'l', 'm', 6, 0, 6, 6, 1, 12, 1, 12, 1, 13), 'm', 0, NPC_REGULAR),
 3203: (3712, lnames[3203], ('rss', 'ls', 'l', 'm', 20, 0, 20, 20, 1, 12, 1, 12, 1, 10), 'm', 0, NPC_REGULAR),
 3204: (3734, lnames[3204], ('mss', 'md', 'l', 'f', 13, 0, 13, 13, 1, 26, 1, 26, 4, 5), 'f', 0, NPC_REGULAR),
 3205: (3721, lnames[3205], 'r', 'm', 0, NPC_REGULAR),
 3206: (3722, lnames[3206], ('hsl', 'ss', 'l', 'f', 21, 0, 21, 21, 1, 0, 1, 0, 11, 27), 'f', 0, NPC_REGULAR),
 3207: (3713, lnames[3207], ('hss', 'ls', 'l', 'm', 13, 0, 13, 13, 0, 0, 0, 0, 1, 15), 'm', 0, NPC_REGULAR),
 3208: (3732, lnames[3208], ('cll', 'ms', 'l', 'm', 5, 0, 5, 5, 0, 1, 0, 1, 1, 12), 'm', 0, NPC_REGULAR),
 3209: (3737, lnames[3209], ('css', 'ss', 'l', 'm', 19, 0, 19, 19, 0, 1, 0, 1, 1, 9), 'm', 0, NPC_REGULAR),
 3210: (3728, lnames[3210], ('pls', 'ls', 's', 'm', 13, 0, 13, 13, 2, 1, 2, 1, 5, 2), 'm', 0, NPC_REGULAR),
 3211: (3710, lnames[3211], 'r', 'f', 0, NPC_REGULAR),
 3212: (3707, lnames[3212], ('dss', 'ss', 's', 'm', 19, 0, 19, 19, 0, 2, 0, 2, 1, 17), 'm', 1, NPC_REGULAR),
 3213: (3739, lnames[3213], ('fll', 'ls', 's', 'm', 12, 0, 12, 12, 1, 2, 1, 2, 1, 14), 'm', 0, NPC_HQ),
 3214: (3739, lnames[3214], ('fsl', 'md', 's', 'f', 4, 0, 4, 4, 1, 4, 1, 4, 3, 1), 'f', 0, NPC_HQ),
 3215: (3739, lnames[3215], ('fls', 'ms', 's', 'm', 19, 0, 19, 19, 1, 3, 1, 3, 1, 6), 'm', 0, NPC_HQ),
 3216: (3739, lnames[3216], ('rll', 'ss', 's', 'm', 12, 0, 12, 12, 1, 4, 1, 4, 1, 1), 'm', 0, NPC_HQ),
 3217: (3738, lnames[3217], ('rss', 'ls', 's', 'm', 4, 0, 4, 4, 1, 4, 1, 4, 1, 19), 'm', 0, NPC_REGULAR),
 3218: (3702, lnames[3218], ('mss', 'ms', 's', 'm', 18, 0, 18, 18, 1, 4, 1, 4, 1, 16), 'm', 1, NPC_REGULAR),
 3219: (3705, lnames[3219], ('mls', 'ss', 's', 'm', 12, 0, 12, 12, 0, 5, 0, 5, 1, 13), 'm', 1, NPC_REGULAR),
 3220: (3706, lnames[3220], ('hsl', 'ls', 's', 'm', 4, 0, 4, 4, 0, 5, 0, 5, 1, 10), 'm', 1, NPC_REGULAR),
 3221: (3708, lnames[3221], ('hss', 'sd', 's', 'f', 19, 0, 19, 19, 0, 8, 0, 8, 7, 12), 'f', 1, NPC_REGULAR),
 3222: (3716, lnames[3222], 'r', 'f', 0, NPC_REGULAR),
 3223: (3718, lnames[3223], ('csl', 'ls', 'm', 'm', 4, 0, 4, 4, 0, 6, 0, 6, 1, 18), 'm', 0, NPC_REGULAR),
 3224: (3719, lnames[3224], ('cls', 'md', 'm', 'f', 18, 0, 18, 18, 0, 9, 0, 9, 17, 27), 'f', 0, NPC_REGULAR),
 3225: (3724, lnames[3225], 'r', 'm', 0, NPC_REGULAR),
 3226: (3725, lnames[3226], ('dss', 'ss', 'm', 'm', 3, 0, 3, 3, 1, 7, 1, 7, 1, 9), 'm', 0, NPC_REGULAR),
 3227: (3726, lnames[3227], ('fll', 'ls', 'm', 'm', 17, 0, 17, 17, 1, 7, 1, 7, 1, 2), 'm', 0, NPC_REGULAR),
 3228: (3730, lnames[3228], ('fsl', 'ls', 'm', 'f', 11, 0, 11, 11, 1, 12, 1, 12, 25, 27), 'f', 0, NPC_REGULAR),
 3229: (3731, lnames[3229], ('fls', 'ms', 'm', 'f', 2, 0, 2, 2, 1, 12, 1, 12, 0, 7), 'f', 0, NPC_REGULAR),
 3230: (3735, lnames[3230], ('rll', 'ls', 'm', 'm', 17, 0, 17, 17, 1, 8, 1, 8, 1, 14), 'm', 0, NPC_REGULAR),
 3231: (3736, lnames[3231], ('rss', 'ms', 'm', 'm', 9, 0, 9, 9, 0, 9, 0, 9, 1, 12), 'm', 0, NPC_REGULAR),
 3232: (3236, lnames[3232], ('rls', 'ss', 'm', 'm', 3, 0, 3, 3, 0, 10, 0, 10, 1, 9), 'm', 0, NPC_FISHERMAN),
 3301: (3810, lnames[3301], ('dsl', 'ms', 'm', 'f', 11, 0, 11, 11, 0, 22, 0, 22, 2, 11), 'f', 0, NPC_REGULAR),
 3302: (3806, lnames[3302], ('dls', 'ls', 'm', 'm', 4, 0, 4, 4, 0, 10, 0, 10, 1, 1), 'm', 1, NPC_REGULAR),
 3303: (3830, lnames[3303], ('fll', 'ms', 'm', 'm', 18, 0, 18, 18, 0, 10, 0, 10, 1, 19), 'm', 0, NPC_REGULAR),
 3304: (3828, lnames[3304], ('pll', 'ls', 'l', 'm', 0, 0, 0, 0, 1, 5, 1, 5, 1, 6), 'f', 0, NPC_REGULAR),
 3305: (3812, lnames[3305], ('fls', 'ls', 'm', 'm', 3, 0, 3, 3, 0, 11, 0, 11, 1, 13), 'm', 0, NPC_REGULAR),
 3306: (3821, lnames[3306], ('bss', 'sd', 'm', 'f', 0, 0, 0, 0, 31, 27, 22, 27, 8, 11), 'f', 0, NPC_REGULAR),
 3307: (3329, lnames[3307], ('rss', 'ls', 'm', 'f', 11, 0, 11, 11, 1, 24, 1, 24, 1, 9), 'f', 0, NPC_FISHERMAN),
 3308: (3815, lnames[3308], ('mss', 'ss', 'm', 'm', 3, 0, 3, 3, 1, 11, 1, 11, 1, 0), 'm', 0, NPC_REGULAR),
 3309: (3826, lnames[3309], ('hll', 'ls', 'm', 'm', 17, 0, 17, 17, 1, 11, 1, 11, 1, 18), 'm', 0, NPC_REGULAR),
 3310: (3823, lnames[3310], ('pll', 'ms', 'm', 'm', 10, 0, 10, 10, 60, 27, 49, 27, 0, 13), 'm', 0, NPC_REGULAR),
 3311: (3829, lnames[3311], 'r', 'f', 0, NPC_REGULAR),
 3312: (3813, lnames[3312], ('rss', 'ms', 'l', 'm', 4, 0, 4, 4, 5, 2, 5, 2, 1, 10), 'm', 0, NPC_REGULAR),
 3313: (3801, lnames[3313], ('css', 'ms', 'l', 'm', 9, 0, 9, 9, 0, 0, 0, 0, 1, 2), 'm', 0, NPC_HQ),
 3314: (3801, lnames[3314], ('cls', 'ms', 'l', 'f', 1, 0, 1, 1, 0, 0, 0, 0, 3, 25), 'f', 0, NPC_HQ),
 3315: (3801, lnames[3315], ('dsl', 'ls', 'l', 'm', 17, 0, 17, 17, 0, 0, 0, 0, 1, 17), 'm', 0, NPC_HQ),
 3316: (3801, lnames[3316], ('dss', 'md', 'l', 'f', 10, 0, 10, 10, 0, 1, 0, 1, 10, 27), 'f', 0, NPC_HQ),
 3317: (3816, lnames[3317], ('fll', 'ls', 'l', 'f', 1, 0, 1, 1, 0, 2, 0, 2, 3, 24), 'f', 0, NPC_REGULAR),
 3318: (3808, lnames[3318], ('dss', 'ms', 'm', 'm', 18, 0, 18, 18, 57, 1, 46, 1, 12, 1), 'm', 1, NPC_REGULAR),
 3319: (3825, lnames[3319], ('fls', 'ls', 'l', 'm', 9, 0, 9, 9, 1, 2, 1, 2, 1, 1), 'm', 0, NPC_REGULAR),
 3320: (3814, lnames[3320], ('rsl', 'ls', 'l', 'f', 1, 0, 1, 1, 1, 3, 1, 3, 12, 27), 'f', 0, NPC_REGULAR),
 3321: (3818, lnames[3321], ('rss', 'ss', 'l', 'm', 16, 0, 16, 16, 1, 2, 1, 2, 1, 16), 'm', 0, NPC_REGULAR),
 3322: (3819, lnames[3322], 'r', 'm', 0, NPC_REGULAR),
 3323: (3811, lnames[3323], ('mls', 'ms', 'l', 'm', 22, 0, 22, 22, 1, 3, 1, 3, 1, 10), 'm', 0, NPC_REGULAR),
 3324: (3809, lnames[3324], 'r', 'm', 1, NPC_REGULAR),
 3325: (3827, lnames[3325], ('hss', 'ls', 'l', 'm', 8, 0, 8, 8, 0, 4, 0, 4, 1, 0), 'm', 0, NPC_REGULAR),
 3326: (3820, lnames[3326], ('cll', 'md', 'l', 'f', 24, 0, 24, 24, 0, 6, 0, 6, 12, 27), 'f', 0, NPC_REGULAR),
 3327: (3824, lnames[3327], ('css', 'ms', 'l', 'm', 15, 0, 15, 15, 0, 5, 0, 5, 1, 15), 'm', 0, NPC_REGULAR),
 3328: (3807, lnames[3328], ('dll', 'sd', 'l', 'f', 8, 0, 8, 8, 0, 25, 0, 25, 14, 27), 'f', 1, NPC_REGULAR),
 3329: (3817, lnames[3329], ('dll', 'ms', 'l', 'm', 6, 0, 6, 6, 0, 1, 0, 1, 1, 1), 'm', 0, NPC_REGULAR),
 4001: (4502, lnames[4001], 'r', 'f', 0, NPC_REGULAR),
 4002: (4504, lnames[4002], ('fll', 'ss', 'm', 'm', 5, 0, 5, 5, 0, 2, 0, 2, 1, 17), 'm', 0, NPC_HQ),
 4003: (4504, lnames[4003], ('fsl', 'md', 'm', 'f', 21, 0, 21, 21, 0, 3, 0, 3, 10, 27), 'f', 0, NPC_HQ),
 4004: (4504, lnames[4004], ('fls', 'ls', 'm', 'f', 13, 0, 13, 13, 1, 3, 1, 3, 2, 11), 'f', 0, NPC_HQ),
 4005: (4504, lnames[4005], ('rll', 'ss', 'm', 'f', 4, 0, 4, 4, 1, 4, 1, 4, 24, 27), 'f', 0, NPC_HQ),
 4006: (4503, lnames[4006], ('rss', 'md', 'm', 'f', 21, 0, 21, 21, 1, 4, 1, 4, 8, 8), 'f', 0, NPC_CLERK),
 4007: (4503, lnames[4007], ('rls', 'ms', 'm', 'm', 12, 0, 12, 12, 1, 3, 1, 3, 1, 19), 'm', 0, NPC_CLERK),
 4008: (4506, lnames[4008], ('mls', 'ms', 'm', 'f', 4, 0, 4, 4, 1, 5, 1, 5, 7, 9), 'f', 0, NPC_TAILOR),
 4009: (4000, lnames[4009], ('hsl', 'ld', 'm', 'f', 19, 0, 19, 19, 1, 6, 1, 6, 12, 27), 'f', 0, NPC_FISHERMAN),
 4010: (4508, lnames[4010], ('hss', 'ms', 'm', 'm', 12, 0, 12, 12, 0, 5, 0, 5, 1, 10), 'm', 0, NPC_PETCLERK),
 4011: (4508, lnames[4011], ('cll', 'ss', 'm', 'm', 4, 0, 4, 4, 0, 5, 0, 5, 1, 4), 'm', 0, NPC_PETCLERK),
 4012: (4508, lnames[4012], ('csl', 'ss', 'm', 'f', 19, 0, 19, 19, 0, 8, 0, 8, 10, 27), 'f', 0, NPC_PETCLERK),
 4013: (4000, lnames[4013], ('bll', 'ls', 's', 'm', 3, 0, 19, 19, 0, 8, 0, 8, 1, 12), 'm', 1, NPC_PARTYPERSON),
 4014: (4000, lnames[4014], ('bss', 'md', 'm', 'f', 24, 0, 19, 19, 0, 24, 0, 24, 0, 12), 'f', 1, NPC_PARTYPERSON),
 4101: (4603, lnames[4101], ('cll', 'ms', 'm', 'm', 16, 0, 16, 16, 1, 7, 1, 7, 0, 6), 'm', 1, NPC_REGULAR),
 4102: (4605, lnames[4102], ('csl', 'ms', 'm', 'f', 9, 0, 9, 9, 1, 11, 1, 11, 10, 27), 'f', 1, NPC_REGULAR),
 4103: (4612, lnames[4103], ('cls', 'ls', 'l', 'm', 2, 0, 2, 2, 1, 8, 1, 8, 0, 19), 'm', 0, NPC_REGULAR),
 4104: (4659, lnames[4104], ('dll', 'ms', 'l', 'm', 16, 0, 16, 16, 1, 8, 1, 8, 0, 16), 'm', 0, NPC_HQ),
 4105: (4659, lnames[4105], ('dss', 'ls', 'l', 'f', 9, 0, 9, 9, 1, 21, 1, 21, 11, 27), 'f', 0, NPC_HQ),
 4106: (4659, lnames[4106], ('fll', 'ss', 'l', 'f', 24, 0, 24, 24, 0, 22, 0, 22, 19, 27), 'f', 0, NPC_HQ),
 4107: (4659, lnames[4107], ('fsl', 'md', 'l', 'f', 16, 0, 16, 16, 0, 22, 0, 22, 17, 27), 'f', 0, NPC_HQ),
 4108: (4626, lnames[4108], ('fls', 'ms', 'l', 'm', 8, 0, 8, 8, 0, 10, 0, 10, 0, 0), 'm', 0, NPC_REGULAR),
 4109: (4606, lnames[4109], ('rll', 'ss', 'l', 'm', 22, 0, 22, 22, 0, 11, 0, 11, 0, 18), 'm', 1, NPC_REGULAR),
 4110: (4604, lnames[4110], ('rss', 'ld', 'l', 'f', 16, 0, 16, 16, 0, 24, 0, 24, 3, 2), 'f', 1, NPC_REGULAR),
 4111: (4607, lnames[4111], 'r', 'm', 1, NPC_REGULAR),
 4112: (4609, lnames[4112], ('mls', 'ms', 'l', 'f', 24, 0, 24, 24, 0, 25, 0, 25, 11, 27), 'f', 1, NPC_REGULAR),
 4113: (4610, lnames[4113], ('hsl', 'ld', 'l', 'f', 15, 0, 15, 15, 1, 25, 1, 25, 14, 27), 'f', 0, NPC_REGULAR),
 4114: (4611, lnames[4114], ('hss', 'ms', 'l', 'm', 7, 0, 7, 7, 1, 11, 1, 11, 1, 20), 'm', 0, NPC_REGULAR),
 4115: (4614, lnames[4115], ('cll', 'ls', 'l', 'f', 23, 0, 23, 23, 1, 26, 1, 26, 10, 27), 'f', 0, NPC_REGULAR),
 4116: (4615, lnames[4116], ('csl', 'ss', 'm', 'm', 15, 0, 15, 15, 1, 12, 1, 12, 1, 14), 'm', 0, NPC_REGULAR),
 4117: (4617, lnames[4117], ('cls', 'md', 'm', 'f', 7, 0, 7, 7, 1, 0, 1, 0, 1, 25), 'f', 0, NPC_REGULAR),
 4118: (4618, lnames[4118], 'r', 'm', 0, NPC_REGULAR),
 4119: (4619, lnames[4119], ('dss', 'ss', 'm', 'm', 14, 0, 14, 14, 0, 0, 0, 0, 1, 1), 'm', 0, NPC_REGULAR),
 4120: (4622, lnames[4120], ('dls', 'ld', 'm', 'f', 7, 0, 7, 7, 0, 1, 0, 1, 26, 27), 'f', 0, NPC_REGULAR),
 4121: (4623, lnames[4121], ('fsl', 'ms', 'm', 'm', 21, 0, 21, 21, 0, 1, 0, 1, 1, 16), 'm', 0, NPC_REGULAR),
 4122: (4625, lnames[4122], ('fls', 'ms', 'm', 'f', 14, 0, 14, 14, 0, 2, 0, 2, 17, 27), 'f', 0, NPC_REGULAR),
 4123: (4628, lnames[4123], ('rll', 'ls', 'm', 'm', 6, 0, 6, 6, 0, 2, 0, 2, 1, 10), 'm', 0, NPC_REGULAR),
 4124: (4629, lnames[4124], ('rss', 'ms', 'm', 'm', 20, 0, 20, 20, 0, 2, 0, 2, 1, 4), 'm', 0, NPC_REGULAR),
 4125: (4630, lnames[4125], ('rls', 'ls', 'm', 'f', 14, 0, 14, 14, 1, 3, 1, 3, 8, 6), 'f', 0, NPC_REGULAR),
 4126: (4631, lnames[4126], ('mls', 'ss', 'm', 'm', 6, 0, 6, 6, 1, 3, 1, 3, 1, 18), 'm', 0, NPC_REGULAR),
 4127: (4632, lnames[4127], ('hll', 'md', 'm', 'f', 22, 0, 22, 22, 1, 4, 1, 4, 23, 27), 'f', 0, NPC_REGULAR),
 4128: (4635, lnames[4128], ('hss', 'ms', 'm', 'm', 13, 0, 13, 13, 1, 3, 1, 3, 1, 12), 'm', 0, NPC_REGULAR),
 4129: (4637, lnames[4129], ('hls', 'ss', 'l', 'f', 6, 0, 6, 6, 1, 5, 1, 5, 26, 27), 'f', 0, NPC_REGULAR),
 4130: (4638, lnames[4130], 'r', 'm', 0, NPC_REGULAR),
 4131: (4639, lnames[4131], 'r', 'm', 0, NPC_REGULAR),
 4132: (4641, lnames[4132], ('dll', 'ms', 'l', 'f', 6, 0, 6, 6, 0, 7, 0, 7, 17, 27), 'f', 0, NPC_REGULAR),
 4133: (4642, lnames[4133], ('dss', 'ls', 'l', 'm', 20, 0, 20, 20, 0, 5, 0, 5, 1, 14), 'm', 0, NPC_REGULAR),
 4134: (4645, lnames[4134], 'r', 'm', 0, NPC_REGULAR),
 4135: (4648, lnames[4135], ('fsl', 'ms', 'l', 'm', 5, 0, 5, 5, 0, 6, 0, 6, 1, 6), 'm', 0, NPC_REGULAR),
 4136: (4652, lnames[4136], ('fss', 'ss', 'l', 'f', 21, 0, 21, 21, 0, 9, 0, 9, 7, 4), 'f', 0, NPC_REGULAR),
 4137: (4654, lnames[4137], ('rll', 'ls', 'l', 'm', 13, 0, 13, 13, 1, 6, 1, 6, 1, 19), 'm', 0, NPC_REGULAR),
 4138: (4655, lnames[4138], ('rsl', 'ms', 'l', 'm', 5, 0, 5, 5, 1, 7, 1, 7, 1, 16), 'm', 0, NPC_REGULAR),
 4139: (4657, lnames[4139], ('rls', 'ss', 'l', 'f', 21, 0, 21, 21, 1, 11, 1, 11, 14, 27), 'f', 0, NPC_REGULAR),
 4140: (4658, lnames[4140], ('mls', 'ls', 'l', 'm', 12, 0, 12, 12, 1, 7, 1, 7, 1, 10), 'm', 0, NPC_REGULAR),
 4141: (4148, lnames[4141], ('hll', 'ms', 'l', 'm', 4, 0, 4, 4, 1, 8, 1, 8, 1, 4), 'm', 0, NPC_FISHERMAN),
 4201: (4704, lnames[4201], ('mss', 'ss', 'l', 'f', 14, 0, 14, 14, 0, 6, 0, 6, 11, 27), 'f', 1, NPC_REGULAR),
 4202: (4725, lnames[4202], ('mls', 'ls', 'l', 'm', 6, 0, 6, 6, 0, 5, 0, 5, 0, 13), 'm', 0, NPC_REGULAR),
 4203: (4702, lnames[4203], ('hsl', 'ms', 'l', 'm', 21, 0, 21, 21, 0, 5, 0, 5, 0, 10), 'm', 1, NPC_REGULAR),
 4204: (4739, lnames[4204], ('hss', 'ss', 'l', 'm', 14, 0, 14, 14, 0, 6, 0, 6, 0, 4), 'm', 0, NPC_HQ),
 4205: (4739, lnames[4205], ('cll', 'ld', 'l', 'f', 6, 0, 6, 6, 1, 8, 1, 8, 10, 27), 'f', 0, NPC_HQ),
 4206: (4739, lnames[4206], ('css', 'sd', 'l', 'f', 22, 0, 22, 22, 1, 8, 1, 8, 25, 27), 'f', 0, NPC_HQ),
 4207: (4739, lnames[4207], ('cls', 'ls', 'l', 'f', 14, 0, 14, 14, 1, 9, 1, 9, 17, 27), 'f', 0, NPC_HQ),
 4208: (4730, lnames[4208], ('dsl', 'ss', 'l', 'f', 6, 0, 6, 6, 1, 9, 1, 9, 10, 27), 'f', 0, NPC_REGULAR),
 4209: (4701, lnames[4209], ('dss', 'md', 'l', 'f', 22, 0, 22, 22, 1, 11, 1, 11, 1, 9), 'f', 1, NPC_REGULAR),
 4211: (4703, lnames[4211], ('fsl', 'ss', 'l', 'm', 5, 0, 5, 5, 1, 8, 1, 8, 0, 20), 'm', 1, NPC_REGULAR),
 4212: (4705, lnames[4212], ('fls', 'ls', 'l', 'm', 20, 0, 20, 20, 0, 9, 0, 9, 0, 17), 'm', 1, NPC_REGULAR),
 4213: (4707, lnames[4213], ('rll', 'sd', 'l', 'f', 13, 0, 13, 13, 0, 21, 0, 21, 24, 27), 'f', 1, NPC_REGULAR),
 4214: (4709, lnames[4214], 'r', 'f', 1, NPC_REGULAR),
 4215: (4710, lnames[4215], ('mss', 'ls', 'l', 'm', 19, 0, 19, 19, 0, 10, 0, 10, 0, 6), 'm', 0, NPC_REGULAR),
 4216: (4712, lnames[4216], ('mls', 'ms', 's', 'm', 13, 0, 13, 13, 0, 10, 0, 10, 0, 1), 'm', 0, NPC_REGULAR),
 4217: (4713, lnames[4217], ('hsl', 'ms', 's', 'm', 5, 0, 5, 5, 0, 10, 0, 10, 0, 19), 'm', 0, NPC_REGULAR),
 4218: (4716, lnames[4218], ('hss', 'ss', 's', 'f', 21, 0, 21, 21, 1, 23, 1, 23, 26, 27), 'f', 0, NPC_REGULAR),
 4219: (4717, lnames[4219], 'r', 'm', 0, NPC_REGULAR),
 4220: (4718, lnames[4220], 'r', 'm', 0, NPC_REGULAR),
 4221: (4719, lnames[4221], ('cls', 'ss', 's', 'm', 19, 0, 19, 19, 1, 11, 1, 11, 0, 4), 'm', 0, NPC_REGULAR),
 4222: (4720, lnames[4222], ('dsl', 'ls', 's', 'm', 12, 0, 12, 12, 1, 11, 1, 11, 0, 0), 'm', 0, NPC_REGULAR),
 4223: (4722, lnames[4223], ('dss', 'sd', 's', 'f', 3, 0, 3, 3, 1, 25, 1, 25, 24, 27), 'f', 0, NPC_REGULAR),
 4224: (4723, lnames[4224], 'r', 'm', 0, NPC_REGULAR),
 4225: (4724, lnames[4225], ('fsl', 'ld', 's', 'f', 12, 0, 12, 12, 0, 27, 0, 27, 11, 27), 'f', 0, NPC_REGULAR),
 4226: (4727, lnames[4226], ('fls', 'sd', 's', 'f', 3, 0, 3, 3, 0, 0, 0, 0, 11, 27), 'f', 0, NPC_REGULAR),
 4227: (4728, lnames[4227], ('rll', 'ls', 's', 'f', 19, 0, 19, 19, 0, 0, 0, 0, 23, 27), 'f', 0, NPC_REGULAR),
 4228: (4729, lnames[4228], ('rss', 'ss', 's', 'f', 11, 0, 11, 11, 0, 1, 0, 1, 0, 1), 'f', 0, NPC_REGULAR),
 4229: (4731, lnames[4229], ('rls', 'md', 'm', 'f', 3, 0, 3, 3, 0, 1, 0, 1, 26, 27), 'f', 0, NPC_REGULAR),
 4230: (4732, lnames[4230], ('mls', 'ms', 'm', 'm', 18, 0, 18, 18, 1, 1, 1, 1, 0, 14), 'm', 0, NPC_REGULAR),
 4231: (4735, lnames[4231], ('hsl', 'ss', 'm', 'f', 11, 0, 11, 11, 1, 2, 1, 2, 8, 0), 'f', 0, NPC_REGULAR),
 4232: (4736, lnames[4232], ('hss', 'ls', 'm', 'm', 3, 0, 3, 3, 1, 2, 1, 2, 1, 6), 'm', 0, NPC_REGULAR),
 4233: (4737, lnames[4233], ('cll', 'ms', 'm', 'm', 17, 0, 17, 17, 1, 2, 1, 2, 1, 1), 'm', 0, NPC_REGULAR),
 4234: (4738, lnames[4234], 'r', 'm', 0, NPC_REGULAR),
 4235: (4240, lnames[4235], ('cls', 'ls', 'm', 'm', 3, 0, 3, 3, 1, 3, 1, 3, 1, 16), 'm', 0, NPC_FISHERMAN),
 4301: (4819, lnames[4301], ('fss', 'md', 'l', 'f', 12, 0, 12, 12, 1, 2, 1, 2, 17, 27), 'f', 0, NPC_REGULAR),
 4302: (4821, lnames[4302], ('fls', 'ls', 'l', 'f', 3, 0, 3, 3, 1, 2, 1, 2, 2, 3), 'f', 0, NPC_REGULAR),
 4303: (4853, lnames[4303], ('rsl', 'ss', 'l', 'm', 18, 0, 18, 18, 1, 2, 1, 2, 0, 18), 'm', 0, NPC_REGULAR),
 4304: (4873, lnames[4304], ('rss', 'ls', 'm', 'm', 12, 0, 12, 12, 0, 2, 0, 2, 0, 15), 'm', 0, NPC_HQ),
 4305: (4873, lnames[4305], ('mss', 'sd', 'm', 'f', 3, 0, 3, 3, 0, 4, 0, 4, 26, 27), 'f', 0, NPC_HQ),
 4306: (4873, lnames[4306], ('hll', 'ms', 'm', 'f', 19, 0, 19, 19, 0, 5, 0, 5, 4, 25), 'f', 0, NPC_HQ),
 4307: (4873, lnames[4307], ('hsl', 'ld', 'm', 'f', 11, 0, 11, 11, 0, 5, 0, 5, 17, 27), 'f', 0, NPC_HQ),
 4308: (4835, lnames[4308], ('css', 'md', 'm', 'f', 6, 0, 6, 6, 3, 5, 3, 5, 0, 14), 'f', 0, NPC_REGULAR),
 4309: (4801, lnames[4309], ('cll', 'ms', 'm', 'm', 18, 0, 18, 18, 0, 4, 0, 4, 0, 17), 'm', 1, NPC_REGULAR),
 4310: (4803, lnames[4310], 'r', 'f', 1, NPC_REGULAR),
 4311: (4804, lnames[4311], 'r', 'f', 1, NPC_REGULAR),
 4312: (4807, lnames[4312], ('dsl', 'ms', 'm', 'm', 18, 0, 18, 18, 1, 5, 1, 5, 0, 9), 'm', 1, NPC_REGULAR),
 4313: (4809, lnames[4313], ('dss', 'ss', 'm', 'm', 10, 0, 10, 10, 1, 5, 1, 5, 0, 2), 'm', 1, NPC_REGULAR),
 4314: (4817, lnames[4314], ('fll', 'ld', 'm', 'f', 2, 0, 2, 2, 1, 8, 1, 8, 12, 27), 'f', 0, NPC_REGULAR),
 4315: (4827, lnames[4315], ('fss', 'sd', 'm', 'f', 18, 0, 18, 18, 1, 9, 1, 9, 26, 27), 'f', 0, NPC_REGULAR),
 4316: (4828, lnames[4316], ('fls', 'ss', 'm', 'm', 9, 0, 9, 9, 1, 6, 1, 6, 0, 14), 'm', 0, NPC_REGULAR),
 4317: (4829, lnames[4317], ('rsl', 'ls', 'l', 'm', 3, 0, 3, 3, 0, 7, 0, 7, 0, 11), 'm', 0, NPC_REGULAR),
 4318: (4836, lnames[4318], ('rss', 'ms', 'l', 'm', 17, 0, 17, 17, 0, 8, 0, 8, 0, 6), 'm', 0, NPC_REGULAR),
 4319: (4838, lnames[4319], ('mss', 'ls', 'l', 'f', 10, 0, 10, 10, 0, 12, 0, 12, 1, 23), 'f', 0, NPC_REGULAR),
 4320: (4840, lnames[4320], ('mls', 'ss', 'l', 'f', 1, 0, 1, 1, 0, 21, 0, 21, 11, 27), 'f', 0, NPC_REGULAR),
 4321: (4841, lnames[4321], ('hsl', 'ls', 'l', 'm', 17, 0, 17, 17, 0, 9, 0, 9, 0, 16), 'm', 0, NPC_REGULAR),
 4322: (4842, lnames[4322], ('hls', 'ms', 'l', 'm', 9, 0, 9, 9, 0, 9, 0, 9, 0, 13), 'm', 0, NPC_REGULAR),
 4323: (4844, lnames[4323], ('cll', 'ss', 'l', 'f', 1, 0, 1, 1, 1, 21, 1, 21, 24, 27), 'f', 0, NPC_REGULAR),
 4324: (4845, lnames[4324], ('css', 'ld', 'l', 'f', 17, 0, 17, 17, 1, 22, 1, 22, 10, 27), 'f', 0, NPC_REGULAR),
 4325: (4848, lnames[4325], ('cls', 'ms', 'l', 'm', 9, 0, 9, 9, 1, 9, 1, 9, 0, 0), 'm', 0, NPC_REGULAR),
 4326: (4850, lnames[4326], ('dsl', 'ms', 'l', 'f', 1, 0, 1, 1, 1, 23, 1, 23, 14, 27), 'f', 0, NPC_REGULAR),
 4327: (4852, lnames[4327], ('dss', 'ld', 'l', 'f', 16, 0, 16, 16, 1, 23, 1, 23, 7, 1), 'f', 0, NPC_REGULAR),
 4328: (4854, lnames[4328], ('fll', 'ms', 'l', 'm', 8, 0, 8, 8, 1, 11, 1, 11, 0, 12), 'm', 0, NPC_REGULAR),
 4329: (4855, lnames[4329], ('fsl', 'ls', 'l', 'f', 24, 0, 24, 24, 0, 25, 0, 25, 26, 27), 'f', 0, NPC_REGULAR),
 4330: (4862, lnames[4330], 'r', 'm', 0, NPC_REGULAR),
 4331: (4867, lnames[4331], 'r', 'm', 0, NPC_REGULAR),
 4332: (4870, lnames[4332], ('rss', 'ms', 'l', 'm', 22, 0, 22, 22, 0, 27, 0, 27, 0, 17), 'm', 0, NPC_REGULAR),
 4333: (4871, lnames[4333], ('mss', 'ss', 'l', 'm', 15, 0, 15, 15, 0, 27, 0, 27, 0, 14), 'm', 0, NPC_REGULAR),
 4334: (4872, lnames[4334], ('mls', 'ls', 'l', 'm', 8, 0, 8, 8, 0, 0, 0, 0, 0, 11), 'm', 0, NPC_REGULAR),
 4335: (4345, lnames[4335], ('hsl', 'ms', 'l', 'm', 22, 0, 22, 22, 1, 0, 1, 0, 0, 6), 'm', 0, NPC_FISHERMAN),
 5001: (5502, lnames[5001], ('fls', 'ls', 's', 'm', 14, 0, 14, 14, 1, 7, 1, 7, 0, 20), 'm', 0, NPC_HQ),
 5002: (5502, lnames[5002], ('rll', 'ms', 's', 'm', 6, 0, 6, 6, 0, 8, 0, 8, 0, 17), 'm', 0, NPC_HQ),
 5003: (5502, lnames[5003], ('rss', 'ms', 's', 'f', 22, 0, 22, 22, 0, 12, 0, 12, 26, 27), 'f', 0, NPC_HQ),
 5004: (5502, lnames[5004], ('rls', 'ld', 's', 'f', 13, 0, 13, 13, 0, 21, 0, 21, 4, 11), 'f', 0, NPC_HQ),
 5005: (5501, lnames[5005], ('mls', 'md', 's', 'f', 6, 0, 6, 6, 0, 21, 0, 21, 2, 3), 'f', 0, NPC_CLERK),
 5006: (5501, lnames[5006], ('hsl', 'ms', 's', 'm', 20, 0, 20, 20, 0, 9, 0, 9, 0, 1), 'm', 0, NPC_CLERK),
 5007: (5503, lnames[5007], ('hss', 'ss', 's', 'f', 13, 0, 13, 13, 0, 22, 0, 22, 3, 2), 'f', 0, NPC_TAILOR),
 5008: (5000, lnames[5008], ('cll', 'md', 's', 'f', 4, 0, 4, 4, 1, 22, 1, 22, 19, 27), 'f', 0, NPC_FISHERMAN),
 5009: (5505, lnames[5009], ('csl', 'ls', 'm', 'f', 21, 0, 21, 21, 1, 23, 1, 23, 8, 23), 'f', 0, NPC_PETCLERK),
 5010: (5505, lnames[5010], ('cls', 'ss', 'm', 'm', 13, 0, 13, 13, 1, 10, 1, 10, 0, 10), 'm', 0, NPC_PETCLERK),
 5011: (5505, lnames[5011], ('dll', 'ls', 'm', 'm', 5, 0, 5, 5, 1, 10, 1, 10, 0, 4), 'm', 0, NPC_PETCLERK),
 5012: (5000, lnames[5012], ('dls', 'ms', 'm', 'm', 13, 0, 12, 12, 0, 1, 0, 1, 0, 6), 'm', 1, NPC_PARTYPERSON),
 5013: (5000, lnames[5013], ('dss', 'md', 'm', 'f', 1, 0, 3, 3, 1, 5, 1, 5, 0, 5), 'f', 1, NPC_PARTYPERSON),
 5101: (5602, lnames[5101], ('dsl', 'ms', 'l', 'm', 10, 0, 10, 10, 1, 4, 1, 4, 0, 11), 'm', 1, NPC_REGULAR),
 5102: (5610, lnames[5102], 'r', 'f', 0, NPC_REGULAR),
 5103: (5615, lnames[5103], ('fll', 'ls', 'l', 'm', 18, 0, 18, 18, 1, 5, 1, 5, 0, 1), 'm', 0, NPC_REGULAR),
 5104: (5617, lnames[5104], ('fsl', 'ms', 'l', 'm', 10, 0, 10, 10, 1, 5, 1, 5, 0, 19), 'm', 0, NPC_REGULAR),
 5105: (5619, lnames[5105], 'r', 'm', 0, NPC_REGULAR),
 5106: (5613, lnames[5106], ('rsl', 'ls', 'l', 'm', 18, 0, 18, 18, 1, 6, 1, 6, 0, 13), 'm', 0, NPC_REGULAR),
 5107: (5607, lnames[5107], 'r', 'm', 1, NPC_REGULAR),
 5108: (5616, lnames[5108], ('mss', 'ls', 'l', 'f', 2, 0, 2, 2, 0, 11, 0, 11, 24, 27), 'f', 0, NPC_REGULAR),
 5109: (5627, lnames[5109], ('mls', 'ss', 'l', 'm', 17, 0, 17, 17, 0, 7, 0, 7, 0, 0), 'm', 1, NPC_HQ),
 5110: (5627, lnames[5110], ('hsl', 'ls', 'l', 'm', 10, 0, 10, 10, 0, 8, 0, 8, 0, 18), 'm', 1, NPC_HQ),
 5111: (5627, lnames[5111], ('hss', 'ls', 'l', 'f', 2, 0, 2, 2, 0, 12, 0, 12, 7, 4), 'f', 1, NPC_HQ),
 5112: (5627, lnames[5112], ('cll', 'ms', 'l', 'f', 17, 0, 17, 17, 0, 21, 0, 21, 14, 27), 'f', 1, NPC_HQ),
 5113: (5601, lnames[5113], ('css', 'ld', 'l', 'f', 10, 0, 10, 10, 0, 21, 0, 21, 3, 2), 'f', 1, NPC_REGULAR),
 5114: (5603, lnames[5114], ('cls', 'ms', 'l', 'm', 2, 0, 2, 2, 1, 9, 1, 9, 0, 2), 'm', 1, NPC_REGULAR),
 5115: (5604, lnames[5115], ('dsl', 'ms', 'l', 'f', 17, 0, 17, 17, 1, 22, 1, 22, 10, 27), 'f', 1, NPC_REGULAR),
 5116: (5605, lnames[5116], ('dss', 'ls', 'l', 'm', 9, 0, 9, 9, 1, 9, 1, 9, 0, 17), 'm', 1, NPC_REGULAR),
 5117: (5606, lnames[5117], ('fll', 'md', 'l', 'f', 1, 0, 1, 1, 1, 23, 1, 23, 17, 27), 'f', 1, NPC_REGULAR),
 5118: (5608, lnames[5118], ('fsl', 'ms', 'l', 'm', 16, 0, 16, 16, 1, 10, 1, 10, 0, 11), 'm', 1, NPC_REGULAR),
 5119: (5609, lnames[5119], ('fls', 'ss', 'l', 'm', 9, 0, 9, 9, 1, 10, 1, 10, 0, 6), 'm', 1, NPC_REGULAR),
 5120: (5611, lnames[5120], ('rsl', 'ss', 'l', 'm', 22, 0, 22, 22, 1, 3, 1, 3, 1, 19), 'm', 0, NPC_REGULAR),
 5121: (5618, lnames[5121], ('rss', 'ss', 'l', 'f', 23, 0, 23, 23, 1, 9, 1, 9, 0, 25), 'f', 0, NPC_REGULAR),
 5122: (5620, lnames[5122], 'r', 'm', 0, NPC_REGULAR),
 5123: (5621, lnames[5123], ('mls', 'sd', 'm', 'f', 7, 0, 7, 7, 1, 11, 1, 11, 25, 27), 'f', 0, NPC_REGULAR),
 5124: (5622, lnames[5124], ('hll', 'ss', 'm', 'm', 21, 0, 21, 21, 0, 8, 0, 8, 0, 4), 'm', 0, NPC_REGULAR),
 5125: (5623, lnames[5125], ('hss', 'ls', 'm', 'm', 14, 0, 14, 14, 0, 9, 0, 9, 0, 0), 'm', 0, NPC_REGULAR),
 5126: (5624, lnames[5126], ('hls', 'sd', 'm', 'f', 7, 0, 7, 7, 0, 21, 0, 21, 14, 27), 'f', 0, NPC_REGULAR),
 5127: (5625, lnames[5127], ('csl', 'ms', 'm', 'f', 23, 0, 23, 23, 0, 22, 0, 22, 2, 2), 'f', 0, NPC_REGULAR),
 5128: (5626, lnames[5128], 'r', 'f', 0, NPC_REGULAR),
 5129: (5139, lnames[5129], ('dll', 'md', 'm', 'f', 7, 0, 7, 7, 0, 23, 0, 23, 17, 27), 'f', 0, NPC_FISHERMAN),
 5201: (5702, lnames[5201], ('hls', 'ls', 'l', 'm', 15, 0, 15, 15, 1, 10, 1, 10, 1, 16), 'm', 1, NPC_REGULAR),
 5202: (5703, lnames[5202], ('cll', 'ls', 'l', 'f', 7, 0, 7, 7, 1, 23, 1, 23, 11, 27), 'f', 1, NPC_REGULAR),
 5203: (5704, lnames[5203], ('css', 'ss', 'l', 'f', 23, 0, 23, 23, 1, 24, 1, 24, 19, 27), 'f', 1, NPC_REGULAR),
 5204: (5726, lnames[5204], ('cls', 'ls', 'l', 'm', 14, 0, 14, 14, 0, 12, 0, 12, 1, 4), 'm', 0, NPC_REGULAR),
 5205: (5718, lnames[5205], 'r', 'm', 0, NPC_REGULAR),
 5206: (5720, lnames[5206], ('dss', 'ss', 'l', 'm', 21, 0, 21, 21, 0, 27, 0, 27, 1, 18), 'm', 0, NPC_REGULAR),
 5207: (5717, lnames[5207], ('fll', 'ld', 'l', 'f', 14, 0, 14, 14, 0, 27, 0, 27, 26, 27), 'f', 0, NPC_REGULAR),
 5208: (5719, lnames[5208], ('fsl', 'sd', 'l', 'f', 7, 0, 7, 7, 0, 27, 0, 27, 1, 12), 'f', 0, NPC_REGULAR),
 5209: (5728, lnames[5209], ('fls', 'ss', 'l', 'm', 21, 0, 21, 21, 0, 0, 0, 0, 1, 9), 'm', 1, NPC_HQ),
 5210: (5728, lnames[5210], ('rsl', 'ss', 'l', 'm', 14, 0, 14, 14, 1, 0, 1, 0, 1, 2), 'm', 1, NPC_HQ),
 5211: (5728, lnames[5211], ('rss', 'md', 'l', 'f', 6, 0, 6, 6, 1, 1, 1, 1, 23, 27), 'f', 1, NPC_HQ),
 5212: (5728, lnames[5212], ('mss', 'ls', 'l', 'f', 22, 0, 22, 22, 1, 1, 1, 1, 10, 27), 'f', 1, NPC_HQ),
 5213: (5701, lnames[5213], ('mls', 'ss', 'l', 'm', 13, 0, 13, 13, 1, 1, 1, 1, 1, 14), 'm', 1, NPC_REGULAR),
 5214: (5705, lnames[5214], ('hsl', 'md', 'l', 'f', 6, 0, 6, 6, 1, 2, 1, 2, 17, 27), 'f', 1, NPC_REGULAR),
 5215: (5706, lnames[5215], 'r', 'f', 1, NPC_REGULAR),
 5216: (5707, lnames[5216], ('cll', 'ss', 'l', 'm', 13, 0, 13, 13, 0, 2, 0, 2, 1, 1), 'm', 1, NPC_REGULAR),
 5217: (5708, lnames[5217], ('csl', 'ls', 'l', 'm', 5, 0, 5, 5, 0, 3, 0, 3, 1, 19), 'm', 1, NPC_REGULAR),
 5218: (5709, lnames[5218], 'r', 'm', 1, NPC_REGULAR),
 5219: (5710, lnames[5219], ('dsl', 'ss', 'l', 'm', 13, 0, 13, 13, 0, 3, 0, 3, 1, 13), 'm', 0, NPC_REGULAR),
 5220: (5711, lnames[5220], 'r', 'f', 0, NPC_REGULAR),
 5221: (5712, lnames[5221], ('fll', 'md', 'l', 'f', 21, 0, 21, 21, 0, 6, 0, 6, 25, 27), 'f', 0, NPC_REGULAR),
 5222: (5713, lnames[5222], 'r', 'f', 0, NPC_REGULAR),
 5223: (5714, lnames[5223], ('fls', 'ss', 's', 'm', 5, 0, 5, 5, 1, 4, 1, 4, 1, 18), 'm', 0, NPC_REGULAR),
 5224: (5715, lnames[5224], ('rll', 'ls', 's', 'm', 19, 0, 19, 19, 1, 5, 1, 5, 1, 15), 'm', 0, NPC_REGULAR),
 5225: (5716, lnames[5225], ('rss', 'sd', 's', 'f', 12, 0, 12, 12, 1, 7, 1, 7, 10, 27), 'f', 0, NPC_REGULAR),
 5226: (5721, lnames[5226], ('rls', 'ss', 's', 'm', 4, 0, 4, 4, 1, 5, 1, 5, 1, 9), 'm', 0, NPC_REGULAR),
 5227: (5725, lnames[5227], ('mls', 'ld', 's', 'f', 19, 0, 19, 19, 1, 8, 1, 8, 23, 27), 'f', 0, NPC_REGULAR),
 5228: (5727, lnames[5228], ('hsl', 'ms', 's', 'm', 12, 0, 12, 12, 1, 6, 1, 6, 1, 20), 'm', 0, NPC_REGULAR),
 5229: (5245, lnames[5229], ('hss', 'ms', 's', 'f', 3, 0, 3, 3, 0, 11, 0, 11, 16, 27), 'f', 0, NPC_FISHERMAN),
 5301: (5802, lnames[5301], ('rss', 'ms', 'l', 'f', 13, 0, 13, 13, 0, 11, 0, 11, 1, 12), 'f', 1, NPC_HQ),
 5302: (5802, lnames[5302], ('mss', 'ss', 'l', 'f', 4, 0, 4, 4, 0, 12, 0, 12, 17, 27), 'f', 1, NPC_HQ),
 5303: (5802, lnames[5303], ('hll', 'ls', 'l', 'm', 19, 0, 19, 19, 1, 8, 1, 8, 1, 18), 'm', 1, NPC_HQ),
 5304: (5802, lnames[5304], ('hsl', 'ls', 'l', 'f', 12, 0, 12, 12, 1, 12, 1, 12, 19, 27), 'f', 1, NPC_HQ),
 5305: (5804, lnames[5305], ('hls', 'ss', 'l', 'f', 4, 0, 4, 4, 1, 21, 1, 21, 16, 27), 'f', 1, NPC_REGULAR),
 5306: (5805, lnames[5306], 'r', 'm', 1, NPC_REGULAR),
 5307: (5809, lnames[5307], ('css', 'ms', 'l', 'm', 12, 0, 12, 12, 1, 9, 1, 9, 1, 2), 'm', 1, NPC_REGULAR),
 5308: (5810, lnames[5308], ('cls', 'ms', 'l', 'f', 4, 0, 4, 4, 1, 22, 1, 22, 10, 27), 'f', 0, NPC_REGULAR),
 5309: (5811, lnames[5309], 'r', 'f', 0, NPC_REGULAR),
 5310: (5815, lnames[5310], ('dls', 'ms', 'l', 'm', 12, 0, 12, 12, 0, 11, 0, 11, 1, 14), 'm', 0, NPC_REGULAR),
 5311: (5817, lnames[5311], ('fll', 'ms', 'm', 'f', 3, 0, 3, 3, 0, 24, 0, 24, 12, 27), 'f', 0, NPC_REGULAR),
 5312: (5819, lnames[5312], ('fss', 'ss', 'm', 'm', 18, 0, 18, 18, 0, 12, 0, 12, 1, 6), 'm', 0, NPC_REGULAR),
 5313: (5821, lnames[5313], ('fls', 'ls', 'm', 'm', 10, 0, 10, 10, 0, 12, 0, 12, 1, 1), 'm', 0, NPC_REGULAR),
 5314: (5826, lnames[5314], 'r', 'f', 0, NPC_REGULAR),
 5315: (5827, lnames[5315], ('rss', 'ss', 'm', 'm', 18, 0, 18, 18, 1, 12, 1, 12, 1, 16), 'm', 0, NPC_REGULAR),
 5316: (5828, lnames[5316], ('mss', 'ls', 'm', 'm', 10, 0, 10, 10, 1, 12, 1, 12, 1, 13), 'm', 0, NPC_REGULAR),
 5317: (5830, lnames[5317], 'r', 'm', 0, NPC_REGULAR),
 5318: (5833, lnames[5318], ('hsl', 'ss', 'm', 'm', 18, 0, 18, 18, 1, 0, 1, 0, 1, 4), 'm', 0, NPC_REGULAR),
 5319: (5835, lnames[5319], 'r', 'f', 0, NPC_REGULAR),
 5320: (5836, lnames[5320], ('cll', 'sd', 'm', 'f', 2, 0, 2, 2, 1, 1, 1, 1, 17, 27), 'f', 0, NPC_REGULAR),
 5321: (5837, lnames[5321], ('css', 'ms', 'm', 'f', 18, 0, 18, 18, 1, 1, 1, 1, 17, 27), 'f', 0, NPC_REGULAR),
 5322: (5318, lnames[5322], ('cls', 'ss', 'm', 'f', 10, 0, 10, 10, 0, 2, 0, 2, 11, 27), 'f', 0, NPC_FISHERMAN),
 6000: (6000, lnames[6000], ('hsl', 'ms', 'm', 'm', 8, 0, 8, 8, 1, 6, 1, 6, 0, 18), 'm', 0, NPC_FISHERMAN),
 8001: (8501, lnames[8001], ('psl', 'ms', 'm', 'm', 13, 0, 13, 13, 0, 11, 0, 11, 2, 10), 'm', 0, NPC_KARTCLERK),
 8002: (8501, lnames[8002], ('psl', 'ld', 's', 'f', 23, 0, 23, 23, 0, 11, 0, 11, 2, 10), 'f', 0, NPC_KARTCLERK),
 8003: (8501, lnames[8003], ('pll', 'ss', 'l', 'f', 1, 0, 1, 1, 0, 11, 0, 11, 2, 10), 'f', 0, NPC_KARTCLERK),
 8004: (8501, lnames[8004], ('pls', 'ms', 'l', 'm', 16, 0, 16, 16, 0, 11, 0, 11, 2, 10), 'm', 0, NPC_KARTCLERK),
 9001: (9503, lnames[9001], ('fll', 'ss', 'l', 'f', 16, 0, 16, 16, 0, 6, 0, 6, 26, 27), 'f', 0, NPC_REGULAR),
 9002: (9502, lnames[9002], 'r', 'm', 0, NPC_REGULAR),
 9003: (9501, lnames[9003], ('fls', 'ms', 'l', 'm', 22, 0, 22, 22, 1, 5, 1, 5, 0, 14), 'm', 0, NPC_REGULAR),
 9004: (9505, lnames[9004], ('rll', 'ms', 'l', 'f', 16, 0, 16, 16, 1, 7, 1, 7, 3, 8), 'f', 1, NPC_HQ),
 9005: (9505, lnames[9005], ('rss', 'ld', 'l', 'f', 9, 0, 9, 9, 1, 8, 1, 8, 19, 27), 'f', 1, NPC_HQ),
 9006: (9505, lnames[9006], ('rls', 'ms', 'l', 'm', 22, 0, 22, 22, 1, 6, 1, 6, 0, 1), 'm', 1, NPC_HQ),
 9007: (9505, lnames[9007], ('mls', 'ms', 'l', 'm', 15, 0, 15, 15, 1, 6, 1, 6, 0, 19), 'm', 1, NPC_HQ),
 9008: (9504, lnames[9008], ('hll', 'ss', 'l', 'f', 8, 0, 8, 8, 1, 9, 1, 9, 12, 27), 'f', 0, NPC_CLERK),
 9009: (9504, lnames[9009], ('hss', 'ls', 'l', 'm', 22, 0, 22, 22, 0, 7, 0, 7, 0, 13), 'm', 0, NPC_CLERK),
 9010: (9506, lnames[9010], ('cll', 'ms', 'l', 'm', 15, 0, 15, 15, 0, 8, 0, 8, 0, 10), 'm', 0, NPC_TAILOR),
 9011: (9000, lnames[9011], ('csl', 'ss', 'l', 'm', 7, 0, 7, 7, 0, 8, 0, 8, 0, 4), 'm', 0, NPC_FISHERMAN),
 9012: (9508, lnames[9012], ('cls', 'ld', 'l', 'f', 23, 0, 23, 23, 0, 21, 0, 21, 10, 27), 'f', 0, NPC_PETCLERK),
 9013: (9508, lnames[9013], ('dll', 'sd', 'l', 'f', 15, 0, 15, 15, 0, 21, 0, 21, 10, 27), 'f', 0, NPC_PETCLERK),
 9014: (9508, lnames[9014], ('dss', 'ss', 'l', 'm', 7, 0, 7, 7, 0, 9, 0, 9, 1, 15), 'm', 0, NPC_PETCLERK),
 9015: (9000, lnames[9015], ('rss', 'ls', 'l', 'm', 21, 0, 20, 20, 0, 12, 0, 12, 0, 11), 'm', 1, NPC_PARTYPERSON),
 9016: (9000, lnames[9016], ('rls', 'md', 'l', 'f', 6, 0, 21, 21, 1, 11, 1, 11, 0, 11), 'f', 1, NPC_PARTYPERSON),
 9101: (9604, lnames[9101], ('css', 'ls', 'l', 'm', 14, 0, 14, 14, 1, 1, 1, 1, 0, 11), 'm', 1, NPC_REGULAR),
 9102: (9607, lnames[9102], 'r', 'f', 1, NPC_REGULAR),
 9103: (9620, lnames[9103], ('dsl', 'ss', 'l', 'm', 20, 0, 20, 20, 0, 2, 0, 2, 0, 1), 'm', 0, NPC_REGULAR),
 9104: (9642, lnames[9104], ('dss', 'ld', 'l', 'f', 14, 0, 14, 14, 0, 3, 0, 3, 0, 23), 'f', 0, NPC_REGULAR),
 9105: (9609, lnames[9105], 'r', 'm', 1, NPC_REGULAR),
 9106: (9619, lnames[9106], ('fsl', 'ss', 'l', 'm', 20, 0, 20, 20, 0, 3, 0, 3, 0, 13), 'm', 0, NPC_REGULAR),
 9107: (9601, lnames[9107], ('fls', 'ld', 'l', 'f', 13, 0, 13, 13, 0, 5, 0, 5, 3, 2), 'f', 1, NPC_REGULAR),
 9108: (9602, lnames[9108], ('rll', 'ms', 'l', 'm', 6, 0, 6, 6, 1, 4, 1, 4, 0, 4), 'm', 1, NPC_REGULAR),
 9109: (9605, lnames[9109], ('rss', 'ls', 'l', 'f', 22, 0, 22, 22, 1, 6, 1, 6, 10, 27), 'f', 1, NPC_REGULAR),
 9110: (9608, lnames[9110], ('mss', 'ss', 'l', 'f', 13, 0, 13, 13, 1, 6, 1, 6, 25, 27), 'f', 1, NPC_REGULAR),
 9111: (9616, lnames[9111], 'r', 'f', 0, NPC_REGULAR),
 9112: (9617, lnames[9112], ('hsl', 'ms', 'm', 'm', 19, 0, 19, 19, 1, 5, 1, 5, 0, 12), 'm', 0, NPC_REGULAR),
 9113: (9622, lnames[9113], ('hss', 'ss', 'm', 'm', 13, 0, 13, 13, 1, 5, 1, 5, 0, 9), 'm', 0, NPC_REGULAR),
 9114: (9625, lnames[9114], ('cll', 'ld', 'm', 'f', 4, 0, 4, 4, 0, 8, 0, 8, 10, 27), 'f', 0, NPC_REGULAR),
 9115: (9626, lnames[9115], 'r', 'm', 0, NPC_REGULAR),
 9116: (9627, lnames[9116], ('cls', 'ss', 'm', 'm', 12, 0, 12, 12, 0, 7, 0, 7, 0, 17), 'm', 0, NPC_REGULAR),
 9117: (9628, lnames[9117], ('dsl', 'ld', 'm', 'f', 4, 0, 4, 4, 0, 11, 0, 11, 2, 9), 'f', 0, NPC_REGULAR),
 9118: (9629, lnames[9118], 'r', 'f', 0, NPC_REGULAR),
 9119: (9630, lnames[9119], ('fll', 'ms', 'm', 'm', 12, 0, 12, 12, 0, 8, 0, 8, 0, 6), 'm', 0, NPC_REGULAR),
 9120: (9631, lnames[9120], 'r', 'f', 0, NPC_REGULAR),
 9121: (9634, lnames[9121], ('fls', 'md', 'm', 'f', 19, 0, 19, 19, 1, 12, 1, 12, 16, 27), 'f', 0, NPC_REGULAR),
 9122: (9636, lnames[9122], ('rll', 'ms', 'm', 'm', 12, 0, 12, 12, 1, 8, 1, 8, 0, 16), 'm', 0, NPC_REGULAR),
 9123: (9639, lnames[9123], ('rss', 'ss', 'm', 'm', 4, 0, 4, 4, 1, 9, 1, 9, 0, 13), 'm', 0, NPC_REGULAR),
 9124: (9640, lnames[9124], ('rls', 'md', 'm', 'f', 19, 0, 19, 19, 1, 22, 1, 22, 8, 9), 'f', 0, NPC_REGULAR),
 9125: (9643, lnames[9125], ('mls', 'ms', 'l', 'm', 10, 0, 10, 10, 1, 9, 1, 9, 0, 4), 'm', 0, NPC_REGULAR),
 9126: (9644, lnames[9126], ('hsl', 'ms', 'l', 'f', 3, 0, 3, 3, 1, 23, 1, 23, 23, 27), 'f', 0, NPC_REGULAR),
 9127: (9645, lnames[9127], ('hss', 'ld', 'l', 'f', 19, 0, 19, 19, 0, 24, 0, 24, 10, 27), 'f', 0, NPC_REGULAR),
 9128: (9647, lnames[9128], ('cll', 'ms', 'l', 'm', 10, 0, 10, 10, 0, 11, 0, 11, 0, 15), 'm', 0, NPC_REGULAR),
 9129: (9649, lnames[9129], ('csl', 'ms', 'l', 'f', 3, 0, 3, 3, 0, 25, 0, 25, 25, 27), 'f', 0, NPC_REGULAR),
 9130: (9650, lnames[9130], ('cls', 'ss', 'l', 'm', 18, 0, 18, 18, 0, 12, 0, 12, 0, 9), 'm', 0, NPC_REGULAR),
 9131: (9651, lnames[9131], 'r', 'f', 0, NPC_REGULAR),
 9132: (9652, lnames[9132], ('dss', 'ls', 'l', 'f', 2, 0, 2, 2, 0, 27, 0, 27, 0, 0), 'f', 0, NPC_HQ),
 9133: (9652, lnames[9133], ('dls', 'ss', 'l', 'm', 17, 0, 17, 17, 1, 12, 1, 12, 0, 17), 'm', 0, NPC_HQ),
 9134: (9652, lnames[9134], ('fsl', 'ls', 'l', 'm', 10, 0, 10, 10, 1, 0, 1, 0, 0, 14), 'm', 0, NPC_HQ),
 9135: (9652, lnames[9135], ('fls', 'ms', 'l', 'm', 3, 0, 3, 3, 1, 0, 1, 0, 0, 11), 'm', 0, NPC_HQ),
 9136: (9153, lnames[9136], ('rll', 'ss', 'l', 'm', 17, 0, 17, 17, 1, 0, 1, 0, 1, 6), 'm', 0, NPC_FISHERMAN),
 9201: (9752, lnames[9201], ('psl', 'ss', 'm', 'm', 9, 0, 9, 9, 17, 11, 0, 11, 7, 20), 'm', 0, NPC_REGULAR),
 9202: (9703, lnames[9202], ('dss', 'ss', 's', 'm', 21, 0, 21, 21, 8, 3, 8, 3, 1, 17), 'm', 1, NPC_REGULAR),
 9203: (9741, lnames[9203], ('pls', 'ls', 's', 'm', 5, 0, 5, 5, 37, 27, 26, 27, 7, 4), 'm', 0, NPC_REGULAR),
 9204: (9704, lnames[9204], ('fsl', 'sd', 's', 'f', 19, 0, 19, 19, 21, 10, 0, 10, 8, 23), 'f', 1, NPC_REGULAR),
 9205: (9736, lnames[9205], ('dsl', 'ms', 'm', 'm', 15, 0, 15, 15, 45, 27, 34, 27, 2, 17), 'm', 0, NPC_REGULAR),
 9206: (9727, lnames[9206], ('rls', 'ld', 'l', 'f', 8, 0, 8, 8, 25, 27, 16, 27, 10, 27), 'f', 0, NPC_REGULAR),
 9207: (9709, lnames[9207], ('hss', 'ss', 's', 'f', 24, 0, 24, 24, 36, 27, 25, 27, 9, 27), 'f', 1, NPC_REGULAR),
 9208: (9705, lnames[9208], ('dsl', 'ms', 's', 'm', 20, 0, 20, 20, 46, 27, 35, 27, 6, 27), 'm', 1, NPC_REGULAR),
 9209: (9706, lnames[9209], ('pll', 'ss', 'm', 'm', 13, 0, 13, 13, 8, 12, 8, 12, 1, 12), 'm', 1, NPC_REGULAR),
 9210: (9740, lnames[9210], ('hsl', 'ls', 'l', 'm', 6, 0, 6, 6, 1, 0, 1, 0, 0, 0), 'm', 0, NPC_REGULAR),
 9211: (9707, lnames[9211], ('rll', 'ss', 's', 'f', 3, 0, 3, 3, 22, 22, 0, 22, 6, 22), 'f', 1, NPC_REGULAR),
 9212: (9753, lnames[9212], ('pss', 'md', 'm', 'f', 16, 0, 16, 16, 45, 27, 34, 27, 0, 3), 'f', 0, NPC_REGULAR),
 9213: (9711, lnames[9213], ('fsl', 'ss', 'm', 'm', 2, 0, 2, 2, 37, 27, 26, 27, 7, 18), 'm', 0, NPC_REGULAR),
 9214: (9710, lnames[9214], ('rll', 'ls', 'l', 'm', 18, 0, 18, 18, 10, 27, 0, 27, 0, 13), 'm', 0, NPC_REGULAR),
 9215: (9744, lnames[9215], ('csl', 'ls', 'l', 'm', 18, 0, 18, 18, 11, 4, 0, 4, 0, 4), 'm', 0, NPC_REGULAR),
 9216: (9725, lnames[9216], ('csl', 'sd', 'm', 'f', 14, 0, 14, 14, 1, 7, 1, 7, 3, 7), 'f', 0, NPC_REGULAR),
 9217: (9713, lnames[9217], ('mss', 'ms', 'm', 'f', 17, 0, 17, 17, 20, 26, 0, 26, 5, 12), 'f', 0, NPC_REGULAR),
 9218: (9737, lnames[9218], ('dss', 'md', 'l', 'f', 23, 0, 23, 23, 24, 27, 15, 27, 11, 27), 'f', 0, NPC_REGULAR),
 9219: (9712, lnames[9219], ('hll', 'sd', 'l', 'f', 10, 0, 10, 10, 9, 22, 9, 22, 12, 27), 'f', 0, NPC_REGULAR),
 9220: (9716, lnames[9220], ('mls', 'ms', 'l', 'm', 7, 0, 7, 7, 0, 27, 0, 27, 1, 10), 'm', 0, NPC_REGULAR),
 9221: (9738, lnames[9221], ('fss', 'md', 'l', 'f', 22, 0, 22, 22, 45, 27, 34, 27, 0, 6), 'f', 0, NPC_REGULAR),
 9222: (9754, lnames[9222], ('hsl', 'ls', 'l', 'm', 10, 0, 10, 10, 52, 27, 41, 27, 12, 27), 'm', 0, NPC_REGULAR),
 9223: (9714, lnames[9223], ('fsl', 'ms', 'm', 'm', 20, 0, 20, 20, 43, 27, 32, 27, 0, 0), 'm', 0, NPC_REGULAR),
 9224: (9718, lnames[9224], ('css', 'ms', 'm', 'f', 1, 0, 1, 1, 6, 8, 6, 8, 6, 8), 'f', 0, NPC_REGULAR),
 9225: (9717, lnames[9225], ('rss', 'md', 'm', 'f', 11, 0, 11, 11, 40, 27, 29, 27, 0, 27), 'f', 0, NPC_REGULAR),
 9226: (9715, lnames[9226], ('mls', 'ms', 's', 'm', 12, 0, 12, 12, 3, 10, 3, 10, 6, 10), 'm', 0, NPC_REGULAR),
 9227: (9721, lnames[9227], ('cls', 'ss', 's', 'm', 13, 0, 13, 13, 8, 5, 8, 5, 3, 18), 'm', 0, NPC_REGULAR),
 9228: (9720, lnames[9228], ('fss', 'sd', 's', 'f', 4, 0, 4, 4, 15, 5, 11, 5, 8, 5), 'f', 0, NPC_REGULAR),
 9229: (9708, lnames[9229], ('css', 'ld', 'm', 'f', 4, 0, 4, 4, 22, 21, 0, 21, 4, 21), 'f', 1, NPC_REGULAR),
 9230: (9719, lnames[9230], ('mss', 'ss', 's', 'm', 8, 0, 8, 8, 53, 27, 42, 27, 13, 27), 'm', 0, NPC_REGULAR),
 9231: (9722, lnames[9231], ('dll', 'ss', 's', 'm', 6, 0, 6, 6, 27, 27, 18, 27, 3, 8), 'm', 0, NPC_REGULAR),
 9232: (9759, lnames[9232], ('pss', 'ld', 'm', 'f', 21, 0, 21, 21, 0, 27, 0, 27, 13, 27), 'f', 0, NPC_REGULAR),
 9233: (9756, lnames[9233], ('csl', 'ls', 'l', 'f', 22, 0, 22, 22, 1, 7, 1, 7, 12, 27), 'f', 0, NPC_HQ),
 9234: (9756, lnames[9234], ('cls', 'ss', 'l', 'm', 14, 0, 14, 14, 1, 5, 1, 5, 0, 19), 'm', 0, NPC_HQ),
 9235: (9756, lnames[9235], ('dll', 'ls', 'l', 'm', 6, 0, 6, 6, 1, 6, 1, 6, 0, 16), 'm', 0, NPC_HQ),
 9236: (9756, lnames[9236], ('dss', 'ms', 'l', 'm', 20, 0, 20, 20, 0, 6, 0, 6, 0, 13), 'm', 0, NPC_HQ),
 9237: (9255, lnames[9237], ('dls', 'ss', 'l', 'm', 14, 0, 14, 14, 0, 7, 0, 7, 0, 10), 'm', 0, NPC_FISHERMAN),
 9301: (9329, lnames[9301], 'r', 'm', 0, NPC_FISHERMAN),
 9302: (9802, lnames[9302], ('dss', 'ld', 'l', 'f', 17, 0, 17, 17, 5, 21, 5, 21, 8, 26), 'f', 0, NPC_REGULAR),
 9303: (9826, lnames[9303], 'r', 'm', 0, NPC_REGULAR),
 9304: (9804, lnames[9304], ('dss', 'ls', 's', 'm', 16, 0, 16, 16, 14, 10, 10, 10, 3, 19), 'm', 0, NPC_REGULAR),
 9305: (9829, lnames[9305], 'r', 'm', 0, NPC_HQ),
 9306: (9829, lnames[9306], 'r', 'm', 0, NPC_HQ),
 9307: (9829, lnames[9307], 'r', 'f', 0, NPC_HQ),
 9308: (9829, lnames[9308], 'r', 'f', 0, NPC_HQ),
 9309: (9808, lnames[9309], ('css', 'ms', 'm', 'm', 26, 0, 26, 26, 8, 4, 8, 4, 7, 4), 'm', 0, NPC_REGULAR),
 9310: (9820, lnames[9310], 'r', 'm', 0, NPC_REGULAR),
 9311: (9809, lnames[9311], ('dls', 'ls', 'm', 'm', 24, 0, 18, 18, 11, 7, 0, 7, 1, 11), 'm', 0, NPC_REGULAR),
 9312: (9828, lnames[9312], 'r', 'f', 0, NPC_REGULAR),
 9313: (9827, lnames[9313], 'r', 'm', 0, NPC_REGULAR),
 9314: (9812, lnames[9314], 'r', 'm', 0, NPC_REGULAR),
 9315: (9813, lnames[9315], 'r', 'f', 0, NPC_REGULAR),
 9316: (9814, lnames[9316], 'r', 'f', 0, NPC_REGULAR),
 9317: (9815, lnames[9317], ('css', 'md', 's', 'f', 22, 0, 22, 22, 7, 4, 7, 4, 8, 11), 'f', 0, NPC_REGULAR),
 9318: (9816, lnames[9318], 'r', 'm', 0, NPC_REGULAR),
 9319: (9817, lnames[9319], ('css', 'ls', 'm', 'm', 26, 0, 26, 26, 5, 11, 5, 11, 5, 11), 'm', 0, NPC_REGULAR),
 9320: (9819, lnames[9320], 'r', 'm', 0, NPC_REGULAR),
 9321: (9824, lnames[9321], ('dss', 'ms', 'm', 'm', 2, 0, 2, 2, 4, 1, 4, 1, 2, 16), 'm', 0, NPC_REGULAR),
 9322: (9821, lnames[9322], ('dss', 'ms', 'm', 'm', 15, 0, 15, 15, 5, 6, 5, 6, 7, 9), 'f', 0, NPC_REGULAR),
 9323: (9822, lnames[9323], ('css', 'ms', 's', 'm', 31, 0, 31, 31, 8, 2, 8, 2, 5, 11), 'm', 0, NPC_REGULAR),
 9324: (9806, lnames[9324], ('fss', 'ls', 'l', 'm', 16, 0, 16, 16, 2, 9, 2, 9, 7, 20), 'm', 0, NPC_REGULAR),
 7001: (-1, lnames[7001], ('bss', 'md', 'm', 'f', 25, 0, 25, 25, 6, 12, 0, 0, 0, 2), 'f', 0, NPC_REGULAR),
 7002: (-1, lnames[7002], ('sss', 'ms', 'l', 'm', 7, 0, 7, 7, 18, 11, 0, 0, 4, 3), 'm', 0, NPC_REGULAR),
 7003: (-1, lnames[7003], ('sss', 'md', 'm', 'f', 21, 0, 21, 21, 45, 0, 0, 0, 7, 6), 'f', 0, NPC_REGULAR),
 7004: (-1, lnames[7004], ('pss', 'ls', 'l', 'm', 16, 0, 16, 16, 27, 0, 0, 0, 7, 16), 'm', 0, NPC_REGULAR),
 7005: (-1, lnames[7005], ('pls', 'ld', 's', 'f', 5, 0, 5, 5, 25, 0, 0, 0, 10, 0), 'f', 0, NPC_REGULAR),
 7006: (-1, lnames[7006], ('bll', 'ms', 's', 'm', 18, 0, 18, 18, 15, 4, 0, 0, 9, 3), 'm', 0, NPC_REGULAR),
 7007: (-1, lnames[7007], ('pls', 'ls', 's', 'm', 11, 0, 11, 11, 46, 0, 0, 0, 5, 16), 'm', 0, NPC_REGULAR),
 7008: (-1, lnames[7008], ('bls', 'ld', 's', 'f', 23, 0, 23, 23, 15, 6, 0, 0, 0, 18), 'f', 0, NPC_REGULAR),
 7009: (-1, lnames[7009], ('sll', 'ss', 's', 'm', 1, 0, 1, 1, 1, 6, 0, 0, 0, 6), 'm', 0, NPC_REGULAR),
 7010: (-1, lnames[7010], ('rll', 'ms', 'm', 'm', 2, 0, 2, 2, 19, 10, 13, 10, 7, 14, 0), 'm', 0, NPC_REGULAR),
 7011: (-1, lnames[7011], ('fll', 'ls', 'm', 'm', 0, 0, 9, 0, 10, 10, 0, 10, 5, 27), 'm', 0, NPC_REGULAR),
 7012: (-1, lnames[7012], ('pss', 'ms', 'l', 'm', 20, 0, 20, 20, 26, 0, 0, 0, 15), 'm', 0, NPC_REGULAR),
 7013: (-1, lnames[7013], ('bsl', 'ms', 'm', 'f', 20, 0, 20, 20, 3, 4, 0, 0, 5, 18), 'f', 0, NPC_REGULAR),
 7014: (-1, lnames[7014], ('bll', 'ss', 's', 'm', 11, 0, 11, 11, 3, 6, 0, 0, 1, 2), 'm', 0, NPC_REGULAR),
 7015: (-1, lnames[7015], ('ssl', 'sd', 'l', 'f', 13, 0, 13, 13, 1, 2, 0, 0, 0, 10), 'f', 0, NPC_REGULAR),
 7016: (-1, lnames[7016], ('hll', 'ls', 'l', 'm', 8, 0, 8, 8, 1, 3, 0, 0, 1, 16), 'm', 0, NPC_REGULAR),
 7017: (-1, lnames[7017], ('dsl', 'ms', 's', 'm', 5, 0, 5, 5, 1, 0, 0, 0, 0, 4), 'm', 0, NPC_REGULAR),
 7018: (-1, lnames[7018], ('pls', 'ls', 's', 'f', 14, 0, 14, 14, 0, 11, 0, 0, 5, 9), 'f', 0, NPC_REGULAR),
 7019: (-1, lnames[7019], ('bsl', 'ls', 'l', 'm', 12, 0, 12, 12, 1, 10, 0, 0, 1, 13), 'm', 0, NPC_REGULAR),
 7020: (-1, lnames[7020], ('sss', 'ms', 'l', 'm', 2, 0, 2, 2, 0, 4, 0, 0, 0, 6), 'm', 0, NPC_REGULAR),
 7021: (-1, lnames[7021], ('fsl', 'ls', 'm', 'm', 17, 0, 17, 17, 4, 4, 0, 0, 0, 10), 'm', 0, NPC_REGULAR),
 7022: (-1, lnames[7022], ('mss', 'sd', 's', 'f', 24, 0, 24, 24, 3, 1, 0, 0, 0, 13), 'f', 0, NPC_REGULAR),
 7023: (-1, lnames[7023], ('pss', 'sd', 'l', 'f', 9, 0, 9, 9, 0, 8, 0, 0, 11, 0), 'f', 0, NPC_REGULAR),
 10001: (10000, lnames[10001], 'r', 'f', 0, NPC_LAFF_RESTOCK),
 10002: (-1, lnames[10002], ('sls', 'ss', 'm', 'm', 15, 0, 15, 15, 111, 27, 97, 27, 41, 27), 'm', 0, NPC_REGULAR),
 11001: (11000, lnames[11001], 'r', 'm', 0, NPC_LAFF_RESTOCK),
 12001: (12000, lnames[12001], 'r', 'm', 0, NPC_LAFF_RESTOCK),
 12002: (-1, lnames[12002], ('pls', 'ls', 'l', 'f', 3, 0, 3, 3, 111, 27, 97, 27, 45, 27), 'f', 0, NPC_REGULAR),
 13001: (13000, lnames[13001], 'r', 'f', 0, NPC_LAFF_RESTOCK),
 13002: (-1, lnames[13002], ('bss', 'ss', 'm', 'm', 19, 0, 19, 19, 0, 3, 0, 3, 1, 16), 'm', 0, NPC_REGULAR)
}

if config.GetBool('want-new-toonhall', 1):
    NPCToonDict[2001] = (2513, lnames[2001], ('dss', 'ms', 'm', 'm', 17, 0, 17, 17, 3, 3, 3, 3, 7, 2), 'm', 1, NPC_FLIPPYTOONHALL)
else:
    NPCToonDict[2001] = (2513, lnames[2001], ('dss', 'ms', 'm', 'm', 17, 0, 17, 17, 3, 3, 3, 3, 7, 2), 'm', 1, NPC_REGULAR)

BlockerPositions = {TTLocalizer.Flippy: (Point3(207.4, 18.81, -0.475), 90.0)}
LaffRestockPositions = {lnames[11001]: ((-27.0, -170.0, -19.6), 215.0),
                        lnames[12001]: ((361.9, -394.4, -23.5), 120.0),
                        lnames[13001]: ((143.7, -381.4, -68.4), 0.0),
                        lnames[10001]: ((135.0, 128.8, 0.025), -212.8)}
GlovePositions = {lnames[2021]: ((101, -14, 4), -305)}
del lnames
zone2NpcDict = {}

def generateZone2NpcDict():
    if zone2NpcDict:
        return

    for id, npcDesc in NPCToonDict.items():
        zoneId = npcDesc[0]
        if zoneId in zone2NpcDict:
            zone2NpcDict[zoneId].append(id)
        else:
            zone2NpcDict[zoneId] = [id]


def getNPCName(npcId):
    npc = NPCToonDict.get(npcId)
    return npc[1] if npc else None


def getNPCZone(npcId):
    npc = NPCToonDict.get(npcId)
    return npc[0] if npc else None


def getBuildingArticle(zoneId):
    return TTLocalizer.zone2TitleDict.get(zoneId, 'Toon Building')[1]


def getBuildingTitle(zoneId):
    return TTLocalizer.zone2TitleDict.get(zoneId, 'Toon Building')[0]



HQnpcFriends = {
 2001: (ToontownBattleGlobals.HEAL_TRACK, 5, ToontownGlobals.MaxHpLimit, 5),
 2132: (ToontownBattleGlobals.HEAL_TRACK, 5, 70, 4),
 2121: (ToontownBattleGlobals.HEAL_TRACK, 5, 45, 3),
 2011: (ToontownBattleGlobals.TRAP_TRACK, 4, 180, 5),
 3007: (ToontownBattleGlobals.TRAP_TRACK, 4, 70, 4),
 1001: (ToontownBattleGlobals.TRAP_TRACK, 4, 50, 3),
 3112: (ToontownBattleGlobals.LURE_TRACK, 5, 0, 5),
 1323: (ToontownBattleGlobals.LURE_TRACK, 5, 0, 3),
 2308: (ToontownBattleGlobals.LURE_TRACK, 5, 0, 3),
 4119: (ToontownBattleGlobals.SOUND_TRACK, 5, 80, 5),
 4219: (ToontownBattleGlobals.SOUND_TRACK, 5, 50, 4),
 4115: (ToontownBattleGlobals.SOUND_TRACK, 5, 40, 3),
 1116: (ToontownBattleGlobals.DROP_TRACK, 5, 170, 5),
 2311: (ToontownBattleGlobals.DROP_TRACK, 5, 100, 4),
 4140: (ToontownBattleGlobals.DROP_TRACK, 5, 60, 3),
 3137: (ToontownBattleGlobals.NPC_COGS_MISS, 0, 0, 4),
 4327: (ToontownBattleGlobals.NPC_COGS_MISS, 0, 0, 4),
 4230: (ToontownBattleGlobals.NPC_COGS_MISS, 0, 0, 4),
 3135: (ToontownBattleGlobals.NPC_TOONS_HIT, 0, 0, 4),
 2208: (ToontownBattleGlobals.NPC_TOONS_HIT, 0, 0, 4),
 5124: (ToontownBattleGlobals.NPC_TOONS_HIT, 0, 0, 4),
 2003: (ToontownBattleGlobals.NPC_RESTOCK_GAGS, -1, 0, 5),
 2126: (ToontownBattleGlobals.NPC_RESTOCK_GAGS, ToontownBattleGlobals.HEAL_TRACK, 0, 3),
 4007: (ToontownBattleGlobals.NPC_RESTOCK_GAGS, ToontownBattleGlobals.TRAP_TRACK, 0, 3),
 1315: (ToontownBattleGlobals.NPC_RESTOCK_GAGS, ToontownBattleGlobals.LURE_TRACK, 0, 3),
 5207: (ToontownBattleGlobals.NPC_RESTOCK_GAGS, ToontownBattleGlobals.SQUIRT_TRACK, 0, 3),
 3129: (ToontownBattleGlobals.NPC_RESTOCK_GAGS, ToontownBattleGlobals.THROW_TRACK, 0, 3),
 4125: (ToontownBattleGlobals.NPC_RESTOCK_GAGS, ToontownBattleGlobals.SOUND_TRACK, 0, 3),
 1329: (ToontownBattleGlobals.NPC_RESTOCK_GAGS, ToontownBattleGlobals.DROP_TRACK, 0, 3)
}

FOnpcFriends = {
 7012: (ToontownBattleGlobals.HEAL_TRACK, 3, 10, 0),
 7013: (ToontownBattleGlobals.HEAL_TRACK, 3, 20, 1),
 7014: (ToontownBattleGlobals.HEAL_TRACK, 3, 30, 2),
 7015: (ToontownBattleGlobals.DROP_TRACK, 1, 20, 0),
 7016: (ToontownBattleGlobals.DROP_TRACK, 2, 35, 1),
 7017: (ToontownBattleGlobals.DROP_TRACK, 3, 50, 2),
 7018: (ToontownBattleGlobals.SOUND_TRACK, 1, 10, 0),
 7019: (ToontownBattleGlobals.SOUND_TRACK, 3, 20, 1),
 7020: (ToontownBattleGlobals.SOUND_TRACK, 4, 30, 2),
 7021: (ToontownBattleGlobals.LURE_TRACK, 1, 0, 0),
 7022: (ToontownBattleGlobals.LURE_TRACK, 1, 0, 1),
 7023: (ToontownBattleGlobals.LURE_TRACK, 3, 0, 2)
}

disabledSosCards = ConfigVariableList('disable-sos-card')

for npcId in disabledSosCards:
    npcId = int(npcId)
    if npcId in HQnpcFriends:
        del HQnpcFriends[npcId]
    if npcId in FOnpcFriends:
        del FOnpcFriends[npcId]

npcFriends = dict(HQnpcFriends)
npcFriends.update(FOnpcFriends)

def getNPCName(npcId):
    if npcId in NPCToonDict:
        return NPCToonDict[npcId][1]

def npcFriendsMinMaxStars(minStars, maxStars):
    return [id for id in npcFriends.keys() if getNPCTrackLevelHpRarity(id)[3] >= minStars and getNPCTrackLevelHpRarity(id)[3] <= maxStars]

def getNPCTrack(npcId):
    if npcId in npcFriends:
        return npcFriends[npcId][0]

def getNPCTrackHp(npcId):
    if npcId in npcFriends:
        track, level, hp, rarity = npcFriends[npcId]
        return (track, hp)
    return (None, None)

def getNPCTrackLevelHp(npcId):
    if npcId in npcFriends:
        track, level, hp, rarity = npcFriends[npcId]
        return (track, level, hp)
    return (None, None, None)

def getNPCTrackLevelHpRarity(npcId):
    if npcId in npcFriends:
        return npcFriends[npcId]
    return (None, None, None, None)
