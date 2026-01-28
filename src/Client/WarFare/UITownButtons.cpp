// UITownButtons.cpp: implementation of the UITownButtons class.
// Simple town teleport button that executes /town command
//
//////////////////////////////////////////////////////////////////////

#include "StdAfx.h"
#include "UITownButtons.h"
#include "GameProcMain.h"

#include <N3Base/N3UIButton.h>

CUITownButtons::CUITownButtons()
{
    m_pBtn_Town = nullptr;
    m_bLoaded = false;
}

CUITownButtons::~CUITownButtons()
{
}

bool CUITownButtons::Load(File& file)
{
    if (!CN3UIBase::Load(file))
        return false;

    // Get the town button by ID
    m_pBtn_Town = GetChildByID<CN3UIButton>("Btn_Town");

    if (m_pBtn_Town != nullptr)
    {
        m_bLoaded = true;
    }

    return true;
}

bool CUITownButtons::ReceiveMessage(CN3UIBase* pSender, uint32_t dwMsg)
{
    if (dwMsg & UIMSG_BUTTON_CLICK)
    {
        if (pSender == m_pBtn_Town)
        {
            // Execute /town command
            if (CGameProcedure::s_pProcMain)
            {
                CGameProcedure::s_pProcMain->ParseChattingCommand("/town");
            }
            return true;
        }
    }

    return true;
}
