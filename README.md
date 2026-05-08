# UI_Test - Claude Code 기반 시각적 QA 파이프라인

> Claude Code hook과 Playwright MCP를 중심으로 구성한 시각적 QA 실행 파이프라인입니다.
> 완전 자율 에이전트 시스템으로 포장하기보다, 무엇을 자동화했고 무엇을 측정하며 어디에 사람의 QA 판단이 필요한지 문서화합니다.

## 데이터 안내

이 저장소의 대상 사이트는 `practicesoftwaretesting.com` 같은 공개 데모 사이트입니다. 현재 또는 과거 회사/고객사의 서비스 URL, 화면, 내부 데이터, 운영 workflow는 포함하지 않습니다. `targets.json`이 검사 대상 URL의 기준입니다.

## 문제

시각적 QA 업무에는 desktop, tablet, mobile viewport를 반복적으로 확인하는 작업이 자주 포함됩니다. 또한 screenshot, console log, issue summary 같은 일관된 증거가 필요합니다.

이 프로젝트는 반복되는 부분을 자동화하되, 사람의 판단 지점을 명확히 남기는 것을 목표로 합니다. QA는 `targets.json`을 편집해 무엇을 검사할지 결정합니다.

## 구현 내용

| 구성 요소 | 역할 |
| --- | --- |
| Playwright MCP 호출 | 페이지 열기, viewport 검사, screenshot 캡처, browser evidence 수집 |
| Claude Code hooks | 실행, 보고, session summary, 선택적 알림에 guardrail 추가 |
| `targets.json` | 공개 데모 사이트와 focus area 정의 |
| 표준 출력 폴더 | `SUMMARY.md`, issue detail, screenshot, report를 반복 가능한 구조로 저장 |

## Hook 설계

| Hook | 시점 | 목적 |
| --- | --- | --- |
| `PreToolUse` | Browser navigation 전 | 대상 접근 가능 여부를 확인하고 unavailable target 차단 |
| `PostToolUse` | 결과 파일 작성 후 | report 생성 및 후속 기록 생성 가능 |
| `Stop` | Claude 작업 종료 시 | PASS/FAIL/WARN count 요약 |
| `SessionStart` | session 시작 시 | 최신 결과와 다음 target context 표시 |

중요한 설계 포인트는 검사 절차와 side effect를 모델의 주 추론 흐름 밖에 둔다는 것입니다.

## 검사 영역

| 분류 | 확인 항목 |
| --- | --- |
| 페이지 로딩 | HTTP response와 resource loading |
| Layout/UI | 깨진 layout, overlap, alignment, clipped text |
| Navigation | menu와 link 동작 |
| Form/interaction | input, button, validation message |
| 반응형 layout | desktop, tablet, mobile viewport |
| Content | image와 text rendering |
| 오류 처리 | invalid input과 console error |

## 심각도 기준

| 수준 | 기준 |
| --- | --- |
| P1 Critical | 핵심 기능이 막힘 |
| P2 Major | 주요 기능 손상, 반응형 깨짐, console error |
| P3 Minor | text clipping, visual polish issue, UX 불편 |

## 빠른 시작

`targets.json`에는 공개 데모 target만 넣습니다.

```json
{
  "targets": [
    {
      "url": "https://your-public-demo-site.example",
      "name": "demo_site",
      "focus": ["responsive", "login", "search"]
    }
  ]
}
```

그 다음 Claude Code에서 실행합니다.

```text
Read targets.json and run a QA inspection.
```

## 출력물

검사 후 파이프라인은 다음 파일을 저장합니다.

- `[date]_[domain]/SUMMARY.md` - issue summary report
- `[date]_[domain]/issues/ISSUE-XXX_*/` - issue detail과 screenshot
- `report.html` - 활성화 시 생성되는 HTML report

## QA 가치

| 수동 방식 | 파이프라인 방식 |
| --- | --- |
| viewport별로 매번 수동 캡처 | desktop/tablet/mobile 증거를 반복 가능한 방식으로 캡처 |
| 사람마다 결과 형식이 달라짐 | `SUMMARY.md`와 `issues/`가 표준 구조를 따름 |
| 증거가 chat이나 email에 흩어짐 | git history를 통해 검사 결과를 보존 가능 |

가치는 한 번의 검사보다, 시간이 지나며 품질 변화를 추적할 수 있다는 점에 있습니다.

## 결과

| 항목 | 측정 |
| --- | --- |
| 하나의 사이트를 세 viewport에서 검사 | 수동 약 25~30분 -> 자동화 약 5~8분 |
| 출력 일관성 | 매 실행마다 동일한 `SUMMARY.md`와 `issues/` 구조 |
| 추적성 | git history를 통해 결과 추적 가능 |
| 사람의 입력 지점 | target set별로 `targets.json`을 한 번 편집 |

## 한계

- 완전한 agentic QA 시스템이 아니라 Claude Code hook과 Playwright MCP 파이프라인입니다.
- 판단 정확도는 아직 충분히 benchmark하지 않았습니다. False positive와 false negative 측정이 더 필요합니다.
- 별도 보안 검토 전까지 target은 공개 데모 사이트로 제한해야 합니다.
- 실행 비용은 Claude reasoning과 검사 빈도에 따라 달라집니다.

## 기술 스택

| 기술 | 목적 |
| --- | --- |
| Claude Code | 실행 환경 |
| Claude Code skill | 검사 절차와 출력 형식 |
| Claude Code hooks | Guardrail과 후처리 |
| Playwright MCP | Browser automation |
| Git | 버전 관리되는 증거와 결과 추적 |

## 로드맵

- False positive/false negative benchmark case 추가
- 반복 검사 간 품질 추세 시각화
- 인증이 필요한 demo target을 위한 별도 secure mode 추가
