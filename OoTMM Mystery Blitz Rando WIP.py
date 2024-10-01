import zlib
import base64
import json
import random
import os

generator_dir = os.path.dirname(os.path.abspath(__file__))

with open("weights.json", "r") as read_file:
    data = json.load(read_file)

basestring = data["SettingsString"]

base_data = basestring.split(".")[1]

padding_needed = len(base_data) % 4
if padding_needed:
    base_data += "=" * (4 - padding_needed)

decoded_data = zlib.decompress(base64.urlsafe_b64decode(base_data))

base_settings = json.loads(decoded_data)

settings = data["GameplaySettings"]

MinMysterySettings = settings["MinimumSettingsAmount"]
MaxMysterySettings = settings["MaximumSettingsAmount"]
MysteryCount = -1
HardCounter = 0

#HarderSettings get rolled first to allow limitations
HARDMODELIMIT = settings["HardModeLimit"]

DefaultJunkList = base_settings["junkLocations"]

DefaultStartingItemList = base_settings["startingItems"]

DefaultHintList = base_settings["hints"]

HintToInsertBefore = {"type":"woth",
                    "amount":9,
                    "extra":1}

DefaultPlando = base_settings["plando"]["locations"]

DefaultBridgeCond = base_settings["specialConds"]["BRIDGE"]

DefaultMoonCond = base_settings["specialConds"]["MOON"]

DefaultGanonBKCond = base_settings["specialConds"]["GANON_BK"]

DefaultMajoraCond = base_settings["specialConds"]["MAJORA"]

WinCond = random.choices(["Ganon and Majora", "Triforce Hunt", "Triforce Quest"], data["Goal"][1])[0]

while MysteryCount < MinMysterySettings or HardCounter > HARDMODELIMIT or MysteryCount > MaxMysterySettings:
    MysteryCount = 0
    HardCounter = 0

    SettingsList = base_settings.copy()

    if WinCond == "Triforce Hunt":
        SettingsList["goal"] = "triforce"
        SettingsList["triforceGoal"] = random.choices(data["TriforcePieces"][0], data["TriforcePieces"][1])[0]
        SettingsList["triforcePieces"] = int(1.5 * SettingsList["triforceGoal"])
    elif WinCond == "Triforce Quest":
        SettingsList["goal"] = "triforce3"
    
    JunkList = DefaultJunkList.copy()
    StartingItemList = DefaultStartingItemList.copy()
    PlandoList = DefaultPlando.copy()
    HintList = DefaultHintList.copy()
    BridgeCond = DefaultBridgeCond.copy()
    MoonCond = DefaultMoonCond.copy()
    GanonBKCond = DefaultGanonBKCond.copy()
    MajoraCond = DefaultMajoraCond.copy()

    if WinCond != "Ganon and Majora":
        BridgeCond["count"] = 3
        BridgeCond["medallions"] = True
        BridgeCond["stones"] = True
        BridgeCond["remains"] = True
        MoonCond["count"] = 0
        MoonCond["stones"] = False
        MoonCond["remains"] = False
        HintIndex = next((i for i, hint in enumerate(HintList) if hint == HintToInsertBefore), None)
        HintList.insert(HintIndex, {"type": "item",
                                    "amount": 1,
                                    "extra": 1,
                                    "item": "SHARED_ARROW_LIGHT"})

    SkipChildZelda = random.choices([True, False], settings["SkipChildZelda"][1])[0]
    if SkipChildZelda == False:
        SettingsList["skipZelda"] = False
        del PlandoList["OOT Zelda's Letter"]
        del PlandoList["OOT Zelda's Song"]
        StartingItemList["OOT_SONG_TP_LIGHT"] = 1
        StartingItemList["OOT_OCARINA"] = 1
        HintIndex = next((i for i, hint in enumerate(HintList) if hint == HintToInsertBefore), None)
        HintList.insert(HintIndex, {"type": "item",
                                    "amount": 1,
                                    "extra": 1,
                                    "item": "OOT_CHICKEN"})

    DoorOfTime = random.choices(["Closed", "Open"], settings["DoorOfTime"][1])[0]
    if DoorOfTime == "Closed":
        SettingsList["doorOfTime"] = "closed"
        
    SongShuffle = random.choices(["Song Locations", "Mixed with Owls", "Anywhere"], settings["SongShuffle"][1])[0]
    if SongShuffle == "Song Locations":
        SettingsList["songs"] = "songLocations"
    else:
        SettingsList["songs"] = "anywhere"
        MysteryCount += 1
        if SongShuffle == "Anywhere":
            HardCounter += 1
            SettingsList["sharedSongTime"] = True
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
        elif SongShuffle == "Mixed with Owls":
            SettingsList["owlShuffle"] = "anywhere"
            PlandoList["MM Clock Town Owl Statue"] = "MM_OWL_CLOCK_TOWN"
            SongAndOwlList = ["OOT_SONG_EPONA", "OOT_SONG_SARIA", "OOT_SONG_TIME", "OOT_SONG_SUN", "SHARED_SONG_STORMS", "OOT_SONG_ZELDA", "OOT_SONG_TP_FOREST", "OOT_SONG_TP_FIRE", "OOT_SONG_TP_WATER", "OOT_SONG_TP_SHADOW", "OOT_SONG_TP_SPIRIT", "MM_SONG_HEALING", "MM_SONG_AWAKENING", "MM_SONG_GORON", "MM_SONG_ZORA", "SHARED_SONG_EMPTINESS", "MM_SONG_ORDER", "MM_OWL_MILK_ROAD", "MM_OWL_SOUTHERN_SWAMP", "MM_OWL_WOODFALL", "MM_OWL_MOUNTAIN_VILLAGE", "MM_OWL_SNOWHEAD", "MM_OWL_GREAT_BAY", "MM_OWL_ZORA_CAPE", "MM_OWL_IKANA_CANYON", "MM_OWL_STONE_TOWER", "SHARED_RECOVERY_HEART", "SHARED_RECOVERY_HEART"]
            SongAndOwlLocation = ["OOT Lon Lon Ranch Malon Song", "OOT Saria's Song", "OOT Graveyard Royal Tomb Song", "OOT Hyrule Field Song of Time", "OOT Windmill Song of Storms", "OOT Sacred Meadow Sheik Song", "OOT Death Mountain Crater Sheik Song", "OOT Ice Cavern Sheik Song", "OOT Kakariko Song Shadow", "OOT Desert Colossus Song Spirit", "OOT Temple of Time Sheik Song", "MM Clock Tower Roof Skull Kid Song of Time", "MM Romani Ranch Epona Song", "MM Southern Swamp Song of Soaring", "MM Beneath The Graveyard Song of Storms", "MM Deku Palace Sonata of Awakening", "MM Goron Elder", "MM Ancient Castle of Ikana Song Emptiness", "MM Oath to Order", "MM Milk Road Owl Statue", "MM Southern Swamp Owl Statue", "MM Woodfall Owl Statue", "MM Mountain Village Owl Statue", "MM Snowhead Owl Statue", "MM Great Bay Coast Owl Statue", "MM Zora Cape Owl Statue", "MM Ikana Canyon Owl Statue", "MM Stone Tower Owl Statue"]
            if SkipChildZelda == False:
                SongAndOwlList.append("SHARED_RECOVERY_HEART")
                SongAndOwlLocation.append("OOT Zelda's Song")
            for key in SongAndOwlLocation:
                ChosenItem = random.choice(SongAndOwlList)
                PlandoList[key] = ChosenItem
                SongAndOwlList.remove(ChosenItem)


    EntranceRandomizer = random.choices(["none", "Regions Only", "Overworld", "Interiors", "Full"], settings["WorldEntranceRandomizer"][1])[0]
    if EntranceRandomizer == "Regions Only":
        SettingsList["erRegions"] = "full"
        SettingsList["erRegionsExtra"] = True
        RegionsShuffle = ["full", True]
        MysteryCount += 1
    elif EntranceRandomizer == "Overworld":
        SettingsList["erOverworld"] = "full"
        MysteryCount += 1
        HardCounter += 1
    elif EntranceRandomizer == "Interiors":
        SettingsList["erIndoors"] = "full"
        SettingsList["erIndoorsMajor"] = True
        SettingsList["erIndoorsExtra"] = True
        MysteryCount += 1
        HardCounter += 1
    elif EntranceRandomizer == "Full":
        SettingsList["erOverworld"] = "full"
        SettingsList["erIndoors"] = "full"
        SettingsList["erIndoorsMajor"] = True
        SettingsList["erIndoorsExtra"] = True
        MysteryCount += 1
        HardCounter += 1

    SettingsList["erGrottos"] = random.choices(["none", "full"], settings["GrottoShuffle"][1])[0]
    if SettingsList["erGrottos"] == "full":
        MysteryCount += 1

    OcarinaButtonWeight = settings["OcarinaButtons"][1]
    if SongShuffle == "anywhere":
        OcarinaButtonWeight = settings["OcarinaButtons"][2]
    OcarinaButtonShuffle = random.choices([True, False], OcarinaButtonWeight)[0]
    if OcarinaButtonShuffle == True:
        SettingsList["ocarinaButtonsShuffleOot"] = True
        SettingsList["ocarinaButtonsShuffleMm"] = True
        SettingsList["sharedOcarinaButtons"] = True
        HardCounter += 1
        MysteryCount += 1

##    GrassShuffle = random.choices(["none", "dungeons", "overworld", "all"], settings["GrassShuffle"][1])[0]
##    SettingsList["shuffleGrassOot"] = GrassShuffle
##    SettingsList["shuffleGrassMm"] = GrassShuffle
##    if GrassShuffle != "none":
##        MysteryCount += 1
##    if GrassShuffle == "overworld" or GrassShuffle == "all":
##        if EntranceRandomizer == "Overworld" or EntranceRandomizer == "Full":
##            SettingsList["shuffleTFGrassMm"] = True
##        else:
##            SettingsList["shuffleTFGrassMm"] = settings["TFGrassAllowed"][0]
##            if SettingsList["shuffleTFGrassMm"] == True:
##                for i in range(1, 19):                      #Limits Termina Field Grass to only 1 potential patch good
##                    GrassAllowed = random.sample(range(1, 13), settings["TFGrassAllowed"][1])
##                    for j in range(1, 13):
##                        if j not in GrassAllowed:
##                            JunkList.append(f"MM Termina Field Grass Pack {i:02} Grass {j:02}")
##    if GrassShuffle == "all":
##        HardCounter += 1  #Looking into limiting


    GrassShuffle = random.choices(["none", "dungeons", "overworld", "all"], settings["GrassShuffle"][1])[0]
    SettingsList["shuffleGrassOot"] = GrassShuffle
    SettingsList["shuffleGrassMm"] = GrassShuffle
    if GrassShuffle != "none":
        MysteryCount += 1
    if GrassShuffle == "overworld" or GrassShuffle == "all":
        TFGrassShuffle = settings["TFGrassAllowed"][0]
        if EntranceRandomizer == "Overworld" or EntranceRandomizer == "Full":
            GrassCount = 12
        elif TFGrassShuffle == True:
            GrassCount = settings["TFGrassAllowed"][1]
        else:
            GrassCount = 0
        for i in range(1, 19):                      #Limits Termina Field Grass to only 1 potential patch good
            GrassAllowed = random.sample(range(1, 13), GrassCount)
            for j in range(1, 13):
                if j not in GrassAllowed:
                    JunkList.append(f"MM Termina Field Grass Pack {i:02} Grass {j:02}")
    if GrassShuffle == "all":
        HardCounter += 1  #Looking into limiting


    PotShuffle = random.choices(["none", "dungeons", "overworld", "all"], settings["PotShuffle"][1])[0]
    SettingsList["shufflePotsOot"] = PotShuffle
    SettingsList["shufflePotsMm"] = PotShuffle
    if PotShuffle != "none":
        MysteryCount += 1
        if PotShuffle == "all":
            HardCounter += 1

    SettingsList["silverRupeeShuffle"] = random.choices(["vanilla", "ownDungeon", "anywhere"], settings["SilverRupeeShuffle"][1])[0]

    SKeyShuffleWeight = settings["SmallKeyShuffle"][1]
    SKeyShuffle = random.choices([["removed", "ownDungeon"], ["removed", "removed"], ["ownDungeon", "ownDungeon"], ["anywhere", "anywhere"]], SKeyShuffleWeight)[0]
    SettingsList["smallKeyShuffleMm"] = SKeyShuffle[0]
    SettingsList["smallKeyShuffleOot"] = SKeyShuffle[1]
    if SKeyShuffle == ["anywhere", "anywhere"]:
        SettingsList["smallKeyShuffleHideout"] = "anywhere"
        SettingsList["smallKeyShuffleChestGame"] = "anywhere"
    else:
        SettingsList["smallKeyShuffleHideout"] = "vanilla"

    BKeyShuffleWeight = settings["BossKeyShuffle"][1]
    BKeyShuffle = random.choices(["removed", "ownDungeon", "anywhere"], BKeyShuffleWeight)[0]
    SettingsList["bossKeyShuffleMm"] = BKeyShuffle
    SettingsList["bossKeyShuffleOot"] = BKeyShuffle

    if SKeyShuffle[0] != "removed" or BKeyShuffle != "removed" or SettingsList["silverRupeeShuffle"] != "vanilla":
        MysteryCount += 1
        if (SKeyShuffle == ["anywhere", "anywhere"] and BKeyShuffle == "anywhere") or (SKeyShuffle == ["anywhere", "anywhere"] and SettingsList["silverRupeeShuffle"] == "anywhere") or (BKeyShuffle == "anywhere" and SettingsList["silverRupeeShuffle"] == "anywhere"):
            HardCounter += 1
        if SKeyShuffle == ["anywhere", "anywhere"] and BKeyShuffle == "anywhere" and SettingsList["silverRupeeShuffle"] == "anywhere":
            SettingsList["skeletonKeyOot"] = True
            SettingsList["skeletonKeyMm"] = True
            SettingsList["sharedSkeletonKey"] = True
            SettingsList["magicalRupee"] = True

    if SKeyShuffle!= ["anywhere", "anywhere"]:
        TCGKeyShuffle = random.choices(["vanilla", "ownDungeon", "anywhere"], settings["TCGKeySettings"][1])[0]
        SettingsList["smallKeyShuffleChestGame"] = TCGKeyShuffle

    SettingsList["clocks"] = random.choices([True, False], settings["ClockShuffle"][1])[0]
    if SettingsList["clocks"] == True:
        HardCounter += 1
        MysteryCount += 1
        SettingsList["progressiveClocks"] = random.choices(["ascending", "descending", "separate"], settings["ProgressiveClockType"][1])[0]
        if SettingsList["progressiveClocks"] == "separate":
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
        SettingsList["soulsBossOot"] = True
        SettingsList["soulsBossMm"] = True
        HardCounter += 1
        MysteryCount += 1

    FreestandingShuffle = random.choices(["none", "dungeons", "overworld", "all"], settings["FreestandingShuffle"][1])[0]
    SettingsList["shuffleFreeRupeesOot"] = FreestandingShuffle
    SettingsList["shuffleFreeRupeesMm"] = FreestandingShuffle
    SettingsList["shuffleFreeHeartsOot"] = FreestandingShuffle
    if FreestandingShuffle == "dungeons" or FreestandingShuffle == "all":
        SettingsList["shuffleFreeHeartsMm"] = True
    else:
        SettingsList["shuffleFreeHeartsMm"] = False
    WonderSpotShuffle = random.choices(["none", "dungeons", "overworld", "all"], settings["WonderSpotShuffle"][1])[0]
    SettingsList["shuffleWonderItemsOot"] = WonderSpotShuffle
    if SettingsList["shuffleWonderItemsOot"] != "none":
        SettingsList["shuffleWonderItemsMm"] = True
    else:
        SettingsList["shuffleWonderItemsMm"] = False

    if FreestandingShuffle != "none" or WonderSpotShuffle != "none":
        MysteryCount += 1
        if FreestandingShuffle == "all" and WonderSpotShuffle == "all":
            HardCounter += 1

    SwordShuffle = random.choices([True, False], settings["SwordShuffle"][1])[0]
    if SwordShuffle == True:
        SettingsList["shuffleMasterSword"] = True
        SettingsList["extraChildSwordsOot"] = True
        if DoorOfTime == "Closed":
            SettingsList["timeTravelSword"] = random.choices([True, False], settings["TimeTravelSword"][2])[0]
        else:
            SettingsList["timeTravelSword"] = random.choices([True, False], settings["TimeTravelSword"][1])[0]
        SettingsList["sharedSwords"] = True
        MysteryCount += 1
        HardCounter += 1
        HintIndex = next((i for i, hint in enumerate(HintList) if hint == HintToInsertBefore), None)
        HintList.insert(HintIndex, {"type": "item",
                                    "amount": 1,
                                    "extra": 1,
                                    "item": "OOT_SWORD_MASTER"})
        StartingItemList.pop("MM_SWORD")
        StartingItemList.pop("SHARED_SHIELD_HYLIAN")

    OwlWeight = settings["OwlShuffle"][1]
    if "erOverworld" in SettingsList and SettingsList["erOverworld"] == "full":
        OwlWeight = settings["OwlShuffle"][2]
    if SongShuffle == "Mixed with Owls":
        OwlWeight = [0, 100]
    OwlShuffle = random.choices(["anywhere", "none"], OwlWeight)[0]
    if OwlShuffle == "anywhere":
        SettingsList["owlShuffle"] = "anywhere"
        PlandoList["MM Clock Town Owl Statue"] = "MM_OWL_CLOCK_TOWN"
        MysteryCount += 1
        HardCounter += 1

    #Other Settings get Randomized here
    SettingsList["townFairyShuffle"] = "vanilla"
    SettingsList["strayFairyOtherShuffle"] = random.choices(["removed","anywhere"], settings["StrayFairyShuffle"][1])[0]
    if SettingsList["strayFairyOtherShuffle"] != "removed":
        MysteryCount += 1
        SettingsList["townFairyShuffle"] = "anywhere"
        
    DungeonEntranceShuffleWeight = settings["DungeonEntranceShuffle"][1]
    DungeonEntranceShuffle = random.choices([True, False], DungeonEntranceShuffleWeight)[0]
    if DungeonEntranceShuffle == True:
        SettingsList["erDungeons"] = "full"
        SettingsList["erMajorDungeons"] = True
        SettingsList["erMinorDungeons"] = True
        SettingsList["erSpiderHouses"] = True
        SettingsList["erPirateFortress"] = True
        SettingsList["erBeneathWell"] = True
        SettingsList["erIkanaCastle"] = True
        SettingsList["erSecretShrine"] = True
        SettingsList["openDungeonsOot"] ={"type":"specific","values":["dekuTreeAdult","wellAdult","fireChild"]}
        MysteryCount += 1
        GanonCastleShuffle = random.choices([True, False], settings["GanonCastleShuffle"][1])[0]
        SettingsList["erGanonCastle"] = GanonCastleShuffle
        GanonTowerShuffle = random.choices([True, False], settings["GanonTowerShuffle"][1])[0]
        SettingsList["erGanonTower"] = GanonTowerShuffle
        if GanonCastleShuffle == True or GanonTowerShuffle == True:
            SettingsList["rainbowBridge"] = "open"
            SettingsList["ganonBossKey"] = "custom"
            GanonBKCond = BridgeCond
            BridgeCond["count"] = 0
            BridgeCond["stones"] = False
            BridgeCond["medallions"] = False
            BridgeCond["remains"] = False
        ClockTowerShuffle = random.choices([True, False], settings["ClockTowerShuffle"][1])[0]
        if ClockTowerShuffle == True:
            SettingsList["erMoon"] = True

    SettingsList["erBoss"] = random.choices(["none","full"],settings["BossEntranceShuffle"][1])[0]
    if SettingsList["erBoss"] == "full":
        MysteryCount += 1

    SharedShopShuffle = random.choices(["none", "full"],settings["ShopShuffle"][1])[0]
    if SharedShopShuffle != "none":
        SettingsList["shopShuffleOot"] = "full"
        SettingsList["shopShuffleMm"] = "full"
        ScrubShuffle = random.choices([True, False], settings["MerchantShuffle"][1])[0]
        SettingsList["scrubsShuffleOot"] = ScrubShuffle
        SettingsList["scrubsShuffleMm"] = ScrubShuffle
        SettingsList["shuffleMerchantsOot"] = ScrubShuffle
        SettingsList["shuffleMerchantsMm"] = ScrubShuffle
        PriceShuffle = random.choices(["affordable", "vanilla", "weighted", "random"], settings["PriceShuffle"][1])[0]
        SettingsList["priceOotShops"] = PriceShuffle
        SettingsList["priceMmShops"] = PriceShuffle
        SettingsList["priceMmTingle"] = PriceShuffle
        SettingsList["priceOotScrubs"] = PriceShuffle
        SettingsList["fillWallets"] = True
        if PriceShuffle == "weighted" or PriceShuffle == "random":
            MaxWalletSize = random.choices(["Giant", "Colossal", "Bottomless"], settings["MaxWalletSize"][1])[0]
            if MaxWalletSize != "Giant":
                SettingsList["rupeeScaling"] = True
                SettingsList["colossalWallets"] = True
                if MaxWalletSize == "Bottomless":
                    SettingsList["bottomlessWallets"] = True

        MysteryCount += 1
        
    SharedCowShuffle = random.choices([True, False],settings["CowShuffle"][1])[0]
    if SharedCowShuffle == True:
        SettingsList["cowShuffleOot"] = True
        SettingsList["cowShuffleMm"] = True
        MysteryCount += 1

    SharedMQDungeons = random.choices(settings["MQDungeonAmount"][0],settings["MQDungeonAmount"][1])[0]
    if SharedMQDungeons > 0:
        SettingsList["dungeon"] = {}
        DungeonList = ["DT", "DC", "JJ", "Forest", "Fire", "Water", "Spirit", "Shadow", "BotW", "IC", "GTG", "Ganon"]
        MQDungeonChosen = random.sample(DungeonList, SharedMQDungeons)
        for key in DungeonList:
            if key in MQDungeonChosen:
                SettingsList["dungeon"][key] = "mq"
            else:
                SettingsList["dungeon"][key] = "vanilla"

    SharedCratesAndBarrels = random.choices(["none", "dungeons", "overworld", "all"], settings["CratesAndBarrelsShuffle"][1])[0]
    SettingsList["shuffleCratesOot"] = SharedCratesAndBarrels
    SettingsList["shuffleCratesMm"] = SharedCratesAndBarrels
    if SharedCratesAndBarrels == "dungeons" or SharedCratesAndBarrels == "all":
        SettingsList["shuffleBarrelsMm"] = "all"
    else:
        SettingsList["shuffleBarrelsMm"] = "none"
    if SharedCratesAndBarrels != "none":
        MysteryCount += 1

    SharedHiveShuffle = random.choices([True, False], settings["HiveShuffle"][1])[0]
    if SharedHiveShuffle == True:
        SettingsList["shuffleHivesOot"] = True
        SettingsList["shuffleHivesMm"] = True
        MysteryCount += 1

    SettingsList["shuffleSnowballsMm"] = random.choices(["none", "dungeons", "overworld", "all"], settings["SnowballShuffle"][1])[0]
    if SettingsList["shuffleSnowballsMm"] != "none":
        MysteryCount += 1

    OoTSkulltulaWeights = settings["OoTSkulltulaShuffle"][1]
    if DungeonEntranceShuffle == True:
        OoTSkulltulaWeights = settings["OoTSkulltulaShuffle"][2]
    SettingsList["goldSkulltulaTokens"] = random.choices(["none", "dungeons", "overworld", "all"], OoTSkulltulaWeights)[0]
    MMSkulltulaWeights = settings["MMSkulltulaShuffle"][1]
    if DungeonEntranceShuffle == True:
        MMSkulltulaWeights = settings["MMSkulltulaShuffle"][2]
    SettingsList["housesSkulltulaTokens"] = random.choices(["none", "cross", "all"], MMSkulltulaWeights)[0]
    if SettingsList["goldSkulltulaTokens"] != "none" or SettingsList["housesSkulltulaTokens"] != "none":
        MysteryCount += 1
    if SettingsList["housesSkulltulaTokens"] == "cross":
        JunkList.remove("OOT Skulltula House 40 Tokens")
        JunkList.remove("OOT Skulltula House 50 Tokens")

    SoulShuffle = random.choices(["None", "Enemy", "NPC", "Full"], settings["SoulShuffle"][1])[0]
    if SoulShuffle != "None":
        MysteryCount += 1
        HardCounter += 1
        if SoulShuffle == "Enemy" or SoulShuffle == "Full":
            SettingsList["soulsEnemyOot"] = True
            SettingsList["soulsEnemyMm"] = True
            SettingsList["sharedSoulsEnemy"] = True
            HintIndex = next((i for i, hint in enumerate(HintList) if hint == HintToInsertBefore), None)
            HintList.insert(HintIndex, {"type": "item",
                                        "amount": 1,
                                        "extra": 1,
                                        "item": "SHARED_SOUL_MISC_GS"})
            HintList.insert(HintIndex, {"type": "item",
                                        "amount": 1,
                                        "extra": 1,
                                        "item": "SHARED_SOUL_ENEMY_LIZALFOS_DINALFOS"})
            HintList.insert(HintIndex, {"type": "item",
                                        "amount": 1,
                                        "extra": 1,
                                        "item": "SHARED_SOUL_ENEMY_KEESE"})
            HintList.insert(HintIndex, {"type": "item",
                                        "amount": 1,
                                        "extra": 1,
                                        "item": "SHARED_SOUL_ENEMY_IRON_KNUCKLE"})
            HintList.insert(HintIndex, {"type": "item",
                                        "amount": 1,
                                        "extra": 1,
                                        "item": "OOT_SOUL_ENEMY_STALFOS"})
        if SoulShuffle == "NPC" or SoulShuffle == "Full":
            SettingsList["soulsNpcOot"] = True
            SettingsList["soulsNpcMm"] = True
            SettingsList["sharedSoulsNpc"] = True
            HintIndex = next((i for i, hint in enumerate(HintList) if hint == HintToInsertBefore), None)
            HintList.insert(HintIndex, {"type": "item",
                                        "amount": 1,
                                        "extra": 1,
                                        "item": "OOT_SOUL_NPC_ZELDA"})
            HintList.insert(HintIndex, {"type": "item",
                                        "amount": 1,
                                        "extra": 1,
                                        "item": "MM_SOUL_NPC_MOON_CHILDREN"})

    FairyFountainShuffle = random.choices([True, False], settings["FairyFountainShuffle"][1])[0]
    if FairyFountainShuffle == True:
        SettingsList["fairyFountainFairyShuffleOot"] = True
        SettingsList["fairyFountainFairyShuffleMm"] = True
        SettingsList["fairySpotShuffleOot"] = True
        MysteryCount += 1

    FishingPondShuffle = random.choices([True, False], settings["FishingPondShuffle"][1])[0]
    if FishingPondShuffle == True:
        SettingsList["pondFishShuffle"] = True
        JunkList.append("OOT Fishing Pond Adult Loach")
        JunkList.append("OOT Fishing Pond Child Loach 1")
        JunkList.append("OOT Fishing Pond Child Loach 2")
        MysteryCount += 1

    DivingGameShuffle = random.choices([True, False], settings["DivingGameShuffle"][1])[0]
    if DivingGameShuffle == True:
        SettingsList["divingGameRupeeShuffle"] = True
        JunkList.append("OOT Zora Domain Diving Game Huge Rupee")

    GerudoCardShuffle = random.choices(["Starting", True, False], settings["GerudoCardShuffle"][1])[0]
    if GerudoCardShuffle != False:
        SettingsList["shuffleGerudoCard"] = True
        if GerudoCardShuffle == "Starting":
            StartingItemList["OOT_GERUDO_CARD"] = 1

    SettingsList["erSpawns"] = random.choices(["none", "child", "adult", "both"], settings["SpawnShuffle"][1])[0]

    WellWeight = settings["GibdoSettings"][1]
    if DungeonEntranceShuffle == True or EntranceRandomizer == "Overworld" or EntranceRandomizer == "Full":
        WellWeight = settings["GibdoSettings"][2]
    SettingsList["beneathWell"] = random.choices(["vanilla", "remorseless", "open"], WellWeight)[0]

    OpenDungeonsWeight = settings["OpenDungeons"][1]
    if DungeonEntranceShuffle == True:
        OpenDungeonsWeight = settings["OpenDungeons"][2]
    OpenDungeonAmount = random.choices(settings["OpenDungeons"][0], OpenDungeonsWeight)[0]
    if OpenDungeonAmount > 0:
        if "openDungeonsOot" not in SettingsList:
            SettingsList["openDungeonsOot"] = {"type": "specific","values": []}
        SettingsList["openDungeonsMm"] = {"type": "specific","values": []}
        OpenDungeonChoice = ["WF", "SH", "GB", "ST", "DC", "BotW", "JJ", "Shadow", "Water"]
        MMDung = ["WF", "SH", "GB", "ST"]
        OpenDungeons = random.sample(OpenDungeonChoice, OpenDungeonAmount)
        for key in OpenDungeons:
            if key in MMDung:
                SettingsList["openDungeonsMm"]["values"].append(key)
            else:
                SettingsList["openDungeonsOot"]["values"].append(key)

    SettingsList["dekuTree"] = random.choices(settings["DekuTree"][0], settings["DekuTree"][1])[0]

    GanonTrialAmount = random.choices(settings["GanonTrialAmount"][0], settings["GanonTrialAmount"][1])[0]
    if DungeonEntranceShuffle == True:
        if SettingsList["erGanonTower"] == True:
            GanonTrialAmount = random.choices(settings["GanonTrialAmount"][0], settings["GanonTrialAmount"][2])[0]
    if GanonTrialAmount > 0:
        MysteryCount += 1
        SettingsList["ganonTrials"] = {"type": "specific", "values": []}
        TrialList = ["Light", "Forest", "Fire", "Water", "Shadow", "Spirit"]
        TrialChosen = random.sample(TrialList, GanonTrialAmount)
        for key in TrialChosen:
            SettingsList["ganonTrials"]["values"].append(key)
        if GanonTrialAmount > 2:
            HardCounter += 1

    if SongShuffle != "Mix with Owls":
        WarpSongShuffle = random.choices([True, False], settings["WarpSongShuffle"][1])[0]
        if WarpSongShuffle == True:
            SettingsList["erWarps"] = True
            MysteryCount += 1

    AgelessAmount = random.choices(settings["AgelessAmount"][0], settings["AgelessAmount"][1])[0]
    if AgelessAmount > 0:
        AgelessItems = ["agelessSwords", "agelessShields", "agelessTunics", "agelessBoots", "agelessSticks", "agelessBoomerang", "agelessHammer", "agelessHookshot", "agelessSlingshot", "agelessBow", "agelessStrength"]
        AgeAllowed = random.sample(AgelessItems, AgelessAmount)
        for key in AgeAllowed:
            SettingsList[key] = True
            
    if SKeyShuffle[0] != "removed" and SKeyShuffle[1] != "removed":     
        if SettingsList["smallKeyShuffleChestGame"] != "vanilla":
            KeyRingAmount = random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], settings["KeyRingAmount"][2])[0]
        else:
            KeyRingAmount = random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], settings["KeyRingAmount"][1])[0]
        if KeyRingAmount > 0:
            SettingsList["smallKeyRingOot"] = {"type": "specific", "values": []}
            SettingsList["smallKeyRingMm"] = {"type": "specific", "values": []}
            KeyRingPlaces = ["Forest","Fire","Water","Shadow","Spirit","BotW","GTG","Ganon","SH","ST"]
            MMKeyRings = ["SH", "ST"]
            if SettingsList["smallKeyShuffleChestGame"] != "vanilla":
                KeyRingPlaces.append("TCG")
            KeyRingsChosen = random.sample(KeyRingPlaces, KeyRingAmount)
            for key in KeyRingsChosen:
                if key in MMKeyRings:
                    SettingsList["smallKeyRingMm"]["values"].append(key)
                else:
                    SettingsList["smallKeyRingOot"]["values"].append(key)
                    

    ChildWallet = random.choices([True, False], settings["ChildWallet"][1])[0]
    if ChildWallet == True:
        SettingsList["childWallet"] = True
        if SharedShopShuffle == "full":
            HardCounter += 1

    PrePlantedBeans = random.choices([True, False], settings["PrePlantedBeans"][1])[0]
    if PrePlantedBeans == True:
        SettingsList["ootPreplantedBeans"] = True
        del PlandoList["OOT Zora River Bean Seller"]

    KingZoraWeights = settings["KingZora"][1]
    if EntranceRandomizer == "Overworld" or EntranceRandomizer == "Full":
        KingZoraWeights = settings["KingZora"][2]
    SettingsList["zoraKing"] = random.choices(["vanilla", "adult", "open"], KingZoraWeights)[0]

    ZoraDomainWeights = settings["ZoraDomainAdultShortcut"][1]
    if EntranceRandomizer == "Overworld" or "EntranceRandomizer" == "Full":
        ZoraDomainWeights = settings["ZoraDomainAdultShortcut"][2]
    SettingsList["openZdShortcut"] = random.choices([True, False], ZoraDomainWeights)[0]

# Builds the Setting List here:
settings_data = SettingsList
settings_data["junkLocations"] = JunkList
settings_data["hints"] = HintList
settings_data["startingItems"] = StartingItemList
settings_data["plando"]["locations"] = PlandoList
settings_data["specialConds"]["BRIDGE"] = BridgeCond
settings_data["specialConds"]["MOON"] = MoonCond
settings_data["specialConds"]["GANON_BK"] = GanonBKCond
settings_data["specialConds"]["MAJORA"] = MajoraCond

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
#print(seed_string)

with open("seed_output.txt", "w") as file:
    file.write("Seed String:\n")
    file.write("\n")
    file.write(seed_string)

with open("settings_output.txt", "w") as file:
    file.write("Settings List:\n")
    file.write("\n")
    for key, value in settings_data.items():
        file.write(f"{key}: {value}\n")

with open("settings_spoiler.txt", "w") as spoiler_file:
    print("OoTMM Mystery Blitz Generator -- Spoiler Log", file=spoiler_file)
    print("Hard Settings Shuffled:", HardCounter, file=spoiler_file)
    print("Major Settings Shuffled:", MysteryCount, file=spoiler_file)
    print("", file=spoiler_file)
    print("Goal:", WinCond, file=spoiler_file)
    if WinCond == "Triforce Hunt":
        print("Triforce Pieces Needed:", SettingsList["triforceGoal"], file=spoiler_file)
        print("Triforce Pieces Overall:", SettingsList["triforcePieces"], file=spoiler_file)
    print("", file=spoiler_file)
    print("Main Settings:", file=spoiler_file)
    print("Skip Child Zelda:", SkipChildZelda, file=spoiler_file)
    print("Door Of Time:", DoorOfTime, file=spoiler_file)
    print("Songsanity:", SongShuffle, file=spoiler_file)
    print("Ocarina Buttons:", OcarinaButtonShuffle, file=spoiler_file)
    print("Sword Shuffle:", SwordShuffle, file=spoiler_file)
    if SwordShuffle == True:
        print("Master Sword needed for Time Travel:", SettingsList["timeTravelSword"], file=spoiler_file)
    print("Gerudo Card Shuffle:", GerudoCardShuffle, file=spoiler_file)
    print("OoT Skullsanity:", SettingsList["goldSkulltulaTokens"].capitalize(), file=spoiler_file)
    print("MM Skullsanity:", SettingsList["housesSkulltulaTokens"].capitalize(), file=spoiler_file)
    print("Grass Shuffle:", GrassShuffle.capitalize(), file=spoiler_file)
    print("Pot Shuffle:", PotShuffle.capitalize(), file=spoiler_file)
    print("Freestanding Rupees and Hearts Shuffle:", FreestandingShuffle.capitalize(), file=spoiler_file)
    print("Wonder Spot Shuffle:", WonderSpotShuffle.capitalize(), file=spoiler_file)
    print("Crate and Barrel Shuffle:", SharedCratesAndBarrels.capitalize(), file=spoiler_file)
    print("Snowball Shuffle:", SettingsList["shuffleSnowballsMm"].capitalize(), file = spoiler_file)
    print("Cow Shuffle:", SharedCowShuffle, file=spoiler_file)
    print("Child Wallet Shuffle:", ChildWallet, file=spoiler_file)
    print("Shop Shuffle:", SharedShopShuffle.capitalize(), file=spoiler_file)
    if SharedShopShuffle == "full":
        print("Merchant Shuffle:", ScrubShuffle, file=spoiler_file)
        print("Price Shuffle:", PriceShuffle.capitalize(), file=spoiler_file)
        if PriceShuffle == "weighted" or PriceShuffle == "random":
            print("Maximum Wallet Size:", MaxWalletSize, file=spoiler_file)
    if SettingsList["clocks"] == True:
        print("Clock Shuffle:", SettingsList["progressiveClocks"].capitalize(), file=spoiler_file)
        if SettingsList["progressiveClocks"] == "separate":
            print("Starting Clock:", StartingClock, file=spoiler_file)
    else:
        print("Clock Shuffle:", SettingsList["clocks"], file=spoiler_file)
    print("Fountain and Spot Fairies Shuffle:", FairyFountainShuffle, file=spoiler_file)
    print("Hive Shuffle:", SharedHiveShuffle, file=spoiler_file)
    print("Soul Shuffle:", SoulShuffle, file=spoiler_file)
    if SongShuffle != "Mixed with Owls":
        print("Owl Statue Shuffle:", OwlShuffle.capitalize(), file=spoiler_file)
    print("Fishing Pond Shuffle:", FishingPondShuffle, file=spoiler_file)
    print("OoT Diving Rupee Shuffle:", DivingGameShuffle, file=spoiler_file)
    print("OoT Pre-Planted Beans:", PrePlantedBeans, file=spoiler_file)
    print("", file=spoiler_file)
    print("Dungeon Item Settings:", file=spoiler_file)
    print("OoT Small Keys:", SKeyShuffle[1].capitalize(), file=spoiler_file)
    print("OoT Game Keys:", SettingsList["smallKeyShuffleChestGame"].capitalize(), file=spoiler_file)
    print("MM Small Keys:", SKeyShuffle[0].capitalize(), file=spoiler_file)
    print("OoT Silver Rupees:", SettingsList["silverRupeeShuffle"].capitalize(), file=spoiler_file)
    print("MM Stray Fairies:", SettingsList["strayFairyOtherShuffle"].capitalize(), file=spoiler_file)
    print("Boss Keys:", BKeyShuffle.capitalize(), file=spoiler_file)
    if BKeyShuffle != "anywhere":
        print("Boss Souls:", SharedBossSoulShuffle, file=spoiler_file)
    print("Deku Tree:", SettingsList["dekuTree"], file=spoiler_file)
    print("King Zora:", SettingsList["zoraKing"].capitalize(), file=spoiler_file)
    print("Zora's Domain Adult Shortcut:", SettingsList["openZdShortcut"], file=spoiler_file)
    print("Gibdo Well:", SettingsList["beneathWell"].capitalize(), file=spoiler_file)
    print("", file=spoiler_file)
    print("Entrance Settings:", file=spoiler_file)
    print("Spawn:", SettingsList["erSpawns"].capitalize(), file=spoiler_file)
    if SongShuffle != "Mix with Owls":
        print("Warp Songs:", WarpSongShuffle, file=spoiler_file)
    print("World Entrances:", EntranceRandomizer.capitalize(), file=spoiler_file)
    print("Grotto Entrances:", SettingsList["erGrottos"]=="full", file=spoiler_file)
    print("Dungeon Entrances:", DungeonEntranceShuffle, file=spoiler_file)
    if DungeonEntranceShuffle == True:
        print("Ganon's Castle Included:", GanonCastleShuffle, file=spoiler_file)
        print("Ganon's Tower Included:", GanonTowerShuffle, file=spoiler_file)
        print("Clock Tower Included:", ClockTowerShuffle, file=spoiler_file)
    print("Boss Entrances:", SettingsList["erBoss"]=="full", file=spoiler_file)
    print("", file=spoiler_file)
    print("Ageless Items:", AgelessAmount, file=spoiler_file)
    if AgelessAmount > 0:
        for key in AgeAllowed:
            if key != AgeAllowed[-1]:
                spoiler_file.write(f"{key[7:]}, ")
            else:
                spoiler_file.write(f"{key[7:]}")
        spoiler_file.write("\n")
    print("", file=spoiler_file)
    print("MQ Dungeons:", SharedMQDungeons, file=spoiler_file)
    if SharedMQDungeons > 0:
        for key in MQDungeonChosen:
            if key != MQDungeonChosen[-1]:
                spoiler_file.write(f"{key}, ")
            else:
                spoiler_file.write(f"{key}")
        spoiler_file.write("\n")
    print("", file=spoiler_file)
    print("Open Dungeons:", OpenDungeonAmount, file=spoiler_file)
    if OpenDungeonAmount > 0:
        for key in OpenDungeons:
            if key != OpenDungeons[-1]:
                spoiler_file.write(f"{key}, ")
            else:
                spoiler_file.write(f"{key}")
        spoiler_file.write("\n")
    print("", file=spoiler_file)
    if SKeyShuffle[0] != "removed" and SKeyShuffle[1] != "removed":
        print("Key Rings:", KeyRingAmount, file=spoiler_file)
        if KeyRingAmount > 0:
            for key in KeyRingsChosen:
                if key != KeyRingsChosen[-1]:
                    spoiler_file.write(f"{key}, ")
                else:
                    spoiler_file.write(f"{key}")
            spoiler_file.write("\n")
        print("", file=spoiler_file)
    print("Ganon Trials:", GanonTrialAmount, file=spoiler_file)
    if GanonTrialAmount > 0:
        for key in TrialChosen:
            if key != TrialChosen[-1]:
                spoiler_file.write(f"{key}, ")
            else:
                spoiler_file.write(f"{key}")


print("Settings generated successfully!")
