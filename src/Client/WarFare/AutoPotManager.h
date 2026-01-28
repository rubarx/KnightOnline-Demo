// AutoPotManager.h: Automatic potion usage system
//
//////////////////////////////////////////////////////////////////////

#if !defined(AFX_AUTOPOT_MANAGER_H__AUTO_POT_SYSTEM__INCLUDED_)
#define AFX_AUTOPOT_MANAGER_H__AUTO_POT_SYSTEM__INCLUDED_

#pragma once

#include <cstdint>

// Potion types
enum e_PotionType : uint8_t
{
    POTION_HP = 0,
    POTION_MP = 1,
    POTION_TYPE_COUNT = 2
};

// Auto-pot configuration
struct AutoPotConfig
{
    bool  bEnabled;       // Is auto-pot enabled for this type
    int   iThreshold;     // Percentage threshold (0-100)
    float fCooldown;      // Cooldown between uses (seconds)
    float fLastUseTime;   // Time of last use (for cooldown tracking)

    AutoPotConfig() : bEnabled(false), iThreshold(50), fCooldown(1.0f), fLastUseTime(0.0f) {}
};

class CAutoPotManager
{
protected:
    AutoPotConfig m_Config[POTION_TYPE_COUNT];
    bool          m_bSystemEnabled;  // Master toggle for entire system

    // Find the best potion in inventory for the given type
    // Returns inventory slot index, or -1 if not found
    int FindPotionSlot(e_PotionType eType) const;

    // Use potion from the given inventory slot
    bool UsePotion(int iSlot);

    // Check if we should use a potion of this type
    bool ShouldUsePotion(e_PotionType eType) const;

    // Get current HP/MP percentage
    int GetCurrentPercentage(e_PotionType eType) const;

public:
    CAutoPotManager();
    ~CAutoPotManager();

    // Called every frame from GameProcMain::Tick()
    void Tick(float fTime);

    // Enable/disable the entire system
    void SetEnabled(bool bEnabled);
    bool IsEnabled() const { return m_bSystemEnabled; }
    void ToggleEnabled();

    // Configure HP auto-pot
    void SetHPEnabled(bool bEnabled) { m_Config[POTION_HP].bEnabled = bEnabled; }
    void SetHPThreshold(int iPercent);
    void SetHPCooldown(float fSeconds) { m_Config[POTION_HP].fCooldown = fSeconds; }

    // Configure MP auto-pot
    void SetMPEnabled(bool bEnabled) { m_Config[POTION_MP].bEnabled = bEnabled; }
    void SetMPThreshold(int iPercent);
    void SetMPCooldown(float fSeconds) { m_Config[POTION_MP].fCooldown = fSeconds; }

    // Get current settings
    bool IsHPEnabled() const { return m_Config[POTION_HP].bEnabled; }
    int  GetHPThreshold() const { return m_Config[POTION_HP].iThreshold; }
    bool IsMPEnabled() const { return m_Config[POTION_MP].bEnabled; }
    int  GetMPThreshold() const { return m_Config[POTION_MP].iThreshold; }
};

#endif // !defined(AFX_AUTOPOT_MANAGER_H__AUTO_POT_SYSTEM__INCLUDED_)
