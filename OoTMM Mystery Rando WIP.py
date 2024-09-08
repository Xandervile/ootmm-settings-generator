import zlib
import base64
import json
import random

MinMysterySettings = 4
MysteryCount = 0
HardModeReached = False

#HarderSettings get rolled first to allow limitations
HARDMODELIMIT = 3

while MysteryCount < MinMysterySettings:
    MysteryCount = 0
    HardCounter = 99

    while HardCounter > HARDMODELIMIT:
        HardCounter = 0

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

        ClockShuffle = random.choices([True, False], [10, 90])[0]
        if ClockShuffle == True:
            HardCounter += 1
            MysteryCount += 1

        BossSoulsWeight = [10, 90]
        if BKeyShuffle == "anywhere":
            BossSoulsWeight[1] += BossSoulsWeight[0]
            BossSoulsWeight[0] = 0
        SharedBossSoulShuffle = random.choices([True, False], BossSoulsWeight)[0]
        if SharedBossSoulShuffle == True:
            HardCounter += 1
            MysteryCount += 1

        StrayFairyShuffle = random.choices(["removed","anywhere"], [85, 15])[0]
        if StrayFairyShuffle != "removed":
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
        
        

    #Other Settings get Randomized here
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
"progressiveClocks":random.choices(["seperate", "ascending", "descending"])[0],
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
"erMajorDungeons":DungeonEntranceShuffle,
"erMinorDungeons":DungeonEntranceShuffle,
"erSpiderHouses":DungeonEntranceShuffle,
"erPirateFortress":DungeonEntranceShuffle,
"erBeneathWell":DungeonEntranceShuffle,
"erIkanaCastle":DungeonEntranceShuffle,
"erSecretShrine":DungeonEntranceShuffle,
"startingItems":{"OOT_NUTS_10":2,
"OOT_SHIELD_DEKU":1,
"OOT_STICK":10,
"MM_SONG_EPONA":1,
"SHARED_SHIELD_HYLIAN":1,
"MM_OCARINA":1,
"OOT_OCARINA":1,
"MM_SWORD":1,
"MM_SONG_SOARING":1},
"junkLocations":["MM Beneath The Graveyard Dampe Chest",
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
"OOT Skulltula House 50 Tokens"],
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
"hints":[{"type":"foolish",
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
#seed_data = seed_string.split(".")[1]

# Add padding if necessary
#padding_needed = len(seed_data) % 4
#if padding_needed:
#    seed_data += "=" * (4 - padding_needed)

# Decode and decompress the seed
#decoded_data = zlib.decompress(base64.urlsafe_b64decode(seed_data))

# Output the decoded data
#print(decoded_data)




