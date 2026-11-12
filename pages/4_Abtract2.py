"""풍선과 추 - 정수의 덧셈과 뺄셈 (Streamlit 버전 2)

실행:  streamlit run app.py
풍선 1개 = +1 m, 추 1개 = -1 m.  사람의 높이 = (풍선 수) - (추 수)

학생이 개수(1~10)를 정하고 버튼을 누르면 그 수만큼 달거나 뗀다.
식에는 (+3), (-2)처럼 정한 개수가 그대로 들어간다.
"""
import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------------- 설정
MAX = 10            # 높이(m) 한계, 풍선/추 개수 한계
U = 12              # 1 m 를 그림에서 몇 칸으로 그릴지
ZERO = 240          # 해수면의 y 좌표
CX = 212            # 사람의 x 좌표
KY = -56            # 풍선 끈이 모이는 매듭 위치
VB_H = 452          # 그림 전체 높이 (+10 m 위쪽과 -10 m 아래쪽만 남기고 줄였다)
SCENE_H = 480       # 화면에 보이는 장면 높이(px)
MINUS = "−"    # 수학용 빼기 기호(−)

# 풍선 10개가 놓이는 자리(사람 기준 x, y). 가로로 넓게 3줄로 쌓아 높이를 줄였다.
BAL = [(0, -74), (-15, -74), (15, -74), (-30, -74), (30, -74),
       (-7.5, -88), (7.5, -88), (-22.5, -88), (22.5, -88),
       (0, -102)]
BAL_COLORS = ["#E5533C", "#D9437A", "#F0802F"]

# 연산 4가지 -> (식에 쓰는 부호, 더하거나 빼는 수의 부호, 높이 변화의 부호)
#   aB: 풍선 달기 = (+n)을 더함   aW: 추 달기 = (-n)을 더함
#   sB: 풍선 떼기 = (+n)을 뺌     sW: 추 떼기 = (-n)을 뺌
OPS = {
    "aB": ("+", +1, +1),
    "aW": ("+", -1, -1),
    "sB": (MINUS, +1, -1),
    "sW": (MINUS, -1, +1),
}
NAMES = {"aB": "풍선 {n}개 달기", "aW": "추 {n}개 달기",
         "sB": "풍선 {n}개 떼기", "sW": "추 {n}개 떼기"}


def sgn(n: int) -> str:
    """정수를 +3, −3, 0 꼴로 쓴다."""
    return f"+{n}" if n > 0 else f"{MINUS}{-n}" if n < 0 else "0"


def desc(h: int) -> str:
    if h > 0:
        return f"해수면보다 {h} m 위"
    if h < 0:
        return f"해수면보다 {-h} m 아래"
    return "해수면과 같은 높이"


def op_value(k: str, n: int) -> int:
    """식에 들어가는 수: 풍선은 +n, 추는 -n."""
    return OPS[k][1] * n


def op_text(k: str, n: int) -> str:
    sign, _, dh = OPS[k]
    verb = "더해요" if sign == "+" else "빼요"
    move = "올라갔어요" if dh > 0 else "내려갔어요"
    return f"{NAMES[k].format(n=n)}: ({sgn(op_value(k, n))})을 {verb}. {n} m {move}."


# ---------------------------------------------------------------- 규칙
def max_n(k: str, b: int, w: int) -> int:
    """지금 한 번에 할 수 있는 가장 큰 개수(0이면 아예 못 함)."""
    h = b - w
    if k == "aB":
        m = min(MAX - b, MAX - h)
    elif k == "aW":
        m = min(MAX - w, MAX + h)
    elif k == "sB":
        m = min(b, MAX + h)
    else:
        m = min(w, MAX - h)
    return max(0, min(m, MAX))


def why(k: str, b: int, w: int) -> str:
    """버튼을 전혀 누를 수 없을 때의 이유."""
    h = b - w
    if k == "aB":
        return "풍선은 10개까지" if b >= MAX else "+10 m가 끝이에요"
    if k == "aW":
        return "추는 10개까지" if w >= MAX else f"{MINUS}10 m가 끝이에요"
    if k == "sB":
        return "달린 풍선 없음" if b == 0 else f"{MINUS}10 m가 끝이에요"
    return "달린 추 없음" if w == 0 else "+10 m가 끝이에요"


def apply(k: str, n: int, direction: int, s) -> None:
    """direction=+1 이면 연산을 하고, -1 이면 되돌린다."""
    if k == "aB":
        s.b += direction * n
    elif k == "aW":
        s.w += direction * n
    elif k == "sB":
        s.b -= direction * n
    else:
        s.w -= direction * n


# ---------------------------------------------------------------- 상태
def remember_before() -> None:
    """애니메이션의 출발점으로 쓰려고 바뀌기 전 상태를 저장한다."""
    s = st.session_state
    s.prev_h, s.prev_b, s.prev_w = s.b - s.w, s.b, s.w


def init_state() -> None:
    s = st.session_state
    if "b" in s:
        return
    s.b, s.w = 3, 1                          # 예시로 시작: 풍선 3개, 추 1개
    s.hist = [("aB", 3), ("aW", 1)]          # (연산, 개수) 목록
    s.prev_h, s.prev_b, s.prev_w = s.b - s.w, s.b, s.w
    s.last = "예시로 풍선 3개와 추 1개를 달아 두었어요. '처음부터'를 누르면 0 m에서 시작해요."
    s.warn = False


def act(k: str) -> None:
    s = st.session_state
    n = int(s.n)
    m = max_n(k, s.b, s.w)
    if n > m:
        s.warn = True
        s.last = (f"{NAMES[k].format(n=n)}는 지금 할 수 없어요. "
                  + (f"{m}개까지만 가능해요. 개수를 바꿔 보세요." if m else why(k, s.b, s.w) + "."))
        return
    remember_before()
    apply(k, n, +1, s)
    s.hist.append((k, n))
    s.last, s.warn = op_text(k, n), False


def undo() -> None:
    s = st.session_state
    if not s.hist:
        return
    remember_before()
    k, n = s.hist.pop()
    apply(k, n, -1, s)
    s.last, s.warn = "방금 한 일을 되돌렸어요.", False


def reset() -> None:
    s = st.session_state
    remember_before()
    s.b, s.w, s.hist = 0, 0, []
    s.last, s.warn = "0 m에서 다시 시작해요. 개수를 정하고 버튼을 눌러 보세요.", False


# ---------------------------------------------------------------- 그림
SCENE_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Jua&display=swap" rel="stylesheet">
<style>
  body{margin:0;background:transparent;font-family:"Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif}
  .scene{position:relative;height:__H__px;max-width:460px;margin:0 auto;border-radius:18px;overflow:hidden;
         border:1px solid #C3D4D9;background:#A6D8F0}
  .scene svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
  svg text{font-family:"Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;user-select:none}
  .cloud{animation:drift 22s ease-in-out infinite alternate}
  .cloud.b{animation-duration:31s;animation-direction:alternate-reverse}
  @keyframes drift{from{transform:translateX(-16px)}to{transform:translateX(16px)}}
  .fish{animation:swim 52s linear infinite}
  @keyframes swim{from{transform:translateX(-170px)}to{transform:translateX(540px)}}
  .wave{animation:wave 3.6s linear infinite}
  .wave.w2{animation-duration:5.2s;animation-direction:reverse}
  @keyframes wave{to{transform:translateX(-40px)}}
  .bob{animation:bob 2.8s ease-in-out infinite}
  @keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-1.6px)}}
  .bub{fill:none;stroke:#fff;stroke-width:.9;opacity:0;animation:rise 2.2s ease-in infinite}
  .bub:nth-child(2){animation-delay:.7s}.bub:nth-child(3){animation-delay:1.4s}
  @keyframes rise{0%{transform:translateY(0);opacity:0}20%{opacity:.9}100%{transform:translateY(-24px);opacity:0}}
  /* 새로 달린 것은 톡 나타나고, 떼어 낸 것은 사라진다 */
  .pn{transform-box:fill-box}
  .pn.b{transform-origin:50% 100%}
  .pn.w{transform-origin:50% 0%}
  .pn.new{animation:popin .4s cubic-bezier(.3,1.5,.5,1) both}
  .pn.gone{animation:popout .4s ease-in both}
  @keyframes popin{from{transform:scale(.15);opacity:0}}
  @keyframes popout{to{transform:scale(.15);opacity:0}}
  .str{fill:none;stroke:#43606F;stroke-width:.8}
  .rope{fill:none;stroke:#4A5A65;stroke-width:1.3}
  .lab{fill:#fff;font-size:7px;font-weight:600;text-anchor:middle;dominant-baseline:central}
  .wl{fill:#EAF2F6;font-size:6.6px;font-weight:600;text-anchor:middle;dominant-baseline:central}
  .mouth{fill:none;stroke:#2C211C;stroke-width:1.1;stroke-linecap:round}
  .rl{font-size:9.5px;fill:#2F5668;text-anchor:end;dominant-baseline:central}
  .rl.edge{font-weight:600;fill:#0C2B3A}
  .note{font-size:9.5px;fill:#2F5668;text-anchor:end}
  .note.lvl{font-weight:600;fill:#0C2B3A}
  .ptx{fill:#fff;font-size:10.5px;font-weight:600;text-anchor:middle;dominant-baseline:central}
  .hud{position:absolute;top:12px;right:16px;text-align:right;color:#0C2B3A;max-width:55%}
  .hud .lbl{font-size:12px;letter-spacing:.04em;color:#2F5668}
  .hud .big{font:400 50px/1.05 "Jua","Noto Sans KR",system-ui,sans-serif}
  .hud .big small{font-size:21px;margin-left:4px}
  .hud .desc{font-size:14px;font-weight:500}
  .hud .cnt{margin-top:4px;font-size:13px;color:#2F5668}
  @media (prefers-reduced-motion:reduce){*{animation:none!important}}
</style>
""".replace("__H__", str(SCENE_H))

FISH = ('<path d="M-9 0 q9-6 18 0 q-9 6-18 0z M-9 0 l-7-4.5 v9z" fill="#F3A74F"/>'
        '<circle cx="4.5" cy="-1.2" r=".9" fill="#2b1d12"/>')


def y_of(m: float) -> float:
    return ZERO - U * m


def ruler_svg() -> str:
    """-11 m ~ +11 m 눈금. 한계(±10)는 굵게 쓴다."""
    out = [f'<line x1="40" x2="40" y1="{y_of(11)}" y2="{y_of(-11)}" stroke="rgba(12,43,58,.5)"/>']
    for m in range(-11, 12):
        length = 8 if m % 2 == 0 else 5
        faint = ' opacity=".35"' if abs(m) > MAX else ""
        out.append(f'<line x1="40" x2="{40 + length}" y1="{y_of(m)}" y2="{y_of(m)}" '
                   f'stroke="rgba(12,43,58,.5)"{faint}/>')
        if m % 2 == 0 and abs(m) <= MAX:
            edge = " edge" if abs(m) == MAX else ""
            out.append(f'<text class="rl{edge}" x="34" y="{y_of(m)}">{sgn(m)}</text>')
    return "".join(out)


def balloons_svg(b: int, prev_b: int) -> str:
    out = []
    for i in range(max(b, prev_b)):
        x, y = BAL[i]
        c = BAL_COLORS[i % 3]
        if i >= b:
            state, delay = "gone", 0
        elif i >= prev_b:
            state, delay = "new", round((i - prev_b) * 0.06, 2)
        else:
            state, delay = "", 0
        out.append(
            f'<g transform="translate({x} {y})"><g class="pn b {state}" style="animation-delay:{delay}s">'
            f'<path class="str" d="M0 9 L{-x} {KY - y}"/>'
            f'<ellipse rx="7.6" ry="9" fill="{c}"/><path d="M0 8.6 l-2 3.2 h4z" fill="{c}"/>'
            f'<ellipse cx="-2.6" cy="-3.4" rx="1.9" ry="3.2" fill="#fff" opacity=".35"/>'
            f'<text class="lab" y="0.6">+1</text></g></g>')
    return "".join(out)


def weight_slot(count: int, i: int):
    """추가 count개 달려 있을 때 i번째 추의 (x, 줄 번호). 많아지면 줄 수를 늘려 높이를 줄인다."""
    cols = 1 if count <= 4 else 2 if count <= 8 else 3
    x = {1: [0], 2: [-9, 9], 3: [-16, 0, 16]}[cols][i % cols]
    return x, i // cols


def weights_svg(w: int, prev_w: int) -> str:
    out = []
    for i in range(max(w, prev_w)):
        if i >= w:
            state, delay = "gone", 0
            x, row = weight_slot(prev_w, i)
        else:
            state = "new" if i >= prev_w else ""
            delay = round((i - prev_w) * 0.06, 2) if i >= prev_w else 0
            x, row = weight_slot(w, i)
        top = 34 + row * 13
        rope = f"M0 0 L{-x} {29 - top}" if row == 0 else "M0 0 L0 -2"
        out.append(
            f'<g transform="translate({x} {top})"><g class="pn w {state}" style="animation-delay:{delay}s">'
            f'<path class="rope" d="{rope}"/><path d="M-5 0H5L7.2 11H-7.2Z" fill="#3A4D5C"/>'
            f'<text class="wl" y="6.6">{MINUS}1</text></g></g>')
    return "".join(out)


def face_svg(h: int) -> str:
    def eyes(r, y):
        return (f'<circle cx="-2.8" cy="{y}" r="{r}" fill="#2C211C"/>'
                f'<circle cx="2.8" cy="{y}" r="{r}" fill="#2C211C"/>')
    if h > 0:       # 웃는 얼굴
        return eyes(.95, -29) + '<path class="mouth" d="M-3.2 -26.2 q3.2 3.6 6.4 0"/>'
    if h == 0:      # 보통
        return eyes(.95, -29) + '<path class="mouth" d="M-2.4 -25.6 h4.8"/>'
    if h > -3:      # 걱정
        return (eyes(.95, -28.6) + '<path class="mouth" d="M-4.8 -31.4 l3 1.1 M4.8 -31.4 l-3 1.1"/>'
                '<path class="mouth" d="M-2.6 -24.8 q2.6 -2.4 5.2 0"/>')
    return eyes(1.3, -28.8) + '<circle class="mouth" cx="0" cy="-25.4" r="1.5"/>'   # 물속


def person_svg(b: int, w: int, h: int, prev_b: int, prev_w: int) -> str:
    bubbles = ('<g><circle class="bub" cx="-4" cy="-40" r="1.8"/><circle class="bub" cx="3" cy="-42" r="1.3"/>'
               '<circle class="bub" cx="-1" cy="-44" r="2.2"/></g>') if h <= -3 else ""
    return f"""
<g class="bob">
  {weights_svg(w, prev_w)}
  <path d="M-6 25 L0 29 L6 25" fill="none" stroke="#4A5A65" stroke-width="1.3"/>
  <circle cx="0" cy="29" r="2.2" fill="none" stroke="#4A5A65" stroke-width="1.6"/>
  <path d="M-4 8 L-6 24 M4 8 L6 24" stroke="#3D5F7D" stroke-width="4.6" stroke-linecap="round"/>
  <ellipse cx="-7.4" cy="26" rx="4" ry="2.2" fill="#2B2B33"/><ellipse cx="7.4" cy="26" rx="4" ry="2.2" fill="#2B2B33"/>
  <rect x="-8.6" y="-22" width="17.2" height="30" rx="7" fill="#F4C14E"/>
  <rect x="-8.6" y="-2" width="17.2" height="4" fill="#6A4A33"/>
  <rect x="-1.6" y="-2.4" width="3.2" height="4.8" rx=".8" fill="#E8C779"/>
  <path d="M-8 -19 L-10 -31 M8 -19 L10 -31" stroke="#F4C14E" stroke-width="5.2" stroke-linecap="round"/>
  <path d="M-10 -31 L-12.5 -43 M10 -31 L12.5 -43" stroke="#F1C4A0" stroke-width="3.4" stroke-linecap="round"/>
  <circle cx="-12.5" cy="-44" r="2.6" fill="#F1C4A0"/><circle cx="12.5" cy="-44" r="2.6" fill="#F1C4A0"/>
  <path d="M-12.5 -45 L0 {KY} L12.5 -45" fill="none" stroke="#43606F" stroke-width=".9" stroke-linecap="round"/>
  {balloons_svg(b, prev_b)}
  <circle cx="0" cy="{KY}" r="1.8" fill="#43606F"/>
  <circle cx="0" cy="-30" r="7.6" fill="#F1C4A0"/>
  <path d="M-7.6 -30.6 a7.6 7.6 0 0 1 15.2 0 Q0 -34.6 -7.6 -30.6Z" fill="#3B2B24"/>
  {face_svg(h)}
</g>
<g>{bubbles}</g>"""


def scene_html(b: int, w: int, prev_h: int, prev_b: int, prev_w: int) -> str:
    h = b - w
    y_new, y_old = y_of(h), y_of(prev_h)
    ease = "cubic-bezier(.3,1.35,.5,1)"
    dur = round(min(1.4, 0.45 + 0.1 * abs(h - prev_h)), 2)   # 많이 움직일수록 조금 더 오래
    move = (f"<style>@keyframes mvr{{from{{transform:translate({CX}px,{y_old}px)}}"
            f"to{{transform:translate({CX}px,{y_new}px)}}}}"
            f"@keyframes mvm{{from{{transform:translateY({y_old}px)}}to{{transform:translateY({y_new}px)}}}}</style>")
    pill = "#C93C26" if h > 0 else "#2F4D69" if h < 0 else "#35596B"
    big_color = "#BA3520" if h > 0 else "#24577F" if h < 0 else "#0C2B3A"
    wave = " q10 -4.5 20 0 t20 0" * 18
    wave_open = f"M-160 {ZERO}{wave}"
    wave_closed = f"{wave_open} V{ZERO + 16} H-160Z"

    svg = f"""
<svg viewBox="0 0 360 {VB_H}" preserveAspectRatio="xMidYMid meet" role="img"
     aria-label="사람이 {desc(h)}에 있어요. 풍선 {b}개, 추 {w}개가 달려 있어요.">
  <defs>
    <linearGradient id="gSky" gradientUnits="userSpaceOnUse" x1="0" y1="-120" x2="0" y2="{ZERO}">
      <stop offset="0" stop-color="#A6D8F0"/><stop offset="1" stop-color="#E8F6FA"/></linearGradient>
    <linearGradient id="gSea" gradientUnits="userSpaceOnUse" x1="0" y1="{ZERO}" x2="0" y2="{ZERO + 270}">
      <stop offset="0" stop-color="#52B7C4"/><stop offset=".45" stop-color="#1F82A2"/>
      <stop offset="1" stop-color="#0B3A5C"/></linearGradient>
  </defs>
  <rect x="-600" y="-600" width="1560" height="{ZERO + 600}" fill="url(#gSky)"/>
  <g transform="translate(78 96)"><g class="cloud"><path fill="#fff" opacity=".75"
     d="M0 22 q0-14 16-14 q6-10 20-4 q12-6 22 6 q14 0 14 12z"/></g></g>
  <g transform="translate(236 168)"><g class="cloud b"><path fill="#fff" opacity=".75"
     d="M0 18 q0-11 13-11 q5-8 16-3 q10-5 18 5 q11 0 11 9z"/></g></g>
  <rect x="-600" y="{ZERO}" width="1560" height="900" fill="url(#gSea)"/>
  <g transform="translate(0 {ZERO + 95})"><g class="fish" style="animation-delay:-14s">{FISH}</g></g>
  <g transform="translate(0 {ZERO + 158})"><g class="fish" style="animation-delay:-36s;animation-duration:64s">{FISH}</g></g>

  <g style="transform:translate({CX}px,{y_new}px);animation:mvr {dur}s {ease} both">
    {person_svg(b, w, h, prev_b, prev_w)}
  </g>

  <rect x="-600" y="{ZERO}" width="1560" height="900" fill="rgba(16,92,128,.38)"/>
  <g transform="translate(0 3)"><g class="wave w2" opacity=".55">
    <path d="{wave_closed}" fill="rgba(255,255,255,.32)"/>
    <path d="{wave_open}" fill="none" stroke="rgba(255,255,255,.85)" stroke-width="1.6"/></g></g>
  <g class="wave">
    <path d="{wave_closed}" fill="rgba(255,255,255,.32)"/>
    <path d="{wave_open}" fill="none" stroke="rgba(255,255,255,.85)" stroke-width="1.6"/></g>

  {ruler_svg()}
  <line x1="48" x2="352" y1="{y_of(10)}" y2="{y_of(10)}" stroke="rgba(12,43,58,.5)" stroke-dasharray="2 4" opacity=".7"/>
  <line x1="48" x2="352" y1="{y_of(-10)}" y2="{y_of(-10)}" stroke="rgba(12,43,58,.5)" stroke-dasharray="2 4" opacity=".7"/>
  <text class="note lvl" x="352" y="{y_of(10) - 6}">최고 +10 m</text>
  <text class="note lvl" x="352" y="{y_of(-10) + 12}">최저 {MINUS}10 m</text>
  <text class="note" x="352" y="{ZERO - 6}">해수면</text>

  <g style="transform:translateY({y_new}px);animation:mvm {dur}s {ease} both">
    <line x1="40" y1="0" x2="198" y2="0" stroke="rgba(12,43,58,.5)" stroke-width="1.2" stroke-dasharray="3 3"/>
    <rect x="1" y="-8" width="35" height="16" rx="8" fill="{pill}"/>
    <text class="ptx" x="18.5" y="0.5">{sgn(h)}</text>
  </g>
</svg>"""

    hud = f"""
<div class="hud">
  <div class="lbl">지금 높이</div>
  <div class="big" style="color:{big_color}">{sgn(h)}<small>m</small></div>
  <div class="desc">{desc(h)}</div>
  <div class="cnt">풍선 {b}개 · 추 {w}개</div>
</div>"""
    return f'{SCENE_CSS}{move}<div class="scene">{svg}{hud}</div>'


# ---------------------------------------------------------------- 식
def color_of(v: int) -> str:
    return "red" if v > 0 else "blue" if v < 0 else "gray"


def equation_markdown(hist: list) -> str:
    """0 + (+3) + (−2) − (+1) 꼴의 식. 양수는 빨강, 음수는 파랑."""
    parts = ["0"]
    for k, n in hist:
        v = op_value(k, n)
        parts.append(f"{OPS[k][0]} :{color_of(v)}[**({sgn(v)})**]")
    return " ".join(parts)


def steps_markdown(hist: list) -> str:
    """한 단계씩 계산했을 때의 높이: 0 → +3 → +1"""
    h, out = 0, ["0"]
    for k, n in hist:
        h += OPS[k][2] * n
        out.append(sgn(h))
    return " → ".join(out)


def state_markdown(b: int, w: int) -> str:
    """지금 달려 있는 것을 정수의 덧셈으로 쓴다: (+3) + (−2) = +1"""
    pb = f":red[**(+{b})**]" if b else ":gray[**(0)**]"
    pw = f":blue[**({MINUS}{w})**]" if w else ":gray[**(0)**]"
    return f"지금 달려 있는 것: {pb} + {pw} = **{sgn(b - w)}**"


# ---------------------------------------------------------------- 화면
def action_button(col, k: str, kind: str = "secondary") -> None:
    s = st.session_state
    n = int(s.n)
    m = max_n(k, s.b, s.w)
    col.button(NAMES[k].format(n=n), key=f"btn_{k}", on_click=act, args=(k,),
               disabled=(m == 0), type=kind, use_container_width=True)
    verb = "더하기" if OPS[k][0] == "+" else "빼기"
    if m == 0:
        col.caption(why(k, s.b, s.w))
    elif n > m:
        col.caption(f":red[지금은 {m}개까지만 가능해요]")
    else:
        col.caption(f"({sgn(op_value(k, n))}) {verb}")


def main() -> None:
    st.set_page_config(page_title="풍선과 추", layout="wide")
    init_state()
    s = st.session_state
    h = s.b - s.w

    st.markdown("## 풍선과 추")
    st.caption("풍선 하나는 +1 m, 추 하나는 −1 m예요. 개수를 정하고 버튼을 눌러 보세요.")

    left, right = st.columns([1, 1], gap="large")

    with left:
        components.html(scene_html(s.b, s.w, s.prev_h, s.prev_b, s.prev_w), height=SCENE_H + 10)

        c_n, c_hint = st.columns([1, 2])
        c_n.number_input("몇 개?", min_value=1, max_value=MAX, value=1, step=1, key="n")
        n = int(s.n)
        c_hint.markdown(f"&nbsp;\n\n풍선 {n}개 = :red[**(+{n})**], 추 {n}개 = :blue[**({MINUS}{n})**]")

        c1, c2 = st.columns(2)
        action_button(c1, "aB", "primary")
        action_button(c2, "sB")
        c3, c4 = st.columns(2)
        action_button(c3, "aW")
        action_button(c4, "sW")

    with right:
        st.subheader("내가 만든 식")
        st.markdown(f"#### {equation_markdown(s.hist)}")
        if s.hist:
            st.caption("한 단계씩 계산하면: " + steps_markdown(s.hist))
        st.markdown(f"## = :{color_of(h)}[{sgn(h)}] m")
        st.markdown(state_markdown(s.b, s.w))
        (st.warning if s.warn else st.info)(s.last)

        t1, t2 = st.columns(2)
        t1.button("되돌리기", on_click=undo, disabled=not s.hist, use_container_width=True)
        t2.button("처음부터", on_click=reset, disabled=not s.hist, use_container_width=True)


main()