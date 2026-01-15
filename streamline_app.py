import streamlit as st
import random
import urllib.parse

# 1. 網頁基本設定
st.set_page_config(page_title="台北請客神器 Pro", page_icon="🍱", layout="centered")

# 自定義 CSS 讓手機版按鈕更顯眼
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_stdio=True)

st.title("🏙️ 今晚吃什麼")
st.caption("版本 3.0 - 已整合最新私廚與米其林名單")
st.write("---")

# 2. 完整資料庫 (包含您新增的所有餐廳)
# 標籤定義: [名稱, 菜系, 適合客戶(True/False), 有無包廂(True/False)]
restaurants = [
    {"name": "頤宮 Le Palais", "cuisine": "中式/粵菜", "for_client": True, "has_box": True},
    {"name": "晶華軒", "cuisine": "中式/粵菜", "for_client": True, "has_box": True},
    {"name": "請客樓", "cuisine": "中式/川揚菜", "for_client": True, "has_box": True},
    {"name": "中山對酌", "cuisine": "私廚", "for_client": True, "has_box": True},
    {"name": "盈科", "cuisine": "私廚/日式", "for_client": True, "has_box": True},
    {"name": "彧割烹", "cuisine": "日式料理", "for_client": True, "has_box": True},
    {"name": "Mume", "cuisine": "現代法式", "for_client": False, "has_box": False},
    {"name": "ÉCRU", "cuisine": "法式料理", "for_client": True, "has_box": True},
    {"name": "T+T", "cuisine": "亞洲創意", "for_client": False, "has_box": False},
    {"name": "EMBERS", "cuisine": "現代台菜", "for_client": False, "has_box": False},
    {"name": "le beaujour 芃卓", "cuisine": "法式料理", "for_client": True, "has_box": True},
    {"name": "WOK by OBOND", "cuisine": "中式/創意", "for_client": False, "has_box": False},
    {"name": "NOBUO", "cuisine": "日法料理", "for_client": True, "has_box": True},
    {"name": "Ad Astra", "cuisine": "現代料理", "for_client": True, "has_box": True},
    {"name": "烹然 PRONG", "cuisine": "原火料理", "for_client": False, "has_box": True},
    {"name": "掬·Kiku", "cuisine": "日式料理", "for_client": True, "has_box": True},
    {"name": "好嶼", "cuisine": "現代台菜", "for_client": False, "has_box": False},
    {"name": "inita", "cuisine": "義法料理", "for_client": False, "has_box": False},
    {"name": "earnestos", "cuisine": "西式料理", "for_client": True, "has_box": False},
    {"name": "Lin restaurant", "cuisine": "私廚", "for_client": True, "has_box": True},
    {"name": "Logy", "cuisine": "亞洲創意", "for_client": False, "has_box": False},
    {"name": "老乾杯", "cuisine": "燒肉/肉食", "for_client": False, "has_box": True},
    {"name": "胡同", "cuisine": "燒肉/肉食", "for_client": False, "has_box": False},
    {"name": "梵燒肉 VANNNE", "cuisine": "燒肉/肉食", "for_client": True, "has_box": True},
    {"name": "本家燒肉 BORNGA", "cuisine": "燒肉/肉食", "for_client": False, "has_box": False},
    {"name": "捌伍添第", "cuisine": "中式/粵菜", "for_client": True, "has_box": True},
    {"name": "Joyce East", "cuisine": "西式料理", "for_client": True, "has_box": True},
    {"name": "名人坊 (世貿店)", "cuisine": "中式/粵菜", "for_client": True, "has_box": True},
    {"name": "寒舍食譜 (艾美)", "cuisine": "中式/粵菜", "for_client": True, "has_box": True},
    {"name": "夜上海 (新光三越)", "cuisine": "中式/海派", "for_client": True, "has_box": True},
    {"name": "橘色涮涮屋", "cuisine": "火鍋/海鮮", "for_client": True, "has_box": True},
    {"name": "89天地", "cuisine": "火鍋/海鮮", "for_client": False, "has_box": False},
    {"name": "SUKHOTHAI", "cuisine": "泰式/特色", "for_client": True, "has_box": True},
    {"name": "國賓中餐廳", "cuisine": "中式", "for_client": True, "has_box": True},
    {"name": "Bencotto", "cuisine": "西式料理", "for_client": True, "has_box": True},
    {"name": "Robin's 牛排屋", "cuisine": "西式料理", "for_client": True, "has_box": True},
    {"name": "龍都酒樓", "cuisine": "中式/烤鴨", "for_client": False, "has_box": True},
]

# 3. 介面設計
st.subheader("🛠️ 快速篩選")

# 自動產生菜系清單
cuisine_list = sorted(list(set(r["cuisine"] for r in restaurants)))
cuisine_choice = st.selectbox("1. 選擇菜系", ["全部"] + cuisine_list)

target_choice = st.radio("2. 請客目的", ["不限", "重要客戶 (需體面)", "朋友聚餐 (重氣氛)"], horizontal=True)

col1, col2 = st.columns(2)
with col1:
    need_box = st.checkbox("🔒 必須有包廂")
with col2:
    st.caption(f"共 {len(restaurants)} 間候選")

# 4. 過濾邏輯
filtered = restaurants

if cuisine_choice != "全部":
    filtered = [r for r in filtered if r["cuisine"] == cuisine_choice]

if target_choice == "重要客戶 (需體面)":
    filtered = [r for r in filtered if r["for_client"]]

if need_box:
    filtered = [r for r in filtered if r["has_box"]]

st.write("---")

# 5. 結果呈現
if st.button("🚀 幫我決定餐廳"):
    if filtered:
        pick = random.choice(filtered)
        st.balloons()
        
        # 顯示結果卡片
        st.markdown(f"### 🎯 推薦您去：**{pick['name']}**")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("菜系", pick['cuisine'])
        c2.metric("包廂", "✅" if pick['has_box'] else "❌")
        c3.metric("性質", "🏛️ 商務" if pick['for_client'] else "🍻 聚會")
        
        # Google Maps 連結
        query = urllib.parse.quote(f"台北市 {pick['name']}")
        map_url = f"https://www.google.com/maps/search/?api=1&query={query}"
        
        st.link_button("🗺️ 打開 Google Maps 導航", map_url)
        
        if pick['name'] in ["頤宮 Le Palais", "中山對酌", "盈科", "Logy"]:
            st.warning("📣 溫馨提示：這間餐廳非常熱門，建議提早預約。")
    else:
        st.error("😭 找不到符合條件的餐廳，請嘗試放寬篩選條件。")

st.write("---")
st.caption("💡 想要修改名單？請直接到 GitHub 編輯 streamlit_app.py 檔案。")
