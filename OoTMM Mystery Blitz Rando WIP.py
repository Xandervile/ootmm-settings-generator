import zlib
import base64
import json
import random

MinMysterySettings = 5
MysteryCount = 0
HardCounter = 0

#HarderSettings get rolled first to allow limitations
HARDMODELIMIT = 2

DefaultJunkList = ["MM Beneath The Graveyard Dampe Chest",
"MM Deku Playground Reward All Days",
"MM Goron Race Reward",
"MM Great Bay Great Fairy",
"MM Honey & Darling Reward All Days",
"MM Ikana Great Fairy",
"MM Laboratory Zora Song",
"MM Moon Fierce Deity Mask",
"MM Mountain Village Frog Choir HP",
"MM Ocean Spider House Wallet",
"MM Pinnacle Rock HP",
"MM Snowhead Great Fairy",
"MM Stock Pot Inn Couple\'s Mask",
"MM Swamp Spider House Mask of Truth",
"MM Town Archery Reward 2",
"MM Waterfall Rapids Beaver Race 2",
"MM Woodfall Great Fairy",
"OOT Skulltula House 40 Tokens",
"OOT Skulltula House 50 Tokens"]

DefaultStartingItemList= {"OOT_NUTS_10":2,
"OOT_SHIELD_DEKU":1,
"OOT_STICK":10,
"MM_SONG_EPONA":1,
"SHARED_SHIELD_HYLIAN":1,
"MM_OCARINA":1,
"OOT_OCARINA":1,
"MM_SWORD":1,
"MM_SONG_SOARING":1,
"MM_SONG_TIME":1}

DefaultHintList = [{"type":"foolish",
"amount":8,
"extra":1},
{"type":"always",
"amount":"max",
"extra":1},
{"type":"sometimes",
"amount":4,
"extra":1},
{"type":"item",
"amount":1,
"extra":1,
"item":"SHARED_SHIELD_MIRROR"},
{"type":"item",
"amount":1,
"extra":1,
"item":"MM_MASK_CAPTAIN"},
{"type":"item",
"amount":1,
"extra":1,
"item":"MM_POWDER_KEG"},
{"type":"item",
"amount":1,
"extra":1,
"item":"SHARED_ARROW_ICE"},
{"type":"playthrough",
"amount":1,
"extra":1},
{"type":"woth",
"amount":9,
"extra":1},
{"type":"sometimes",
"amount":"max",
"extra":1}]

HintToInsertBefore = {"type": "playthrough",
                      "amount": 1,
                      "extra": 1}

DefaultPlando = {"OOT Zora River Bean Seller":"OOT_MAGIC_BEAN",
"OOT Zelda\'s Letter":"OOT_OCARINA",
"OOT Zelda\'s Song":"OOT_SONG_TP_LIGHT",
"MM Initial Song of Healing":"SHARED_RECOVERY_HEART"}

while MysteryCount < MinMysterySettings or HardCounter > HARDMODELIMIT:
    MysteryCount = 0
    HardCounter = 0

    JunkList = DefaultJunkList.copy()
    StartingItemList = DefaultStartingItemList.copy()
    PlandoList = DefaultPlando.copy()
    HintList = DefaultHintList.copy()

    SongShuffle = random.choices(["songLocations", "anywhere"], [75, 25])[0]
    if SongShuffle == "anywhere":
        HardCounter += 1
        MysteryCount += 1
        StartingItemList.pop("MM_SONG_TIME")
        HintList = [hint for hint in HintList if hint.get("item") not in ["MM_MASK_CAPTAIN", "MM_POWDER_KEG", "SHARED_SHIELD_MIRROR"]]
        HintIndex = next((i for i, hint in enumerate(HintList) if hint == HintToInsertBefore), None)
        HintList.insert(HintIndex, {"type": "item",
                            "amount": 1,
                            "extra": 1,
                            "item": "OOT_SONG_ZELDA"})
        HintList.insert(HintIndex, {"type": "item",
                            "amount": 1,
                            "extra": 1,
                            "item": "SHARED_SONG_TIME"})
        HintList.insert(HintIndex, {"type": "item",
                            "amount": 1,
                            "extra": 1,
                            "item": "OOT_SONG_EPONA"})

    GrassShuffleWeight = [10, 90]
    GrassShuffle = random.choices([True, False], GrassShuffleWeight)[0]
    if GrassShuffle == True:
        HardCounter += 1
        MysteryCount += 1

    PotShuffleWeight = [20, 80]
    PotShuffle = random.choices([True, False], PotShuffleWeight)[0]
    if PotShuffle == True:
        HardCounter += 1
        MysteryCount += 1

    SilverRupeeShuffle = random.choices(["vanilla", "own Dungeon", "anywhere"], [70, 25, 5])[0]

    SKeyShuffleWeight = [50, 10, 30, 10]
    SKeyShuffle = random.choices([["removed", "ownDungeon"], ["removed", "removed"], ["ownDungeon", "ownDungeon"], ["anywhere", "anywhere"]], SKeyShuffleWeight)[0]
    smallKeyShuffleMm = SKeyShuffle[0]
    smallKeyShuffleOot = SKeyShuffle[1]

    BKeyShuffleWeight = [30, 60, 10]
    BKeyShuffle = random.choices(["removed", "ownDungeon", "anywhere"], BKeyShuffleWeight)[0]
    bossKeyShuffleMm = BKeyShuffle
    bossKeyShuffleOot = BKeyShuffle

    if SKeyShuffle != ["removed", "ownDungeon"] or BKeyShuffle != "removed" or SilverRupeeShuffle != "vanilla":
        MysteryCount += 1
        if (SKeyShuffle == ["anywhere", "anywhere"] and BKeyShuffle == "anywhere") or (SKeyShuffle == ["anywhere", "anywhere"] and SilverRupeeShuffle == "anywhere") or (BKeyShuffle == "anywhere" and SilverRupeeShuffle == "anywhere") or (SKeyShuffle == ["anywhere", "anywhere"] and SilverRupeeShuffle == "anywhere" and BKeyShuffle == "anywhere"):
            HardCounter += 1

    ProgressiveClockType = "separate"
    ClockShuffle = random.choices([True, False], [10, 90])[0]
    if ClockShuffle == True:
        HardCounter += 1
        MysteryCount += 1
        ProgressiveClockType = random.choices(["ascending", "descending", "separate"], [20, 30, 50])[0]
        if ProgressiveClockType == "separate":
            StartingClock = \
            random.choices(["MM_CLOCK1", "MM_CLOCK2", "MM_CLOCK3", "MM_CLOCK4", "MM_CLOCK5", "MM_CLOCK6"],
                           [10, 10, 10, 10, 10, 10])[0]
            StartingItemList[StartingClock] = 1
            if StartingClock != "MM_CLOCK6":
                HintIndex = next((i for i, hint in enumerate(HintList) if hint == HintToInsertBefore), None)
                HintList.insert(HintIndex, {"type": "item",
                                            "amount": 1,
                                            "extra": 1,
                                            "item": "MM_CLOCK6"})

    BossSoulsWeight = [10, 90]
    if BKeyShuffle == "anywhere":
        BossSoulsWeight[1] += BossSoulsWeight[0]
        BossSoulsWeight[0] = 0
    SharedBossSoulShuffle = random.choices([True, False], BossSoulsWeight)[0]
    if SharedBossSoulShuffle == True:
        HardCounter += 1
        MysteryCount += 1

    FreestandingShuffle = random.choices([True, False], [20, 80])[0]
    WonderSpotShuffle = random.choices([True, False], [20, 80])[0]

    if FreestandingShuffle != False or WonderSpotShuffle != False:
        MysteryCount += 1
        if FreestandingShuffle != False and WonderSpotShuffle != False:
            HardCounter += 1

    PotShuffle = random.choices([True, False], [15, 85])[0]
    if PotShuffle == True:
        MysteryCount += 1
        HardCounter += 1
        JunkList.append("MM Goron Race Reward")

    SwordShuffle = random.choices([True, False], [15, 85])[0]
    if SwordShuffle == True:
        MysteryCount += 1
        HardCounter += 1
        HintIndex = next((i for i, hint in enumerate(HintList) if hint == HintToInsertBefore), None)
        HintList.insert(HintIndex, {"type": "item",
                                    "amount": 1,
                                    "extra": 1,
                                    "item": "OOT_SWORD_MASTER"})
        StartingItemList.pop("MM_SWORD")
        StartingItemList.pop("SHARED_SHIELD_HYLIAN")

    RegionsShuffle = ["none", False]
    OverworldShuffle = "none"
    InteriorShuffle = ["none", False]
    EntranceRandomizer = random.choices(["none", "Regions Only", "Overworld", "Interiors", "Full"], [80, 10, 4, 4, 2])[0]
    if EntranceRandomizer == "Regions Only":
        RegionsShuffle = ["full", True]
        MysteryCount += 1
    elif EntranceRandomizer == "Overworld":
        OverworldShuffle = "full"
        MysteryCount += 1
        HardCounter += 1
    elif EntranceRandomizer == "Interiors":
        InteriorShuffle = ["full", True]
        MysteryCount += 1
        HardCounter += 1
    elif EntranceRandomizer == "Full":
        OverworldShuffle = "full"
        InteriorShuffle = ["full", True]
        MysteryCount += 1
        HardCounter += 1

    #Other Settings get Randomized here
    TownFairy = "vanilla"
    StrayFairyShuffle = random.choices(["removed","anywhere"], [80, 20])[0]
    if StrayFairyShuffle != "removed":
        MysteryCount += 1
        TownFairy = "anywhere"
        
    DungeonEntranceShuffleWeight = [20, 80]
    DungeonEntranceShuffle = random.choices([True, False], DungeonEntranceShuffleWeight)[0]
    erDungeons = "none"
    if DungeonEntranceShuffle == True:
        erDungeons = "full"
        MysteryCount += 1

    BossEntranceShuffle = random.choices(["none","full"],[80, 20])[0]
    if BossEntranceShuffle == "full":
        MysteryCount += 1

    ScrubShuffle = False
    SharedShopShuffle = random.choices(["none", "full"],[70, 30])[0]
    if SharedShopShuffle != "none":
        ScrubShuffle = True
        MysteryCount += 1
        
    SharedCowShuffle = random.choices([True, False],[20, 80])[0]
    if SharedCowShuffle == True:
        MysteryCount += 1

    SharedMQDungeons = random.choices(["vanilla", "mq", "random"],[70, 10, 20])[0]
    if SharedMQDungeons != "vanilla":
        MysteryCount += 1

    SharedCratesAndBarrels = random.choices([True, False], [10, 90])[0]
    if SharedCratesAndBarrels == True:
        MysteryCount += 1

    SnowballShuffle = random.choices([True, False], [20, 80])[0]
    if SnowballShuffle == True:
        MysteryCount += 1

    SkulltulaShuffle = random.choices(["none", "all"], [75, 25])[0]
    if SkulltulaShuffle == "all":
        MysteryCount += 1

    GrottoShuffle = random.choices(["none", "full"], [80, 20])[0]
    if GrottoShuffle == "full":
        MysteryCount += 1
        
        

# Rest of the settings are not stored already so are randomised here. To add: 
settings_data = {
"hintImportance":True,
"songs":SongShuffle,
"goldSkulltulaTokens":SkulltulaShuffle,
"housesSkulltulaTokens":SkulltulaShuffle,
"tingleShuffle":"starting",
"mapCompassShuffle":"starting",
"smallKeyShuffleOot":smallKeyShuffleOot,
"smallKeyShuffleMm":smallKeyShuffleMm,
"smallKeyShuffleHideout":"vanilla",
"bossKeyShuffleOot":bossKeyShuffleOot,
"bossKeyShuffleMm":bossKeyShuffleMm,
"silverRupeeShuffle":SilverRupeeShuffle,
"townFairyShuffle": TownFairy,
"strayFairyChestShuffle":"starting",
"strayFairyOtherShuffle":StrayFairyShuffle,
"scrubsShuffleOot":ScrubShuffle,
"scrubsShuffleMm":ScrubShuffle,
"cowShuffleOot":SharedCowShuffle,
"cowShuffleMm":SharedCowShuffle,
"shopShuffleOot":SharedShopShuffle,
"shopShuffleMm":SharedShopShuffle,
"shufflePotsOot":PotShuffle,
"shufflePotsMm":PotShuffle,
"shuffleCratesOot":SharedCratesAndBarrels,
"shuffleCratesMm":SharedCratesAndBarrels,
"shuffleBarrelsMm":SharedCratesAndBarrels,
"shuffleGrassOot":GrassShuffle,
"shuffleGrassMm":GrassShuffle,
"shuffleFreeRupeesOot":FreestandingShuffle,
"shuffleFreeRupeesMm":FreestandingShuffle,
"shuffleWonderItemsOot":WonderSpotShuffle,
"shuffleWonderItemsMm":WonderSpotShuffle,
"shuffleSnowballsMm":SnowballShuffle,
"shuffleMasterSword":SwordShuffle,
"shuffleGerudoCard":False,
"moonCrash":"cycle",
"startingAge":"random",
"swordlessAdult":True,
"timeTravelSword":True,
"doorOfTime":"open",
"ageChange":"always",
"dekuTree":"closed",
"clearStateDungeonsMm":"both",
"kakarikoGate":"open",
"gerudoFortress":"single",
"skipZelda":True,
"rainbowBridge":"custom",
"bossWarpPads":"remains",
"freeScarecrowOot":True,
"freeScarecrowMm":True,
"preCompletedDungeons":True,
"preCompletedDungeonsMajor":6,
"preCompletedDungeonsStones":2,
"preCompletedDungeonsMedallions":2,
"preCompletedDungeonsRemains":2,
"openMaskShop":True,
"mmPreActivatedOwls":{"type":"specific",
"values":["clocktown"]},
"crossAge":True,
"crossWarpOot":True,
"crossWarpMm":"full",
"csmcSkulltula":True,
"csmcCow":True,
"keepItemsReset":True,
"fastMasks":True,
"shadowFastBoat":True,
"progressiveGoronLullaby":"single",
"progressiveClocks":ProgressiveClockType,
"bottleContentShuffle":True,
"blueFireArrows":True,
"sunlightArrows":True,
"shortHookshotMm":True,
"bombchuBagOot":True,
"bombchuBagMm":True,
"spellFireMm":True,
"spellWindMm":True,
"spellLoveMm":True,
"bootsIronMm":True,
"bootsHoverMm":True,
"tunicGoronMm":True,
"tunicZoraMm":True,
"scalesMm":True,
"strengthMm":True,
"extraChildSwordsOot":SwordShuffle,
"blastMaskOot":True,
"stoneMaskOot":True,
"elegyOot":True,
"soulsBossOot":SharedBossSoulShuffle,
"soulsBossMm":SharedBossSoulShuffle,
"clocks":ClockShuffle,
"lenientSpikes":False,
"songOfDoubleTimeOot":True,
"sharedBows":True,
"sharedBombBags":True,
"sharedMagic":True,
"sharedMagicArrowFire":True,
"sharedMagicArrowIce":True,
"sharedMagicArrowLight":True,
"sharedSongStorms":True,
"sharedSongTime": SongShuffle == "anywhere",
"sharedHookshot":True,
"sharedLens":True,
"sharedMaskGoron":True,
"sharedMaskZora":True,
"sharedMaskBunny":True,
"sharedMaskKeaton":True,
"sharedMaskTruth":True,
"sharedMaskBlast":True,
"sharedMaskStone":True,
"sharedSongElegy":True,
"sharedWallets":True,
"sharedHealth":True,
"sharedSwords":SwordShuffle,
"sharedShields":True,
"sharedBombchuBags":True,
"sharedSpellFire":True,
"sharedSpellWind":True,
"sharedSpellLove":True,
"sharedBootsIron":True,
"sharedBootsHover":True,
"sharedTunicGoron":True,
"sharedTunicZora":True,
"sharedScales":True,
"sharedStrength":True,
"agelessChildTrade":True,
"erBoss":BossEntranceShuffle,
"erDungeons":erDungeons,
"erGrottos": GrottoShuffle,
"erMajorDungeons":DungeonEntranceShuffle,
"erMinorDungeons":DungeonEntranceShuffle,
"erSpiderHouses":DungeonEntranceShuffle,
"erPirateFortress":DungeonEntranceShuffle,
"erBeneathWell":DungeonEntranceShuffle,
"erIkanaCastle":DungeonEntranceShuffle,
"erSecretShrine":DungeonEntranceShuffle,
"erRegions": RegionsShuffle[0],
"erRegionsExtra": RegionsShuffle[1],
"erRegionsShortcuts": RegionsShuffle[1],
"erOverworld": OverworldShuffle,
"erIndoors": InteriorShuffle[0],
"erIndoorsMajor": InteriorShuffle[1],
"erIndoorsExtra": InteriorShuffle[1],
"startingItems":StartingItemList,
"junkLocations": JunkList,
"tricks":[
"MM_EVAN_FARORE",
"MM_LENS",
"MM_NO_SEAHORSE",
"MM_ONE_MASK_STONE_TOWER",
"MM_PALACE_BEAN_SKIP",
"MM_SOUTHERN_SWAMP_SCRUB_HP_GORON",
"MM_TUNICS",
"MM_ZORA_HALL_SCRUB_HP_NO_DEKU",
"OOT_DC_JUMP",
"OOT_DEAD_HAND_STICKS",
"OOT_FOREST_HOOK",
"OOT_HAMMER_WALLS",
"OOT_HIDDEN_GROTTOS",
"OOT_LENS",
"OOT_MAN_ON_ROOF",
"OOT_NIGHT_GS",
"OOT_TUNICS",
"OOT_VOLCANO_HOVERS",
"OOT_WINDMILL_HP_NOTHING"],
"dungeon":{
    "DT":SharedMQDungeons,
    "DC":SharedMQDungeons,
    "JJ":SharedMQDungeons,
    "Forest":SharedMQDungeons,
    "Fire":SharedMQDungeons,
    "Water":SharedMQDungeons,
    "Spirit":SharedMQDungeons,
    "Shadow":SharedMQDungeons,
    "BotW":SharedMQDungeons,
    "IC":SharedMQDungeons,
    "GTG":SharedMQDungeons,
    "Ganon":SharedMQDungeons},
"specialConds":{
    "BRIDGE":{
        "count":9,
        "stones":True,
        "medallions":True,
        "remains":False,
        "skullsGold":False,
        "skullsSwamp":False,
        "skullsOcean":False,
        "fairiesWF":False,
        "fairiesSH":False,
        "fairiesGB":False,
        "fairiesST":False,
        "fairyTown":False,
        "masksRegular":False,
        "masksTransform":False,
        "masksOot":False,
        "triforce":False,
        "coinsRed":False,
        "coinsGreen":False,
        "coinsBlue":False,
        "coinsYellow":False},
    "MOON":{
        "count":7,
        "stones":True,
        "medallions":False,
        "remains":True,
        "skullsGold":False,
        "skullsSwamp":False,
        "skullsOcean":False,
        "fairiesWF":False,
        "fairiesSH":False,
        "fairiesGB":False,
        "fairiesST":False,
        "fairyTown":False,
        "masksRegular":False,
        "masksTransform":False,
        "masksOot":False,
        "triforce":False,
        "coinsRed":False,
        "coinsGreen":False,
        "coinsBlue":False,
        "coinsYellow":False},
    "LACS":{
        "count":0,
        "stones":False,
        "medallions":False,
        "remains":False,
        "skullsGold":False,
        "skullsSwamp":False,
        "skullsOcean":False,
        "fairiesWF":False,
        "fairiesSH":False,
        "fairiesGB":False,
        "fairiesST":False,
        "fairyTown":False,
        "masksRegular":False,
        "masksTransform":False,
        "masksOot":False,
        "triforce":False,
        "coinsRed":False,
        "coinsGreen":False,
        "coinsBlue":False,
        "coinsYellow":False},
    "GANON_BK":{
        "count":0,
        "stones":False,
        "medallions":False,
        "remains":False,
        "skullsGold":False,
        "skullsSwamp":False,
        "skullsOcean":False,
        "fairiesWF":False,
        "fairiesSH":False,
        "fairiesGB":False,
        "fairiesST":False,
        "fairyTown":False,
        "masksRegular":False,
        "masksTransform":False,
        "masksOot":False,
        "triforce":False,
        "coinsRed":False,
        "coinsGreen":False,
        "coinsBlue":False,
        "coinsYellow":False},
    "MAJORA":{
        "count":0,
        "stones":False,
        "medallions":False,
        "remains":False,
        "skullsGold":False,
        "skullsSwamp":False,
        "skullsOcean":False,
        "fairiesWF":False,
        "fairiesSH":False,
        "fairiesGB":False,
        "fairiesST":False,
        "fairyTown":False,
        "masksRegular":False,
        "masksTransform":False,
        "masksOot":False,
        "triforce":False,
        "coinsRed":False,
        "coinsGreen":False,
        "coinsBlue":False,
        "coinsYellow":False}},
"plando":{"locations": PlandoList},
"hints": HintList
}

# Convert the settings into a JSON string (or similar format if required)
settings_json = json.dumps(settings_data)

# Compress the settings using zlib
compressed_data = zlib.compress(settings_json.encode())

# Base64 encode the compressed data
encoded_data = base64.urlsafe_b64encode(compressed_data).decode()

# Remove any unnecessary padding (optional, as the decoder will usually handle it)
encoded_data = encoded_data.rstrip("=")

# Format the final seed string (prepend 'v1.' to the encoded string)
seed_string = f"v1.{encoded_data}"

with open("seed_output.txt", "w") as file:
    file.write("Seed String:\n")
    file.write("\n")
    file.write(seed_string)

with open("settings_output.txt", "w") as file:
    file.write("Settings Spoiler:\n")
    file.write("\n")
    for key, value in settings_data.items():
        file.write(f"{key}: {value}\n")


#Decoding Part
#seed_string = "v1.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"
#seed_data = seed_string.split(".")[1]

# Add padding if necessary
#padding_needed = len(seed_data) % 4
#if padding_needed:
#    seed_data += "=" * (4 - padding_needed)

# Decode and decompress the seed
#decoded_data = zlib.decompress(base64.urlsafe_b64decode(seed_data))

# Output the decoded data
#print(decoded_data)

