# UI_Test — QA Visual Tester

Playwright MCP + Claude Code Hook 기반 웹 애플리케이션 시각적 QA 자동화 시스템

---

## 아키텍처

```
[Cron 스케줄러]  평일 09:03 자동 트리거
        ↓
[SessionStart Hook] 마지막 QA 결과 대시보드 표시
        ↓
[PreToolUse Hook]   URL 접근 가능 여부 사전 검증
        ↓
Claude + qa-visual-tester 스킬 + Playwright MCP
        ↓
[PostToolUse Hook]  SUMMARY.md 저장 → 자동 git push
        ↓
[Stop Hook]         터미널에 PASS/FAIL/WARN 요약 출력
```

사람이 직접 명령하거나, Cron이 자동으로 트리거 — 두 경우 모두 동일한 파이프라인을 탄다.

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
- `[날짜]_[도메인]/SUMMARY.md` — 이슈 요약 리포트 생성
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

- **Claude Code** — AI 에이전트 실행 환경
- **Playwright MCP** (`@playwright/mcp`) — 실제 브라우저 제어
- **Hook Pipeline** — PreToolUse / PostToolUse / Stop 자동화
- **Git** — 테스트 결과 자동 버전 관리
