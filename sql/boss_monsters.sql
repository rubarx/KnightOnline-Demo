-- =============================================================================
-- Boss Monsters Script for KnightOnline-Demo v1.5.0
-- =============================================================================
-- This script adds 7 boss monsters using existing client assets (sPid mappings)
-- Run this script on the KN_online database after server deployment
-- =============================================================================

USE KN_online;
GO

-- =============================================================================
-- SECTION 1: Insert Boss Monsters into K_NPC
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
INSERT INTO K_NPC (sSid, strName, sPid, sSize, iWeapon1, iWeapon2, byGroup, byActType, byType, byFamily, byRank, byTitle, iSellingGroup, sLevel, iExp, iLoyalty, iHpPoint, sMpPoint, sAtk, sAc, sHitRate, sEvadeRate, sDamage, sAttackDelay, bySpeed1, bySpeed2, sStandtime, iMagic1, iMagic2, iMagic3, sFireR, sColdR, sLightningR, sMagicR, sDiseaseR, sPoisonR, sLightR, sBulk, byAttackRange, bySearchRange, byTracingRange, iMoney, sItem, byDirectAttack, byMagicAttack, byMoneyType)
VALUES (9001, 'Attila the Destroyer', 1400, 150, 0, 0, 0, 2, 0, 0, 5, 0, 0, 83, 500000, 5000, 5000000, 10000, 800, 500, 300, 50, 2500, 1500, 100, 80, 1000, 0, 0, 0, 50, 50, 50, 30, 40, 40, 50, 100, 3, 40, 50, 100000, 9001, 1, 0, 0);

-- Boss 2: Manticore Lord (Level 80)
INSERT INTO K_NPC (sSid, strName, sPid, sSize, iWeapon1, iWeapon2, byGroup, byActType, byType, byFamily, byRank, byTitle, iSellingGroup, sLevel, iExp, iLoyalty, iHpPoint, sMpPoint, sAtk, sAc, sHitRate, sEvadeRate, sDamage, sAttackDelay, bySpeed1, bySpeed2, sStandtime, iMagic1, iMagic2, iMagic3, sFireR, sColdR, sLightningR, sMagicR, sDiseaseR, sPoisonR, sLightR, sBulk, byAttackRange, bySearchRange, byTracingRange, iMoney, sItem, byDirectAttack, byMagicAttack, byMoneyType)
VALUES (9002, 'Manticore Lord', 3800, 140, 0, 0, 0, 2, 0, 0, 4, 0, 0, 80, 350000, 3500, 3500000, 8000, 700, 450, 280, 45, 2000, 1800, 90, 70, 1000, 0, 0, 0, 60, 30, 40, 25, 35, 35, 40, 100, 4, 35, 45, 80000, 9002, 1, 0, 0);

-- Boss 3: Centaur Warlord (Level 78)
INSERT INTO K_NPC (sSid, strName, sPid, sSize, iWeapon1, iWeapon2, byGroup, byActType, byType, byFamily, byRank, byTitle, iSellingGroup, sLevel, iExp, iLoyalty, iHpPoint, sMpPoint, sAtk, sAc, sHitRate, sEvadeRate, sDamage, sAttackDelay, bySpeed1, bySpeed2, sStandtime, iMagic1, iMagic2, iMagic3, sFireR, sColdR, sLightningR, sMagicR, sDiseaseR, sPoisonR, sLightR, sBulk, byAttackRange, bySearchRange, byTracingRange, iMoney, sItem, byDirectAttack, byMagicAttack, byMoneyType)
VALUES (9003, 'Centaur Warlord', 2600, 130, 0, 0, 0, 2, 0, 0, 4, 0, 0, 78, 250000, 2500, 2500000, 6000, 650, 400, 270, 55, 1800, 1600, 110, 90, 1000, 0, 0, 0, 40, 40, 50, 30, 30, 30, 50, 100, 5, 40, 50, 60000, 9003, 1, 0, 0);

-- Boss 4: Golem King (Level 82)
INSERT INTO K_NPC (sSid, strName, sPid, sSize, iWeapon1, iWeapon2, byGroup, byActType, byType, byFamily, byRank, byTitle, iSellingGroup, sLevel, iExp, iLoyalty, iHpPoint, sMpPoint, sAtk, sAc, sHitRate, sEvadeRate, sDamage, sAttackDelay, bySpeed1, bySpeed2, sStandtime, iMagic1, iMagic2, iMagic3, sFireR, sColdR, sLightningR, sMagicR, sDiseaseR, sPoisonR, sLightR, sBulk, byAttackRange, bySearchRange, byTracingRange, iMoney, sItem, byDirectAttack, byMagicAttack, byMoneyType)
VALUES (9004, 'Golem King', 2400, 180, 0, 0, 0, 2, 0, 0, 4, 0, 0, 82, 400000, 4000, 4000000, 5000, 900, 600, 250, 20, 2200, 2000, 60, 50, 1500, 0, 0, 0, 70, 70, 30, 20, 50, 50, 30, 100, 2, 30, 40, 90000, 9004, 1, 0, 0);

-- Boss 5: Troll King (Level 79)
INSERT INTO K_NPC (sSid, strName, sPid, sSize, iWeapon1, iWeapon2, byGroup, byActType, byType, byFamily, byRank, byTitle, iSellingGroup, sLevel, iExp, iLoyalty, iHpPoint, sMpPoint, sAtk, sAc, sHitRate, sEvadeRate, sDamage, sAttackDelay, bySpeed1, bySpeed2, sStandtime, iMagic1, iMagic2, iMagic3, sFireR, sColdR, sLightningR, sMagicR, sDiseaseR, sPoisonR, sLightR, sBulk, byAttackRange, bySearchRange, byTracingRange, iMoney, sItem, byDirectAttack, byMagicAttack, byMoneyType)
VALUES (9005, 'Troll King', 1701, 160, 0, 0, 0, 2, 0, 0, 4, 0, 0, 79, 280000, 2800, 2800000, 7000, 600, 380, 260, 40, 1900, 1700, 85, 70, 1000, 0, 0, 0, 35, 45, 35, 25, 40, 40, 35, 100, 3, 35, 45, 70000, 9005, 1, 0, 0);

-- Boss 6: Shadow Apostle (Level 81)
INSERT INTO K_NPC (sSid, strName, sPid, sSize, iWeapon1, iWeapon2, byGroup, byActType, byType, byFamily, byRank, byTitle, iSellingGroup, sLevel, iExp, iLoyalty, iHpPoint, sMpPoint, sAtk, sAc, sHitRate, sEvadeRate, sDamage, sAttackDelay, bySpeed1, bySpeed2, sStandtime, iMagic1, iMagic2, iMagic3, sFireR, sColdR, sLightningR, sMagicR, sDiseaseR, sPoisonR, sLightR, sBulk, byAttackRange, bySearchRange, byTracingRange, iMoney, sItem, byDirectAttack, byMagicAttack, byMoneyType)
VALUES (9006, 'Shadow Apostle', 2100, 120, 0, 0, 0, 2, 0, 0, 4, 0, 0, 81, 320000, 3200, 3200000, 12000, 550, 350, 290, 60, 2100, 1400, 120, 100, 800, 0, 0, 0, 45, 45, 60, 50, 30, 30, 60, 100, 4, 45, 55, 85000, 9006, 1, 0, 0);

-- Boss 7: Crimson Harpy Queen (Level 77)
INSERT INTO K_NPC (sSid, strName, sPid, sSize, iWeapon1, iWeapon2, byGroup, byActType, byType, byFamily, byRank, byTitle, iSellingGroup, sLevel, iExp, iLoyalty, iHpPoint, sMpPoint, sAtk, sAc, sHitRate, sEvadeRate, sDamage, sAttackDelay, bySpeed1, bySpeed2, sStandtime, iMagic1, iMagic2, iMagic3, sFireR, sColdR, sLightningR, sMagicR, sDiseaseR, sPoisonR, sLightR, sBulk, byAttackRange, bySearchRange, byTracingRange, iMoney, sItem, byDirectAttack, byMagicAttack, byMoneyType)
VALUES (9007, 'Crimson Harpy Queen', 2200, 100, 0, 0, 0, 2, 0, 0, 3, 0, 0, 77, 220000, 2200, 2200000, 9000, 450, 300, 300, 70, 1600, 1200, 130, 110, 700, 0, 0, 0, 30, 30, 50, 40, 25, 25, 50, 100, 6, 50, 60, 55000, 9007, 1, 0, 0);

-- =============================================================================
-- SECTION 2: Insert Loot Tables into K_MONSTER_ITEM
-- =============================================================================
-- sPersent values: 10000 = 100%, 1000 = 10%, 500 = 5%, 100 = 1%
--
-- BALANCE DESIGN based on Boss Rank (byRank):
-- - Rank 5 (Main Boss): 1-3% weapons, 5% armor, 10% scrolls
-- - Rank 4 (Major Boss): 2-5% weapons, 8% armor, 15% scrolls
-- - Rank 3 (Minor Boss): 3-8% weapons, 10% armor, 20% scrolls
--
-- REAL ITEM IDS from Item_Org_us.tbl.csv:
-- Weapons: 126410000 (Mirage 2H), 121210000 (Slayer 1H), 111210000 (Shard Dagger)
-- Armor: 205001000-005 (Chitin), 206001000-005 (Chitin Shell)
-- Scrolls: 379016000 (Upgrade), 379021000 (Blessed Upgrade)

-- Delete existing entries if any
DELETE FROM K_MONSTER_ITEM WHERE sIndex BETWEEN 9001 AND 9007;
GO

-- =============================================================================
-- ATTILA THE DESTROYER (Rank 5 - Main Boss - Lv83 - Lowest drop rates)
-- Drops: Best weapons (Mirage 2H, Slayer), Chitin Shell armor, Blessed scrolls
-- =============================================================================
INSERT INTO K_MONSTER_ITEM (sIndex, iItem01, sPersent01, iItem02, sPersent02, iItem03, sPersent03, iItem04, sPersent04, iItem05, sPersent05)
VALUES (9001,
    126410000, 100,     -- Mirage (2H Sword Lv64) - 1% drop (very rare)
    206001000, 300,     -- Chitin Shell Pauldron - 3% drop
    379021000, 500,     -- Blessed Upgrade Scroll - 5% drop
    121210000, 200,     -- Slayer (1H Sword Lv66) - 2% drop
    205003000, 800      -- Chitin Armor Helmet - 8% drop
);

-- =============================================================================
-- MANTICORE LORD (Rank 4 - Major Boss - Lv80)
-- =============================================================================
INSERT INTO K_MONSTER_ITEM (sIndex, iItem01, sPersent01, iItem02, sPersent02, iItem03, sPersent03, iItem04, sPersent04, iItem05, sPersent05)
VALUES (9002,
    111210000, 200,     -- Shard (Dagger Lv66) - 2% drop
    205001000, 500,     -- Chitin Armor Pauldron - 5% drop
    379016000, 800,     -- Upgrade Scroll - 8% drop
    131110000, 300,     -- Deep Scar (Axe Lv61) - 3% drop
    205002000, 600      -- Chitin Armor Pads - 6% drop
);

-- =============================================================================
-- CENTAUR WARLORD (Rank 4 - Major Boss - Lv78)
-- =============================================================================
INSERT INTO K_MONSTER_ITEM (sIndex, iItem01, sPersent01, iItem02, sPersent02, iItem03, sPersent03, iItem04, sPersent04, iItem05, sPersent05)
VALUES (9003,
    121210000, 300,     -- Slayer (1H Sword Lv66) - 3% drop
    245001000, 600,     -- Rogue Chitin Pauldron - 6% drop
    379016000, 1000,    -- Upgrade Scroll - 10% drop
    141110000, 400,     -- Impact (Mace Lv63) - 4% drop
    245002000, 700      -- Rogue Chitin Pads - 7% drop
);

-- =============================================================================
-- GOLEM KING (Rank 4 - Major Boss - Lv82)
-- Drops more warrior-focused gear
-- =============================================================================
INSERT INTO K_MONSTER_ITEM (sIndex, iItem01, sPersent01, iItem02, sPersent02, iItem03, sPersent03, iItem04, sPersent04, iItem05, sPersent05)
VALUES (9004,
    136210000, 250,     -- Blade Axe (2H Axe Lv61) - 2.5% drop
    206002000, 400,     -- Chitin Shell Pads - 4% drop
    379021000, 600,     -- Blessed Upgrade Scroll - 6% drop
    126410000, 150,     -- Mirage (2H Sword) - 1.5% drop
    206003000, 500      -- Chitin Shell Helmet - 5% drop
);

-- =============================================================================
-- TROLL KING (Rank 4 - Major Boss - Lv79)
-- =============================================================================
INSERT INTO K_MONSTER_ITEM (sIndex, iItem01, sPersent01, iItem02, sPersent02, iItem03, sPersent03, iItem04, sPersent04, iItem05, sPersent05)
VALUES (9005,
    131110000, 400,     -- Deep Scar (Axe Lv61) - 4% drop
    205004000, 700,     -- Chitin Armor Gauntlet - 7% drop
    379016000, 1200,    -- Upgrade Scroll - 12% drop
    141110000, 350,     -- Impact (Mace Lv63) - 3.5% drop
    205005000, 700      -- Chitin Armor Boots - 7% drop
);

-- =============================================================================
-- SHADOW APOSTLE (Rank 4 - Major Boss - Lv81)
-- Drops mixed gear (rogue + caster friendly)
-- =============================================================================
INSERT INTO K_MONSTER_ITEM (sIndex, iItem01, sPersent01, iItem02, sPersent02, iItem03, sPersent03, iItem04, sPersent04, iItem05, sPersent05)
VALUES (9006,
    111210000, 350,     -- Shard (Dagger Lv66) - 3.5% drop
    245003000, 650,     -- Rogue Chitin Helmet - 6.5% drop
    379021000, 700,     -- Blessed Upgrade Scroll - 7% drop
    121210000, 250,     -- Slayer (1H Sword) - 2.5% drop
    245004000, 550      -- Rogue Chitin Gauntlet - 5.5% drop
);

-- =============================================================================
-- CRIMSON HARPY QUEEN (Rank 3 - Minor Boss - Lv77 - Higher drop rates)
-- =============================================================================
INSERT INTO K_MONSTER_ITEM (sIndex, iItem01, sPersent01, iItem02, sPersent02, iItem03, sPersent03, iItem04, sPersent04, iItem05, sPersent05)
VALUES (9007,
    111210000, 500,     -- Shard (Dagger Lv66) - 5% drop
    245005000, 1000,    -- Rogue Chitin Boots - 10% drop
    379016000, 1500,    -- Upgrade Scroll - 15% drop
    131110000, 600,     -- Deep Scar (Axe) - 6% drop
    245001000, 800      -- Rogue Chitin Pauldron - 8% drop
);

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
INSERT INTO K_NPCPOS (ZoneID, NpcID, ActType, RegenType, DungeonFamily, SpecialType, TrapNumber, LeftX, TopZ, RightX, BottomZ, LimitMinZ, LimitMinX, LimitMaxX, LimitMaxZ, NumNPC, RegTime, byDirection, DotCnt, path)
VALUES (72, 9001, 2, 0, 1, 0, 0, 990, 1111, 990, 1111, 0, 0, 0, 0, 1, 7200, 0, 0, '');

-- Manticore Lord in Forgotten Temple (Zone 43) - 1 hour respawn
INSERT INTO K_NPCPOS (ZoneID, NpcID, ActType, RegenType, DungeonFamily, SpecialType, TrapNumber, LeftX, TopZ, RightX, BottomZ, LimitMinZ, LimitMinX, LimitMaxX, LimitMaxZ, NumNPC, RegTime, byDirection, DotCnt, path)
VALUES (43, 9002, 2, 0, 2, 0, 0, 500, 500, 500, 500, 0, 0, 0, 0, 1, 3600, 0, 0, '');

-- Centaur Warlord in El Morad outer area (Zone 11) - 1 hour respawn
INSERT INTO K_NPCPOS (ZoneID, NpcID, ActType, RegenType, DungeonFamily, SpecialType, TrapNumber, LeftX, TopZ, RightX, BottomZ, LimitMinZ, LimitMinX, LimitMaxX, LimitMaxZ, NumNPC, RegTime, byDirection, DotCnt, path)
VALUES (11, 9003, 2, 0, 3, 0, 0, 800, 700, 800, 700, 0, 0, 0, 0, 1, 3600, 0, 0, '');

-- Golem King in Karus outer area (Zone 21) - 1.5 hour respawn
INSERT INTO K_NPCPOS (ZoneID, NpcID, ActType, RegenType, DungeonFamily, SpecialType, TrapNumber, LeftX, TopZ, RightX, BottomZ, LimitMinZ, LimitMinX, LimitMaxX, LimitMaxZ, NumNPC, RegTime, byDirection, DotCnt, path)
VALUES (21, 9004, 2, 0, 4, 0, 0, 600, 800, 600, 800, 0, 0, 0, 0, 1, 5400, 0, 0, '');

-- Troll King in El Morad training area (Zone 1) - 45 min respawn
INSERT INTO K_NPCPOS (ZoneID, NpcID, ActType, RegenType, DungeonFamily, SpecialType, TrapNumber, LeftX, TopZ, RightX, BottomZ, LimitMinZ, LimitMinX, LimitMaxX, LimitMaxZ, NumNPC, RegTime, byDirection, DotCnt, path)
VALUES (1, 9005, 2, 0, 5, 0, 0, 1200, 1000, 1200, 1000, 0, 0, 0, 0, 1, 2700, 0, 0, '');

-- Shadow Apostle in Karus training area (Zone 2) - 45 min respawn
INSERT INTO K_NPCPOS (ZoneID, NpcID, ActType, RegenType, DungeonFamily, SpecialType, TrapNumber, LeftX, TopZ, RightX, BottomZ, LimitMinZ, LimitMinX, LimitMaxX, LimitMaxZ, NumNPC, RegTime, byDirection, DotCnt, path)
VALUES (2, 9006, 2, 0, 6, 0, 0, 1100, 900, 1100, 900, 0, 0, 0, 0, 1, 2700, 0, 0, '');

-- Crimson Harpy Queen in Ronark Land east (Zone 72) - 30 min respawn
INSERT INTO K_NPCPOS (ZoneID, NpcID, ActType, RegenType, DungeonFamily, SpecialType, TrapNumber, LeftX, TopZ, RightX, BottomZ, LimitMinZ, LimitMinX, LimitMaxX, LimitMaxZ, NumNPC, RegTime, byDirection, DotCnt, path)
VALUES (72, 9007, 2, 0, 7, 0, 0, 1300, 800, 1300, 800, 0, 0, 0, 0, 1, 1800, 0, 0, '');

-- =============================================================================
-- VERIFICATION QUERIES
-- =============================================================================
-- Run these to verify the insertions:

-- SELECT sSid, strName, sLevel, iHpPoint FROM K_NPC WHERE sSid >= 9001 AND sSid <= 9007;
-- SELECT * FROM K_MONSTER_ITEM WHERE sIndex >= 9001 AND sIndex <= 9007;
-- SELECT ZoneID, NpcID, RegTime FROM K_NPCPOS WHERE NpcID >= 9001 AND NpcID <= 9007;

PRINT 'Boss monsters script completed successfully!';
PRINT '7 bosses added: Attila, Manticore Lord, Centaur Warlord, Golem King, Troll King, Shadow Apostle, Crimson Harpy Queen';
GO
