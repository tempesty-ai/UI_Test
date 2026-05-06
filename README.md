# UI_Test — QA Visual Tester

> Playwright MCP + Claude Code Hook 기반 웹 애플리케이션 시각적 QA 자동화 시스템

---

## 무엇을 만들었나

이 프로젝트는 세 개의 레이어로 구성된다.

### Layer 1 — SKILL.md (Claude의 두뇌 스크립트)

`qa-visual-tester/SKILL.md` — Claude가 직접 읽는 파일. QA를 어떻게 수행할지 **생각의 순서와 출력 형식**을 정의한다.

| 정의 내용 | 예시 |
|---------|------|
| 실행 단계 | 요구사항 수집 → 테스트 시트 작성 → Playwright 실행 → 이슈 기록 |
| 출력 형식 | ISSUE.md 템플릿, QA_SHEET.md 표 구조, SUMMARY.md 형식 |
| 도구 사용법 | playwright_navigate / playwright_screenshot / playwright_evaluate 사용 순서 |
| 판단 기준 | PASS / FAIL / WARNING 판정 방식, 이슈 심각도 분류 |

> SKILL.md가 없으면 Claude는 QA를 어떻게 해야 할지 모른다. 스킬은 Claude에게 역할과 절차를 부여하는 파일이다.

### Layer 2 — 하네스 (에이전트를 감싸는 제어 구조)

`settings.json` — **Claude Code 런타임**이 읽는 파일. Claude가 도구를 실행하는 타이밍에 자동으로 끼어든다. Claude는 Hook의 존재를 모른다.

| 구성요소 | Hook 이벤트 | 누가 읽는가 | 역할 |
|---------|------------|-----------|------|
| **URL 가드레일** | `PreToolUse` | Claude Code 런타임 | 브라우저 열기 직전 대상 사이트 생사 여부 체크. 다운이면 차단 |
| **자동 git push** | `PostToolUse` | Claude Code 런타임 | SUMMARY.md 저장을 감지해 자동으로 git add → commit → push |
| **결과 요약** | `Stop` | Claude Code 런타임 | 세션 종료 시 PASS / FAIL / WARN 카운트를 터미널에 출력 |
| **시작 대시보드** | `SessionStart` | Claude Code 런타임 | 세션 열릴 때 마지막 QA 결과 + 다음 테스트 대상을 Claude에게 주입 |

### Layer 3 — 자율 트리거 (에이전트를 자동으로 깨우는 것)

| 구성요소 | 파일 | 누가 읽는가 | 역할 |
|---------|------|-----------|------|
| **Cron 스케줄러** | Claude Code 내장 | Claude Code 스케줄러 | 평일 09:00 세션에 QA 프롬프트 자동 주입. 사람 없이 자율 트리거 |
| **targets.json** | `targets.json` | Claude (스킬 내부에서) | 무엇을 테스트할지 외부화. URL만 바꾸면 스킬 수정 없이 대상 변경 |
| **Playwright MCP** | 전역 MCP 설정 | Claude (도구로 호출) | 실제 브라우저(Chrome)를 직접 조작하는 실행 도구 |

---

## 전체 흐름

```
[Cron 09:00]  자동 트리거 (또는 사람이 직접 명령)
      ↓
[SessionStart Hook]  마지막 결과 대시보드 출력
      ↓
[qa-visual-tester 스킬]  targets.json 읽고 테스트 계획 수립
      ↓
[PreToolUse Hook]  URL 접근 가능 여부 검증 → 실패 시 차단
      ↓
[Playwright MCP]  실제 브라우저에서 3개 뷰포트 테스트
      ↓
[PostToolUse Hook]  SUMMARY.md 저장 감지 → GitHub 자동 push
      ↓
[Stop Hook]  PASS / FAIL / WARN 요약 출력
```

---

## 빠른 시작

### 1. 테스트 대상 설정

`targets.json` 에서 URL을 수정한다:

```json
{
  "targets": [
    {
      "url": "https://your-site.com",
      "name": "your_site",
      "focus": ["반응형", "로그인", "검색"]
    }
  ]
}
```

### 2. 테스트 실행

`D:\code\qa` 에서 Claude Code를 열고:

```
targets.json 읽고 QA 테스트 실행해줘
```

### 3. 결과 확인

테스트 완료 후 자동으로:
- `[날짜]_[도메인]/SUMMARY.md` — 이슈 요약 리포트
- `[날짜]_[도메인]/issues/ISSUE-XXX_*/` — 이슈별 스크린샷 + 상세 기록
- GitHub에 자동 push

---

## 테스트 항목

| 카테고리 | 내용 |
|---------|------|
| 페이지 로딩 | HTTP 응답, 리소스 로딩 |
| 레이아웃/UI | 깨짐, 겹침, 정렬 |
| 네비게이션 | 메뉴, 링크 동작 |
| 폼/인터랙션 | 입력, 버튼, 유효성 검사 |
| 반응형 | 데스크톱(1280px) / 태블릿(768px) / 모바일(375px) |
| 콘텐츠 | 이미지 로딩, 텍스트 |
| 에러 처리 | 잘못된 입력, 에러 메시지 |

## 이슈 심각도

| 레벨 | 기준 |
|------|------|
| P1 Critical | 핵심 기능 동작 불가 |
| P2 Major | 주요 기능 손상, 반응형 깨짐, 콘솔 에러 |
| P3 Minor | UI 텍스트 잘림, UX 불편 |

---

## 기술 스택

| 기술 | 용도 |
|------|------|
| **Claude Code** | AI 에이전트 실행 환경 |
| **Claude Code Skill** | `qa-visual-tester` — 재사용 가능한 QA 플로우 정의 |
| **Claude Code Hooks** | 4단계 하네스 파이프라인 (PreToolUse / PostToolUse / Stop / SessionStart) |
| **Playwright MCP** (`@playwright/mcp`) | 실제 브라우저 제어 |
| **CronCreate** | 자율 스케줄링 (평일 09:00 자동 실행) |
| **Git** | 테스트 결과 자동 버전 관리 |
