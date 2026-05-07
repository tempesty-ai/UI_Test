"""
QA 결과 HTML 리포트 생성기
SUMMARY.md + ISSUE.md 파일을 읽어 시각적 HTML 리포트를 생성한다.

사용법:
  python scripts/generate_report.py [SUMMARY.md 경로]
  python scripts/generate_report.py  # 최신 SUMMARY.md 자동 탐색
"""
import os, re, glob, sys
from datetime import datetime
from pathlib import Path


# ── 데이터 파싱 ──────────────────────────────────────────────────────────────

def parse_summary(summary_path: str) -> dict:
    content = open(summary_path, encoding="utf-8").read()

    def get(pattern):
        m = re.search(pattern, content)
        return m.group(1).strip() if m else "?"

    passes  = get(r"PASS\*\*:\s*([0-9]+)")
    fails   = get(r"FAIL\*\*:\s*([0-9]+)")
    warns   = get(r"WARNING\*\*:\s*([0-9]+)")
    url     = get(r"대상 URL\*\*:\s*(https?://\S+)")
    date    = get(r"테스트 일시\*\*:\s*(.+?)(?:\n|$)")
    total   = get(r"총 테스트 항목\*\*:\s*([0-9]+)")

    # 회귀 분석 섹션
    regression_raw = ""
    reg_m = re.search(r"## 회귀 분석(.+?)(?=##|$)", content, re.DOTALL)
    if reg_m:
        regression_raw = reg_m.group(1).strip()

    return {
        "url": url, "date": date, "total": total,
        "passes": passes, "fails": fails, "warns": warns,
        "regression": regression_raw,
        "raw": content,
    }


def parse_issues(session_dir: str) -> list:
    issues = []
    for issue_md in sorted(glob.glob(os.path.join(session_dir, "issues", "*", "ISSUE.md"))):
        content = open(issue_md, encoding="utf-8").read()

        def get(pattern):
            m = re.search(pattern, content)
            return m.group(1).strip() if m else ""

        title   = get(r"# (ISSUE-[0-9]+: .+)")
        sev     = get(r"\*\*심각도\*\*: (.+)")
        cat     = get(r"\*\*카테고리\*\*: (.+)")
        url     = get(r"\*\*URL\*\*: (.+)")
        status  = get(r"\*\*상태\*\*: (.+)")
        symptom_m = re.search(r"## 현상\n(.+?)(?=##)", content, re.DOTALL)
        symptom = symptom_m.group(1).strip()[:300] if symptom_m else ""

        has_shot = os.path.exists(os.path.join(os.path.dirname(issue_md), "screenshot.png"))
        shot_rel = "../" + os.path.relpath(
            os.path.join(os.path.dirname(issue_md), "screenshot.png"),
            session_dir
        ).replace("\\", "/") if has_shot else ""

        issues.append({
            "title": title, "sev": sev, "cat": cat,
            "url": url, "status": status or "Open",
            "symptom": symptom, "screenshot": shot_rel,
        })
    return issues


# ── HTML 생성 ─────────────────────────────────────────────────────────────────

SEV_COLOR = {
    "P1": ("#B60205", "#fff"),
    "P2": ("#b8860b", "#fff"),
    "P3": ("#0075CA", "#fff"),
}
STATUS_COLOR = {
    "Open":     "#e74c3c",
    "Fixed":    "#27ae60",
    "Reopened": "#e67e22",
}


def sev_badge(sev: str) -> str:
    key = sev[:2] if sev else "P3"
    bg, fg = SEV_COLOR.get(key, ("#888", "#fff"))
    return f'<span style="background:{bg};color:{fg};padding:2px 8px;border-radius:4px;font-size:12px;font-weight:bold">{sev}</span>'


def status_badge(status: str) -> str:
    color = STATUS_COLOR.get(status, "#888")
    return f'<span style="color:{color};font-weight:bold">{status}</span>'


def regression_html(text: str) -> str:
    if not text or "첫 번째 테스트" in text:
        return '<p style="color:#888">📌 첫 번째 테스트 실행 — 비교 대상 없음</p>'

    rows = ""
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("-") and "비교" in line:
            continue
        if "|" in line and "---" not in line and "상태" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 3:
                icon_map = {"🆕": "#e74c3c", "🔁": "#e67e22", "✅": "#27ae60"}
                icon = cells[0]
                color = next((v for k, v in icon_map.items() if k in icon), "#333")
                rows += f'<tr><td style="color:{color};font-size:18px">{icon}</td><td>{cells[1]}</td><td>{cells[2]}</td></tr>'

    if not rows:
        return f'<pre style="font-size:13px;color:#555">{text}</pre>'

    return f"""
    <table style="width:100%;border-collapse:collapse;font-size:14px">
      <thead><tr style="background:#f0f0f0">
        <th style="padding:6px;text-align:left">상태</th>
        <th style="padding:6px;text-align:left">이슈</th>
        <th style="padding:6px;text-align:left">심각도</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>"""


def build_html(summary: dict, issues: list, session_dir: str) -> str:
    total   = summary["total"]
    passes  = summary["passes"]
    fails   = summary["fails"]
    warns   = summary["warns"]
    url     = summary["url"]
    date    = summary["date"]

    try:
        p, f, w = int(passes), int(fails), int(warns)
        total_n = p + f + w or 1
        pass_pct = round(p / total_n * 100)
        fail_pct = round(f / total_n * 100)
        warn_pct = 100 - pass_pct - fail_pct
        overall_color = "#27ae60" if f == 0 else "#e74c3c"
        overall_label = "ALL PASS" if f == 0 else f"FAIL {f}건"
    except Exception:
        pass_pct = fail_pct = warn_pct = 0
        overall_color = "#888"
        overall_label = "?"

    issue_cards = ""
    for iss in issues:
        shot = f'<img src="{iss["screenshot"]}" style="width:100%;border-radius:6px;margin-top:12px;border:1px solid #eee" onerror="this.style.display=\'none\'">' if iss["screenshot"] else ""
        issue_cards += f"""
        <div style="background:#fff;border:1px solid #e0e0e0;border-radius:10px;padding:18px;margin-bottom:16px;box-shadow:0 1px 4px rgba(0,0,0,.06)">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
            <strong style="font-size:15px">{iss['title']}</strong>
            <div>{sev_badge(iss['sev'])} &nbsp; {status_badge(iss['status'])}</div>
          </div>
          <div style="font-size:12px;color:#888;margin-bottom:8px">
            📂 {iss['cat']} &nbsp;|&nbsp; 🔗 <a href="{iss['url']}" target="_blank">{iss['url']}</a>
          </div>
          <p style="font-size:13px;color:#444;margin:0">{iss['symptom']}</p>
          {shot}
        </div>"""

    if not issue_cards:
        issue_cards = '<p style="color:#27ae60;font-weight:bold">🎉 발견된 이슈 없음</p>'

    generated = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>QA Report — {url}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; color: #222; }}
  .wrap {{ max-width: 860px; margin: 0 auto; padding: 32px 16px; }}
  h2 {{ font-size: 16px; font-weight: 600; margin-bottom: 12px; color: #333; }}
  .card {{ background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 1px 6px rgba(0,0,0,.07); }}
</style>
</head>
<body>
<div class="wrap">

  <!-- 헤더 -->
  <div class="card" style="border-left: 5px solid {overall_color}">
    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px">
      <div>
        <div style="font-size:12px;color:#888;margin-bottom:4px">QA REPORT</div>
        <div style="font-size:20px;font-weight:700">{url}</div>
        <div style="font-size:13px;color:#888;margin-top:4px">테스트 일시: {date}</div>
      </div>
      <div style="text-align:center">
        <div style="font-size:28px;font-weight:800;color:{overall_color}">{overall_label}</div>
        <div style="font-size:12px;color:#888">총 {total}개 항목</div>
      </div>
    </div>
  </div>

  <!-- 통계 바 -->
  <div class="card">
    <h2>테스트 결과</h2>
    <div style="display:flex;height:12px;border-radius:6px;overflow:hidden;margin:12px 0">
      <div style="width:{pass_pct}%;background:#27ae60"></div>
      <div style="width:{fail_pct}%;background:#e74c3c"></div>
      <div style="width:{warn_pct}%;background:#f39c12"></div>
    </div>
    <div style="display:flex;gap:24px;font-size:14px">
      <div><span style="color:#27ae60;font-size:20px;font-weight:700">{passes}</span> <span style="color:#888">PASS</span></div>
      <div><span style="color:#e74c3c;font-size:20px;font-weight:700">{fails}</span> <span style="color:#888">FAIL</span></div>
      <div><span style="color:#f39c12;font-size:20px;font-weight:700">{warns}</span> <span style="color:#888">WARN</span></div>
    </div>
  </div>

  <!-- 회귀 분석 -->
  <div class="card">
    <h2>회귀 분석</h2>
    {regression_html(summary['regression'])}
  </div>

  <!-- 이슈 목록 -->
  <div class="card">
    <h2>발견된 이슈 ({len(issues)}건)</h2>
    <div style="margin-top:12px">{issue_cards}</div>
  </div>

  <!-- 푸터 -->
  <div style="text-align:center;font-size:12px;color:#aaa;padding:16px 0">
    Generated by QA Visual Tester · {generated} ·
    <a href="https://github.com/tempesty-ai/UI_Test" style="color:#aaa">GitHub</a>
  </div>

</div>
</body>
</html>"""


# ── 실행 ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) > 1:
        summary_path = sys.argv[1]
    else:
        files = glob.glob("D:/code/qa/*/SUMMARY.md")
        if not files:
            print("❌ SUMMARY.md 파일을 찾을 수 없습니다.")
            sys.exit(1)
        summary_path = max(files, key=os.path.getmtime)

    session_dir  = os.path.dirname(summary_path)
    summary      = parse_summary(summary_path)
    issues       = parse_issues(session_dir)
    html         = build_html(summary, issues, session_dir)
    output_path  = os.path.join(session_dir, "report.html")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ HTML 리포트 생성 완료: {output_path}")
    return output_path


if __name__ == "__main__":
    main()
