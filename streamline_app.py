import streamlit as st
import random

# 設定網頁標題與圖示
st.set_page_config(page_title="台北請客助手", page_icon="🍴")

st.title("🍽️ 台北高端餐廳選擇器")
st.subheader("2500~5000元/人 精選清單")

# 您的專屬資料庫
db = {
    "中式/粵菜": ["頤宮", "晶華軒", "請客樓", "國賓中餐廳", "世貿聯誼社", "潮粵坊", "龍都", "夜上海", "明宮"],
    "私廚 (預約制)": ["中山對酌", "春韭", "聚苑", "鄒記食舖", "徐家私廚"],
    "燒肉/肉食": ["梵燒肉", "本家燒肉", "ROU by T-HAM"],
    "西式/義式": ["Bencotto", "Robin's", "CLOVER BELLAVITA"],
    "火鍋/海鮮/泰式": ["橘色涮涮屋", "89天地", "SUKHOTHAI"]
}

# 手機友善介面
choice = st.selectbox("今天想吃哪種風格？", list(db.keys()))

if st.button("✨ 幫我選一間", use_container_width=True):
    pick = random.choice(db[choice])
    st.balloons() # 慶祝動畫
    st.markdown(f"### 🎯 推薦您去：**{pick}**")
    st.write("---")
    st.caption("建議提前確認是否有包廂位子。")

st.info("💡 未來如需增加餐廳，請直接修改 GitHub 上的清單。")
