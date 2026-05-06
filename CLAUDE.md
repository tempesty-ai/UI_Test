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

## Git 워크플로

```bash
# 테스트 결과 push
cd D:\code\qa
git add .
git commit -m "feat: [사이트명] QA 테스트 결과 추가"
git push
```

`.gitignore`에 `*.skill` 이 등록되어 있어 패키징된 스킬 파일은 push되지 않는다.
