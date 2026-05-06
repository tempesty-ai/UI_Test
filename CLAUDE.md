# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

이 레포는 **QA 시각적 테스트 자동화** 저장소다. `qa-visual-tester` 스킬을 사용해 웹 애플리케이션을 Playwright MCP로 직접 브라우저 검증하고, 발견된 이슈를 날짜별 디렉토리에 체계적으로 기록한다.

GitHub: https://github.com/tempesty-ai/UI_Test

---

## 디렉토리 구조

```
D:\code\qa\
├── qa-visual-tester/
│   └── SKILL.md                        ← QA 스킬 정의 (Claude 스킬)
├── [YYYYMMDD]_[도메인]/                 ← 테스트 세션 (날짜_사이트명)
│   ├── QA_SHEET.md                     ← 테스트 케이스 + 전체 결과표
│   ├── SUMMARY.md                      ← 이슈 요약 리포트
│   └── issues/
│       └── ISSUE-[번호]_[제목]/
│           ├── ISSUE.md                ← 이슈 상세 (심각도/재현방법/스크린샷)
│           └── screenshot.png
└── CLAUDE.md
```

---

## QA 테스트 실행

새 사이트 테스트 시 `qa-visual-tester` 스킬을 사용한다. 스킬이 자동으로:
1. 테스트 시트 작성
2. Playwright MCP(`mcp__playwright__*`)로 실제 브라우저 검증
3. `D:\code\qa\[YYYYMMDD_도메인]\` 하위에 결과 저장

**Playwright MCP 주요 도구**
- `mcp__playwright__browser_navigate` — URL 이동
- `mcp__playwright__browser_take_screenshot` — 스크린샷 저장 (저장 경로는 반드시 허용 루트 내부로 지정)
- `mcp__playwright__browser_resize` — 반응형 뷰포트 전환 (데스크톱 1280×800 / 태블릿 768×1024 / 모바일 375×812)
- `mcp__playwright__browser_evaluate` — JS 실행 (이미지 broken 여부 등 검사)

**스크린샷 저장 경로 주의**
Playwright MCP는 프로젝트 루트 내부에만 파일 저장이 가능하다. 스크린샷을 `.playwright-mcp/qa-session/` 에 저장한 뒤 `D:\code\qa\` 로 복사한다.

---

## 이슈 심각도 기준

| 레벨 | 기준 |
|------|------|
| P1 Critical | 핵심 기능 동작 불가, 결제/인증 오류 |
| P2 Major | 주요 기능 손상, 반응형 레이아웃 깨짐, 콘솔 에러 |
| P3 Minor | UI 텍스트 잘림, 아이콘 위치, UX 불편 |

---

## 회귀 테스트 추적

이미 발견된 이슈가 수정 후 재테스트될 때 상태를 추적한다.

**ISSUE.md 상태 필드** — 모든 이슈에 아래 필드를 포함한다:

```markdown
- **상태**: Open | Fixed | Reopened
- **수정 확인일**: YYYY-MM-DD (Fixed 시 기재)
```

**재테스트 시 디렉토리 규칙**
- 동일 이슈가 재발한 경우: 기존 `ISSUE.md`의 상태를 `Reopened`로 변경하고 재현 날짜를 비고에 추가
- 신규 테스트 세션에서 이전 이슈 재확인 시: `QA_SHEET.md`의 해당 항목에 `♻️ REOPEN` 표기

---

## 인증이 필요한 사이트 테스트

로그인/인증이 필요한 사이트 테스트 시 아래 규칙을 따른다.

- 계정 정보는 **절대 ISSUE.md, QA_SHEET.md, 코드에 하드코딩하지 않는다**
- 테스트용 계정은 `.env.test` 파일로 관리하며 `.gitignore`에 등록한다
- Playwright 세션 쿠키/토큰이 스크린샷에 노출되지 않도록 민감 영역은 크롭 처리한다

```bash
# .env.test 예시 (gitignore 대상)
TEST_EMAIL=your@email.com
TEST_PASSWORD=yourpassword
```

ISSUE.md 작성 시 계정 정보 대신 `[테스트 계정]` 으로 마스킹한다.

---

## 이슈 디렉토리 네이밍 규칙

한글 디렉토리명은 OS/Git 환경에 따라 인코딩이 깨질 수 있으므로 **영문+숫자+언더스코어**만 사용한다.

```
# ❌ 피할 것
ISSUE-001_모바일_이미지_미렌더링/

# ✅ 올바른 형식
ISSUE-001_mobile_image_not_rendering/
ISSUE-002_mobile_price_text_truncated/
ISSUE-003_console_errors_on_load/
ISSUE-004_cart_icon_hidden_in_mobile/
```

테스트 세션 디렉토리도 동일하게 영문으로 작성한다:
```
# ✅
20260506_practicesoftwaretesting/
20260506_bunjang_co_kr/
```

---

## Git 워크플로

```bash
# 테스트 결과 push
cd D:\code\qa
git add .
git commit -m "feat: [사이트명] QA 테스트 결과 추가"
git push
```

`.gitignore`에 `*.skill` 이 등록되어 있어 패키징된 스킬 파일은 push되지 않는다.
