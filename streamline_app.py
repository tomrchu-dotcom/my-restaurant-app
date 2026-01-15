import streamlit as st
import random
import urllib.parse  # 用來處理網址編碼

st.set_page_config(page_title="台北請客助手 Pro", page_icon="📍", layout="centered")

st.title("🏙️ 台北高端餐廳決策器")
st.caption("版本 2.0 - 支援 Google Maps 直接導航")
st.write("---")

# 1. 資料庫 (加入搜尋關鍵字，確保 Google Map 導航精準)
restaurants = [
    {"name": "頤宮 Le Palais", "cuisine": "中式/粵菜", "for_client": True, "has_box": True},
    {"name": "晶華軒", "cuisine": "中式/粵菜", "for_client": True, "has_box": True},
    {"name": "請客樓", "cuisine": "中式/川揚菜", "for_client": True, "has_box": True},
    {"name": "中山對酌", "cuisine": "私廚", "for_client": True, "has_box": True},
    {"name": "春韭 (基河店)", "cuisine": "私廚", "for_client": False, "has_box": True},
    {"name": "梵燒肉", "cuisine": "燒肉/肉食", "for_client": True, "has_box": True},
    {"name": "本家燒肉 BORNGA", "cuisine": "燒肉/肉食", "for_client": False, "has_box": False},
    {"name": "ROU by T-HAM", "cuisine": "燒肉/肉食", "for_client": False, "has_box": False},
    {"name": "Bencotto", "cuisine": "西式/義式", "for_client": True, "has_box": True},
    {"name": "Robin's 牛排屋", "cuisine": "西式/義式", "for_client": True, "has_box": True},
    {"name": "橘色涮涮屋", "cuisine": "火鍋/海鮮", "for_client": True, "has_box": True},
    {"name": "89天地 (89海鮮)", "cuisine": "火鍋/海鮮", "for_client": False, "has_box": False},
    {"name": "SUKHOTHAI", "cuisine": "泰式/特色", "for_client": True, "has_box": True},
    {"name": "夜上海", "cuisine": "中式/蘇杭", "for_client": True, "has_box": True},
    {"name": "世貿聯誼社 (漢來軒)", "cuisine": "中式", "for_client": True, "has_box": True},
    {"name": "龍都酒樓", "cuisine": "中式/烤鴨", "for_client": False, "has_box": True},
    {"name": "明宮中餐廳", "cuisine": "中式/粵菜", "for_client": True, "has_box": True},
    {"name": "潮粵坊", "cuisine": "中式/粵菜", "for_client": True, "has_box": True},
    {"name": "國賓中餐廳", "cuisine": "中式", "for_client": True, "has_box": True},
]

# 2. 篩選介面
st.subheader("🛠️ 設定您的需求")
col1, col2 = st.columns(2)
with col1:
    cuisine_choice = st.selectbox("想吃哪種風格？", ["全部"] + sorted(list(set(r["cuisine"] for r in restaurants))))
with col2:
    target_choice = st.selectbox("請客對象？", ["不限", "重要客戶", "老朋友/親友"])

need_box = st.toggle("🔒 必須要有包廂", value=False)

# 過濾邏輯
filtered = [r for r in restaurants if 
            (cuisine_choice == "全部" or r["cuisine"] == cuisine_choice) and
            (target_choice != "重要客戶" or r["for_client"]) and
            (not need_box or r["has_box"])]

st.write("---")

# 3. 輸出與 Google Map 綁定
if st.button("🚀 點我挑選餐廳", use_container_width=True):
    if filtered:
        pick = random.choice(filtered)
        st.balloons()
        st.success(f"### 🎯 推薦您去：**{pick['name']}**")
        
        # 動態生成 Google Map 連結
        query = urllib.parse.quote(f"台北市 {pick['name']}")
        map_url = f"https://www.google.com/maps/search/?api=1&query={query}"
        
        # 顯示詳細資訊與地圖按鈕
        c1, c2 = st.columns(2)
        c1.write(f"🔹 **菜系**：{pick['cuisine']}")
        c2.write(f"🔹 **包廂**：{'✅ 有' if pick['has_box'] else '❌ 較少'}")
        
        # 強大的地圖按鈕
        st.link_button(f"🗺️ 打開 Google Maps 導航", map_url, use_container_width=True)
        
    else:
        st.error("😭 找不到符合條件的餐廳，請放寬一點篩選。")

st.caption(f"目前口袋名單中共有 {len(filtered)} 間符合條件")
