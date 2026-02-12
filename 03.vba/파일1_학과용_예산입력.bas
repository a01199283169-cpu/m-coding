'###############################################################################
'#                                                                             #
'#                 【파일1】 학과용 예산사용현황 입력 시스템                      #
'#                                                                             #
'#   각 학과 담당자가 사용하는 파일입니다.                                       #
'#   예산 집행 내역을 입력하고 공유폴더에 CSV로 저장합니다.                       #
'#                                                                             #
'#   [시트 구성]                                                                #
'#   - 설정: 학과명, 담당자명, 공유폴더 경로                                    #
'#   - 입력: 예산액/총지출액/현재잔액 + 지출내역 입력                           #
'#                                                                             #
'#   [사용법]                                                                   #
'#   1. Excel에서 Alt+F11 (VBA 편집기 열기)                                    #
'#   2. [삽입] → [모듈] 클릭                                                   #
'#   3. 이 코드 전체를 붙여넣기                                                 #
'#   4. Alt+F8 → "초기설정" 선택 → 실행                                        #
'#                                                                             #
'###############################################################################

Option Explicit

'===============================================================================
' 상수 정의
'===============================================================================
Private Const WS_SET As String = "설정"
Private Const WS_INP As String = "입력"

'===============================================================================
' 초기 설정 (최초 1회 실행)
'===============================================================================
Public Sub 초기설정()
    Dim wsSet As Worksheet, wsInp As Worksheet

    Application.ScreenUpdating = False

    ' ===== 설정 시트 생성 =====
    Set wsSet = GetSheet(WS_SET)
    With wsSet
        .Cells.Clear

        ' 헤더
        .Range("A1:B1").Value = Array("항목", "값")
        FormatHeader .Range("A1:B1"), RGB(70, 130, 180)

        ' 설정 항목
        .Range("A2").Value = "학과명"
        .Range("A3").Value = "담당자명"
        .Range("A4").Value = "공유폴더"

        .Range("B2").Value = "(학과명 입력)"
        .Range("B3").Value = "(담당자명 입력)"
        .Range("B4").Value = "(폴더선택 버튼 클릭)"
        .Range("B2:B4").Font.Color = RGB(150, 150, 150)

        ' 서식
        .Range("A1:B4").Borders.LineStyle = xlContinuous
        .Columns("A").ColumnWidth = 15
        .Columns("B").ColumnWidth = 40
    End With

    ' ===== 입력 시트 생성 =====
    Set wsInp = GetSheet(WS_INP)
    With wsInp
        .Cells.Clear

        ' ----- 예산 요약 영역 -----
        .Range("A1:C1").Value = Array("예산액", "총지출액", "현재잔액")
        FormatHeader .Range("A1:C1"), RGB(192, 80, 77)

        .Range("A2").Value = 0
        .Range("B2").Formula = "=SUMIF(C:C,"">0"",C:C)"
        .Range("C2").Formula = "=A2-B2"

        .Range("A2:C2").NumberFormat = "#,##0"
        .Range("A2:C2").Font.Size = 14
        .Range("A2:C2").Font.Bold = True
        .Range("A1:C2").Borders.LineStyle = xlContinuous

        ' ----- 지출내역 헤더 -----
        .Range("A4:G4").Value = Array("날짜", "세부항목", "금액", "적요", "관련문서번호", "비고", "입력일시")
        FormatHeader .Range("A4:G4"), RGB(70, 130, 180)

        ' ----- 열 너비 및 서식 -----
        .Columns("A").ColumnWidth = 12
        .Columns("B").ColumnWidth = 20
        .Columns("C").ColumnWidth = 15
        .Columns("D").ColumnWidth = 25
        .Columns("E").ColumnWidth = 15
        .Columns("F").ColumnWidth = 15
        .Columns("G").ColumnWidth = 18

        .Columns("A").NumberFormat = "YYYY-MM-DD"
        .Columns("C").NumberFormat = "#,##0"
        .Columns("G").NumberFormat = "YYYY-MM-DD HH:MM:SS"

        .Rows(4).RowHeight = 22
        .Activate
        .Range("A5").Select
    End With

    ' 버튼 생성
    CreateButtons

    Application.ScreenUpdating = True

    MsgBox "초기 설정 완료!" & vbLf & vbLf & _
           "1. [설정] 시트에서 학과정보 입력" & vbLf & _
           "2. [입력] 시트에서 예산액 입력" & vbLf & _
           "3. 지출내역 작성 후 [공유폴더 저장] 클릭", vbInformation
End Sub

'===============================================================================
' 버튼 생성
'===============================================================================
Private Sub CreateButtons()
    Dim wsSet As Worksheet, wsInp As Worksheet, shp As Shape

    Set wsSet = ThisWorkbook.Worksheets(WS_SET)
    Set wsInp = ThisWorkbook.Worksheets(WS_INP)

    ' 기존 버튼 삭제
    For Each shp In wsSet.Shapes
        If Left(shp.Name, 3) = "btn" Then shp.Delete
    Next
    For Each shp In wsInp.Shapes
        If Left(shp.Name, 3) = "btn" Then shp.Delete
    Next

    ' 설정 시트 버튼
    AddButton wsSet, "btn1", "폴더 선택", "D2", 100, 28, RGB(70, 130, 180), "폴더선택"
    AddButton wsSet, "btn2", "입력시트 이동", "D4", 100, 28, RGB(100, 150, 100), "GoInput"

    ' 입력 시트 버튼
    AddButton wsInp, "btn1", "공유폴더 저장", "E1", 110, 35, RGB(70, 130, 180), "데이터저장"
    AddButton wsInp, "btn2", "새 행 추가", "F1", 90, 35, RGB(100, 150, 100), "새행추가"
    AddButton wsInp, "btn3", "데이터 초기화", "G1", 100, 35, RGB(200, 100, 80), "데이터초기화"
    AddButton wsInp, "btn4", "설정시트 이동", "H1", 100, 35, RGB(128, 128, 128), "GoSet"
End Sub

Private Sub AddButton(ws As Worksheet, nm As String, cap As String, pos As String, _
                      w As Double, h As Double, clr As Long, act As String)
    Dim shp As Shape, rng As Range
    Set rng = ws.Range(pos)
    Set shp = ws.Shapes.AddShape(msoShapeRoundedRectangle, rng.Left + 5, rng.Top + 2, w, h)

    With shp
        .Name = nm
        .Fill.ForeColor.RGB = clr
        .Line.Visible = msoFalse
        .TextFrame2.TextRange.Text = cap
        .TextFrame2.TextRange.Font.Fill.ForeColor.RGB = vbWhite
        .TextFrame2.TextRange.Font.Size = 10
        .TextFrame2.TextRange.Font.Bold = msoTrue
        .TextFrame2.TextRange.ParagraphFormat.Alignment = msoAlignCenter
        .TextFrame2.VerticalAnchor = msoAnchorMiddle
        .OnAction = act
    End With
End Sub

'===============================================================================
' 폴더 선택 다이얼로그
'===============================================================================
Public Sub 폴더선택()
    Dim fd As FileDialog, wsSet As Worksheet
    Set fd = Application.FileDialog(msoFileDialogFolderPicker)

    With fd
        .Title = "공유폴더를 선택하세요"
        .InitialFileName = "C:\"
        If .Show = -1 Then
            Set wsSet = ThisWorkbook.Worksheets(WS_SET)
            wsSet.Range("B4").Value = .SelectedItems(1) & "\"
            wsSet.Range("B4").Font.Color = vbBlack
            MsgBox "폴더가 설정되었습니다." & vbLf & .SelectedItems(1), vbInformation
        End If
    End With
End Sub

'===============================================================================
' 공유폴더에 데이터 저장 (CSV)
'===============================================================================
Public Sub 데이터저장()
    Dim wsSet As Worksheet, wsInp As Worksheet
    Dim strPath As String, strFile As String, strDept As String
    Dim lastRow As Long, i As Long, fNum As Integer
    Dim dblBudget As Double, dblSpent As Double, dblBalance As Double

    Set wsSet = ThisWorkbook.Worksheets(WS_SET)
    Set wsInp = ThisWorkbook.Worksheets(WS_INP)

    ' ----- 유효성 검사 -----
    strDept = Trim(wsSet.Range("B2").Value)
    strPath = Trim(wsSet.Range("B4").Value)

    If strDept = "" Or InStr(strDept, "입력") > 0 Then
        MsgBox "학과명을 입력해주세요.", vbExclamation
        wsSet.Activate
        wsSet.Range("B2").Select
        Exit Sub
    End If

    If strPath = "" Or InStr(strPath, "클릭") > 0 Then
        MsgBox "공유폴더를 선택해주세요.", vbExclamation
        wsSet.Activate
        Exit Sub
    End If

    If Right(strPath, 1) <> "\" Then strPath = strPath & "\"

    If Dir(strPath, vbDirectory) = "" Then
        MsgBox "폴더를 찾을 수 없습니다:" & vbLf & strPath, vbExclamation
        Exit Sub
    End If

    lastRow = wsInp.Cells(wsInp.Rows.Count, "A").End(xlUp).Row
    If lastRow < 5 Then
        MsgBox "저장할 지출내역이 없습니다.", vbInformation
        Exit Sub
    End If

    ' ----- 예산 정보 -----
    dblBudget = Val(wsInp.Range("A2").Value)
    dblSpent = Val(wsInp.Range("B2").Value)
    dblBalance = Val(wsInp.Range("C2").Value)

    ' ----- CSV 파일 저장 -----
    strFile = strPath & strDept & "_예산현황.csv"
    fNum = FreeFile
    Open strFile For Output As #fNum

    ' 헤더 + 예산정보
    Print #fNum, "학과명,담당자,예산액,총지출액,현재잔액"
    Print #fNum, Q(strDept) & "," & Q(wsSet.Range("B3").Value) & "," & _
                 dblBudget & "," & dblSpent & "," & dblBalance
    Print #fNum, ""
    Print #fNum, "날짜,세부항목,금액,적요,관련문서번호,비고,입력일시"

    ' 지출 데이터
    For i = 5 To lastRow
        If wsInp.Cells(i, 1).Value <> "" Then
            Print #fNum, Q(Format(wsInp.Cells(i, 1).Value, "YYYY-MM-DD")) & "," & _
                         Q(wsInp.Cells(i, 2).Value) & "," & _
                         wsInp.Cells(i, 3).Value & "," & _
                         Q(wsInp.Cells(i, 4).Value) & "," & _
                         Q(wsInp.Cells(i, 5).Value) & "," & _
                         Q(wsInp.Cells(i, 6).Value) & "," & _
                         Q(Format(Now, "YYYY-MM-DD HH:MM:SS"))
        End If
    Next i

    Close #fNum

    MsgBox "저장 완료!" & vbLf & vbLf & _
           "파일: " & strFile & vbLf & _
           "건수: " & (lastRow - 4) & "건", vbInformation
End Sub

' CSV용 따옴표 처리
Private Function Q(s As String) As String
    Q = Chr(34) & s & Chr(34)
End Function

'===============================================================================
' 새 행 추가
'===============================================================================
Public Sub 새행추가()
    Dim wsInp As Worksheet, r As Long
    Set wsInp = ThisWorkbook.Worksheets(WS_INP)

    r = wsInp.Cells(wsInp.Rows.Count, "A").End(xlUp).Row + 1
    If r < 5 Then r = 5

    wsInp.Cells(r, 1).Value = Date
    wsInp.Cells(r, 7).Value = Now
    wsInp.Cells(r, 2).Select
End Sub

'===============================================================================
' 데이터 초기화
'===============================================================================
Public Sub 데이터초기화()
    Dim wsInp As Worksheet, lastRow As Long
    Set wsInp = ThisWorkbook.Worksheets(WS_INP)

    lastRow = wsInp.Cells(wsInp.Rows.Count, "A").End(xlUp).Row
    If lastRow < 5 Then
        MsgBox "삭제할 데이터가 없습니다.", vbInformation
        Exit Sub
    End If

    If MsgBox("모든 지출내역을 삭제하시겠습니까?", vbQuestion + vbYesNo) = vbYes Then
        wsInp.Range("A5:G" & lastRow).ClearContents
        MsgBox "초기화되었습니다.", vbInformation
    End If
End Sub

'===============================================================================
' 시트 이동
'===============================================================================
Public Sub GoInput()
    ThisWorkbook.Worksheets(WS_INP).Activate
End Sub

Public Sub GoSet()
    ThisWorkbook.Worksheets(WS_SET).Activate
End Sub

'===============================================================================
' 유틸리티 함수
'===============================================================================
Private Function GetSheet(nm As String) As Worksheet
    On Error Resume Next
    Set GetSheet = ThisWorkbook.Worksheets(nm)
    If GetSheet Is Nothing Then
        Set GetSheet = ThisWorkbook.Worksheets.Add(After:=ThisWorkbook.Worksheets(ThisWorkbook.Worksheets.Count))
        GetSheet.Name = nm
    End If
End Function

Private Sub FormatHeader(rng As Range, clr As Long)
    With rng
        .Font.Bold = True
        .Font.Color = vbWhite
        .Interior.Color = clr
        .HorizontalAlignment = xlCenter
        .RowHeight = 22
    End With
End Sub

'===============================================================================
' 버튼 재생성 (버튼이 사라졌을 때 사용)
'===============================================================================
Public Sub 버튼재생성()
    CreateButtons
    MsgBox "버튼이 재생성되었습니다.", vbInformation
End Sub
