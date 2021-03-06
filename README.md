# RPG.PY
## RPG.PY is an RPG playable in your terminal (even over SSH)
### About the game

RPG.py takes place in a persistent world known as Beladir, it's a simple fantasy RPG with turn-based combat.

### Upcoming Features
1. Combat
    - [ ] Battlefields
      - [ ] Type (Plains, Dungeon, Cave, Grassland etc)
      - [ ] Hazards/Weather (Lava, rain, snow)
    - [x] Weapon disarming
    - [x] Disabling of dead limbs

2. World 
    - [ ] Cities
      - [x] Starter Town
      - [ ] Blackcliff
      - [ ] Ork'Theral
      - [ ] Arkthal
      - [ ] Ruins of Brym
      - [ ] Berum
      
    - [x] Flora (for Alchemy)
    - [x] Alchemy
    - [x] Farming
    - [ ] Wilderness
### Current Features

1. Combat
      - Debuffs
      - Limb damage
        - For example hitting a rat in the head causes more damage than striking it's paw
      - Different weapon types
        - Stab (better armor penetration)
        - Crush (more limb damage)
        - Slash (Chance to chop off limbs)
      - Spells
        - Direct damage spells (Fireball, Lifebolts)
        - Damage over time and debuff spells (scorch, chill)
        - Hybrid spells (Woodland Charm, Infest)
      - Weapon effects
        - Stuns, chills, bleeds, poison
      - Equipment
        - ARPG-Like stats
          - Spelldamage conversion (ex. Fire -> Occult)
          - Multipliers
            - Conditional (ex. +4 firedamage to spells, 30% increased arcane damage)
            - General (ex. +3 damage to all spells, 10% increased spelldamage)
          - On hit / On getting hit (ex. 0-2 damage reflected to attacker)
          - Unique stats examples:
            - Unarmed attacks are now kicks, scaling with Strength.
            - While Equipped: Gain access to Tempest spell.
            - Gain the ability to Dodge.
            - Gain Magic Barrier buff while blocking.
    
2. World
      - Player Housing
        - Buy a house and upgrade it get access to:
          - Teleportation system
          - Alchemy Station
          - Storage stashes
          - Herb Garden
          - Weapon Smithing and upgrading
          - Make-a-spell custom spellstation
      - Quests
        - Changing dialogue options depending on stats
        - Unique dialogue system with secret alternatives
        - Puzzles
      - Randomly Generated Dungeons
        - Random cave layout
    
3. Races
      - Elves
        - Racial abilities
          - Nature Bond: Attuned to all gods of the land.
          - Large Mind: Efficient at learning new things
          - Elvish Hivemind: Can occupy other Elves at will
          - Arcane Defiency: Weakness to the Arcane arts

      - Humans
        - Racial abilities
          - Sneaky Tongue: Increased chance to trick people
          - Eagle eyes: increased perception of surroundings
          - Weak-bodied: Weakness to flesh wounds

      - Dwarves
        - Racial abilities
          - Pale Skin: Immune to certain diseases
          - Abandoned: Has no obligation to any god
          - Murky Eyes: Efficient at combat in the dark
          - Deep Dweller: Local foods may be problematic
          - Vertically Handicapped: Surface travel takes longer

      - Orcs
        - Racial abilities
          - Tough Skin: Resilient to many status effects
          - Ravager: Efficient at combat on open plains
          - Worker's hands: Highly efficient crafters
          - Large Hands: Capable of wielding two-handed weapons with one hand
          - Dry Throat: Weakness to water
