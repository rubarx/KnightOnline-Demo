// UITownButtons.h: interface for the UITownButtons class.
// Simple town teleport button that executes /town command
//
//////////////////////////////////////////////////////////////////////

#if !defined(AFX_UITownButtons_H__TOWN_TELEPORT_BUTTONS__INCLUDED_)
#define AFX_UITownButtons_H__TOWN_TELEPORT_BUTTONS__INCLUDED_

#pragma once

#include <N3Base/N3UIBase.h>

class CUITownButtons : public CN3UIBase
{
protected:
    class CN3UIButton* m_pBtn_Town;
    bool m_bLoaded;

public:
    CUITownButtons();
    ~CUITownButtons() override;

    bool Load(File& file) override;
    bool ReceiveMessage(CN3UIBase* pSender, uint32_t dwMsg) override;

    bool IsLoaded() const { return m_bLoaded; }
};

#endif // !defined(AFX_UITownButtons_H__TOWN_TELEPORT_BUTTONS__INCLUDED_)
