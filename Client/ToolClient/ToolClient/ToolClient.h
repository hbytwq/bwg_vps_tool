
// ToolClient.h : PROJECT_NAME Ӧ�ó������ͷ�ļ�
//

#pragma once

#ifndef __AFXWIN_H__
	#error "�ڰ������ļ�֮ǰ������stdafx.h�������� PCH �ļ�"
#endif

#include "resource.h"		// ������


// CToolClientApp:
// �йش����ʵ�֣������ ToolClient.cpp
//

class CToolClientApp : public CWinApp
{
public:
	CToolClientApp();

// ��д
public:
	virtual BOOL InitInstance();

// ʵ��

	DECLARE_MESSAGE_MAP()
};

extern CToolClientApp theApp;