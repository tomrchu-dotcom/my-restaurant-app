import streamlit as st
import random

# 設定網頁標題與風格
st.set_page_config(page_title="台北請客神隊友", page_icon="🍱", layout="centered")

st.title("🏙️ 台北高端餐廳選擇器")
st.write("---")

# 1. 建立結構化資料庫 (加入標籤功能)
# tags 說明: [菜系, 是否適合客戶(True/False), 是否有包廂(True/False)]
restaurants = [
    {"name": "頤宮", "cuisine": "中式/粵菜", "for_client": True, "has_box": True},
    {"name": "晶華軒", "cuisine": "中式/粵菜", "for_client": True, "has_box": True},
    {"name": "請客樓", "cuisine": "中式/川揚菜", "for_client": True, "has_box": True},
    {"name": "中山對酌", "cuisine": "私廚", "for_client": True, "has_box": True},
    {"name": "春韭", "cuisine": "私廚", "for_client": False, "has_box": True},
    {"name": "梵燒肉", "cuisine": "燒肉/肉食", "for_client": True, "has_box": True},
    {"name": "本家燒肉", "cuisine": "燒肉/肉食", "for_client": False, "has_box": False},
    {"name": "ROU by T-HAM", "cuisine": "燒肉/肉食", "for_client": False, "has_box": False},
    {"name": "Bencotto", "cuisine": "西式/義式", "for_client": True, "has_box": True},
    {"name": "Robin's", "cuisine": "西式/義式", "for_client": True, "has_box": True},
    {"name": "橘色涮涮屋", "cuisine": "火鍋/海鮮", "for_client": True, "has_box": True},
    {"name": "89天地", "cuisine": "火鍋/海鮮", "for_client": False, "has_box": False},
    {"name": "SUKHOTHAI", "cuisine": "泰式/特色", "for_client": True, "has_box": True},
    {"name": "夜上海", "cuisine": "中式/蘇杭", "for_client": True, "has_box": True},
    {"name": "世貿聯誼社", "cuisine": "中式", "for_client": True, "has_box": True},
    {"name": "龍都酒樓", "cuisine": "中式/烤鴨", "for_client": False, "has_box": True},
    {"name": "明宮中餐廳", "cuisine": "中式/粵菜", "for_client": True, "has_box": True},
    {"name": "潮粵坊", "cuisine": "中式/粵菜", "for_client": True, "has_box": True},
    {"name": "國賓中餐廳", "cuisine": "中式", "for_client": True, "has_box": True},
]

# 2. 手機介面選擇區
st.subheader("🛠️ 篩選您的需求")

col1, col2 = st.columns(2)

with col1:
    cuisine_choice = st.selectbox("1. 想吃什麼菜系？", 
                                ["全部", "中式/粵菜", "私廚", "燒肉/肉食", "西式/義式", "火鍋/海鮮", "泰式/特色"])

with col2:
    target_choice = st.selectbox("2. 請客對象是？", ["不限", "重要客戶", "老朋友/親友"])

# 加入切換開關 (適合手指點擊)
need_box = st.toggle("🔒 必須要有獨立包廂", value=False)

# 3. 過濾邏輯
filtered_list = restaurants

# 菜系過濾
if cuisine_choice != "全部":
    filtered_list = [r for r in filtered_list if r["cuisine"] == cuisine_choice]

# 對象過濾
if target_choice == "重要客戶":
    filtered_list = [r for r in filtered_list if r["for_client"] == True]

# 包廂過濾
if need_box:
    filtered_list = [r for r in filtered_list if r["has_box"] == True]

st.write("---")

# 4. 輸出結果
if st.button("🚀 點我挑選餐廳", use_container_width=True):
    if len(filtered_list) > 0:
        pick = random.choice(filtered_list)
        st.balloons()
        st.success(f"### 🎯 為您推薦：{pick['name']}")
        
        # 顯示餐廳詳細標籤
        st.write(f"🔹 **菜系**：{pick['cuisine']}")
        st.write(f"🔹 **包廂**：{'✅ 有提供' if pick['has_box'] else '❌ 較少'}")
        st.write(f"🔹 **屬性**：{'🏛️ 適合商務體面' if pick['for_client'] else '🍻 適合輕鬆聚餐'}")
        
        # 加個小提醒
        if pick['name'] == "頤宮" or pick['name'] == "中山對酌":
            st.warning("⚠️ 這間非常難訂，建議立刻打電話確認！")
    else:
        st.error("😭 哎呀！目前的篩選條件下找不到餐廳，請放寬一點條件（例如取消勾選包廂）。")

# 顯示目前符合條件的數量 (增加互動感)
st.caption(f"目前符合條件的餐廳共有 {len(filtered_list)} 家")
