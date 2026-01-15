import streamlit as st
import random
import urllib.parse

# 1. 網頁基本設定
st.set_page_config(page_title="台北請客神器", page_icon="🍱", layout="centered")

# 手機版按鈕美化
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #FF4B4B;
        color: white;
        height: 65px;
        font-size: 22px;
        font-weight: bold;
        border-radius: 15px;
        width: 100%;
    }
    .phone-btn {
        background-color: #28a745 !important;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ 今晚吃什麼")
st.caption("版本 5.0 - 支援一鍵撥號與地圖導航")
st.write("---")

# 2. 餐廳資料庫 (已加入電話欄位，部分餐廳已幫您查好，其餘您可以自行補上)
restaurants = [
    # 中式料理
    {"name": "頤宮 Le Palais", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0221819950#3261"},
    {"name": "晶華軒", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0225215000#3236"},
    {"name": "請客樓", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0223211818"},
    {"name": "捌伍添第", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0281010085"},
    {"name": "名人坊 (世貿店)", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0227232938"},
    {"name": "寒舍食譜", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0266228833"},
    {"name": "夜上海 (新光三越)", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0223453600"},
    {"name": "潮粵坊", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0277223390"},
    {"name": "明宮中餐廳", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0225423266#318"},
    {"name": "國賓中餐廳", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0221002100#2383"},
    {"name": "龍都酒樓", "cuisine": "中式料理", "for_client": False, "has_box": True, "phone": "0225639293"},
    
    # 私廚 (電話通常較隱密，部分需透過 Line 或熟人)
    {"name": "中山對酌", "cuisine": "私廚", "for_client": True, "has_box": True, "phone": "0225970720"},
    {"name": "盈科", "cuisine": "私廚", "for_client": True, "has_box": True, "phone": ""},
    {"name": "Lin restaurant", "cuisine": "私廚", "for_client": True, "has_box": True, "phone": ""},
    {"name": "春韭", "cuisine": "私廚", "for_client": False, "has_box": True, "phone": "0228823939"},
    {"name": "鄒記食舖", "cuisine": "私廚", "for_client": True, "has_box": True, "phone": "0227689895"},
    
    # 日式料理
    {"name": "彧割烹", "cuisine": "日式料理", "for_client": True, "has_box": True, "phone": "0225030303"},
    {"name": "掬·Kiku", "cuisine": "日式料理", "for_client": True, "has_box": True, "phone": "0227220559"},
    {"name": "足立壽司", "cuisine": "日式料理", "for_client": True, "has_box": True, "phone": ""},
    
    # 西式/現代料理
    {"name": "le beaujour 芃卓", "cuisine": "西式/現代料理", "for_client": True, "has_box": True, "phone": "0225672218"},
    {"name": "Ad Astra", "cuisine": "西式/現代料理", "for_client": True, "has_box": True, "phone": ""},
    {"name": "NOBUO", "cuisine": "西式/現代料理", "for_client": True, "has_box": True, "phone": "0223556450"},
    {"name": "Bencotto", "cuisine": "西式/現代料理", "for_client": True, "has_box": True, "phone": "0227156668"},
    {"name": "Robin's 牛排屋", "cuisine": "西式/現代料理", "for_client": True, "has_box": True, "phone": "0225215000#3930"},
    
    # 燒肉/肉食
    {"name": "梵燒肉 VANNNE", "cuisine": "燒肉/肉食", "for_client": True, "has_box": True, "phone": "0227710530"},
    {"name": "老乾杯", "cuisine": "燒肉/肉食", "for_client": False, "has_box": True, "phone": "0227253311"},
    
    # 火鍋/海鮮/泰式
    {"name": "橘色涮涮屋", "cuisine": "火鍋/海鮮/泰式", "for_client": True, "has_box": True, "phone": "0227761658"},
    {"name": "SUKHOTHAI", "cuisine": "火鍋/海鮮/泰式", "for_client": True, "has_box": True, "phone": "0223211818"},
]

# 3. 介面篩選
st.subheader("🛠️ 設定您的需求")

cuisine_list = sorted(list(set(r["cuisine"] for r in restaurants)))
cuisine_choice = st.selectbox("1. 選擇菜系", ["全部"] + cuisine_list)

target_choice = st.radio("2. 請客目的", ["不限", "重要客戶 (商務體面)", "朋友聚餐 (放鬆聚會)"], horizontal=True)

need_box = st.toggle("🔒 必須要有包廂", value=False)

# 4. 過濾邏輯
filtered = [r for r in restaurants if 
            (cuisine_choice == "全部" or r["cuisine"] == cuisine_choice) and
            (target_choice != "重要客戶 (商務體面)" or r["for_client"]) and
            (not need_box or r["has_box"])]

st.write("---")

# 5. 結果呈現
if st.button("🚀 幫我挑選餐廳"):
    if filtered:
        pick = random.choice(filtered)
        st.balloons()
        
        st.markdown(f"## 🎯 推薦您：**{pick['name']}**")
        
        c1, c2 = st.columns(2)
        c1.info(f"🍴 菜系：{pick['cuisine']}")
        c2.info(f"📦 包廂：{'有' if pick['has_box'] else '較少'}")
        
        # Google Maps 按鈕
        map_query = urllib.parse.quote(f"台北市 {pick['name']}")
        map_url = f"https://www.google.com/maps/search/?api=1&query={map_query}"
        st.link_button("🗺️ 打開 Google Maps 導航", map_url, use_container_width=True)
        
        # 電話撥打按鈕 (僅當有電話資料時顯示)
        if pick.get("phone"):
            # tel: 協定可以讓手機直接撥號
            phone_url = f"tel:{pick['phone']}"
            st.link_button(f"📞 立即撥號：{pick['phone']}", phone_url, use_container_width=True)
        else:
            st.warning("⚠️ 暫無電話資料，請透過 Google Maps 查詢預約方式。")
            
    else:
        st.error("😭 找不到符合條件的餐廳，請試著放寬條件。")

st.caption(f"目前篩選條件下共有 {len(filtered)} 家餐廳可供挑選")
