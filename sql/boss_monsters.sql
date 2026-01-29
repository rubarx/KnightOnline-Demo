-- =============================================================================
-- Boss Monsters Script for KnightOnline-Demo v1.5.0
-- =============================================================================
-- This script adds 7 boss monsters using existing client assets (sPid mappings)
-- Run this script on the KN_online database after server deployment
-- =============================================================================

USE KN_online;
GO

-- =============================================================================
-- SECTION 1: Insert Boss Monsters into K_NPC (or K_MONSTER)
-- =============================================================================
-- Using existing sPid values that map to client models:
-- sPid 1400 = mob_attila.n3chr
-- sPid 2400 = mob_golem.n3chr
-- sPid 2600 = mob_centaur.n3chr
-- sPid 3800 = mob_mon_bigpig.n3chr (Manticore)
-- sPid 1701 = mob_dun_trol.n3chr
-- sPid 2100 = mob_deruvisy.n3chr
-- sPid 2200 = mob_harppy.n3chr

-- Boss 1: Attila the Destroyer (Main Boss - Level 83)
INSERT INTO K_NPC (
    sSid, strName, sPid, sLevel, iHpPoint, byRank, byType, sItem, byActType,
    sDamage, sDefense, sAC, iFireR, iColdR, iLightR, iMagicR, iDiseaseR, iPoisonR,
    bySearchRange, byAttackRange, sAttackDelay, sHitRate, byEvadeRate,
    sSize, iWeapon1, iWeapon2
)
VALUES (
    9001, 'Attila the Destroyer', 1400, 83, 5000000, 5, 0, 9001, 2,
    2500, 800, 500, 50, 50, 50, 30, 40, 40,
    40, 3, 1500, 300, 50,
    150, 0, 0
);

-- Boss 2: Manticore Lord (Level 80)
INSERT INTO K_NPC (
    sSid, strName, sPid, sLevel, iHpPoint, byRank, byType, sItem, byActType,
    sDamage, sDefense, sAC, iFireR, iColdR, iLightR, iMagicR, iDiseaseR, iPoisonR,
    bySearchRange, byAttackRange, sAttackDelay, sHitRate, byEvadeRate,
    sSize, iWeapon1, iWeapon2
)
VALUES (
    9002, 'Manticore Lord', 3800, 80, 3500000, 4, 0, 9002, 2,
    2000, 700, 450, 60, 30, 40, 25, 35, 35,
    35, 4, 1800, 280, 45,
    140, 0, 0
);

-- Boss 3: Centaur Warlord (Level 78)
INSERT INTO K_NPC (
    sSid, strName, sPid, sLevel, iHpPoint, byRank, byType, sItem, byActType,
    sDamage, sDefense, sAC, iFireR, iColdR, iLightR, iMagicR, iDiseaseR, iPoisonR,
    bySearchRange, byAttackRange, sAttackDelay, sHitRate, byEvadeRate,
    sSize, iWeapon1, iWeapon2
)
VALUES (
    9003, 'Centaur Warlord', 2600, 78, 2500000, 4, 0, 9003, 2,
    1800, 650, 400, 40, 40, 50, 30, 30, 30,
    40, 5, 1600, 270, 55,
    130, 0, 0
);

-- Boss 4: Golem King (Level 82)
INSERT INTO K_NPC (
    sSid, strName, sPid, sLevel, iHpPoint, byRank, byType, sItem, byActType,
    sDamage, sDefense, sAC, iFireR, iColdR, iLightR, iMagicR, iDiseaseR, iPoisonR,
    bySearchRange, byAttackRange, sAttackDelay, sHitRate, byEvadeRate,
    sSize, iWeapon1, iWeapon2
)
VALUES (
    9004, 'Golem King', 2400, 82, 4000000, 4, 0, 9004, 2,
    2200, 900, 600, 70, 70, 30, 20, 50, 50,
    30, 2, 2000, 250, 20,
    180, 0, 0
);

-- Boss 5: Troll King (Level 79)
INSERT INTO K_NPC (
    sSid, strName, sPid, sLevel, iHpPoint, byRank, byType, sItem, byActType,
    sDamage, sDefense, sAC, iFireR, iColdR, iLightR, iMagicR, iDiseaseR, iPoisonR,
    bySearchRange, byAttackRange, sAttackDelay, sHitRate, byEvadeRate,
    sSize, iWeapon1, iWeapon2
)
VALUES (
    9005, 'Troll King', 1701, 79, 2800000, 4, 0, 9005, 2,
    1900, 600, 380, 35, 45, 35, 25, 40, 40,
    35, 3, 1700, 260, 40,
    160, 0, 0
);

-- Boss 6: Shadow Apostle (Level 81)
INSERT INTO K_NPC (
    sSid, strName, sPid, sLevel, iHpPoint, byRank, byType, sItem, byActType,
    sDamage, sDefense, sAC, iFireR, iColdR, iLightR, iMagicR, iDiseaseR, iPoisonR,
    bySearchRange, byAttackRange, sAttackDelay, sHitRate, byEvadeRate,
    sSize, iWeapon1, iWeapon2
)
VALUES (
    9006, 'Shadow Apostle', 2100, 81, 3200000, 4, 0, 9006, 2,
    2100, 550, 350, 45, 45, 60, 50, 30, 30,
    45, 4, 1400, 290, 60,
    120, 0, 0
);

-- Boss 7: Crimson Harpy Queen (Level 77)
INSERT INTO K_NPC (
    sSid, strName, sPid, sLevel, iHpPoint, byRank, byType, sItem, byActType,
    sDamage, sDefense, sAC, iFireR, iColdR, iLightR, iMagicR, iDiseaseR, iPoisonR,
    bySearchRange, byAttackRange, sAttackDelay, sHitRate, byEvadeRate,
    sSize, iWeapon1, iWeapon2
)
VALUES (
    9007, 'Crimson Harpy Queen', 2200, 77, 2200000, 3, 0, 9007, 2,
    1600, 450, 300, 30, 30, 50, 40, 25, 25,
    50, 6, 1200, 300, 70,
    100, 0, 0
);

-- =============================================================================
-- SECTION 2: Insert Loot Tables into K_MONSTER_ITEM
-- =============================================================================
-- Item IDs are examples - adjust according to your item database
-- sPersent values: 10000 = 100%, 1000 = 10%, 500 = 5%, 100 = 1%

-- Attila the Destroyer drops (best loot)
INSERT INTO K_MONSTER_ITEM (sIndex, iItem01, sPersent01, iItem02, sPersent02, iItem03, sPersent03, iItem04, sPersent04, iItem05, sPersent05)
VALUES (9001, 389015000, 500, 389016000, 500, 810200000, 1000, 810201000, 1000, 399210000, 2000);

-- Manticore Lord drops
INSERT INTO K_MONSTER_ITEM (sIndex, iItem01, sPersent01, iItem02, sPersent02, iItem03, sPersent03, iItem04, sPersent04, iItem05, sPersent05)
VALUES (9002, 389014000, 800, 810199000, 1500, 399209000, 2500, 900001000, 5000, 0, 0);

-- Centaur Warlord drops
INSERT INTO K_MONSTER_ITEM (sIndex, iItem01, sPersent01, iItem02, sPersent02, iItem03, sPersent03, iItem04, sPersent04, iItem05, sPersent05)
VALUES (9003, 389013000, 1000, 810198000, 2000, 399208000, 3000, 900001000, 5000, 0, 0);

-- Golem King drops
INSERT INTO K_MONSTER_ITEM (sIndex, iItem01, sPersent01, iItem02, sPersent02, iItem03, sPersent03, iItem04, sPersent04, iItem05, sPersent05)
VALUES (9004, 389014500, 700, 810199500, 1200, 399209500, 2000, 900001000, 5000, 0, 0);

-- Troll King drops
INSERT INTO K_MONSTER_ITEM (sIndex, iItem01, sPersent01, iItem02, sPersent02, iItem03, sPersent03, iItem04, sPersent04, iItem05, sPersent05)
VALUES (9005, 389012000, 1200, 810197000, 2500, 399207000, 3500, 900001000, 5000, 0, 0);

-- Shadow Apostle drops
INSERT INTO K_MONSTER_ITEM (sIndex, iItem01, sPersent01, iItem02, sPersent02, iItem03, sPersent03, iItem04, sPersent04, iItem05, sPersent05)
VALUES (9006, 389013500, 900, 810198500, 1800, 399208500, 2800, 900001000, 5000, 0, 0);

-- Crimson Harpy Queen drops
INSERT INTO K_MONSTER_ITEM (sIndex, iItem01, sPersent01, iItem02, sPersent02, iItem03, sPersent03, iItem04, sPersent04, iItem05, sPersent05)
VALUES (9007, 389011000, 1500, 810196000, 3000, 399206000, 4000, 900001000, 5000, 0, 0);

-- =============================================================================
-- SECTION 3: Insert Spawn Positions into K_NPCPOS
-- =============================================================================
-- ZoneID reference:
-- 72 = Ronark Land
-- 43 = Forgotten Temple
-- 11 = El Morad Castle area
-- 21 = Karus Castle area
-- 1 = El Morad starting zone
-- 2 = Karus starting zone

-- Attila in Ronark Land center (Zone 72) - 2 hour respawn
INSERT INTO K_NPCPOS (
    ZoneID, NpcID, ActType, RegenType, DungeonFamily, SpecialType, TrapNumber,
    LeftX, TopZ, RightX, BottomZ, LimitMinZ, LimitMaxZ,
    NumNpc, RegTime, byDirection, DotCnt, Path
)
VALUES (72, 9001, 2, 0, 1, 0, 0, 990, 1111, 990, 1111, 0, 0, 1, 7200, 0, 0, '');

-- Manticore Lord in Forgotten Temple (Zone 43) - 1 hour respawn
INSERT INTO K_NPCPOS (
    ZoneID, NpcID, ActType, RegenType, DungeonFamily, SpecialType, TrapNumber,
    LeftX, TopZ, RightX, BottomZ, LimitMinZ, LimitMaxZ,
    NumNpc, RegTime, byDirection, DotCnt, Path
)
VALUES (43, 9002, 2, 0, 2, 0, 0, 500, 500, 500, 500, 0, 0, 1, 3600, 0, 0, '');

-- Centaur Warlord in El Morad outer area (Zone 11) - 1 hour respawn
INSERT INTO K_NPCPOS (
    ZoneID, NpcID, ActType, RegenType, DungeonFamily, SpecialType, TrapNumber,
    LeftX, TopZ, RightX, BottomZ, LimitMinZ, LimitMaxZ,
    NumNpc, RegTime, byDirection, DotCnt, Path
)
VALUES (11, 9003, 2, 0, 3, 0, 0, 800, 700, 800, 700, 0, 0, 1, 3600, 0, 0, '');

-- Golem King in Karus outer area (Zone 21) - 1.5 hour respawn
INSERT INTO K_NPCPOS (
    ZoneID, NpcID, ActType, RegenType, DungeonFamily, SpecialType, TrapNumber,
    LeftX, TopZ, RightX, BottomZ, LimitMinZ, LimitMaxZ,
    NumNpc, RegTime, byDirection, DotCnt, Path
)
VALUES (21, 9004, 2, 0, 4, 0, 0, 600, 800, 600, 800, 0, 0, 1, 5400, 0, 0, '');

-- Troll King in El Morad training area (Zone 1) - 45 min respawn
INSERT INTO K_NPCPOS (
    ZoneID, NpcID, ActType, RegenType, DungeonFamily, SpecialType, TrapNumber,
    LeftX, TopZ, RightX, BottomZ, LimitMinZ, LimitMaxZ,
    NumNpc, RegTime, byDirection, DotCnt, Path
)
VALUES (1, 9005, 2, 0, 5, 0, 0, 1200, 1000, 1200, 1000, 0, 0, 1, 2700, 0, 0, '');

-- Shadow Apostle in Karus training area (Zone 2) - 45 min respawn
INSERT INTO K_NPCPOS (
    ZoneID, NpcID, ActType, RegenType, DungeonFamily, SpecialType, TrapNumber,
    LeftX, TopZ, RightX, BottomZ, LimitMinZ, LimitMaxZ,
    NumNpc, RegTime, byDirection, DotCnt, Path
)
VALUES (2, 9006, 2, 0, 6, 0, 0, 1100, 900, 1100, 900, 0, 0, 1, 2700, 0, 0, '');

-- Crimson Harpy Queen in Ronark Land east (Zone 72) - 30 min respawn
INSERT INTO K_NPCPOS (
    ZoneID, NpcID, ActType, RegenType, DungeonFamily, SpecialType, TrapNumber,
    LeftX, TopZ, RightX, BottomZ, LimitMinZ, LimitMaxZ,
    NumNpc, RegTime, byDirection, DotCnt, Path
)
VALUES (72, 9007, 2, 0, 7, 0, 0, 1300, 800, 1300, 800, 0, 0, 1, 1800, 0, 0, '');

-- =============================================================================
-- VERIFICATION QUERIES
-- =============================================================================
-- Run these to verify the insertions:

-- SELECT * FROM K_NPC WHERE sSid >= 9001 AND sSid <= 9007;
-- SELECT * FROM K_MONSTER_ITEM WHERE sIndex >= 9001 AND sIndex <= 9007;
-- SELECT * FROM K_NPCPOS WHERE NpcID >= 9001 AND NpcID <= 9007;

PRINT 'Boss monsters script completed successfully!';
PRINT '7 bosses added: Attila, Manticore Lord, Centaur Warlord, Golem King, Troll King, Shadow Apostle, Crimson Harpy Queen';
GO
