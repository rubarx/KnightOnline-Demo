// MacroManager.h: Skill macro system for automated skill sequences
//
//////////////////////////////////////////////////////////////////////

#if !defined(AFX_MACRO_MANAGER_H__SKILL_MACROS__INCLUDED_)
#define AFX_MACRO_MANAGER_H__SKILL_MACROS__INCLUDED_

#pragma once

#include <cstdint>
#include <string>
#include <vector>

// Maximum number of macro slots
constexpr int MAX_MACROS = 6;

// Maximum skills per macro
constexpr int MAX_SKILLS_PER_MACRO = 10;

// Single skill entry in a macro
struct MacroSkillEntry
{
    uint32_t dwSkillID;   // Skill ID to execute
    float    fDelay;      // Delay after this skill before next (seconds)

    MacroSkillEntry() : dwSkillID(0), fDelay(0.5f) {}
    MacroSkillEntry(uint32_t id, float delay = 0.5f) : dwSkillID(id), fDelay(delay) {}
};

// A complete macro definition
struct SkillMacro
{
    std::string             szName;       // Display name
    std::vector<MacroSkillEntry> skills;  // Skills in sequence
    bool                    bLoop;        // Loop the macro continuously
    bool                    bEnabled;     // Is this macro configured

    SkillMacro() : bLoop(false), bEnabled(false) {}

    void AddSkill(uint32_t dwSkillID, float fDelay = 0.5f)
    {
        if (skills.size() < MAX_SKILLS_PER_MACRO)
        {
            skills.push_back(MacroSkillEntry(dwSkillID, fDelay));
            bEnabled = true;
        }
    }

    void Clear()
    {
        szName.clear();
        skills.clear();
        bLoop = false;
        bEnabled = false;
    }
};

// Macro execution state
enum e_MacroState : uint8_t
{
    MACRO_IDLE = 0,      // Not executing any macro
    MACRO_RUNNING,       // Currently executing a macro
    MACRO_WAITING,       // Waiting for delay between skills
    MACRO_PAUSED         // Manually paused
};

class CMacroManager
{
protected:
    SkillMacro     m_Macros[MAX_MACROS];      // Macro definitions
    e_MacroState   m_eState;                   // Current execution state
    int            m_iCurrentMacro;            // Index of currently running macro (-1 if none)
    int            m_iCurrentStep;             // Current step in macro
    float          m_fNextStepTime;            // Time when next step should execute
    float          m_fLastTickTime;            // Time of last Tick call

    // Execute the current step of the macro
    bool ExecuteCurrentStep();

    // Move to next step
    void AdvanceStep();

    // Check if we can use skills (not dead, not stunned, etc.)
    bool CanExecuteSkills() const;

public:
    CMacroManager();
    ~CMacroManager();

    // Called every frame from GameProcMain::Tick()
    void Tick(float fTime);

    // Macro definition
    void SetMacro(int iSlot, const SkillMacro& macro);
    void ClearMacro(int iSlot);
    SkillMacro& GetMacro(int iSlot) { return m_Macros[iSlot]; }
    const SkillMacro& GetMacro(int iSlot) const { return m_Macros[iSlot]; }

    // Quick setup helpers
    void SetupMacro(int iSlot, const std::string& name, const std::vector<uint32_t>& skillIds, float defaultDelay = 0.5f, bool loop = false);

    // Macro execution
    void StartMacro(int iSlot);
    void StopMacro();
    void PauseMacro();
    void ResumeMacro();
    void ToggleMacro(int iSlot);

    // State queries
    bool IsRunning() const { return m_eState == MACRO_RUNNING || m_eState == MACRO_WAITING; }
    bool IsPaused() const { return m_eState == MACRO_PAUSED; }
    int GetCurrentMacro() const { return m_iCurrentMacro; }
    int GetCurrentStep() const { return m_iCurrentStep; }
    e_MacroState GetState() const { return m_eState; }

    // Default macro presets for common class combos
    void SetupDefaultPresets();
};

#endif // !defined(AFX_MACRO_MANAGER_H__SKILL_MACROS__INCLUDED_)
