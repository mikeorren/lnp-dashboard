
import json, sys

with open("data.json") as f:
    D = json.load(f)
M = D["meta"]

DOCTYPE = chr(60) + chr(33) + 'DOCTYPE html>'

CSS = r"""
<style>
  :root{--green:#4C902F;--green-dk:#3a6f24;--tan:#E5E0DE;--ink:#1f2418;--up:#2f8f3f;--down:#c0392b;--flat:#6b7280;--line:#dcd7d2;}
  *{box-sizing:border-box}
  body{margin:0;background:#f6f4f2;color:var(--ink);font-family:'Inter',-apple-system,Segoe UI,Roboto,sans-serif;font-size:15px;line-height:1.45}
  .wrap{max-width:1160px;margin:0 auto;padding:28px 22px 60px}
  header.top{border-bottom:4px solid var(--green);padding-bottom:14px;margin-bottom:8px}
  h1{font-family:'Oswald',sans-serif;font-weight:700;letter-spacing:.5px;text-transform:uppercase;color:var(--green-dk);margin:0;font-size:30px}
  .sub{color:#555;font-size:13.5px;margin-top:4px}
  .meta{display:flex;flex-wrap:wrap;gap:8px 18px;font-size:12.5px;color:#666;margin-top:10px}
  .meta b{color:var(--ink)}
  h2{font-family:'Oswald',sans-serif;font-weight:600;text-transform:uppercase;letter-spacing:.6px;font-size:18px;color:var(--green-dk);margin:30px 0 10px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
  h2 .src{font-family:'Inter';text-transform:none;letter-spacing:0;font-size:11.5px;font-weight:600;color:#fff;background:var(--green);padding:2px 8px;border-radius:20px}
  h2 .pend{background:#9aa0a6}
  .cap{font-family:'Oswald';text-transform:uppercase;letter-spacing:.5px;font-size:13px;color:var(--green-dk);font-weight:600;margin:20px 0 6px}
  table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden}
  th,td{padding:9px 12px;text-align:right;font-variant-numeric:tabular-nums}
  th:first-child,td:first-child{text-align:left}
  thead th{background:var(--green);color:#fff;font-family:'Oswald';font-weight:500;letter-spacing:.4px;font-size:12.5px;text-transform:uppercase}
  thead th small{display:block;font-weight:400;font-size:10.5px;opacity:.85;letter-spacing:0}
  tbody tr:nth-child(even){background:#faf9f7}
  tbody td{border-top:1px solid var(--line);font-size:13.5px}
  td.metric{font-weight:600}
  .delta{font-weight:600;font-size:13px}
  .down{color:var(--down)} .up{color:var(--up)} .flat{color:var(--flat)}
  .neg{color:var(--down)}
  .grp td{background:var(--tan);font-family:'Oswald';text-transform:uppercase;letter-spacing:.5px;font-size:12px;color:var(--green-dk);font-weight:600;text-align:left}
  .totrow td{font-weight:700;border-top:2px solid var(--green)}
  .sub-row td{background:#fbfcf8}
  .chan{display:grid;grid-template-columns:1fr auto auto;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden;margin-top:6px}
  .chan .cell{padding:8px 12px;border-top:1px solid var(--line);font-size:13.5px;font-variant-numeric:tabular-nums;text-align:right}
  .chan .cell.name{text-align:left;font-weight:500}
  .chan .head .cell{background:var(--green);color:#fff;border-top:0;font-family:'Oswald';font-size:12px;text-transform:uppercase;letter-spacing:.4px}
  .note{font-size:12.5px;color:#666;margin-top:8px}
  .flag{background:#fff8e8;border:1px solid #eacb6b;border-left:5px solid #d99e00;border-radius:8px;padding:10px 13px;margin-top:8px;font-size:12.5px;color:#5b4a12}
  .ok{background:#eef7ea;border:1px solid #bcdcae;border-left:5px solid var(--green);border-radius:8px;padding:10px 13px;margin-top:8px;font-size:12.5px;color:#31541f}
  footer{margin-top:34px;border-top:1px solid var(--line);padding-top:14px;font-size:12px;color:#777}
  .pill{display:inline-block;background:var(--tan);color:var(--green-dk);font-weight:600;font-size:11px;padding:2px 9px;border-radius:20px;margin-right:6px}
</style>
"""

def dsp(d):
    if not d: return ""
    return '<span class="delta %s">%s</span>' % (d["d"], d["t"])

def cellcls(i, row):
    if i in row.get("neg", []): return ' class="neg"'
    if i in row.get("pos", []): return ' class="up"'
    if i in row.get("flat", []): return ' class="flat"'
    return ""

out = []
out.append(DOCTYPE)
out.append('<html lang="en"><head><meta charset="utf-8">')
out.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
out.append('<meta name="robots" content="noindex,nofollow">')
out.append('<title>LNP / Always Lancaster \u2014 Living Data Dashboard</title>')
out.append('<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">')
out.append(CSS)
out.append('</head><body><div class="wrap">')

# Header
out.append('<header class="top"><h1>Living Data Dashboard</h1>')
out.append('<div class="sub">LNP&nbsp;|&nbsp;LancasterOnline / Always Lancaster &mdash; financial health, audience &amp; subscriptions</div>')
out.append('<div class="meta">')
out.append('<span><b>Generated:</b> %s</span>' % M["generated"])
out.append('<span><b>Financials:</b> ' + M["fin_report_label"] + ' report &mdash; Actual / Forecast / Prior Yr</span>')
out.append('<span><b>Audience:</b> GA4 (317546010) &mdash; %s</span>' % M["audience_week"])
out.append('<span><b>Subscriptions:</b> Piano Analytics + Subscription Report</span>')
out.append('</div></header>')

# Financials consolidated
out.append('<h2>Financials &mdash; LNP | Always Lancaster (consolidated) <span class="src">' + M["fin_mo"] + ' Financials</span></h2>')
out.append('<table><thead><tr><th>Metric</th>'
           '<th>Actual<small>' + M["fin_mo"] + '</small></th><th>Forecast<small>' + M["fin_mo"] + '</small></th><th>Prior yr<small>' + M["fin_mo_py"] + '</small></th>'
           '<th>Actual<small>YTD 2026</small></th><th>Forecast<small>YTD 2026</small></th><th>Prior yr<small>YTD 2025</small></th></tr></thead><tbody>')
for row in D["fin_consolidated"]:
    if "group" in row:
        out.append('<tr class="grp"><td colspan="7">%s</td></tr>' % row["group"])
        continue
    out.append('<tr><td class="metric">%s</td>' % row["label"])
    for i, c in enumerate(row["cells"]):
        out.append('<td%s>%s</td>' % (cellcls(i, row), c))
    out.append('</tr>')
out.append('</tbody></table>')
out.append('<div class="note">%s</div>' % D["fin_note"])

# By publication
out.append('<div class="cap">By publication (Actual)</div>')
out.append('<table><thead><tr><th>Publication</th><th>Revenue<small>' + M["fin_mo_short"] + '</small></th><th>Revenue<small>YTD</small></th><th>Net income<small>' + M["fin_mo_short"] + '</small></th><th>Net income<small>YTD</small></th></tr></thead><tbody>')
for row in D["fin_by_pub"]:
    tr = ' class="totrow"' if row.get("total") else ''
    out.append('<tr%s><td class="metric">%s</td>' % (tr, row["label"]))
    for i, c in enumerate(row["cells"]):
        out.append('<td%s>%s</td>' % (cellcls(i, row), c))
    out.append('</tr>')
out.append('</tbody></table>')

# Revenue mix
out.append('<div class="cap">Revenue mix &mdash; LancasterOnline (print vs digital)</div>')
out.append('<table><thead><tr><th>Revenue line</th><th>Actual<small>' + M["fin_mo"] + '</small></th><th>Actual<small>YTD 2026</small></th><th>YTD YoY</th></tr></thead><tbody>')
for row in D["fin_revmix"]:
    tr = ' class="totrow"' if row.get("total") else ''
    out.append('<tr%s><td class="metric">%s</td><td>%s</td><td>%s</td><td class="delta %s">%s</td></tr>'
               % (tr, row["label"], row["cells"][0], row["cells"][1], row["delta"]["d"], row["delta"]["t"]))
out.append('</tbody></table>')
out.append('<div class="note">%s</div>' % D["fin_revmix_note"])

# Audience
out.append('<h2>Audience <span class="src">%s</span></h2>' % M["audience_src"])
out.append('<table><thead><tr><th>Metric</th>'
           '<th>Current week<small>%s</small></th><th>Same wk prior yr<small>%s</small></th><th>Wk YoY</th>'
           '<th>YTD<small>%s</small></th><th>Prior YTD<small>%s</small></th><th>YTD YoY</th></tr></thead><tbody>'
           % (M["audience_week"], M["audience_week_py"], M["audience_ytd"], M["audience_ytd_py"]))
for r in D["audience_rows"]:
    out.append('<tr><td class="metric">%s</td><td>%s</td><td>%s</td><td class="delta %s">%s</td><td>%s</td><td>%s</td><td class="delta %s">%s</td></tr>'
               % (r["label"], r["wk"], r["pywk"], r["wd"]["d"], r["wd"]["t"], r["ytd"], r["pyytd"], r["yd"]["d"], r["yd"]["t"]))
out.append('</tbody></table>')
if M.get("audience_stale"):
    out.append('<div class="flag"><b>Heads up &mdash; audience not yet auto-refreshing.</b> These numbers are a manual snapshot from %s. Once the refresh routine is live this updates every week automatically.</div>' % M["audience_week"])
else:
    out.append('<div class="ok"><b>Live.</b> Audience auto-refreshes weekly &mdash; last updated %s.</div>' % M.get("audience_refreshed",""))
out.append('<div class="note">%s</div>' % D["audience_note"])

# Channels
out.append('<h2>Traffic by channel <span class="src">%s</span></h2>' % M["audience_src"])
out.append('<div class="chan"><div class="head" style="display:contents"><div class="cell name">Channel</div><div class="cell">Current week (sessions / share)</div><div class="cell">YTD (sessions / share)</div></div>')
for c in D["channels"]:
    out.append('<div style="display:contents"><div class="cell name">%s</div><div class="cell">%s</div><div class="cell">%s</div></div>' % (c["name"], c["wk"], c["ytd"]))
out.append('</div>')
out.append('<div class="note">%s</div>' % D["channels_note"])

# Subscriptions
out.append('<h2>Subscriptions <span class="src">Piano Analytics + Subscription Report</span></h2>')
out.append('<table><thead><tr><th>Metric</th>'
           '<th>Prior month<small>Jul 2026</small></th><th>Same mo prior yr<small>Jul 2025</small></th><th>Mo YoY</th>'
           '<th>YTD<small>Jan&ndash;Jul 2026</small></th><th>Prior YTD<small>Jan&ndash;Jul 2025</small></th><th>YTD YoY</th></tr></thead><tbody>')
for r in D["subs_rows"]:
    if r.get("sub"):
        out.append('<tr class="sub-row"><td class="metric" style="font-weight:500">%s</td><td>%s</td><td colspan="5" style="color:#6b7280;font-style:italic;text-align:left">%s</td></tr>'
                   % (r["label"], r["c0"], r.get("note","")))
    elif "note" in r and "c3" not in r:
        out.append('<tr><td class="metric">%s</td><td>%s</td><td>%s</td><td class="delta %s">%s</td><td colspan="3" style="color:#8a8f98;font-style:italic;text-align:left">%s</td></tr>'
                   % (r["label"], r["c0"], r["c1"], r["d1"]["d"], r["d1"]["t"], r["note"]))
    else:
        out.append('<tr><td class="metric">%s</td><td>%s</td><td>%s</td><td class="delta %s">%s</td><td>%s</td><td>%s</td><td class="delta %s">%s</td></tr>'
                   % (r["label"], r["c0"], r["c1"], r["d1"]["d"], r["d1"]["t"], r["c3"], r["c4"], r["d5"]["d"], r["d5"]["t"]))
out.append('</tbody></table>')
out.append('<div class="note">%s</div>' % D["subs_note"])

# Still to wire
out.append('<h2>Still to wire <span class="src pend">pending source</span></h2>')
out.append('<div class="note" style="font-size:13px">%s</div>' % D["still_to_wire"])

# Footer
out.append('<footer>')
out.append('<div><span class="pill">Sources</span> Financials: ' + M["fin_report_label"] + ' report (LNP | Always Lancaster consolidated). Audience: GA4 property 317546010. Subscriptions: Piano Analytics + Subscription Report term export (as of %s).</div>' % M["subs_asof"])
out.append('<div style="margin-top:6px"><span class="pill">Cadence</span> Audience weekly; subscriptions &amp; financials monthly.</div>')
out.append('<div style="margin-top:6px"><span class="pill">Auto</span> Rendered from data.json by the LNP Living Dashboard refresh routine.</div>')
out.append('</footer>')

out.append('</div></body></html>')

html = "\n".join(out)
with open("index.html","w") as f:
    f.write(html)
print("index.html bytes:", len(html.encode("utf-8")))
