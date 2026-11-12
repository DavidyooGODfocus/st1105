import streamlit as st
import pandas as pd
import seaborn as sns

st.title("2_연습하기")
# 펭귄데이터 불러와서 산점도 만들어달라고
penguins = sns.load_dataset("penguins")
st.write(penguins)
