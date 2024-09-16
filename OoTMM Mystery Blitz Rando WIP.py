import zlib
import base64
import json
import random

MinMysterySettings = 5
MysteryCount = 0
HardCounter = 99

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
"MM_SONG_SOARING":1}

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

HintToInsertBefore = {"type": "woth",
                      "amount": 4,
                      "extra": 1}

while MysteryCount < MinMysterySettings or HardCounter > HARDMODELIMIT:
    MysteryCount = 0
    HardCounter = 0

    JunkList = DefaultJunkList.copy()
    StartingItemList = DefaultStartingItemList.copy()
    HintList = DefaultHintList.copy()
    HintIndex = next((i for i, hint in enumerate(HintList) if hint == HintToInsertBefore), None)

    SongShuffle = random.choices(["songLocations", "anywhere"], [75, 25])[0]
    if SongShuffle == "anywhere":
        HardCounter += 1
        MysteryCount += 1

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

    ProgressiveClockType = "seperate"
    ClockShuffle = random.choices([True, False], [10, 90])[0]
    if ClockShuffle == True:
        HardCounter += 1
        MysteryCount += 1
        ProgressiveClockType = random.choices(["ascending", "descending", "seperate"], [20, 30, 50])[0]
        if ProgressiveClockType == "separate":
            StartingClock = \
            random.choices(["MM_CLOCK1", "MM_CLOCK2", "MM_CLOCK3", "MM_CLOCK4", "MM_CLOCK5", "MM_CLOCK6"],
                           [10, 10, 10, 10, 10, 10])[0]
            StartingItems[StartingClock] = 1
            if StartingClock != "MM_CLOCK6":
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

    SharedMQDungeons = random.choices(["vanilla", "mq", "random"],[75, 5, 20])[0]
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
"shuffleMasterSword":False,
"shuffleGerudoCard":False,
"startingAge":"random",
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
"plando":{"locations":{"OOT Zora River Bean Seller":"OOT_MAGIC_BEAN",
"OOT Zelda\'s Letter":"OOT_OCARINA",
"OOT Zelda\'s Song":"OOT_SONG_TP_LIGHT",
"MM Initial Song of Healing":"MM_SONG_TIME"}},
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

# Output the result
print("Encoded Seed String:")
print(seed_string)


#Decoding Part
#seed_string = "v1.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"
seed_data = seed_string.split(".")[1]

# Add padding if necessary
padding_needed = len(seed_data) % 4
if padding_needed:
    seed_data += "=" * (4 - padding_needed)

# Decode and decompress the seed
decoded_data = zlib.decompress(base64.urlsafe_b64decode(seed_data))

# Output the decoded data
print(decoded_data)



