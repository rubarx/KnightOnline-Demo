// MacroManager.cpp: Skill macro system implementation
//
//////////////////////////////////////////////////////////////////////

#include "StdAfx.h"
#include "MacroManager.h"
#include "GameProcedure.h"
#include "GameProcMain.h"
#include "PlayerMySelf.h"
#include "MagicSkillMng.h"
#include "GameBase.h"

CMacroManager::CMacroManager()
{
    m_eState = MACRO_IDLE;
    m_iCurrentMacro = -1;
    m_iCurrentStep = 0;
    m_fNextStepTime = 0.0f;
    m_fLastTickTime = 0.0f;

    // Initialize default presets
    SetupDefaultPresets();
}

CMacroManager::~CMacroManager()
{
}

void CMacroManager::SetupDefaultPresets()
{
    // ==========================================================================
    // Default macro presets for common class combos
    // Skill IDs from Skill_Magic_Main_us.tbl
    // Users can customize these via the macro editor UI or chat commands
    // ==========================================================================

    // Macro 1 (Numpad 1): Mage - Ice Combo (PvP focused)
    // Ice arrow → Ice orb → Ice blast → Frost nova
    m_Macros[0].szName = "Mage Ice Combo";
    m_Macros[0].bEnabled = true;
    m_Macros[0].bLoop = false;
    m_Macros[0].AddSkill(109615, 1.5f);  // Ice arrow
    m_Macros[0].AddSkill(109627, 1.5f);  // Ice orb
    m_Macros[0].AddSkill(109635, 1.5f);  // Ice blast
    m_Macros[0].AddSkill(109660, 2.0f);  // Frost nova (AoE finisher)

    // Macro 2 (Numpad 2): Mage - Fire Combo (high damage)
    // Fire ball → Fire spear → Fire blast → Hell fire → Inferno
    m_Macros[1].szName = "Mage Fire Combo";
    m_Macros[1].bEnabled = true;
    m_Macros[1].bLoop = false;
    m_Macros[1].AddSkill(109515, 1.5f);  // Fire ball
    m_Macros[1].AddSkill(109527, 1.5f);  // Fire spear
    m_Macros[1].AddSkill(109535, 1.5f);  // Fire blast
    m_Macros[1].AddSkill(109539, 1.5f);  // Hell fire
    m_Macros[1].AddSkill(109545, 2.0f);  // Inferno (AoE)

    // Macro 3 (Numpad 3): Mage - Lightning Combo (anti-mage)
    // Spark → Lightning → Thunder → Thunder blast → Discharge
    m_Macros[2].szName = "Mage Lightning Combo";
    m_Macros[2].bEnabled = true;
    m_Macros[2].bLoop = false;
    m_Macros[2].AddSkill(109009, 1.5f);  // Spark
    m_Macros[2].AddSkill(109715, 1.5f);  // Lightning
    m_Macros[2].AddSkill(109727, 1.5f);  // Thunder
    m_Macros[2].AddSkill(109735, 1.5f);  // Thunder blast
    m_Macros[2].AddSkill(109739, 2.0f);  // Discharge

    // Macro 4 (Numpad 4): Archer - Burst Combo
    // Guided arrow → Fire shot → Explosive shot → Arrow shower
    m_Macros[3].szName = "Archer Burst";
    m_Macros[3].bEnabled = true;
    m_Macros[3].bLoop = false;
    m_Macros[3].AddSkill(108520, 1.2f);  // Guided arrow (100% hit)
    m_Macros[3].AddSkill(108530, 1.2f);  // Fire shot
    m_Macros[3].AddSkill(108545, 1.2f);  // Explosive shot
    m_Macros[3].AddSkill(108555, 1.5f);  // Arrow shower (5 arrows)

    // Macro 5 (Numpad 5): Rogue - Assassination Combo
    // Stab → Jab → Shock → Thrust → Cut
    m_Macros[4].szName = "Rogue Assassin";
    m_Macros[4].bEnabled = true;
    m_Macros[4].bLoop = false;
    m_Macros[4].AddSkill(108005, 0.8f);  // Stab (150%)
    m_Macros[4].AddSkill(108600, 0.8f);  // Jab
    m_Macros[4].AddSkill(108620, 0.8f);  // Shock
    m_Macros[4].AddSkill(108635, 1.0f);  // Thrust (400%)
    m_Macros[4].AddSkill(108640, 1.0f);  // Cut

    // Macro 6 (Numpad 6): Warrior - Basic Combo
    // Slash → Crash → Thrust
    m_Macros[5].szName = "Warrior Combo";
    m_Macros[5].bEnabled = true;
    m_Macros[5].bLoop = false;
    m_Macros[5].AddSkill(105003, 1.0f);  // Slash (120%)
    m_Macros[5].AddSkill(105005, 1.0f);  // Crash (1.5x hit chance)
    m_Macros[5].AddSkill(105555, 1.2f);  // Thrust (200%, never miss)
}

void CMacroManager::SetupMacro(int iSlot, const std::string& name, const std::vector<uint32_t>& skillIds, float defaultDelay, bool loop)
{
    if (iSlot < 0 || iSlot >= MAX_MACROS)
        return;

    m_Macros[iSlot].Clear();
    m_Macros[iSlot].szName = name;
    m_Macros[iSlot].bLoop = loop;
    m_Macros[iSlot].bEnabled = !skillIds.empty();

    for (uint32_t skillId : skillIds)
    {
        m_Macros[iSlot].AddSkill(skillId, defaultDelay);
    }
}

void CMacroManager::SetMacro(int iSlot, const SkillMacro& macro)
{
    if (iSlot < 0 || iSlot >= MAX_MACROS)
        return;

    m_Macros[iSlot] = macro;
}

void CMacroManager::ClearMacro(int iSlot)
{
    if (iSlot < 0 || iSlot >= MAX_MACROS)
        return;

    m_Macros[iSlot].Clear();
}

bool CMacroManager::CanExecuteSkills() const
{
    CPlayerMySelf* pPlayer = CGameBase::s_pPlayer;
    if (pPlayer == nullptr)
        return false;

    // Cannot use skills if dead
    if (pPlayer->IsDead())
        return false;

    // Cannot use skills if stunned
    if (pPlayer->m_bStun)
        return false;

    // TODO: Add more checks (casting, in trade, etc.)

    return true;
}

void CMacroManager::StartMacro(int iSlot)
{
    if (iSlot < 0 || iSlot >= MAX_MACROS)
        return;

    if (!m_Macros[iSlot].bEnabled || m_Macros[iSlot].skills.empty())
    {
        if (CGameProcedure::s_pProcMain)
            CGameProcedure::s_pProcMain->MsgOutput("Macro slot " + std::to_string(iSlot + 1) + " is not configured.", 0xFFFF3B3B);
        return;
    }

    // Stop any currently running macro
    if (m_eState != MACRO_IDLE)
        StopMacro();

    m_iCurrentMacro = iSlot;
    m_iCurrentStep = 0;
    m_eState = MACRO_RUNNING;
    m_fNextStepTime = 0.0f; // Execute first step immediately

    // Notify player
    if (CGameProcedure::s_pProcMain)
    {
        std::string szMsg = "Macro started: " + m_Macros[iSlot].szName;
        CGameProcedure::s_pProcMain->MsgOutput(szMsg, 0xFF00FF00);
    }
}

void CMacroManager::StopMacro()
{
    if (m_eState == MACRO_IDLE)
        return;

    // Notify player
    if (CGameProcedure::s_pProcMain && m_iCurrentMacro >= 0)
    {
        std::string szMsg = "Macro stopped: " + m_Macros[m_iCurrentMacro].szName;
        CGameProcedure::s_pProcMain->MsgOutput(szMsg, 0xFFFF0000);
    }

    m_eState = MACRO_IDLE;
    m_iCurrentMacro = -1;
    m_iCurrentStep = 0;
    m_fNextStepTime = 0.0f;
}

void CMacroManager::PauseMacro()
{
    if (m_eState == MACRO_RUNNING || m_eState == MACRO_WAITING)
    {
        m_eState = MACRO_PAUSED;

        if (CGameProcedure::s_pProcMain)
            CGameProcedure::s_pProcMain->MsgOutput("Macro paused", 0xFFFFFF00);
    }
}

void CMacroManager::ResumeMacro()
{
    if (m_eState == MACRO_PAUSED)
    {
        m_eState = MACRO_WAITING;
        m_fNextStepTime = m_fLastTickTime; // Resume immediately

        if (CGameProcedure::s_pProcMain)
            CGameProcedure::s_pProcMain->MsgOutput("Macro resumed", 0xFF00FF00);
    }
}

void CMacroManager::ToggleMacro(int iSlot)
{
    // If this macro is already running, stop it
    if (m_iCurrentMacro == iSlot && IsRunning())
    {
        StopMacro();
        return;
    }

    // Otherwise, start this macro
    StartMacro(iSlot);
}

bool CMacroManager::ExecuteCurrentStep()
{
    if (m_iCurrentMacro < 0 || m_iCurrentMacro >= MAX_MACROS)
        return false;

    SkillMacro& macro = m_Macros[m_iCurrentMacro];
    if (m_iCurrentStep < 0 || m_iCurrentStep >= static_cast<int>(macro.skills.size()))
        return false;

    MacroSkillEntry& entry = macro.skills[m_iCurrentStep];

    // Find the skill in the skill table
    __TABLE_UPC_SKILL* pSkill = CGameBase::s_pTbl_Skill.Find(entry.dwSkillID);
    if (pSkill == nullptr)
    {
        // Skill not found, skip to next step
        return false;
    }

    // Execute the skill
    CGameProcMain* pMain = CGameProcedure::s_pProcMain;
    if (pMain == nullptr || pMain->m_pMagicSkillMng == nullptr)
        return false;

    // Use current target for offensive skills, self for buffs
    int iIDTarget = CGameBase::s_pPlayer->m_iIDTarget;
    if (iIDTarget == 0)
        iIDTarget = CGameBase::s_pPlayer->IDNumber(); // Self-target if no target

    bool bSuccess = pMain->m_pMagicSkillMng->MsgSend_MagicProcess(iIDTarget, pSkill);

    return bSuccess;
}

void CMacroManager::AdvanceStep()
{
    if (m_iCurrentMacro < 0 || m_iCurrentMacro >= MAX_MACROS)
        return;

    SkillMacro& macro = m_Macros[m_iCurrentMacro];

    m_iCurrentStep++;

    // Check if macro is complete
    if (m_iCurrentStep >= static_cast<int>(macro.skills.size()))
    {
        if (macro.bLoop)
        {
            // Loop back to start
            m_iCurrentStep = 0;
        }
        else
        {
            // Macro complete
            StopMacro();
        }
    }
}

void CMacroManager::Tick(float fTime)
{
    m_fLastTickTime = fTime;

    if (m_eState == MACRO_IDLE || m_eState == MACRO_PAUSED)
        return;

    if (m_iCurrentMacro < 0 || m_iCurrentMacro >= MAX_MACROS)
    {
        StopMacro();
        return;
    }

    // Check if we can execute skills
    if (!CanExecuteSkills())
    {
        // Player can't use skills right now, wait
        return;
    }

    SkillMacro& macro = m_Macros[m_iCurrentMacro];
    if (macro.skills.empty())
    {
        StopMacro();
        return;
    }

    // Check if it's time to execute the next step
    if (m_eState == MACRO_RUNNING || (m_eState == MACRO_WAITING && fTime >= m_fNextStepTime))
    {
        // Execute current step
        if (ExecuteCurrentStep())
        {
            // Calculate delay for next step
            if (m_iCurrentStep < static_cast<int>(macro.skills.size()))
            {
                float fDelay = macro.skills[m_iCurrentStep].fDelay;
                m_fNextStepTime = fTime + fDelay;
            }
        }

        // Advance to next step
        AdvanceStep();

        // Set state to waiting for next step
        if (m_eState != MACRO_IDLE)
            m_eState = MACRO_WAITING;
    }
}
