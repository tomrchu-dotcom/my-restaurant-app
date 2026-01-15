import streamlit as st
import random
import urllib.parse

# 1. 網頁基本設定
st.set_page_config(page_title="台北請客助手 Pro", page_icon="🍱", layout="centered")

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
        background-color: #ffffff !important;
        border: 1px solid #ddd !important;
        color: #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ 今晚吃什麼")
st.caption("版本 8.0 - 支援智慧搜尋訂位功能")
st.write("---")

# 2. 餐廳資料庫 (整合所有名單)
restaurants = [
    # 中式
    {"name": "頤宮 Le Palais", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0221819950#3261", "url": "https://inline.app/booking/palaisdechine/lepalais"},
    {"name": "晶華軒", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0225215000#3236", "url": "https://inline.app/booking/regenttaipei/silks-house"},
    {"name": "請客樓", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0223211818", "url": "https://inline.app/booking/sheratongrandetaipei/the-guest-house"},
    {"name": "捌伍添第", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0281010085", "url": "https://inline.app/booking/85td/85td"},
    {"name": "名人坊 (世貿店)", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0227232938", "url": ""},
    {"name": "寒舍食譜", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0266228833", "url": ""},
    {"name": "夜上海 (新光三越)", "cuisine": "中式料理", "for_client": True, "has_box": True, "phone": "0223453600", "url": ""},
    {"name": "龍都酒樓", "cuisine": "中式料理", "for_client": False, "has_box": True, "phone": "0225639293", "url": ""},
    
    # 私廚
    {"name": "中山對酌", "cuisine": "私廚", "for_client": True, "has_box": True, "phone": "0225970720", "url": ""},
    {"name": "盈科", "cuisine": "私廚", "for_client": True, "has_box": True, "phone": "", "url": "https://inline.app/booking/eika/eika"},
    {"name": "鄒記食舖", "cuisine": "私廚", "for_client": True, "has_box": True, "phone": "0227689895", "url": ""},
    {"name": "春韭", "cuisine": "私廚", "for_client": False, "has_box": True, "phone": "0228823939", "url": ""},
    {"name": "Lin restaurant", "cuisine": "私廚", "for_client": True, "has_box": True, "phone": "", "url": ""},
    
    # 日式
    {"name": "彧割烹", "cuisine": "日式料理", "for_client": True, "has_box": True, "phone": "0225030303", "url": ""},
    {"name": "掬·Kiku", "cuisine": "日式料理", "for_client": True, "has_box": True, "phone": "0227220559", "url": ""},
    {"name": "足立壽司", "cuisine": "日式料理", "for_client": True, "has_box": True, "phone": "", "url": ""},
    
    # 西式/現代/創意
    {"name": "le beaujour 芃卓", "cuisine": "西式/現代料理", "for_client": True, "has_box": True, "phone": "0225672218", "url": "https://inline.app/booking/lebeaujour/lebeaujour"},
    {"name": "Ad Astra", "cuisine": "西式/現代料理", "for_client": True, "has_box": True, "phone": "", "url": "https://inline.app/booking/adastra/adastra"},
    {"name": "NOBUO", "cuisine": "西式/現代料理", "for_client": True, "has_box": True, "phone": "0223556450", "url": "https://inline.app/booking/nobuo/nobuo"},
    {"name": "Mume", "cuisine": "西式/現代料理", "for_client": False, "has_box": False, "phone": "0227000901", "url": "https://inline.app/booking/mume/mume"},
    {"name": "Logy", "cuisine": "西式/現代料理", "for_client": False, "has_box": False, "phone": "", "url": "https://inline.app/booking/logy/logy"},
    {"name": "T+T", "cuisine": "西式/現代料理", "for_client": False, "has_box": False, "phone": "0227199191", "url": "https://inline.app/booking/tt/tt"},
    {"name": "inita", "cuisine": "西式/現代料理", "for_client": False, "has_box": False, "phone": "0227527088", "url": "https://inline.app/booking/inita/inita"},
    
    # 燒肉/肉食
    {"name": "梵燒肉 VANNNE", "cuisine": "燒肉/肉食", "for_client": True, "has_box": True, "phone": "0227710530", "url": "https://inline.app/booking/vannne/vannne"},
    {"name": "老乾杯", "cuisine": "燒肉/肉食", "for_client": False, "has_box": True, "phone": "0227253311", "url": "https://www.kanpai-booking.com.tw/"},
    {"name": "橘色涮涮屋", "cuisine": "火鍋/海鮮/泰式", "for_client": True, "has_box": True, "phone": "0227761658", "url": "https://inline.app/booking/orangeshuan/orange-shuan-1"},
]

# 3. 篩選介面
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
                st.markdown(f"#### {i}. **{pick['name']}**")
                st.caption(f"{pick['cuisine']} | {'✅ 包廂' if pick['has_box'] else '❌ 無包廂'}")
                
                b1, b2, b3 = st.columns(3)
                
                # 地圖
                q = urllib.parse.quote(f"台北市 {pick['name']}")
                b1.link_button("🗺️ 地圖", f"https://www.google.com/maps/search/?api=1&query={q}", use_container_width=True)
                
                # 電話
                if pick['phone']:
                    b2.link_button("📞 電話", f"tel:{pick['phone']}", use_container_width=True)
                else:
                    b2.button("🚫 無電話", disabled=True, use_container_width=True)
                
                # 智慧訂位連結
                if pick['url']:
                    b3.link_button("📅 訂位", pick['url'], use_container_width=True)
                else:
                    # 如果沒有網址，自動生成 Google 搜尋連結
                    search_q = urllib.parse.quote(f"{pick['name']} 訂位")
                    search_url = f"https://www.google.com/search?q={search_q}"
                    b3.link_button("🔍 找訂位", search_url, use_container_width=True)
                st.divider()
    else:
        st.error("😭 找不到符合條件的餐廳。")
