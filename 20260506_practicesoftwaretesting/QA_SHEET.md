# QA 테스트 시트 — practicesoftwaretesting.com

- **테스트 일시**: 2026-05-06
- **테스트 환경**: Chrome via Playwright MCP
- **대상 URL**: https://practicesoftwaretesting.com/

| # | 카테고리 | 테스트 항목 | 우선순위 | 결과 | 이슈 |
|---|---------|-----------|---------|------|------|
| 1 | 페이지 로딩 | 메인 페이지 정상 로드 | P1 | ✅ PASS | - |
| 2 | 레이아웃/UI | 헤더·푸터·메뉴 렌더링 | P1 | ✅ PASS | - |
| 3 | 네비게이션 | 상단 메뉴 링크 동작 | P1 | ✅ PASS | - |
| 4 | 기능 | 상품 검색 기능 | P1 | ✅ PASS | - |
| 5 | 기능 | 상품 카테고리 필터 | P2 | ✅ PASS | - |
| 6 | 기능 | 로그인 폼 유효성 검사 | P1 | ✅ PASS | - |
| 7 | 기능 | 장바구니 담기 | P2 | ⚠️ WARN | ISSUE-004 |
| 8 | 반응형 | 모바일(375px) 레이아웃 | P2 | ❌ FAIL | ISSUE-001, ISSUE-002 |
| 9 | 반응형 | 태블릿(768px) 레이아웃 | P3 | ❌ FAIL | ISSUE-001 |
| 10 | 콘텐츠 | 상품 이미지 로딩 | P2 | ⚠️ WARN | ISSUE-001, ISSUE-003 |
