This script randomly generates settings strings for OoTMM. This allows the settings themselves to be randomly picked. This script allows for fine control over which settings can be randomised and the likelihoods of various options.

Whilst OoTMM itself has a 'Random Settings' option, it has very little flexibility. For example: the 'Goal' has a 5/8ths chance of being 'Ganon and Majora'. Without this script, there's no way to change these odds, nor remove the chance of alternative goals (such as Triforce Hunt) entirely.

Out-of-the-box, you can use this script with the `Config - OoTMM Mystery Blitz Rando WIP.json` configuration file. This file is designed to give a Blitz-like experience. By editting this file - or starting a new config file - you can customise the settings randomisation process to match your preferences.

# Installation

You can install either the 'Command Line' or the (outdated) 'Graphical Interface' version.

## Command Line installation

- Ensure you have Python installed
- Download this repository - ensure the contents are unzipped once they are on your computer. Unzipped contents should preferably be in their own folder.

## Graphical Interface installation (outdated)
(For those unfamiliar with using programs via the 'Command Line'.)

- Download the [latest release](https://github.com/Xandervile/ootmm-settings-generator/releases) zip file (contains an exe). At present on Github, releases are found in the sidebar.

# Usage
Basic outline of steps:

1. (Optional.) Customisation!
2. Use this script to generate a settings string.
3. Paste your settings string into OoTMM and then generate your seed

## 1. Customisation
**Only available to those using the CLI option**.

The script comes with a default configuration file: `Config - OoTMM Mystery Blitz Rando WIP.json`.

When you use the CLI interface, you'll be able to choose which config file gets loaded. So you have the option to either:
- Edit the default config file directly; or:
- Make additional config files and then choose which one to load when generating new settings strings.

The config file can be edited to control the weighting of settings; for example to make things you like happen more often (or everytime). You can also disable options.

The 'Mystery Blitz' config file contains limited documenation.

## 2. Using this script to generate a settings string

### Via command-line

1. Start your CLI (command line interface)
2. Use `py generate.py` to run the script.
    - If your configuration file has a different name from the default one (the mystery blitz one), then supply the name of that file afterwards. For example: `py generate.py my-custom-file.json`. (If your filename has spaces or special characters, you may need to use quotes or other formatting as dictated by your CLI application)

### Via graphical interface 
TODO

## 3. Pasting your settings string into OoTMM and generating the seed

To load into the OoTMM website:
1. (After running the script). Open up `seed_output.txt`. Copy the settings string from this file (it starts with `v1.`).
2. Click 'Generate a Seed' - (you may also trying using OoTMM's dev generator).
3. Find the 'Import/Export Settings' option and paste the settings string into it
4. Generate your seed! 

# Current settings added

- Songs can be either on Songs, on Songs and Owls, or Anywhere (in Anywhere, Song of Time is shared AND shuffled, as settings are Moon Crash starts a fresh new cycle so less stress)! As an experiment, Songs on Dungeon Rewards has ALSO been added! More info in the weights file.
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

# Future plans
- Add Triforce Quest/Hunt options in for more random settings (these to have their own weights for settings?). [PYTHON UPDATED WITH THIS]
- Potentially open the moon up for checks (need to think about how to balance this?) - Added in Triforce Hunt and Triforce Quest. Thinking for standard Blitz now.
- Enemy and NPC souls to look at at some point - would be a pain to balance though. [PYTHON UPDATED WITH THIS - WILL ALSO ADD A WEIGHTED PICK ABOUT "PROPORTION OF SOULS TO START WITH" TO MAKE IT SLIGHTLY LESS TEDIOUS]
- Make the weights json easier to understand (similar to OoTRSL layout, gonna adapt their code for this)

# Issues
- Song and Owl Shuffle CAN create a seed that won't gen, as does Songs on Dungeon Rewards. This is due to the lack of logic I used to create such a setting. Just reroll settings if you get one that doesn't gen and errors - currently experimenting with basic logic to reduce (but doesn't eliminate) this. Can only be truly eliminated if/when Dungeon Entrance Plando is added.

# Credits
- eedefeed for contributing the CLI interface and making generalisations!
- Revven for playtesting at every possible moment
