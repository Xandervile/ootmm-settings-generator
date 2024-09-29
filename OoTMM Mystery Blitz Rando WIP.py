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

while MysteryCount < MinMysterySettings or HardCounter > HARDMODELIMIT or MysteryCount > MaxMysterySettings:
    MysteryCount = 0
    HardCounter = 0

    SettingsList = base_settings.copy()
    
    JunkList = DefaultJunkList.copy()
    StartingItemList = DefaultStartingItemList.copy()
    PlandoList = DefaultPlando.copy()
    HintList = DefaultHintList.copy()

    SettingsList["songs"] = random.choices(["songLocations", "anywhere"], settings["SongShuffle"][1])[0]
    if SettingsList["songs"] == "anywhere":
        HardCounter += 1
        MysteryCount += 1
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
    if SettingsList["songs"] == "anywhere":
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
##                            JunkList.append(f"MM Termina Field Grass Pack {i:02} Bush {j:02}")
##    if GrassShuffle == "all":
##        HardCounter += 1  #Looking into limiting


    GrassShuffle = random.choices(["none", "dungeons", "overworld", "all"], settings["GrassShuffle"][1])[0]
    SettingsList["shuffleGrassOot"] = GrassShuffle
    SettingsList["shuffleGrassMm"] = GrassShuffle
    if GrassShuffle != "none":
        MysteryCount += 1
    if GrassShuffle == "overworld" or GrassShuffle == "all":
        TFGrassShuffle = settings["TFGrassAllowed"][0]
        if EntranceRandomizer == "overworld" or EntranceRandomizer == "all":
            GrassCount = 12
        elif TFGrassShuffle == True:
            GrassCount = settings["TFGrassAllowed"][1]
        else:
            GrassCount = 0
        for i in range(1, 19):                      #Limits Termina Field Grass to only 1 potential patch good
            GrassAllowed = random.sample(range(1, 13), GrassCount)
            for j in range(1, 13):
                if j not in GrassAllowed:
                    JunkList.append(f"MM Termina Field Grass Pack {i:02} Bush {j:02}")
    if GrassShuffle == "all":
        HardCounter += 1  #Looking into limiting


    PotShuffle = random.choices(["none", "dungeons", "overworld", "all"], settings["PotShuffle"][1])[0]
    SettingsList["shufflePotsOot"] = PotShuffle
    SettingsList["shufflePotsMm"] = PotShuffle
    if PotShuffle == True:
        HardCounter += 1
        MysteryCount += 1

    SettingsList["silverRupeeShuffle"] = random.choices(["vanilla", "ownDungeon", "anywhere"], settings["SilverRupeeShuffle"][1])[0]

    SKeyShuffleWeight = settings["SmallKeyShuffle"][1]
    SKeyShuffle = random.choices([["removed", "ownDungeon"], ["removed", "removed"], ["ownDungeon", "ownDungeon"], ["anywhere", "anywhere"]], SKeyShuffleWeight)[0]
    SettingsList["smallKeyShuffleMm"] = SKeyShuffle[0]
    SettingsList["smallKeyShuffleOot"] = SKeyShuffle[1]
    if SKeyShuffle == ["anywhere", "anywhere"]:
        SettingsList["smallKeyShuffleHideout"] = "anywhere"
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
        SettingsList["timeTravelSword"] = False
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
    SettingsList["owlShuffle"] = random.choices([True, False], OwlWeight)[0]
    if SettingsList["owlShuffle"] == True:
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
                SettingsList["dungeon"][key]="mq"
            else:
                SettingsList["dungeon"][key]="vanilla"

    SharedCratesAndBarrels = random.choices(["none", "dungeons", "overworld", "all"], settings["CratesAndBarrelsShuffle"][1])[0]
    SettingsList["shuffleCratesOot"] = SharedCratesAndBarrels
    SettingsList["shuffleCratesMm"] = SharedCratesAndBarrels
    SettingsList["shuffleBarrelsMm"] = SharedCratesAndBarrels
    if SharedCratesAndBarrels != "none":
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

    FairyFountainShuffle = random.choices([True, False], settings["FairyFountainShuffle"][1])[0]
    if FairyFountainShuffle == True:
        SettingsList["fairyFountainFairyShuffleOot"] = True
        SettingsList["fairyFountainFairyShuffleMm"] = True
        MysteryCount += 1

    GerudoCardShuffle = random.choices(["Starting", True, False], settings["GerudoCardShuffle"][1])[0]
    if GerudoCardShuffle != False:
        SettingsList["shuffleGerudoCard"] = True
        if GerudoCardShuffle == "Starting":
            StartingItemList["OOT_GERUDO_CARD"] = 1

    SettingsList["erSpawns"] = random.choices(["none", "child", "adult", "both"], settings["SpawnShuffle"][1])[0]

    WellWeight = settings["GibdoSettings"][1]
    if DungeonEntranceShuffle == True:
        WellWeight = settings["GibdoSettings"][2]
    SettingsList["beneathWell"] = random.choices(["vanilla", "remorseless", "open"], WellWeight)[0]

    AgelessAmount = random.choices(settings["AgelessAmount"][0], settings["AgelessAmount"][1])[0]
    if AgelessAmount > 0:
        AgelessItems = ["agelessSwords", "agelessShields", "agelessTunics", "agelessBoots", "agelessSticks", "agelessBoomerang", "agelessHammer", "agelessHookshot", "agelessSlingshot", "agelessBow", "agelessStrength"]
        AgeAllowed = random.sample(AgelessItems, AgelessAmount)
        for key in AgeAllowed:
            SettingsList[key] = True

# Builds the Setting List here: 
settings_data = SettingsList
settings_data["junkLocations"] = JunkList
settings_data["hints"] = HintList
settings_data["startingItems"] = StartingItemList

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
    print("Main Settings:", file=spoiler_file)
    print("Songsanity:", SettingsList["songs"].capitalize(), file=spoiler_file)
    print("Ocarina Buttons:", OcarinaButtonShuffle, file=spoiler_file)
    print("Sword Shuffle:", SwordShuffle, file=spoiler_file)
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
    print("Shop Shuffle:", SharedShopShuffle.capitalize(), file=spoiler_file)
    if SharedShopShuffle == "full":
        print("Merchant Shuffle:", ScrubShuffle, file=spoiler_file)
        print("Price Shuffle:", PriceShuffle.capitalize(), file=spoiler_file)
    if SettingsList["clocks"] == True:
        print("Clock Shuffle:", SettingsList["progressiveClocks"].capitalize(), file=spoiler_file)
        if SettingsList["progressiveClocks"] == "separate":
            print("Starting Clock:", StartingClock, file=spoiler_file)
    else:
        print("Clock Shuffle:", SettingsList["clocks"], file=spoiler_file)
    print("Fountain Fairies Shuffle:", FairyFountainShuffle, file=spoiler_file)
    print("Owl Statue Shuffle:", SettingsList["owlShuffle"], file=spoiler_file)
    print("", file=spoiler_file)
    print("Dungeon Item Settings:", file=spoiler_file)
    print("OoT Small Keys:", SKeyShuffle[1].capitalize(), file=spoiler_file)
    print("MM Small Keys:", SKeyShuffle[0].capitalize(), file=spoiler_file)
    print("OoT Silver Rupees:", SettingsList["silverRupeeShuffle"].capitalize(), file=spoiler_file)
    print("MM Stray Fairies:", SettingsList["strayFairyOtherShuffle"].capitalize(), file=spoiler_file)
    print("Boss Keys:", BKeyShuffle.capitalize(), file=spoiler_file)
    if BKeyShuffle != "anywhere":
        print("Boss Souls:", SharedBossSoulShuffle, file=spoiler_file)
    print("Gibdo Well:", SettingsList["beneathWell"].capitalize(), file=spoiler_file)
    print("", file=spoiler_file)
    print("Entrance Settings:", file=spoiler_file)
    print("Spawn:", SettingsList["erSpawns"].capitalize(), file=spoiler_file)
    print("World Entrances:", EntranceRandomizer.capitalize(), file=spoiler_file)
    print("Grotto Entrances:", SettingsList["erGrottos"]=="full", file=spoiler_file)
    print("Dungeon Entrances:", DungeonEntranceShuffle, file=spoiler_file)
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

print("Settings generated successfully!")
