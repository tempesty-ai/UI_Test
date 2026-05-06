# UI_Test — QA Visual Tester

> Playwright MCP + Claude Code Hook 기반 웹 애플리케이션 시각적 QA 자동화 시스템

GitHub: https://github.com/tempesty-ai/UI_Test

---

## 핵심 개념 정리

### AI 에이전트란?

일반 프로그램은 "A이면 B해라"처럼 모든 행동이 코드에 미리 적혀있다.
**AI 에이전트는 목표만 주면 스스로 방법을 판단하고 행동한다.**

```
일반 프로그램  →  시키는 것만 함 (판단 없음)
AI 에이전트   →  목표를 받아 스스로 계획하고 실행 (판단 있음)
```

이 프로젝트에서 Claude는 `"QA 해줘"` 한 마디를 받아
무엇을 먼저 테스트할지, 어떤 도구를 쓸지, 이슈를 어떻게 분류할지
**스스로 판단해서 끝까지 실행한다.**

---

### 하네스 엔지니어링이란?

AI 에이전트가 혼자 행동하면 실수하거나 비효율적일 수 있다.
**하네스(Harness)는 에이전트 바깥에서 행동 전후를 자동으로 통제하는 구조다.**

> 하네스(Harness) = 말에 채우는 마구(고삐). 말이 아무리 빨라도 방향을 잡아주는 것.

- 에이전트가 잘못된 방향으로 가면 → **막는다** (가드레일)
- 에이전트가 결과를 저장하면 → **자동으로 백업한다** (부작용 자동화)
- 에이전트가 일을 끝내면 → **요약을 뽑아낸다** (자동 리포트)

**에이전트는 하네스의 존재를 모른다. 그냥 일하는데 뒤에서 알아서 돌아간다.**

---

### SKILL.md는 뭐가 다른가?

```
SKILL.md   →  에이전트 안에 영향을 준다
              "QA를 할 때는 이런 순서로 생각해" 라고 가르치는 것
              에이전트 설계

하네스     →  에이전트 밖에서 개입한다
              에이전트가 행동하는 타이밍에 자동으로 끼어드는 것
              에이전트 제어
```

| | SKILL.md | 하네스 (Hook) |
|--|---------|--------------|
| 누가 읽나 | Claude | Claude Code 런타임 |
| 언제 작동 | Claude가 생각할 때 | Claude가 도구를 쓰는 순간 |
| 목적 | 판단 방식 가르치기 | 행동 전후 자동 제어 |
| Claude가 아나 | ✅ 알고 따름 | ❌ 모름 |

---

## 이 프로젝트에 적용한 것들

### AI 에이전트 — Claude가 스스로 판단하는 부분

| 구성요소 | 역할 |
|---------|------|
| **SKILL.md** | Claude에게 QA 절차·판단 기준·출력 형식을 가르침 |
| **targets.json** | Claude가 읽는 설정 파일. URL만 바꾸면 대상 자동 변경 |
| **Playwright MCP** | Claude가 직접 호출하는 브라우저 조작 도구 |
| **Cron 스케줄러** | 평일 09:00 Claude에게 자동으로 QA 프롬프트 주입 |

### 하네스 — 에이전트 밖에서 자동으로 제어하는 부분

| Hook | 언제 발동 | 하는 일 |
|------|---------|--------|
| **PreToolUse** | Claude가 브라우저 열기 직전 | 대상 사이트 생사 여부 확인. 다운이면 차단 |
| **PostToolUse** | Claude가 SUMMARY.md 저장 직후 | 자동으로 git add → commit → push |
| **Stop** | Claude가 응답 완료 직후 | PASS / FAIL / WARN 카운트 터미널 출력 |
| **SessionStart** | Claude Code 세션 시작 시 | 마지막 결과 + 다음 대상 대시보드 주입 |

---

## 전체 흐름

```
[Cron 09:00] 자동 트리거 ──────────────────────────────┐
                                                       │ 사람이 직접 말해도 동일
[SessionStart Hook] "어제 결과 / 오늘 대상" 브리핑       │
        ↓                                              │
[Claude + SKILL.md] targets.json 읽고 테스트 계획 수립 ←┘
        ↓
[PreToolUse Hook] URL 죽었으면 여기서 차단
        ↓
[Playwright MCP] 실제 브라우저 — 3개 뷰포트 테스트
        ↓
[PostToolUse Hook] SUMMARY.md 저장 감지 → GitHub 자동 push
        ↓
[Stop Hook] PASS / FAIL / WARN 요약 출력
```

**에이전트가 일하고, 하네스가 그 전후를 통제한다. 사람은 targets.json URL만 관리하면 끝.**

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
| **Claude Code Skill** | `qa-visual-tester` — QA 판단 절차 정의 |
| **Claude Code Hooks** | 4단계 하네스 (PreToolUse / PostToolUse / Stop / SessionStart) |
| **Playwright MCP** (`@playwright/mcp`) | 실제 브라우저 제어 |
| **CronCreate** | 자율 스케줄링 (평일 09:00 자동 실행) |
| **Git** | 테스트 결과 자동 버전 관리 |
