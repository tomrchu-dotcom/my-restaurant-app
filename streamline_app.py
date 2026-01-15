import streamlit as st
import random
import urllib.parse

# 1. 網頁基本設定
st.set_page_config(page_title="台北請客神器 Pro", page_icon="🍱", layout="centered")

# 手機版樣式優化
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #FF4B4B;
        color: white;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 12px;
        width: 100%;
    }
    .stLinkButton > a {
        font-size: 14px !important;
        padding: 0.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ 今晚吃什麼")
st.caption("版本 7.0 - 支援 Inline 訂位、電話與導航")
st.write("---")

# 2. 餐廳資料庫 (已加入電話與訂位網址)
# 提示：您可以自行在 booking_url 填入 inline 或官網連結
restaurants = [
    {"name": "頤宮 Le Palais", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0221819950#3261", "booking_url": "https://inline.app/booking/palaisdechine/lepalais"},
    {"name": "晶華軒", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0225215000#3236", "booking_url": "https://inline.app/booking/regenttaipei/silks-house"},
    {"name": "請客樓", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0223211818", "booking_url": "https://inline.app/booking/sheratongrandetaipei/the-guest-house"},
    {"name": "捌伍添第", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0281010085", "booking_url": "https://inline.app/booking/85td/85td"},
    {"name": "Mume", "cuisine": "西式/現代料理", "for_client": False, "has_box": False, "phone": "0227000901", "booking_url": "https://inline.app/booking/mume/mume"},
    {"name": "T+T", "cuisine": "西式/現代料理", "for_client": False, "has_box": False, "phone": "0227199191", "booking_url": "https://inline.app/booking/tt/tt"},
    {"name": "Logy", "cuisine": "西式/現代料理", "for_client": False, "has_box": False, "phone": "", "booking_url": "https://inline.app/booking/logy/logy"},
    {"name": "inita", "cuisine": "西式/現代料理", "for_client": False, "has_box": False, "phone": "0227527088", "booking_url": "https://inline.app/booking/inita/inita"},
    {"name": "NOBUO", "cuisine": "西式/現代料理", "for_client": True, "has_box": True, "phone": "0223556450", "booking_url": "https://inline.app/booking/nobuo/nobuo"},
    {"name": "梵燒肉 VANNNE", "cuisine": "燒肉/肉食", "for_client": True, "has_box": True, "phone": "0227710530", "booking_url": "https://inline.app/booking/vannne/vannne"},
    {"name": "老乾杯", "cuisine": "燒肉/肉食", "for_client": False, "has_box": True, "phone": "0227253311", "booking_url": "https://www.kanpai-booking.com.tw/"},
    {"name": "橘色涮涮屋", "cuisine": "火鍋/海鮮/泰式", "for_client": True, "has_box": True, "phone": "0227761658", "booking_url": "https://inline.app/booking/orangeshuan/orange-shuan-1"},
    {"name": "le beaujour 芃卓", "cuisine": "西式/現代料理", "for_client": True, "has_box": True, "phone": "0225672218", "booking_url": "https://inline.app/booking/lebeaujour/lebeaujour"},
    {"name": "Ad Astra", "cuisine": "西式/現代料理", "for_client": True, "has_box": True, "phone": "", "booking_url": "https://inline.app/booking/adastra/adastra"},
    {"name": "彧割烹", "cuisine": "日式料理", "for_client": True, "has_box": True, "phone": "0225030303", "booking_url": ""},
    {"name": "盈科", "cuisine": "私廚", "for_client": True, "has_box": True, "phone": "", "booking_url": "https://inline.app/booking/eika/eika"},
]

# 3. 介面篩選
st.subheader("🛠️ 設定需求")
cuisine_list = sorted(list(set(r["cuisine"] for r in restaurants)))
cuisine_choice = st.selectbox("選擇菜系", ["全部"] + cuisine_list)
target_choice = st.radio("請客目的", ["不限", "重要客戶 (商務體面)", "朋友聚餐 (放鬆聚會)"], horizontal=True)
need_box = st.toggle("必須要有包廂", value=False)

# 4. 過濾邏輯
filtered = [r for r in restaurants if 
            (cuisine_choice == "全部" or r["cuisine"] == cuisine_choice) and
            (target_choice != "重要客戶 (商務體面)" or r["for_client"]) and
            (not need_box or r["has_box"])]

st.write("---")

# 5. 結果呈現
if st.button("🚀 幫我精選三間方案"):
    if filtered:
        num_to_sample = min(len(filtered), 3)
        picks = random.sample(filtered, num_to_sample)
        st.balloons()
        
        for i, pick in enumerate(picks, 1):
            with st.container():
                st.markdown(f"#### 方案 {i}: **{pick['name']}**")
                st.caption(f"{pick['cuisine']} | {'✅ 有包廂' if pick['has_box'] else '❌ 無包廂'} | {'🏛️ 適合商務' if pick['for_client'] else '🍻 適合聚餐'}")
                
                # 按鈕列：三欄佈局
                btn_col1, btn_col2, btn_col3 = st.columns(3)
                
                # 1. 地圖
                map_query = urllib.parse.quote(f"台北市 {pick['name']}")
                map_url = f"https://www.google.com/maps/search/?api=1&query={map_query}"
                btn_col1.link_button("🗺️ 地圖", map_url, use_container_width=True)
                
                # 2. 電話
                if pick.get("phone"):
                    btn_col2.link_button("📞 電話", f"tel:{pick['phone']}", use_container_width=True)
                else:
                    btn_col2.button("🚫 無電話", disabled=True, use_container_width=True)
                
                # 3. 訂位連結
                if pick.get("booking_url"):
                    btn_col3.link_button("📅 訂位", pick['booking_url'], use_container_width=True)
                else:
                    btn_col3.button("📝 現場/電話", disabled=True, use_container_width=True)
                
                st.divider()
    else:
        st.error("😭 找不到符合條件的餐廳，請嘗試放寬條件。")
