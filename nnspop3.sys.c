/* This file was generated by the Hex-Rays decompiler.
   Copyright (c) 2007-2020 Hex-Rays <info@hex-rays.com>

   Detected compiler: Visual C++
*/

#include <windows.h>
#include <defs.h>

#include <stdarg.h>


//-------------------------------------------------------------------------
// Function declarations

__int64 __fastcall sub_11008(__int64 a1, unsigned __int16 a2, __int64 a3);
__int64 __fastcall sub_1102C(__int64 a1, unsigned __int16 a2, __int64 a3, int a4);
__int64 __fastcall sub_11068(__int64 a1);
__int64 __fastcall sub_110CC(__int64 a1, __int64 a2, __int64 a3, __int16 a4, __int64 a5);
__int64 __fastcall sub_11B1C(__int64 a1, IRP *a2);
__int64 sub_123A8(__int64 a1, unsigned __int16 a2, __int64 a3, ...);
__int64 sub_127F8(__int64 a1, unsigned __int16 a2, __int64 a3, ...);
__int64 __fastcall sub_13BB8(__int64 a1, unsigned __int16 a2, __int64 a3, int a4);
__int64 sub_13C18(__int64 a1, unsigned __int16 a2, __int64 a3, ...);
__int64 sub_13C60(__int64 a1, __int64 a2, __int64 a3, ...);
__int64 sub_13CCC(__int64 a1, __int64 a2, __int64 a3, ...);
__int64 sub_13D3C(__int64 a1, __int64 a2, __int64 a3, ...);
__int64 __fastcall sub_13DA0(__int64 a1, unsigned __int16 a2, __int64 a3, int a4);
__int64 __fastcall sub_13DE8(__int64 a1, __int64 a2, __int64 a3, const char *a4);
__int64 __fastcall sub_182D8(_DWORD, _DWORD, _DWORD, _DWORD, _DWORD, __int64); // weak
void *__cdecl memmove(void *Dst, const void *Src, size_t MaxCount);
__int64 __fastcall memset(_QWORD, _QWORD, _QWORD); // weak
// PVOID __stdcall ExAllocatePoolWithTag(POOL_TYPE PoolType, SIZE_T NumberOfBytes, ULONG Tag);
// void __stdcall ExFreePoolWithTag(PVOID P, ULONG Tag);
// NTSTATUS __stdcall IoWMIWriteEvent(PVOID WnodeEventItem);
// void __stdcall IofCompleteRequest(PIRP Irp, CCHAR PriorityBoost);

//-------------------------------------------------------------------------
// Data declarations

_UNKNOWN unk_2AB30; // weak
_UNKNOWN unk_2AB60; // weak
__int64 (__fastcall *qword_2C518)(_QWORD, _QWORD, _QWORD, _QWORD, _QWORD) = NULL; // weak


//----- (0000000000011008) ----------------------------------------------------
__int64 __fastcall sub_11008(__int64 a1, unsigned __int16 a2, __int64 a3)
{
  return qword_2C518(a1, 43i64, a3, a2, 0i64);
}
// 2C518: using guessed type __int64 (__fastcall *qword_2C518)(_QWORD, _QWORD, _QWORD, _QWORD, _QWORD);

//----- (000000000001102C) ----------------------------------------------------
__int64 __fastcall sub_1102C(__int64 a1, unsigned __int16 a2, __int64 a3, int a4)
{
  int v5; // [rsp+68h] [rbp+20h] BYREF

  v5 = a4;
  return qword_2C518(a1, 43i64, a3, a2, &v5);
}
// 2C518: using guessed type __int64 (__fastcall *qword_2C518)(_QWORD, _QWORD, _QWORD, _QWORD, _QWORD);

//----- (0000000000011068) ----------------------------------------------------
__int64 __fastcall sub_11068(__int64 a1)
{
  strlen((const char *)L"\\Device\\NNS_Parser9");
  return qword_2C518(a1, 43i64, &unk_2AB60, 12i64, L"\\Device\\NNS_Parser9");
}
// 2C518: using guessed type __int64 (__fastcall *qword_2C518)(_QWORD, _QWORD, _QWORD, _QWORD, _QWORD);

//----- (00000000000110CC) ----------------------------------------------------
__int64 __fastcall sub_110CC(__int64 a1, __int64 a2, __int64 a3, __int16 a4, __int64 a5)
{
  char *v7; // rsi
  __int64 *v8; // rax
  __int64 v9; // r8
  SIZE_T v10; // rbx
  unsigned __int64 v11; // rcx
  int *v12; // rdx
  __int64 v13; // r9
  char *v15; // rax
  __int64 v16; // rbp
  const void **i; // rdi
  size_t v18; // rbx
  unsigned int v19; // ebx
  __int64 WnodeEventItem[7]; // [rsp+30h] [rbp-D8h] BYREF
  int v21; // [rsp+68h] [rbp-A0h] BYREF
  char *v22; // [rsp+70h] [rbp-98h]
  int v23; // [rsp+78h] [rbp-90h]
  __int16 v24; // [rsp+128h] [rbp+20h] BYREF

  v24 = a4;
  v7 = 0i64;
  memset(WnodeEventItem, 0i64, 48i64);
  WnodeEventItem[1] = a1;
  WnodeEventItem[6] = (__int64)&v24;
  v8 = &a5;
  WnodeEventItem[3] = a3;
  HIDWORD(WnodeEventItem[5]) = 1703936;
  BYTE4(WnodeEventItem[0]) = -1;
  v21 = 2;
  v9 = a5;
  v10 = 0i64;
  v11 = 0i64;
  if ( a5 )
  {
    v12 = &v21;
    do
    {
      v13 = v8[1];
      ++v11;
      v12 += 4;
      v10 += v13;
      if ( v11 <= 7 )
      {
        *((_QWORD *)v12 - 1) = v9;
        *v12 = v13;
      }
      v8 += 2;
      v9 = *v8;
    }
    while ( *v8 );
  }
  if ( v10 > 0x2000 )
    return 3221225473i64;
  if ( v11 <= 7 )
  {
    LOWORD(WnodeEventItem[0]) = 16 * (v11 + 4);
  }
  else
  {
    v15 = (char *)ExAllocatePoolWithTag(NonPagedPool, v10, 0x45435453u);
    v7 = v15;
    if ( !v15 )
      return 3221225495i64;
    v22 = v15;
    v23 = v10;
    v16 = 0i64;
    for ( i = (const void **)&a5; *i; i += 2 )
    {
      v18 = (size_t)i[1];
      memmove(&v7[v16], *i, v18);
      v16 += v18;
    }
    LOWORD(WnodeEventItem[0]) = 80;
  }
  v19 = IoWMIWriteEvent(WnodeEventItem);
  if ( v7 )
    ExFreePoolWithTag(v7, 0);
  return v19;
}
// 29A60: using guessed type __int64 __fastcall memset(_QWORD, _QWORD, _QWORD);

//----- (0000000000011B1C) ----------------------------------------------------
__int64 __fastcall sub_11B1C(__int64 a1, IRP *a2)
{
  a2->IoStatus.Status = 0;
  a2->IoStatus.Information = 0i64;
  IofCompleteRequest(a2, 0);
  return 0i64;
}

//----- (00000000000123A8) ----------------------------------------------------
__int64 sub_123A8(__int64 a1, unsigned __int16 a2, __int64 a3, ...)
{
  va_list va; // [rsp+68h] [rbp+20h] BYREF

  va_start(va, a3);
  return qword_2C518(a1, 43i64, a3, a2, (__int64 *)va);
}
// 2C518: using guessed type __int64 (__fastcall *qword_2C518)(_QWORD, _QWORD, _QWORD, _QWORD, _QWORD);

//----- (00000000000127F8) ----------------------------------------------------
__int64 sub_127F8(__int64 a1, unsigned __int16 a2, __int64 a3, ...)
{
  va_list va; // [rsp+78h] [rbp+20h] BYREF

  va_start(va, a3);
  return qword_2C518(a1, 43i64, a3, a2, (__int64 *)va);
}
// 2C518: using guessed type __int64 (__fastcall *qword_2C518)(_QWORD, _QWORD, _QWORD, _QWORD, _QWORD);

//----- (0000000000013BB8) ----------------------------------------------------
__int64 __fastcall sub_13BB8(__int64 a1, unsigned __int16 a2, __int64 a3, int a4)
{
  int v5; // [rsp+88h] [rbp+20h] BYREF

  v5 = a4;
  return qword_2C518(a1, 43i64, &unk_2AB30, a2, &v5);
}
// 2C518: using guessed type __int64 (__fastcall *qword_2C518)(_QWORD, _QWORD, _QWORD, _QWORD, _QWORD);

//----- (0000000000013C18) ----------------------------------------------------
__int64 sub_13C18(__int64 a1, unsigned __int16 a2, __int64 a3, ...)
{
  va_list va; // [rsp+78h] [rbp+20h] BYREF

  va_start(va, a3);
  return qword_2C518(a1, 43i64, a3, a2, (__int64 *)va);
}
// 2C518: using guessed type __int64 (__fastcall *qword_2C518)(_QWORD, _QWORD, _QWORD, _QWORD, _QWORD);

//----- (0000000000013C60) ----------------------------------------------------
__int64 sub_13C60(__int64 a1, __int64 a2, __int64 a3, ...)
{
  va_list va; // [rsp+98h] [rbp+20h] BYREF

  va_start(va, a3);
  return qword_2C518(a1, 43i64, &unk_2AB30, 66i64, (__int64 *)va);
}
// 2C518: using guessed type __int64 (__fastcall *qword_2C518)(_QWORD, _QWORD, _QWORD, _QWORD, _QWORD);

//----- (0000000000013CCC) ----------------------------------------------------
__int64 sub_13CCC(__int64 a1, __int64 a2, __int64 a3, ...)
{
  va_list va; // [rsp+98h] [rbp+20h] BYREF

  va_start(va, a3);
  return qword_2C518(a1, 43i64, &unk_2AB30, 84i64, (__int64 *)va);
}
// 2C518: using guessed type __int64 (__fastcall *qword_2C518)(_QWORD, _QWORD, _QWORD, _QWORD, _QWORD);

//----- (0000000000013D3C) ----------------------------------------------------
__int64 sub_13D3C(__int64 a1, __int64 a2, __int64 a3, ...)
{
  va_list va; // [rsp+88h] [rbp+20h] BYREF

  va_start(va, a3);
  return qword_2C518(a1, 43i64, &unk_2AB30, 105i64, (__int64 *)va);
}
// 2C518: using guessed type __int64 (__fastcall *qword_2C518)(_QWORD, _QWORD, _QWORD, _QWORD, _QWORD);

//----- (0000000000013DA0) ----------------------------------------------------
__int64 __fastcall sub_13DA0(__int64 a1, unsigned __int16 a2, __int64 a3, int a4)
{
  int v5; // [rsp+78h] [rbp+20h] BYREF

  v5 = a4;
  return qword_2C518(a1, 43i64, a3, a2, &v5);
}
// 2C518: using guessed type __int64 (__fastcall *qword_2C518)(_QWORD, _QWORD, _QWORD, _QWORD, _QWORD);

//----- (0000000000013DE8) ----------------------------------------------------
__int64 __fastcall sub_13DE8(__int64 a1, __int64 a2, __int64 a3, const char *a4)
{
  const char *v5; // rax

  if ( a4 )
    strlen(a4);
  v5 = "NULL";
  if ( a4 )
    v5 = a4;
  return qword_2C518(a1, 43i64, &unk_2AB30, 35i64, v5);
}
// 2C518: using guessed type __int64 (__fastcall *qword_2C518)(_QWORD, _QWORD, _QWORD, _QWORD, _QWORD);

//----- (00000000000182D8) ----------------------------------------------------
#error "182D8: decompilation has been cancelled (funcsize=6068)"

// nfuncs=171 queued=170 decompiled=170 lumina nreq=0 worse=0 better=0
// Cancelled by the user
