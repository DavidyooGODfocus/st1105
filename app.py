import streamlit as st

st.title("참새가 어찌 봉황의 뜻을 알리오")
st.header("사랑에서 행해지는 일은 항상 선악의 저편에서 일어난다.")
st.subheader("고통 없는 사회의 최고 가치는 생존으로 변한다")
st.info("안녕하시오. 소개페이지입니다.")
st.error("도가도비상도 명가명비상명")
st.success("별 하나를 잉태하기 위해선 가슴 속에 혼돈을 지니고 있어야 한다.")
st.warning("신과 신 사이에 무한한 거리가 십자가이다.")
st.write("모든 상황에 대하여 사용할 수 있는 말은 단 하나이다")
st.markdown("This is **TEXT**")
st.latex("a^2+b^2=c^2") # 
st.code("print('hello world')") # 주로 안에 있는 내용을 복사해야할 때 사용
st.write("---") # 구분선

st.image("image1.png", width=300) # 크기도 조절 가능
st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7F0_0SDhvTvbKRmapEUqjEJqGNpAsWWAAQiipFRi_5dLezAG-n_8xVPhh&s=10")
st.video("https://www.youtube.com/watch?v=cy2xS4sblb0&t=15s")
st.link_button("Desmos 바로가기","https://www.desmos.com/calculator?lang=ko")
st.components.v1.iframe("https://www.desmos.com/?lang=ko",
                        height=1100)