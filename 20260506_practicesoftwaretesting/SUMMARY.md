# QA 테스트 결과 요약

- **테스트 일시**: 2026-05-06
- **대상 URL**: https://practicesoftwaretesting.com/
- **테스트 환경**: Chrome (Playwright MCP), Desktop 1280px / Tablet 768px / Mobile 375px
- **총 테스트 항목**: 10개
- **PASS**: 6개 | **FAIL**: 2개 | **WARNING**: 2개

---

## 발견된 이슈 (심각도 순)

### P2 Major

- **[ISSUE-001](./issues/ISSUE-001_모바일_이미지_미렌더링/ISSUE.md)**: 모바일/태블릿 뷰포트에서 hammer 계열 상품 이미지 4종 미렌더링
  - 영향: 375px, 768px 뷰포트에서 Claw Hammer, Hammer, Thor Hammer 등 4개 상품 이미지 공백
  - 데스크톱(1280px)에서는 정상 → lazy loading 또는 AVIF 렌더링 타이밍 버그 추정

- **[ISSUE-003](./issues/ISSUE-003_콘솔에러_3건/ISSUE.md)**: 전 페이지 JavaScript 콘솔 에러 3건 상시 발생
  - 영향: 잠재적 기능 오동작 위험, 코드 품질 저하

### P3 Minor

- **[ISSUE-002](./issues/ISSUE-002_모바일_가격텍스트_잘림/ISSUE.md)**: 모바일(375px)에서 상품 가격 텍스트 잘림
  - 예: $14.15 → "$14.5"로 표시

- **[ISSUE-004](./issues/ISSUE-004_장바구니_아이콘_숨김/ISSUE.md)**: 소형 뷰포트에서 장바구니 아이콘 햄버거 메뉴 내부에만 표시
  - 상품 담은 후 헤더에서 즉시 카트 상태 확인 불가

---

## 정상 동작 확인 항목

| 항목 | 결과 |
|------|------|
| 메인 페이지 로드 | ✅ 정상 |
| 헤더/푸터/네비게이션 렌더링 | ✅ 정상 |
| 메뉴 링크 동작 (Home, Categories, Contact, Sign in) | ✅ 정상 |
| 상품 검색 ("hammer" → 6개 결과) | ✅ 정상 |
| 카테고리 필터 (Hand Tools + 하위 항목 자동 선택) | ✅ 정상 |
| 로그인 빈 값 제출 에러 메시지 | ✅ 정상 |
| 로그인 잘못된 이메일 형식 에러 메시지 | ✅ 정상 |
| 장바구니 담기 + 수량 뱃지 표시 (데스크톱) | ✅ 정상 |

---

## 권고 사항

1. **즉시 수정 권고 (P2)**
   - 모바일/태블릿 hammer 상품 이미지 렌더링 문제 → AVIF lazy loading 정책 검토
   - 콘솔 에러 3건 원인 파악 및 수정

2. **차순위 개선 권고 (P3)**
   - 모바일 가격 텍스트 CSS overflow 수정 (`white-space: nowrap` 또는 컨테이너 너비 조정)
   - 모바일 헤더에 장바구니 아이콘 고정 노출 처리

---

## 저장 경로

```
D:\code\qa\20260506_practicesoftwaretesting\
├── QA_SHEET.md
├── SUMMARY.md
└── issues\
    ├── ISSUE-001_모바일_이미지_미렌더링\
    ├── ISSUE-002_모바일_가격텍스트_잘림\
    ├── ISSUE-003_콘솔에러_3건\
    └── ISSUE-004_장바구니_아이콘_숨김\
```
