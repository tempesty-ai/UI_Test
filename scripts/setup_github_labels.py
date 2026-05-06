"""
GitHub 라벨 초기 설정 스크립트
실행 전 GH_TOKEN 환경변수 필요:
  Windows: [System.Environment]::SetEnvironmentVariable("GH_TOKEN", "ghp_...", "User")

실행:
  python scripts/setup_github_labels.py
"""
import os, json, urllib.request, urllib.error

REPO   = "tempesty-ai/UI_Test"
TOKEN  = os.environ.get("GH_TOKEN", "")

if not TOKEN:
    print("❌ GH_TOKEN 환경변수가 없습니다.")
    print("   GitHub → Settings → Developer settings → Personal access tokens → Generate new token (repo 권한 필요)")
    exit(1)

LABELS = [
    {"name": "P1-critical", "color": "B60205", "description": "핵심 기능 동작 불가, 결제/인증 오류"},
    {"name": "P2-major",    "color": "E4E669", "description": "주요 기능 손상, 반응형 깨짐, 콘솔 에러"},
    {"name": "P3-minor",    "color": "0075CA", "description": "UI 텍스트 잘림, 아이콘 위치, UX 불편"},
    {"name": "QA-auto",     "color": "5319E7", "description": "QA 에이전트 자동 등록"},
]

headers = {
    "Authorization": f"token {TOKEN}",
    "Content-Type":  "application/json",
    "Accept":        "application/vnd.github.v3+json",
}

for label in LABELS:
    try:
        req = urllib.request.Request(
            f"https://api.github.com/repos/{REPO}/labels",
            data=json.dumps(label).encode("utf-8"),
            headers=headers,
        )
        urllib.request.urlopen(req, timeout=10)
        print(f"✅ 생성: {label['name']}")
    except urllib.error.HTTPError as e:
        if e.code == 422:
            print(f"⏭️  이미 존재: {label['name']}")
        else:
            print(f"❌ 실패: {label['name']} ({e.code})")

print("\n완료! GitHub Issues 탭에서 라벨을 확인하세요.")
print(f"https://github.com/{REPO}/labels")
