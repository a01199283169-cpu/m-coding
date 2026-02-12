'###############################################################################
'#                                                                             #
'#                 【파일2】 담당자용 예산취합 시스템                             #
'#                                                                             #
'#   예산 담당자가 사용하는 파일입니다.                                          #
'#   공유폴더에 저장된 모든 학과 CSV 파일을 자동으로 불러와 집계합니다.          #
'#                                                                             #
'#   [시트 구성]                                                                #
'#   - 설정: 공유폴더 경로만 지정                                               #
'#   - 취합결과: 전체 학과 데이터 + 학과별 소계 + 전체 합계                      #
'#   - 학과요약: 학과별 예산/지출/잔액 요약표                                    #
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
Private Const WS_RES As String = "취합결과"
Private Const WS_SUM As String = "학과요약"

'===============================================================================
' 초기 설정 (최초 1회 실행)
'===============================================================================
Public Sub 초기설정()
    Dim wsSet As Worksheet, wsRes As Worksheet, wsSum As Worksheet

    Application.ScreenUpdating = False

    ' ===== 설정 시트 생성 =====
    Set wsSet = GetSheet(WS_SET)
    With wsSet
        .Cells.Clear

        ' 공유폴더 설정
        .Range("A1:B1").Value = Array("항목", "값")
        FormatHeader .Range("A1:B1"), RGB(70, 130, 180)

        .Range("A2").Value = "공유폴더"
        .Range("B2").Value = "(폴더선택 버튼 클릭)"
        .Range("B2").Font.Color = RGB(150, 150, 150)
        .Range("A1:B2").Borders.LineStyle = xlContinuous

        .Columns("A").ColumnWidth = 15
        .Columns("B").ColumnWidth = 50

        ' 안내 문구
        .Range("A4").Value = "※ 공유폴더를 선택하면 그 안의 모든 학과 CSV 파일을 자동으로 불러옵니다."
        .Range("A4").Font.Color = RGB(100, 100, 100)
    End With

    ' ===== 취합결과 시트 생성 =====
    Set wsRes = GetSheet(WS_RES)
    With wsRes
        .Cells.Clear
        .Range("A1:G1").Value = Array("학과명", "날짜", "세부항목", "금액", "관련문서번호", "비고", "입력일시")
        FormatHeader .Range("A1:G1"), RGB(70, 130, 180)

        .Columns("A").ColumnWidth = 18
        .Columns("B").ColumnWidth = 12
        .Columns("C").ColumnWidth = 20
        .Columns("D").ColumnWidth = 15
        .Columns("E").ColumnWidth = 18
        .Columns("F").ColumnWidth = 15
        .Columns("G").ColumnWidth = 20
    End With

    ' ===== 학과요약 시트 생성 =====
    Set wsSum = GetSheet(WS_SUM)
    With wsSum
        .Cells.Clear
        .Range("A1:E1").Value = Array("학과명", "예산액", "총지출액", "현재잔액", "집행률(%)")
        FormatHeader .Range("A1:E1"), RGB(192, 80, 77)

        .Columns("A").ColumnWidth = 20
        .Columns("B").ColumnWidth = 15
        .Columns("C").ColumnWidth = 15
        .Columns("D").ColumnWidth = 15
        .Columns("E").ColumnWidth = 12
    End With

    ' 버튼 생성
    CreateButtons

    Application.ScreenUpdating = True

    MsgBox "초기 설정 완료!" & vbLf & vbLf & _
           "1. [폴더 선택] 버튼으로 공유폴더 지정" & vbLf & _
           "2. [데이터 취합] 버튼 클릭" & vbLf & _
           "   → 공유폴더의 모든 학과 파일 자동 집계", vbInformation
End Sub

'===============================================================================
' 버튼 생성
'===============================================================================
Private Sub CreateButtons()
    Dim wsSet As Worksheet, wsRes As Worksheet, wsSum As Worksheet, shp As Shape

    Set wsSet = ThisWorkbook.Worksheets(WS_SET)
    Set wsRes = ThisWorkbook.Worksheets(WS_RES)
    Set wsSum = ThisWorkbook.Worksheets(WS_SUM)

    ' 기존 버튼 삭제
    For Each shp In wsSet.Shapes: If Left(shp.Name, 3) = "btn" Then shp.Delete: Next
    For Each shp In wsRes.Shapes: If Left(shp.Name, 3) = "btn" Then shp.Delete: Next
    For Each shp In wsSum.Shapes: If Left(shp.Name, 3) = "btn" Then shp.Delete: Next

    ' 설정 시트 버튼
    AddButton wsSet, "btn1", "폴더 선택", "D1", 100, 30, RGB(70, 130, 180), "폴더선택"
    AddButton wsSet, "btn2", "데이터 취합", "E1", 100, 30, RGB(100, 150, 100), "데이터취합"

    ' 취합결과 시트 버튼
    AddButton wsRes, "btn1", "데이터 취합", "I1", 100, 30, RGB(100, 150, 100), "데이터취합"
    AddButton wsRes, "btn2", "학과요약 생성", "J1", 110, 30, RGB(70, 130, 180), "학과요약생성"
    AddButton wsRes, "btn3", "데이터 초기화", "K1", 100, 30, RGB(200, 100, 80), "데이터초기화"

    ' 학과요약 시트 버튼
    AddButton wsSum, "btn1", "학과요약 생성", "G1", 110, 30, RGB(70, 130, 180), "학과요약생성"
    AddButton wsSum, "btn2", "취합결과 이동", "H1", 110, 30, RGB(100, 150, 100), "GoResult"
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
        .Title = "공유폴더를 선택하세요 (학과 CSV 파일이 있는 폴더)"
        .InitialFileName = "C:\"
        If .Show = -1 Then
            Set wsSet = ThisWorkbook.Worksheets(WS_SET)
            wsSet.Range("B2").Value = .SelectedItems(1) & "\"
            wsSet.Range("B2").Font.Color = vbBlack
            MsgBox "폴더가 설정되었습니다." & vbLf & .SelectedItems(1), vbInformation
        End If
    End With
End Sub

'===============================================================================
' 데이터 취합 (메인 기능)
' - 공유폴더의 모든 *_예산현황.csv 파일을 자동으로 읽어서 집계
'===============================================================================
Public Sub 데이터취합()
    Dim wsSet As Worksheet, wsRes As Worksheet
    Dim strPath As String, strFile As String
    Dim fso As Object, ts As Object
    Dim arrLine() As String, arrData() As String
    Dim i As Long, r As Long, fileCnt As Long, dataCnt As Long
    Dim deptName As String
    Dim dblBudget As Double, dblSpent As Double, dblBalance As Double
    Dim totalBudget As Double, totalSpent As Double, totalBalance As Double
    Dim startRow As Long, dataStartIdx As Long

    Set wsSet = ThisWorkbook.Worksheets(WS_SET)
    Set wsRes = ThisWorkbook.Worksheets(WS_RES)

    ' ----- 유효성 검사 -----
    strPath = Trim(wsSet.Range("B2").Value)
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

    ' ----- 취합결과 초기화 -----
    Dim lastClear As Long
    lastClear = wsRes.Cells(wsRes.Rows.Count, "A").End(xlUp).Row
    If lastClear > 1 Then
        wsRes.Range("A2:G" & lastClear).ClearContents
        wsRes.Range("A2:G" & lastClear).ClearFormats
    End If

    r = 2
    fileCnt = 0
    dataCnt = 0
    totalBudget = 0
    totalSpent = 0
    totalBalance = 0

    Application.ScreenUpdating = False
    Set fso = CreateObject("Scripting.FileSystemObject")

    ' ----- 공유폴더의 모든 CSV 파일 검색 및 처리 -----
    strFile = Dir(strPath & "*_예산현황.csv")

    Do While strFile <> ""
        Application.StatusBar = "처리중: " & strFile

        ' CSV 파일 읽기
        Set ts = fso.OpenTextFile(strPath & strFile, 1, False, -2)
        Dim fileContent As String
        fileContent = ts.ReadAll
        ts.Close

        arrLine = Split(fileContent, vbCrLf)
        If UBound(arrLine) < 1 Then GoTo NextFile

        ' 헤더 정보 파싱 (2번째 줄: 학과명, 담당자, 예산액, 총지출액, 현재잔액)
        arrData = ParseCSVLine(arrLine(1))
        If UBound(arrData) < 4 Then GoTo NextFile

        deptName = arrData(0)
        dblBudget = Val(arrData(2))
        dblSpent = Val(arrData(3))
        dblBalance = Val(arrData(4))

        startRow = r

        ' 데이터 행 시작점 찾기 (날짜,세부항목 헤더 다음)
        dataStartIdx = -1
        For i = 0 To UBound(arrLine)
            If InStr(arrLine(i), "날짜") > 0 And InStr(arrLine(i), "세부항목") > 0 Then
                dataStartIdx = i + 1
                Exit For
            End If
        Next i
        If dataStartIdx = -1 Then GoTo NextFile

        ' 지출 데이터 입력
        For i = dataStartIdx To UBound(arrLine)
            If Trim(arrLine(i)) = "" Then GoTo ContinueLoop

            arrData = ParseCSVLine(arrLine(i))
            If UBound(arrData) < 6 Then GoTo ContinueLoop
            If Trim(arrData(0)) = "" Then GoTo ContinueLoop

            wsRes.Cells(r, 1).Value = deptName           ' 학과명
            wsRes.Cells(r, 2).Value = arrData(0)         ' 날짜
            wsRes.Cells(r, 3).Value = arrData(1)         ' 세부항목
            wsRes.Cells(r, 4).Value = Val(arrData(2))    ' 금액
            wsRes.Cells(r, 5).Value = arrData(4)         ' 관련문서번호
            wsRes.Cells(r, 6).Value = arrData(5)         ' 비고
            wsRes.Cells(r, 7).Value = arrData(6)         ' 입력일시

            dataCnt = dataCnt + 1
            r = r + 1
ContinueLoop:
        Next i

        ' ----- 학과별 소계 행 추가 -----
        If r > startRow Then
            wsRes.Cells(r, 1).Value = "【" & deptName & " 소계】"
            wsRes.Cells(r, 2).Value = "예산액:"
            wsRes.Cells(r, 3).Value = dblBudget
            wsRes.Cells(r, 4).Value = "지출액:"
            wsRes.Cells(r, 5).Value = dblSpent
            wsRes.Cells(r, 6).Value = "잔액:"
            wsRes.Cells(r, 7).Value = dblBalance

            ' 소계 행 서식
            With wsRes.Range("A" & r & ":G" & r)
                .Font.Bold = True
                .Interior.Color = RGB(230, 230, 230)
            End With
            wsRes.Range("C" & r).NumberFormat = "#,##0"
            wsRes.Range("E" & r).NumberFormat = "#,##0"
            wsRes.Range("G" & r).NumberFormat = "#,##0"

            r = r + 1

            totalBudget = totalBudget + dblBudget
            totalSpent = totalSpent + dblSpent
            totalBalance = totalBalance + dblBalance
            fileCnt = fileCnt + 1
        End If

NextFile:
        strFile = Dir()
    Loop

    ' ----- 전체 합계 행 추가 (빈 행 후) -----
    If fileCnt > 0 Then
        r = r + 1  ' 빈 행

        wsRes.Cells(r, 1).Value = "【전체 합계】"
        wsRes.Cells(r, 2).Value = "총 예산액:"
        wsRes.Cells(r, 3).Value = totalBudget
        wsRes.Cells(r, 4).Value = "총 지출액:"
        wsRes.Cells(r, 5).Value = totalSpent
        wsRes.Cells(r, 6).Value = "총 잔액:"
        wsRes.Cells(r, 7).Value = totalBalance

        ' 전체 합계 행 서식
        With wsRes.Range("A" & r & ":G" & r)
            .Font.Bold = True
            .Font.Size = 12
            .Interior.Color = RGB(70, 130, 180)
            .Font.Color = vbWhite
        End With
        wsRes.Range("C" & r).NumberFormat = "#,##0"
        wsRes.Range("E" & r).NumberFormat = "#,##0"
        wsRes.Range("G" & r).NumberFormat = "#,##0"
    End If

    ' ----- 서식 적용 -----
    With wsRes
        .Columns("D").NumberFormat = "#,##0"
        .Columns("B").NumberFormat = "YYYY-MM-DD"
        .Range("A1:G1").Borders.LineStyle = xlContinuous
        If r > 2 Then .Range("A2:G" & r).Borders.LineStyle = xlContinuous

        ' 열 너비 자동 조정
        .Columns("A:G").AutoFit
    End With

    Application.StatusBar = False
    Application.ScreenUpdating = True

    wsRes.Activate
    wsRes.Range("A1").Select

    If fileCnt = 0 Then
        MsgBox "공유폴더에 CSV 파일이 없습니다." & vbLf & vbLf & _
               "폴더: " & strPath & vbLf & _
               "파일 형식: 학과명_예산현황.csv", vbExclamation
    Else
        MsgBox "취합 완료!" & vbLf & vbLf & _
               "취합 학과: " & fileCnt & "개" & vbLf & _
               "지출 건수: " & dataCnt & "건" & vbLf & vbLf & _
               "총 예산액: " & Format(totalBudget, "#,##0") & "원" & vbLf & _
               "총 지출액: " & Format(totalSpent, "#,##0") & "원" & vbLf & _
               "총 잔  액: " & Format(totalBalance, "#,##0") & "원", vbInformation
    End If
End Sub

'===============================================================================
' CSV 라인 파싱 (쌍따옴표 처리)
'===============================================================================
Private Function ParseCSVLine(line As String) As String()
    Dim result() As String
    Dim i As Long, cnt As Long, inQuote As Boolean
    Dim ch As String, field As String

    ReDim result(0 To 20)
    cnt = 0
    inQuote = False
    field = ""

    For i = 1 To Len(line)
        ch = Mid(line, i, 1)

        If ch = Chr(34) Then  ' 쌍따옴표
            inQuote = Not inQuote
        ElseIf ch = "," And Not inQuote Then
            result(cnt) = field
            cnt = cnt + 1
            field = ""
        Else
            field = field & ch
        End If
    Next i
    result(cnt) = field

    ReDim Preserve result(0 To cnt)
    ParseCSVLine = result
End Function

'===============================================================================
' 학과요약 생성
'===============================================================================
Public Sub 학과요약생성()
    Dim wsRes As Worksheet, wsSum As Worksheet
    Dim dictDept As Object
    Dim lastRow As Long, i As Long, r As Long
    Dim deptName As String
    Dim dblBudget As Double, dblSpent As Double, dblBalance As Double
    Dim totalBudget As Double, totalSpent As Double, totalBalance As Double

    Set wsRes = ThisWorkbook.Worksheets(WS_RES)
    Set wsSum = ThisWorkbook.Worksheets(WS_SUM)
    Set dictDept = CreateObject("Scripting.Dictionary")

    lastRow = wsRes.Cells(wsRes.Rows.Count, "A").End(xlUp).Row
    If lastRow < 2 Then
        MsgBox "취합된 데이터가 없습니다." & vbLf & "먼저 [데이터 취합]을 실행해주세요.", vbExclamation
        Exit Sub
    End If

    ' 취합결과에서 소계 행 파싱
    For i = 2 To lastRow
        deptName = wsRes.Cells(i, 1).Value

        If InStr(deptName, "소계") > 0 And InStr(deptName, "전체") = 0 Then
            deptName = Replace(deptName, "【", "")
            deptName = Replace(deptName, " 소계】", "")

            dblBudget = Val(wsRes.Cells(i, 3).Value)
            dblSpent = Val(wsRes.Cells(i, 5).Value)
            dblBalance = Val(wsRes.Cells(i, 7).Value)

            If Not dictDept.Exists(deptName) Then
                dictDept.Add deptName, Array(dblBudget, dblSpent, dblBalance)
            End If
        End If
    Next i

    ' 학과요약 시트 초기화
    Dim lastClear As Long
    lastClear = wsSum.Cells(wsSum.Rows.Count, "A").End(xlUp).Row
    If lastClear > 1 Then
        wsSum.Range("A2:E" & lastClear).ClearContents
        wsSum.Range("A2:E" & lastClear).ClearFormats
    End If

    ' 학과요약 작성
    r = 2
    totalBudget = 0
    totalSpent = 0
    totalBalance = 0

    Dim key As Variant, arr As Variant
    For Each key In dictDept.Keys
        arr = dictDept(key)
        wsSum.Cells(r, 1).Value = key
        wsSum.Cells(r, 2).Value = arr(0)
        wsSum.Cells(r, 3).Value = arr(1)
        wsSum.Cells(r, 4).Value = arr(2)

        If arr(0) > 0 Then
            wsSum.Cells(r, 5).Value = Round(arr(1) / arr(0) * 100, 1)
        Else
            wsSum.Cells(r, 5).Value = 0
        End If

        totalBudget = totalBudget + arr(0)
        totalSpent = totalSpent + arr(1)
        totalBalance = totalBalance + arr(2)
        r = r + 1
    Next key

    ' 합계 행 (빈 행 후)
    If r > 2 Then
        r = r + 1
        wsSum.Cells(r, 1).Value = "【합 계】"
        wsSum.Cells(r, 2).Value = totalBudget
        wsSum.Cells(r, 3).Value = totalSpent
        wsSum.Cells(r, 4).Value = totalBalance
        If totalBudget > 0 Then
            wsSum.Cells(r, 5).Value = Round(totalSpent / totalBudget * 100, 1)
        End If

        With wsSum.Range("A" & r & ":E" & r)
            .Font.Bold = True
            .Interior.Color = RGB(192, 80, 77)
            .Font.Color = vbWhite
        End With
    End If

    ' 서식 적용
    With wsSum
        .Columns("B:D").NumberFormat = "#,##0"
        .Columns("E").NumberFormat = "0.0"
        .Range("A1:E" & r).Borders.LineStyle = xlContinuous
        .Columns("A:E").AutoFit
    End With

    wsSum.Activate
    wsSum.Range("A1").Select

    MsgBox "학과요약 생성 완료!" & vbLf & vbLf & _
           "학과 수: " & dictDept.Count & "개" & vbLf & _
           "총 예산액: " & Format(totalBudget, "#,##0") & "원" & vbLf & _
           "총 지출액: " & Format(totalSpent, "#,##0") & "원" & vbLf & _
           "평균 집행률: " & IIf(totalBudget > 0, Round(totalSpent / totalBudget * 100, 1), 0) & "%", vbInformation
End Sub

'===============================================================================
' 데이터 초기화
'===============================================================================
Public Sub 데이터초기화()
    Dim wsRes As Worksheet, wsSum As Worksheet
    Dim lastRowRes As Long, lastRowSum As Long

    Set wsRes = ThisWorkbook.Worksheets(WS_RES)
    Set wsSum = ThisWorkbook.Worksheets(WS_SUM)

    lastRowRes = wsRes.Cells(wsRes.Rows.Count, "A").End(xlUp).Row
    lastRowSum = wsSum.Cells(wsSum.Rows.Count, "A").End(xlUp).Row

    If lastRowRes < 2 And lastRowSum < 2 Then
        MsgBox "삭제할 데이터가 없습니다.", vbInformation
        Exit Sub
    End If

    If MsgBox("취합결과와 학과요약 데이터를 모두 삭제하시겠습니까?", vbQuestion + vbYesNo) = vbYes Then
        If lastRowRes >= 2 Then
            wsRes.Range("A2:G" & lastRowRes).ClearContents
            wsRes.Range("A2:G" & lastRowRes).ClearFormats
        End If
        If lastRowSum >= 2 Then
            wsSum.Range("A2:E" & lastRowSum).ClearContents
            wsSum.Range("A2:E" & lastRowSum).ClearFormats
        End If
        MsgBox "초기화되었습니다.", vbInformation
    End If
End Sub

'===============================================================================
' 시트 이동
'===============================================================================
Public Sub GoResult()
    ThisWorkbook.Worksheets(WS_RES).Activate
End Sub

Public Sub GoSet()
    ThisWorkbook.Worksheets(WS_SET).Activate
End Sub

Public Sub GoSum()
    ThisWorkbook.Worksheets(WS_SUM).Activate
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
