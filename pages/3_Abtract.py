import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ---------------------------------------------------------
# 1. 페이지 및 폰트 설정 (와이드 레이아웃 적용)
# ---------------------------------------------------------
st.set_page_config(page_title="정수의 사칙연산 탐험대", page_icon="🎈", layout="wide")

# Windows 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ---------------------------------------------------------
# 2. 세션 상태(Session State) 초기화 및 콜백 함수
# ---------------------------------------------------------
if "balloons" not in st.session_state:
    st.session_state.balloons = 0
if "weights" not in st.session_state:
    st.session_state.weights = 0

def add_balloon():
    st.session_state.balloons += 1

def remove_balloon():
    if st.session_state.balloons > 0:
        st.session_state.balloons -= 1

def add_weight():
    st.session_state.weights += 1

def remove_weight():
    if st.session_state.weights > 0:
        st.session_state.weights -= 1

def reset():
    st.session_state.balloons = 0
    st.session_state.weights = 0

# ---------------------------------------------------------
# 3. 메인 화면 구성 (좌우 2분할)
# ---------------------------------------------------------
st.title("🎈⚓ 풍선과 추로 배우는 정수의 연산")
st.write("버튼을 누르면 오른쪽에 풍선과 추가 달리고 사람의 높이가 즉시 변합니다!")

col_left, col_right = st.columns([1, 1.2], gap="large")

# --- [왼쪽 컬럼: 버튼 조작 및 수학 수식] ---
with col_left:
    st.subheader("🎮 1. 풍선과 추 조작하기")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### 🎈 풍선 (양수 $+1$)")
        st.button("🎈 풍선 달기 (+1m)", on_click=add_balloon, use_container_width=True)
        st.button("🎈 풍선 떼기 (-1m)", on_click=remove_balloon, use_container_width=True)
        
    with c2:
        st.markdown("##### ⚓ 추 (음수 $-1$)")
        st.button("⚓ 추 달기 (-1m)", on_click=add_weight, use_container_width=True)
        st.button("⚓ 추 떼기 (+1m)", on_click=remove_weight, use_container_width=True)
        
    st.button("🔄 0m 위치로 리셋", on_click=reset, use_container_width=True)

    st.divider()
    
    st.subheader("📐 2. 현재 상태 및 수학 수식")
    
    b_cnt = st.session_state.balloons
    w_cnt = st.session_state.weights
    current_height = b_cnt - w_cnt
    
    m1, m2, m3 = st.columns(3)
    m1.metric("🎈 풍선 개수", f"{b_cnt} 개")
    m2.metric("⚓ 추 개수", f"{w_cnt} 개")
    m3.metric("📏 현재 높이", f"{current_height} m")
    
    st.latex(fr"\text{{현재 위치}} = (+{b_cnt}) + (-{w_cnt}) = {current_height}\text{{m}}")
    
    if current_height > 0:
        st.info(f"🌤️ 해수면(0m)보다 **{current_height}m 위**에 떠 있습니다!")
    elif current_height < 0:
        st.warning(f"🌊 해수면(0m)보다 **{abs(current_height)}m 아래** 물속에 있습니다!")
    else:
        st.success("⚓ 현재 **해수면(0m)**에 딱 맞춰 떠 있습니다!")

# --- [오른쪽 컬럼: 사람, 풍선, 추 시각화] ---
with col_right:
    st.subheader("📺 3. 실시간 위치 시각화")
    
    fig, ax = plt.subplots(figsize=(6, 7))
    
    # 동적 y축 범위 설정
    y_max = max(6, current_height + 4)
    y_min = min(-6, current_height - 4)
    
    # 하늘/바다 배경 영역
    ax.axhspan(0, y_max + 5, color='#E0F7FA', alpha=0.85)
    ax.axhspan(y_min - 5, 0, color='#0288D1', alpha=0.45)
    ax.axhline(0, color='#0D47A1', linewidth=2.5, linestyle='--', label='해수면 (0m)')
    
    y = current_height
    
    # A. 사람 (Stick Figure) 그리기
    ax.add_patch(patches.Circle((0, y + 0.5), 0.15, color='#FFCC80', ec='#E65100', lw=1.5, zorder=5)) # 머리
    ax.plot([0, 0], [y + 0.1, y + 0.35], color='#212121', lw=3, zorder=5)                            # 몸통
    ax.plot([-0.2, 0.2], [y + 0.25, y + 0.25], color='#212121', lw=3, zorder=5)                      # 팔
    ax.plot([0, -0.15], [y + 0.1, y - 0.1], color='#212121', lw=3, zorder=5)                         # 왼다리
    ax.plot([0, 0.15], [y + 0.1, y - 0.1], color='#212121', lw=3, zorder=5)                          # 오른다리
    
    # B. 풍선들 매달기 (머리 위로 연결선과 풍선 배치)
    for i in range(b_cnt):
        bx = (i - (b_cnt - 1) / 2) * 0.25 if b_cnt > 1 else 0
        by = y + 0.95 + (i % 2) * 0.25
        # 실
        ax.plot([0, bx], [y + 0.25, by - 0.18], color='#90A4AE', lw=1.2, zorder=4)
        # 풍선 타원 및 묶음
        ax.add_patch(patches.Ellipse((bx, by), 0.22, 0.32, color='#FF5252', ec='#D32F2F', lw=1.5, zorder=6))
        ax.add_patch(patches.Polygon([[bx-0.03, by-0.16], [bx+0.03, by-0.16], [bx, by-0.14]], color='#D32F2F', zorder=6))
        
    # C. 추 매달기 (발 아래로 밧줄과 철퇴/추 배치)
    for i in range(w_cnt):
        wx = (i - (w_cnt - 1) / 2) * 0.25 if w_cnt > 1 else 0
        wy = y - 0.45 - (i % 2) * 0.25
        # 밧줄
        ax.plot([0, wx], [y - 0.1, wy + 0.1], color='#795548', lw=2, zorder=4)
        # 사각형 추
        ax.add_patch(patches.Rectangle((wx - 0.1, wy - 0.1), 0.2, 0.2, color='#455A64', ec='#263238', lw=1.5, zorder=6))
        ax.text(wx, wy, "W", fontsize=8, fontweight='bold', ha='center', va='center', color='white', zorder=7)

    # 위치 텍스트 상자
    ax.text(0.4, y, f"현재: {y}m", fontsize=12, fontweight='bold', 
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9, edgecolor='#1976D2'))
            
    # 축 레이아웃 설정
    ax.set_ylim(y_min, y_max)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylabel("높이 (m)", fontsize=12)
    ax.set_xticks([])
    ax.set_title("해수면 기준 사람의 위치 시각화", fontsize=14, pad=15)
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.legend(loc='upper right')
    
    st.pyplot(fig)