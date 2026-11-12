import streamlit as st

classcode = "1234"
codes = st.text_input("클래스 코드를 입력하세요")

# 비어 있으면 입력 안내, 1234면 환영, 그 외에는 불일치
if codes == "":
    st.warning("코드를 입력하시오")
elif codes == classcode:
    st.success("환영합니다.")
else:
    st.error("코드가 일치하지 않습니다.")

st.subheader("다양한 인풋")
# 객관식(라디오 버튼,체크박스), 주관식(숫자만 입력, 텍스트 입력), 슬라이더, 파일 업로드

#1번이 답이야, 1번을 선택하면 정답, 나머지는 오답
answer = st.radio("일차방정식 2x+3=5의 해는?", ["1", "2", "3", "4", "5"])
if answer == "1":
    st.success("정답입니다.")
elif answer == "4":
    st.warning("이항을 다시 해보세요!")
else:
    st.error("오답입니다.")

agree = st.checkbox("동의합니다") # 체크박스
if agree == True:
    st.success("동의하셨습니다.")
else:
    st.error("동의하지 않으셨습니다.")

text_input = st.text_input("이름을 알려주세요!", placeholder="David Yoo")
number_input = st.number_input("나이를 알려주세요!",
placeholder = '20', 
min_value=0, 
max_value=100,
step=10)

st.write(number_input*3+1)

if st.button("Check"):
    st.success("확인되었습니다.")

# 라디오버튼 문제에 대한 정답을 확인하는 버튼을 만들어줘
answer2 = st.radio("일차방정식 2x+3=9의 해는?", ["-1", "0", "3", "-4", "9"])
if st.button("정답 확인하기"):
    if answer2 == "3":
        st.success("정답입니다.")
    else:
        st.error("오답입니다.")

# 슬라이더
age = st.slider("나이를 선택하세요!", min_value=0, max_value=100, step=1)
if age < 20:
    st.warning("미성년자입니다.")
else:
    st.success("성인입니다.")