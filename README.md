A settings string generator for customised settings for offline use. Mainly for Weighted Random settings a la Majora's Mask Mystery, where you know what COULD be randomised but it isn't guaranteed, and unlike the Randomise Settings option, this can be weighted for your own choosing.

Current Settings Added:
- Songs can be either on Songs, on Songs and Owls, or Anywhere (in Anywhere, Song of Time is shared AND shuffled, as settings are Moon Crash starts a fresh new cycle so less stress)!
- Grass, Pots, Freestanding Rupees and Hearts, Crates and Barrels and Snowballs can be unshuffled, overworld only, dungeon only or all! Independently! (Grass currently bugged so that is all or nothing)
- Hives can be shuffled!
- All swords can be shuffled! (in this case, Master Sword may be needed to time travel!)
- Skulltulas can be shuffled!
- Entrances can be shuffled! (No Mixed or Decoupled though!)
- MM Stray Fairies COULD be shuffled!
- Fairy Fountains and those big fat fairies in OoT can also be shuffled!
- COWS can be shuffled!
- Fishing can be shuffled, as can Diving Game (Loach and Huge Rupees are guaranteed junk as no one likes a massive RNG fest)!
- CLOCKS can be shuffled! AND you get a guaranteed Night 3 hint if they are separate!
- Owl Statues can be shuffled!
- Ocarina Buttons can be shuffled!
- Small Keys can be shuffled! If there are no Keysy settings, they can even be Keyrings!
- Boss Keys can be shuffled, or even Boss Souls (one or the other)!
- Some dungeons may be Master Quest, or Pre Opened!
- Beneath the Well can be Remorseless, or even fully open! Even more likely to be opened if any entrance near it can be shuffled!
- Door of Time COULD be closed!
- Items may not require ages!
- Ganon's Trials may be on OR off, AND may lead to a dungeon (if Castle or Tower are shuffled, Rainbow Bridge is automatically on!)
- Silver Rupees in OoT may be shuffled (default is Vanilla or Own Dungeon, but with tweaking, soon maybe anywhere or any dungeon?)
- All containers have "appearance match contents" for easier clarity on settings!

To use:
- Download Python (for dev build) or exe (doesn't have Future Plan stuff that may be in the python) and associated weights file
- Put both anywhere but in the same folder
- Adjust weights to your liking (I tried to label them as best I could)
- run python script.
- Open Settings String txt and copy the string into the OoTMM settings string box


Future Plans:
- Add Triforce Quest/Hunt options in for more random settings (these to have their own weights for settings?). [PYTHON UPDATED WITH THIS]
- Potentially open the moon up for checks (need to think about how to balance this?) - Added in Triforce Hunt and Triforce Quest. Thinking for standard Blitz now.
- Enemy and NPC souls to look at at some point - would be a pain to balance though. [PYTHON UPDATED WITH THIS]

Issues:
- If Silver Rupees are shuffled in own dungeons, SAVE in the dungeon before collecting any. Combo Rando has an issue where collecting the last silver rupee in the same room as the cutscene that triggers whilst being airborne softlocks, so this means you can preplan the rupees easier to not lead into that crash
- Song and Owl Shuffle CAN create a seed that won't gen, as does Songs on Dungeon Rewards. This is due to the lack of logic I used to create such a setting. Just reroll settings if you get one that doesn't gen and errors.
