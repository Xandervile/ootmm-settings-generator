import zlib
import base64
import json
import random
import os

generator_dir = os.path.dirname(os.path.abspath(__file__))

with open("weights.json", "r") as read_file:
    data = json.load(read_file)

settings = data["GameplaySettings"]

MinMysterySettings = settings["MinimumSettingsAmount"]
MysteryCount = 0
HardCounter = 0

#HarderSettings get rolled first to allow limitations
HARDMODELIMIT = settings["HardModeLimit"]

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

    SongShuffle = random.choices(["songLocations", "anywhere"], settings["SongShuffle"][1])[0]
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

    GrassShuffle = random.choices([True, False], settings["GrassShuffle"][1])[0]
    if GrassShuffle == True:
        HardCounter += 1
        MysteryCount += 1

    PotShuffleWeight = [20, 80]
    PotShuffle = random.choices([True, False], settings["PotShuffle"][1])[0]
    if PotShuffle == True:
        HardCounter += 1
        MysteryCount += 1

    SilverRupeeShuffle = random.choices(["vanilla", "own Dungeon", "anywhere"], settings["SilverRupeeShuffle"][1])[0]

    SKeyShuffleWeight = settings["SmallKeyShuffle"][1]
    SKeyShuffle = random.choices([["removed", "ownDungeon"], ["removed", "removed"], ["ownDungeon", "ownDungeon"], ["anywhere", "anywhere"]], SKeyShuffleWeight)[0]
    smallKeyShuffleMm = SKeyShuffle[0]
    smallKeyShuffleOot = SKeyShuffle[1]
    if SKeyShuffle == ["anywhere", "anywhere"]:
        GerudoKey = "anywhere"
    else:
        GerudoKey = "vanilla"

    BKeyShuffleWeight = settings["BossKeyShuffle"][1]
    BKeyShuffle = random.choices(["removed", "ownDungeon", "anywhere"], BKeyShuffleWeight)[0]
    bossKeyShuffleMm = BKeyShuffle
    bossKeyShuffleOot = BKeyShuffle

    if SKeyShuffle != ["removed", "ownDungeon"] or BKeyShuffle != "removed" or SilverRupeeShuffle != "vanilla":
        MysteryCount += 1
        if (SKeyShuffle == ["anywhere", "anywhere"] and BKeyShuffle == "anywhere") or (SKeyShuffle == ["anywhere", "anywhere"] and SilverRupeeShuffle == "anywhere") or (BKeyShuffle == "anywhere" and SilverRupeeShuffle == "anywhere") or (SKeyShuffle == ["anywhere", "anywhere"] and SilverRupeeShuffle == "anywhere" and BKeyShuffle == "anywhere"):
            HardCounter += 1

    ProgressiveClockType = "separate"
    ClockShuffle = random.choices([True, False], settings["ClockShuffle"][1])[0]
    if ClockShuffle == True:
        HardCounter += 1
        MysteryCount += 1
        ProgressiveClockType = random.choices(["ascending", "descending", "separate"], settings["ProgressiveClockType"][1])[0]
        if ProgressiveClockType == "separate":
            StartingClock = \
            random.choices(["MM_CLOCK1", "MM_CLOCK2", "MM_CLOCK3", "MM_CLOCK4", "MM_CLOCK5", "MM_CLOCK6"],
                           settings["StartingClock"][1])[0]
            StartingItemList[StartingClock] = 1
            if StartingClock != "MM_CLOCK6":
                HintIndex = next((i for i, hint in enumerate(HintList) if hint == HintToInsertBefore), None)
                HintList.insert(HintIndex, {"type": "item",
                                            "amount": 1,
                                            "extra": 1,
                                            "item": "MM_CLOCK6"})

    BossSoulsWeight = settings["BossSoulsWeight"][1]
    if BKeyShuffle == "anywhere":
        BossSoulsWeight = settings["BossSoulsWeight"][2]
    SharedBossSoulShuffle = random.choices([True, False], BossSoulsWeight)[0]
    if SharedBossSoulShuffle == True:
        HardCounter += 1
        MysteryCount += 1

    FreestandingShuffle = random.choices([True, False], settings["FreestandingShuffle"][1])[0]
    WonderSpotShuffle = random.choices([True, False], settings["WonderSpotShuffle"][1])[0]

    if FreestandingShuffle != False or WonderSpotShuffle != False:
        MysteryCount += 1
        if FreestandingShuffle != False and WonderSpotShuffle != False:
            HardCounter += 1

    SwordShuffle = random.choices([True, False], settings["SwordShuffle"][1])[0]
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
    EntranceRandomizer = random.choices(["none", "Regions Only", "Overworld", "Interiors", "Full"], settings["WorldEntranceRandomizer"][1])[0]
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

    OwlWeight = settings["OwlShuffle"][1]
    if OverworldShuffle == "full":
      OwlWeight = settings["OwlShuffle"][2]
    OwlShuffle = random.choices([True, False], OwlWeight)[0]
    if OwlShuffle == True:
        MysteryCount += 1
        HardCounter += 1

    #Other Settings get Randomized here
    TownFairy = "vanilla"
    StrayFairyShuffle = random.choices(["removed","anywhere"], settings["StrayFairyShuffle"][1])[0]
    if StrayFairyShuffle != "removed":
        MysteryCount += 1
        TownFairy = "anywhere"
        
    DungeonEntranceShuffleWeight = settings["DungeonEntranceShuffle"][1]
    DungeonEntranceShuffle = random.choices([True, False], DungeonEntranceShuffleWeight)[0]
    erDungeons = "none"
    if DungeonEntranceShuffle == True:
        erDungeons = "full"
        MysteryCount += 1

    BossEntranceShuffle = random.choices(["none","full"],settings["BossEntranceShuffle"][1])[0]
    if BossEntranceShuffle == "full":
        MysteryCount += 1

    ScrubShuffle = False
    SharedShopShuffle = random.choices(["none", "full"],settings["ShopShuffle"][1])[0]
    if SharedShopShuffle != "none":
        ScrubShuffle = random.choices([True, False], settings["MerchantShuffle"][1])[0]
        MysteryCount += 1
        
    SharedCowShuffle = random.choices([True, False],settings["CowShuffle"][1])[0]
    if SharedCowShuffle == True:
        MysteryCount += 1

    SharedMQDungeons = random.choices(["vanilla", "mq", "random"],settings["MQDungeons"][1])[0]
    if SharedMQDungeons != "vanilla":
        MysteryCount += 1

    SharedCratesAndBarrels = random.choices([True, False], settings["CratesAndBarrelsShuffle"][1])[0]
    if SharedCratesAndBarrels == True:
        MysteryCount += 1

    SnowballShuffle = random.choices([True, False], settings["SnowballShuffle"][1])[0]
    if SnowballShuffle == True:
        MysteryCount += 1

    SkulltulaShuffle = random.choices(["none", "all"], settings["SkulltulaShuffle"][1])[0]
    if SkulltulaShuffle == "all":
        MysteryCount += 1

    GrottoShuffle = random.choices(["none", "full"], settings["GrottoShuffle"][1])[0]
    if GrottoShuffle == "full":
        MysteryCount += 1

    GerudoCardShuffle = random.choices(["starting", True, False], settings["GerudoCardShuffle"][1])[0]
    if GerudoCardShuffle == "starting":
        GerudoCardShuffle = True
        StartingItemList["OOT_GERUDO_CARD"] = 1
        MysteryCount += 1

    PriceShuffle = random.choices(["affordable", "vanilla", "weighted", "random"], settings["PriceShuffle"][1])[0]
    if PriceShuffle == "weighted" or PriceShuffle == "random":
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
"smallKeyShuffleHideout":GerudoKey,
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
"owlShuffle":OwlShuffle,
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
"shuffleMerchantsOot":ScrubShuffle,
"shuffleMerchantsMm":ScrubShuffle,
"shuffleMasterSword":SwordShuffle,
"shuffleGerudoCard":GerudoCardShuffle,
"priceOotShops":PriceShuffle,
"priceOotScrubs":PriceShuffle,
"priceMmShops":PriceShuffle,
"priceMmTingle":PriceShuffle,
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
"crossGameFw":OverworldShuffle == "full",
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

# Output the result
print("Encoded Seed String:")
print(seed_string)

with open("seed_output.txt", "w") as file:
    file.write("Seed String:\n")
    file.write("\n")
    file.write(seed_string)

with open("settings_output.txt", "w") as file:
    file.write("Settings Spoiler:\n")
    file.write("\n")
    for key, value in settings_data.items():
        file.write(f"{key}: {value}\n")
