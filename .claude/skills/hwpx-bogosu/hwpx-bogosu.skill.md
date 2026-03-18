# hwpx-bogosu

한글 문서(hwpx) 보고서 양식 생성 스킬

## Description

두 가지 표준 보고서 양식을 기반으로 한글(hwpx) 문서를 생성합니다.
- **양식1**: 정식 보고서 기본 양식 (상세형)
- **양식2**: 보고서 요약 양식 (간략형)

## Trigger Keywords

hwpx, 한글 문서, 보고서 양식, 한컴 문서, 보고서 작성, report template,
hwp, 한글, 양식, 문서 생성, 공식 보고서, 제안서

## Scope

**Level**: All (Starter/Dynamic/Enterprise)
**Use Cases**:
- 공식 보고서/제안서 작성
- 사업 계획서 작성
- 프로젝트 보고서 작성
- 회계/감사 문서 작성

## Usage

### 양식 선택

**양식1 - 정식 보고서 (상세형)**
```
/hwpx-bogosu 양식1 "제목" --type proposal
```
- 대상: 공공기관, 대학교, 대기업 공식 문서
- 구조: 표지 + 목차 + 상세 섹션
- 예시: 제안 요청서, 회계감사 보고서, 평가 문서

**양식2 - 보고서 요약 (간략형)**
```
/hwpx-bogosu 양식2 "제목" --type business
```
- 대상: 신사업 보고서, 내부 보고서
- 구조: 1페이지 요약 + 붙임
- 예시: 신사업 제안, 프로젝트 요약, 진행 보고

### 옵션

- `--title`: 문서 제목
- `--department`: 소속 부서
- `--author`: 작성자
- `--date`: 작성일 (기본값: 오늘)
- `--sections`: 커스텀 섹션 추가

### 예시

```bash
# 양식1: 회계감사 제안서
/hwpx-bogosu 양식1 "2027년 회계감사인 선임 제안서" \
  --department "전략실(전략부)" \
  --author "홍길동 팀장" \
  --date "2026.02.14"

# 양식2: 신사업 보고서
/hwpx-bogosu 양식2 "AI 챗봇 시스템 도입 보고서" \
  --department "IT혁신부서" \
  --author "김철수 부장" \
  --sections "개요,추진방안,사업예산,기타사항"
```

## Template Structure

### 양식1 - 정식 보고서 구조

```
┌─────────────────────────────────┐
│          표지 페이지             │
│  - 제목 (HY헤드라인M 18pt)      │
│  - 날짜                         │
│  - 부서/담당자 정보 (테이블)    │
│  - 수신처                       │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│            목차                  │
│  - 로마숫자 장 구분              │
│  - 아라비아숫자 절 구분          │
│  - 페이지 번호                   │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│       본문 섹션                  │
│  Ⅰ. 사업 개요                   │
│    □ 항목 (헤드라인M 15pt)      │
│      ○ 세부 (휴먼명조 14pt)     │
│        - 상세 (휴먼명조 14pt)   │
│          ※ 주석 (휴먼명조 11pt) │
│                                  │
│  Ⅱ. 요구 사항                   │
│  Ⅲ. 계약 사항                   │
│  Ⅳ. 평가요소 및 방법            │
│  Ⅴ. 제안서 규격 및 제출요령      │
│  Ⅵ. 보안관리                     │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│        별지 (첨부 서식)          │
│  • 별지 제1호~제5호             │
└─────────────────────────────────┘
```

### 양식2 - 보고서 요약 구조

```
┌─────────────────────────────────┐
│          표지 헤더               │
│  (빈 행 / 테두리)               │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│          제목 영역               │
│  OOO 신사업 보고서              │
│  폰트 HY헤드라인M, 크기 18       │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│        메타 정보                 │
│  소속부서: OOOO부서, 날짜       │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│       개요 or 목적               │
│  (1~2줄 요약)                   │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│      추진방안 or 본문            │
│  추진방안 1: ...                │
│  추진방안 2: ...                │
│  추진방안 3: ...                │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│        실행방안                  │
│  내용1                          │
│  내용2                          │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│        사업예산                  │
│  항목별 예산 내역               │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│   기타사항 or 협조사항           │
│  협력 필요 사항                 │
│  리스크 대응 방안               │
│  붙임1 참고                     │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│      붙임 (새 페이지)            │
│  붙임 | 사업 추진일정           │
│  ─────────────────────         │
│  개요                           │
│  추진체계                       │
│  일정                           │
└─────────────────────────────────┘
```

## Font Specifications

### 양식1 폰트 규격

| 항목 | 폰트 | 크기 | 용도 |
|------|------|------|------|
| 대제목 (Ⅰ, Ⅱ, Ⅲ) | 헤드라인M | 15pt | 장 제목 |
| 중항목 (□) | 헤드라인M | 15pt | 주요 항목 |
| 소항목 (○) | 휴먼명조 | 14pt | 세부 항목 |
| 상세 (-) | 휴먼명조 | 14pt | 상세 내용 |
| 주석 (※) | 휴먼명조 | 11pt | 주석/참고 |

### 양식2 폰트 규격

| 항목 | 폰트 | 크기 | 용도 |
|------|------|------|------|
| 문서 제목 | HY헤드라인M | 18pt | 표지 제목 |
| 섹션 제목 | HY헤드라인M | 15pt | 개요, 추진방안 등 |
| 본문 내용 | 휴먼명조 | 13pt | 일반 본문 |
| 메타 정보 | 휴먼명조 | 12pt | 부서, 날짜 |
| 상세 내용 | 휴먼명조 | 12pt | 내용1, 내용2 |

## HWPX Structure

hwpx 파일은 ZIP 기반 XML 문서 형식입니다.

### 파일 구조
```
document.hwpx
├── mimetype
├── version.xml
├── settings.xml
├── META-INF/
│   ├── manifest.xml
│   ├── container.xml
│   └── container.rdf
├── Contents/
│   ├── header.xml
│   ├── section0.xml      (주요 문서 내용)
│   └── content.hpf
├── Preview/
│   ├── PrvText.txt
│   └── PrvImage.png
└── BinData/
    └── image*.{png,bmp}  (삽입 이미지)
```

### 핵심 XML 구조

**section0.xml** - 문서의 실제 내용
```xml
<hp:p>                    <!-- 단락 -->
  <hp:run>                <!-- 텍스트 런 -->
    <hp:t>텍스트</hp:t>   <!-- 텍스트 내용 -->
  </hp:run>
</hp:p>

<hp:tbl>                  <!-- 표 -->
  <hp:tr>                 <!-- 행 -->
    <hp:tc>               <!-- 셀 -->
      <hp:subList>
        <hp:p>...</hp:p>
      </hp:subList>
    </hp:tc>
  </hp:tr>
</hp:tbl>
```

## Implementation Guide

### Python 기반 생성 방법

```python
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime

def create_hwpx_report(template_type, title, **options):
    """
    hwpx 보고서 생성

    Args:
        template_type: 'type1' 또는 'type2'
        title: 문서 제목
        **options: 추가 옵션 (department, author, date 등)
    """
    # 1. 템플릿 파일 복사
    template_path = f"assets/(샘플양식{template_type}) 보고서.hwpx"

    # 2. ZIP 압축 해제
    # 3. section0.xml 수정
    # 4. 텍스트 치환
    # 5. ZIP 재압축
    pass

# 사용 예시
create_hwpx_report(
    template_type='2',
    title='AI 챗봇 시스템 도입 보고서',
    department='IT혁신부서',
    author='김철수 부장',
    date='2026.03.11',
    sections={
        'overview': '최신 AI 기술을 활용한 고객 서비스 개선',
        'approach': ['AI 모델 선정', '시스템 구축', '테스트 및 배포'],
        'budget': {'모델 구매': '10억원', '개발비': '20억원'}
    }
)
```

### JavaScript 기반 생성 방법

```javascript
const JSZip = require('jszip');
const fs = require('fs');

async function createHwpxReport(templateType, title, options = {}) {
    // 1. 템플릿 로드
    const template = await JSZip.loadAsync(
        fs.readFileSync(`assets/(샘플양식${templateType}) 보고서.hwpx`)
    );

    // 2. section0.xml 추출 및 수정
    const section0 = await template.file('Contents/section0.xml').async('string');

    // 3. 텍스트 치환
    let modified = section0
        .replace(/OOO 신사업 보고서/g, title)
        .replace(/OOOO부서/g, options.department || '부서명')
        .replace(/2022\.12\.31/g, options.date || new Date().toLocaleDateString('ko-KR'));

    // 4. 수정된 내용 저장
    template.file('Contents/section0.xml', modified);

    // 5. hwpx 파일 생성
    const output = await template.generateAsync({type: 'nodebuffer'});
    fs.writeFileSync(`${title}.hwpx`, output);
}

// 사용 예시
createHwpxReport('2', 'AI 챗봇 시스템 도입 보고서', {
    department: 'IT혁신부서',
    author: '김철수 부장',
    date: '2026.03.11'
});
```

## Use Cases

### 1. 공공기관 제안서 (양식1)

```bash
/hwpx-bogosu 양식1 "2027년도 클라우드 전환 사업 제안서" \
  --department "디지털혁신부" \
  --author "이영희 팀장" \
  --sections "사업개요,요구사항,계약사항,평가요소,제안서규격,보안관리"
```

### 2. 신사업 기획서 (양식2)

```bash
/hwpx-bogosu 양식2 "메타버스 플랫폼 구축 사업" \
  --department "신사업개발팀" \
  --overview "차세대 메타버스 플랫폼 구축을 통한 신규 수익 창출" \
  --budget "기획: 5억원, 개발: 30억원, 운영: 10억원"
```

### 3. 내부 보고서 (양식2)

```bash
/hwpx-bogosu 양식2 "2026년 1분기 실적 보고" \
  --department "경영관리팀" \
  --sections "실적요약,주요성과,개선사항,향후계획"
```

## Customization Options

### 섹션 커스터마이징

**양식1 섹션 구조**:
- Ⅰ. 사업 개요
- Ⅱ. 요구 사항
- Ⅲ. 계약 사항
- Ⅳ. 평가요소 및 방법
- Ⅴ. 제안서 규격 및 제출요령
- Ⅵ. 보안관리

**양식2 섹션 구조**:
- 개요 or 목적
- 추진방안 or 본문
- 실행방안
- 사업예산
- 기타사항 or 협조사항
- 붙임 (별첨)

### 스타일 커스터마이징

```python
# 폰트 변경
style_config = {
    'title_font': 'HY헤드라인M',
    'title_size': 18,
    'heading_font': 'HY헤드라인M',
    'heading_size': 15,
    'body_font': '휴먼명조',
    'body_size': 13
}

# 색상 변경
color_config = {
    'title_color': '#000000',
    'heading_color': '#000000',
    'table_border': '#000000',
    'emphasis': '#FF0000'
}
```

## Tips

1. **양식 선택 기준**
   - 10페이지 이상 상세 문서 → 양식1
   - 1-2페이지 요약 문서 → 양식2

2. **폰트 일관성 유지**
   - 공식 문서는 지정된 폰트 엄수
   - 헤드라인M, 휴먼명조 조합 사용

3. **구조 계층화**
   - 양식1: Ⅰ > □ > ○ > - > ※
   - 양식2: 섹션 > 항목 > 상세

4. **이미지 삽입**
   - BinData 폴더에 이미지 추가
   - section0.xml에서 참조 설정

5. **PDF 변환**
   - 한컴오피스에서 열기 → 파일 → PDF로 저장
   - 또는 온라인 변환 서비스 활용

## Error Handling

### 일반적인 오류

1. **파일이 열리지 않음**
   - hwpx 구조 검증 (mimetype, manifest.xml)
   - XML 문법 오류 확인

2. **깨진 문자**
   - UTF-8 인코딩 확인
   - XML 특수문자 이스케이프 (&lt;, &gt;, &amp;)

3. **레이아웃 깨짐**
   - 원본 템플릿 스타일 ID 유지
   - 테이블 구조 수정 시 주의

## Dependencies

### Python
```bash
pip install python-docx zipfile36
```

### JavaScript
```bash
npm install jszip
```

### 한컴오피스
- 한글 2014 이상 (hwpx 지원)
- 또는 한컴오피스 뷰어 (무료)

## Related Skills

- `/pdca`: PDCA 문서 생성 시 보고서 형식으로 출력
- `/code-review`: 코드 리뷰 결과를 보고서로 출력
- `/bkit-templates`: 기타 문서 템플릿

## Version

- v1.0.0: 초기 버전
- 양식1: 정식 보고서 기본 양식 지원
- 양식2: 보고서 요약 양식 지원

## License

MIT License

## References

- [한글 문서 파일 형식 hwpx](https://www.hancom.com)
- 샘플양식1: 보고서 기본 양식.hwpx
- 샘플양식2: 보고서 기반 양식(요약).hwpx
