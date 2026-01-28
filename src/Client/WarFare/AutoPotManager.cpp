// AutoPotManager.cpp: Automatic potion usage system implementation
//
//////////////////////////////////////////////////////////////////////

#include "StdAfx.h"
#include "AutoPotManager.h"
#include "GameProcedure.h"
#include "GameProcMain.h"
#include "PlayerMySelf.h"
#include "UIInventory.h"
#include "MagicSkillMng.h"
#include "GameBase.h"

// Item class for potions (ITEM_CLASS_POTION already defined in ItemDef.h)
// constexpr uint8_t ITEM_CLASS_POTION = 97;

// HP potion item ID ranges (from Item_Org_us.tbl)
// 389010000 - Holy water (HP Recovery)
// 389011000 - Water of life (90HP)
// 389012000 - Water of love (180HP)
// 389013000 - Water of grace (360HP)
// 389014000 - Water of favors (720HP)
// 389015000 - Water of favor (1440HP)
constexpr uint32_t HP_POTION_ID_MIN = 389010000;
constexpr uint32_t HP_POTION_ID_MAX = 389015999;

// MP potion item ID ranges (from Item_Org_us.tbl)
// 389016000 - Potion of spirit (120MP)
// 389017000 - Potion of intelligence (240MP)
// 389018000 - Potion of sagacity (480MP)
// 389019000 - Potion of wisdom (960MP)
// 389020000 - Potion of soul (1920MP)
constexpr uint32_t MP_POTION_ID_MIN = 389016000;
constexpr uint32_t MP_POTION_ID_MAX = 389020999;

// Alternative: Check item name prefixes (for servers with different item IDs)
static bool IsHPPotion(__TABLE_ITEM_BASIC* pItem)
{
    if (pItem == nullptr || pItem->byClass != ITEM_CLASS_POTION)
        return false;

    // Check by ID range
    uint32_t dwID = pItem->dwID;
    if (dwID >= HP_POTION_ID_MIN && dwID <= HP_POTION_ID_MAX)
        return true;

    // Check by name (contains "HP" or "Health" or "Life")
    const std::string& szName = pItem->szName;
    if (szName.find("HP") != std::string::npos ||
        szName.find("Health") != std::string::npos ||
        szName.find("Life") != std::string::npos ||
        szName.find("체력") != std::string::npos)  // Korean for HP
        return true;

    return false;
}

static bool IsMPPotion(__TABLE_ITEM_BASIC* pItem)
{
    if (pItem == nullptr || pItem->byClass != ITEM_CLASS_POTION)
        return false;

    // Check by ID range
    uint32_t dwID = pItem->dwID;
    if (dwID >= MP_POTION_ID_MIN && dwID <= MP_POTION_ID_MAX)
        return true;

    // Check by name (contains "MP" or "Mana" or "Magic")
    const std::string& szName = pItem->szName;
    if (szName.find("MP") != std::string::npos ||
        szName.find("Mana") != std::string::npos ||
        szName.find("Magic") != std::string::npos ||
        szName.find("마나") != std::string::npos)  // Korean for Mana
        return true;

    return false;
}

CAutoPotManager::CAutoPotManager()
{
    m_bSystemEnabled = false;

    // Default HP auto-pot: 50% threshold, 1.0s cooldown
    m_Config[POTION_HP].bEnabled = true;
    m_Config[POTION_HP].iThreshold = 50;
    m_Config[POTION_HP].fCooldown = 1.0f;
    m_Config[POTION_HP].fLastUseTime = 0.0f;

    // Default MP auto-pot: 30% threshold, 1.0s cooldown
    m_Config[POTION_MP].bEnabled = true;
    m_Config[POTION_MP].iThreshold = 30;
    m_Config[POTION_MP].fCooldown = 1.0f;
    m_Config[POTION_MP].fLastUseTime = 0.0f;
}

CAutoPotManager::~CAutoPotManager()
{
}

void CAutoPotManager::SetEnabled(bool bEnabled)
{
    m_bSystemEnabled = bEnabled;

    // Notify player
    std::string szMsg;
    if (bEnabled)
        szMsg = "Auto-Pot System: ENABLED (HP: " + std::to_string(m_Config[POTION_HP].iThreshold) +
                "%, MP: " + std::to_string(m_Config[POTION_MP].iThreshold) + "%)";
    else
        szMsg = "Auto-Pot System: DISABLED";

    if (CGameProcedure::s_pProcMain)
        CGameProcedure::s_pProcMain->MsgOutput(szMsg, bEnabled ? 0xFF00FF00 : 0xFFFF0000);
}

void CAutoPotManager::ToggleEnabled()
{
    SetEnabled(!m_bSystemEnabled);
}

void CAutoPotManager::SetHPThreshold(int iPercent)
{
    if (iPercent < 10) iPercent = 10;
    if (iPercent > 90) iPercent = 90;
    m_Config[POTION_HP].iThreshold = iPercent;
}

void CAutoPotManager::SetMPThreshold(int iPercent)
{
    if (iPercent < 10) iPercent = 10;
    if (iPercent > 90) iPercent = 90;
    m_Config[POTION_MP].iThreshold = iPercent;
}

int CAutoPotManager::GetCurrentPercentage(e_PotionType eType) const
{
    CPlayerMySelf* pPlayer = CGameBase::s_pPlayer;
    if (pPlayer == nullptr)
        return 100;

    if (eType == POTION_HP)
    {
        if (pPlayer->m_InfoBase.iHPMax <= 0)
            return 100;
        return (pPlayer->m_InfoBase.iHP * 100) / pPlayer->m_InfoBase.iHPMax;
    }
    else if (eType == POTION_MP)
    {
        if (pPlayer->m_InfoBase.iMPMax <= 0)
            return 100;
        return (pPlayer->m_InfoBase.iMP * 100) / pPlayer->m_InfoBase.iMPMax;
    }

    return 100;
}

bool CAutoPotManager::ShouldUsePotion(e_PotionType eType) const
{
    if (!m_bSystemEnabled)
        return false;

    if (!m_Config[eType].bEnabled)
        return false;

    // Check threshold
    int iCurrentPercent = GetCurrentPercentage(eType);
    if (iCurrentPercent > m_Config[eType].iThreshold)
        return false;

    return true;
}

int CAutoPotManager::FindPotionSlot(e_PotionType eType) const
{
    if (CGameProcedure::s_pProcMain == nullptr)
        return -1;

    CUIInventory* pInv = CGameProcedure::s_pProcMain->m_pUIInventory;
    if (pInv == nullptr)
        return -1;

    // Search inventory for matching potion
    for (int i = 0; i < MAX_ITEM_INVENTORY; i++)
    {
        __IconItemSkill* pItem = pInv->m_pMyInvWnd[i];
        if (pItem == nullptr)
            continue;

        __TABLE_ITEM_BASIC* pItemBasic = pItem->pItemBasic;
        if (pItemBasic == nullptr)
            continue;

        // Check if this is the right type of potion
        if (eType == POTION_HP && IsHPPotion(pItemBasic))
            return i;
        else if (eType == POTION_MP && IsMPPotion(pItemBasic))
            return i;
    }

    return -1;
}

bool CAutoPotManager::UsePotion(int iSlot)
{
    if (iSlot < 0 || iSlot >= MAX_ITEM_INVENTORY)
        return false;

    CGameProcMain* pMain = CGameProcedure::s_pProcMain;
    if (pMain == nullptr)
        return false;

    CUIInventory* pInv = pMain->m_pUIInventory;
    if (pInv == nullptr)
        return false;

    __IconItemSkill* pItem = pInv->m_pMyInvWnd[iSlot];
    if (pItem == nullptr || pItem->pItemBasic == nullptr)
        return false;

    // Get the skill associated with this item
    __TABLE_UPC_SKILL* pSkill = CGameBase::s_pTbl_Skill.Find(pItem->pItemBasic->dwEffectID1);
    if (pSkill == nullptr)
        return false;

    // Use the skill (self-target for potions)
    int iIDTarget = CGameBase::s_pPlayer->IDNumber();
    return pMain->m_pMagicSkillMng->MsgSend_MagicProcess(iIDTarget, pSkill);
}

void CAutoPotManager::Tick(float fTime)
{
    if (!m_bSystemEnabled)
        return;

    CPlayerMySelf* pPlayer = CGameBase::s_pPlayer;
    if (pPlayer == nullptr)
        return;

    // Don't auto-pot if dead
    if (pPlayer->IsDead())
        return;

    // Don't auto-pot if stunned
    if (pPlayer->m_bStun)
        return;

    // Check HP
    if (ShouldUsePotion(POTION_HP))
    {
        // Check cooldown
        if (fTime - m_Config[POTION_HP].fLastUseTime >= m_Config[POTION_HP].fCooldown)
        {
            int iSlot = FindPotionSlot(POTION_HP);
            if (iSlot >= 0 && UsePotion(iSlot))
            {
                m_Config[POTION_HP].fLastUseTime = fTime;
            }
        }
    }

    // Check MP
    if (ShouldUsePotion(POTION_MP))
    {
        // Check cooldown
        if (fTime - m_Config[POTION_MP].fLastUseTime >= m_Config[POTION_MP].fCooldown)
        {
            int iSlot = FindPotionSlot(POTION_MP);
            if (iSlot >= 0 && UsePotion(iSlot))
            {
                m_Config[POTION_MP].fLastUseTime = fTime;
            }
        }
    }
}
