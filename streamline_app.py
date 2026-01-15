import streamlit as st
import random
import urllib.parse

# 1. 網頁基本設定 (設定手機版顯示效果)
st.set_page_config(page_title="台北請客神器", page_icon="🍱", layout="centered")

# 自定義 CSS，讓手機版按鈕更大更好按
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #FF4B4B;
        color: white;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 15px;
        width: 100%;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ 台北高端餐廳選擇器")
st.write("2500~5000元 / 人 精選決策工具")
st.write("---")

# 2. 完整餐廳資料庫
# 屬性：[名稱, 菜系, 適合客戶(True/False), 是否有包廂(True/False)]
restaurants = [
    # --- 您剛才新增的餐廳 ---
    {"name": "彧割烹", "cuisine": "日式料理", "for_client": True, "has_box": True},
    {"name": "盈科", "cuisine": "私廚/日式", "for_client": True, "has_box": True},
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
    {"name": "捌伍添第", "cuisine": "中式/粵菜", "for_client": True, "has_box": True},
    {"name": "Joyce East", "cuisine": "西式料理", "for_client": True, "has_box": True},
    {"name": "名人坊 (世貿店)", "cuisine": "中式/粵菜", "for_client": True, "has_box": True},
    {"name": "寒舍食譜", "cuisine": "中式/粵菜", "for_client": True, "has_box": True},
    {"name": "夜上海 (新光三越)", "cuisine": "中式/海派", "for_client": True, "has_box": True},
    
    # --- 之前的經典清單 ---
    {"name": "頤宮 Le Palais", "cuisine": "中式/粵菜", "for_client": True, "has_box": True},
    {"name": "晶華軒", "cuisine": "中式/粵菜", "for_client": True, "has_box": True},
    {"name": "請客樓", "cuisine": "中式/川揚菜", "for_client": True, "has_box": True},
    {"name": "中山對酌", "cuisine": "私廚", "for_client": True, "has_box": True},
    {"name": "春韭", "cuisine": "私廚", "for_client": False, "has_box": True},
    {"name": "梵燒肉 VANNNE", "cuisine": "燒肉/肉食", "for_client": True, "has_box": True},
    {"name": "本家燒肉 BORNGA", "cuisine": "燒肉/肉食", "for_client": False, "has_box": False},
    {"name": "ROU by T-HAM", "cuisine": "燒肉/肉食", "for_client": False, "has_box": False},
    {"name": "Bencotto", "cuisine": "西式料理", "for_client": True, "has_box": True},
    {"name": "Robin's 牛排屋", "cuisine": "西式料理", "for_client": True, "has_box": True},
    {"name": "橘色涮涮屋", "cuisine": "火鍋/海鮮", "for_client": True, "has_box": True},
    {"name": "89天地", "cuisine": "火鍋/海鮮", "for_client": False, "has_box": False},
    {"name": "SUKHOTHAI", "cuisine": "泰式/特色", "for_client": True, "has_box": True},
    {"name": "國賓中餐廳", "cuisine": "中式", "for_client": True, "has_box": True},
    {"name": "龍都酒樓", "cuisine": "中式/烤鴨", "for_client": False, "has_box": True},
]

# 3. 介面篩選
st.subheader("🛠️ 快速設定")

# 自動從名單提取菜系
cuisine_list = sorted(list(set(r["cuisine"] for r in restaurants)))
cuisine_choice = st.selectbox("1. 您想吃哪種菜系？", ["全部"] + cuisine_list)

target_choice = st.radio("2. 您的請客目的？", ["不限", "重要客戶 (體面/包廂)", "朋友聚餐 (放鬆/話題)"], horizontal=True)

# 加入包廂過濾
need_box = st.toggle("🔒 必須要有包廂", value=False)

# 4. 過濾邏輯
filtered = restaurants

if cuisine_choice != "全部":
    filtered = [r for r in filtered if r["cuisine"] == cuisine_choice]

if target_choice == "重要客戶 (體面/包廂)":
    filtered = [r for r in filtered if r["for_client"]]

if need_box:
    filtered = [r for r in filtered if r["has_box"]]

st.write("---")

# 5. 結果呈現
if st.button("🚀 幫我挑選餐廳 (點我)"):
    if filtered:
        pick = random.choice(filtered)
        st.balloons()
        
        # 顯示大大的推薦結果
        st.markdown(f"## 🎯 推薦您去：**{pick['name']}**")
        
        # 顯示屬性標籤
        col1, col2 = st.columns(2)
        col1.info(f"🍴 菜系：{pick['cuisine']}")
        col2.info(f"📦 包廂：{'有' if pick['has_box'] else '較少'}")
        
        # Google Maps 直接連結
        # 處理網址編碼，避免特殊字元造成連結斷掉
        map_query = urllib.parse.quote(f"台北市 {pick['name']}")
        map_url = f"https://www.google.com/maps/search/?api=1&query={map_query}"
        
        st.link_button("🗺️ 點我開啟 Google Maps 導航", map_url)
        
    else:
        st.error("😭 找不到符合條件的餐廳，請試著放寬篩選條件。")

st.caption(f"目前口袋名單共有 {len(filtered)} 家符合條件")
