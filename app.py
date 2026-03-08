import streamlit as st
from groq import Groq
import random
import json
import time

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="Life in UK 記憶助手",
    page_icon="🇬🇧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@300;400;600;700&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Serif TC', serif;
}

/* Main bg */
.stApp { background: #f7f2e8; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #1a1208 !important;
}
[data-testid="stSidebar"] * { color: #e8dfc8 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label { color: #d4a829 !important; font-weight: 600; }

/* Headers */
h1, h2, h3 { font-family: 'Lora', serif !important; color: #1a1208; }

/* Memory cards */
.memory-card {
    background: #fffdf7;
    border: 1px solid #c8b89a;
    border-left: 5px solid #b8860b;
    border-radius: 4px;
    padding: 20px 24px;
    margin: 12px 0;
    box-shadow: 0 2px 12px rgba(26,18,8,0.08);
}
.memory-card h3 { color: #b8860b; margin: 0 0 8px 0; font-size: 1rem; }
.memory-card p { color: #1a1208; line-height: 1.8; margin: 0; font-size: 0.95rem; }

/* Mnemonic box */
.mnemonic-box {
    background: linear-gradient(135deg, #1a1208 0%, #2d2010 100%);
    border-radius: 8px;
    padding: 20px 24px;
    margin: 12px 0;
    color: #f7f2e8;
}
.mnemonic-title { color: #d4a829; font-weight: 700; font-size: 0.85rem; letter-spacing: 0.1em; margin-bottom: 10px; }
.mnemonic-text { font-size: 1.15rem; line-height: 1.9; color: #f7f2e8; }
.highlight { color: #d4a829; font-weight: 700; }
.highlight-red { color: #e87878; font-weight: 700; }

/* Quiz option buttons */
.stButton > button {
    border-radius: 3px !important;
    font-family: 'Noto Serif TC', serif !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    border-color: #b8860b !important;
    color: #b8860b !important;
}

/* Tags */
.tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 2px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    margin: 2px;
}
.tag-history { background: #f0e8d0; color: #8b4513; border: 1px solid #c8a060; }
.tag-gov { background: #d8e8f0; color: #1a4a6b; border: 1px solid #6090b0; }
.tag-culture { background: #e8d8f0; color: #4a1a6b; border: 1px solid #9060b0; }
.tag-geo { background: #d0f0e0; color: #1a6b40; border: 1px solid #60b080; }

/* Visual memory panel */
.visual-panel {
    background: #fffdf7;
    border: 1px solid #c8b89a;
    border-radius: 4px;
    padding: 20px;
    text-align: center;
    min-height: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

/* Keyword chain */
.keyword-chain {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 6px;
    margin: 10px 0;
}
.keyword-node {
    background: #b8860b;
    color: white;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
}
.keyword-arrow { color: #b8860b; font-size: 1.2rem; }

/* Story card */
.story-card {
    background: #fff8ee;
    border: 1px solid #e8d0a0;
    border-radius: 6px;
    padding: 18px 20px;
    font-size: 0.9rem;
    line-height: 1.9;
    color: #3a2a10;
    font-style: italic;
}

/* Score badge */
.score-badge {
    background: #1a1208;
    color: #d4a829;
    padding: 8px 20px;
    border-radius: 4px;
    font-size: 1.1rem;
    font-weight: 700;
    text-align: center;
    display: inline-block;
}

/* Flashcard */
.flashcard {
    background: linear-gradient(145deg, #fffdf7, #f0e8d0);
    border: 2px solid #b8860b;
    border-radius: 8px;
    padding: 30px;
    text-align: center;
    min-height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    cursor: pointer;
    box-shadow: 4px 4px 0px #b8860b;
}
.flashcard-q { font-size: 1.1rem; line-height: 1.7; color: #1a1208; font-family: 'Lora', serif; }
.flashcard-a { font-size: 1rem; color: #8b1a1a; font-weight: 600; margin-top: 12px; }

div[data-testid="metric-container"] {
    background: #fffdf7;
    border: 1px solid #c8b89a;
    border-radius: 4px;
    padding: 12px;
}
</style>
""", unsafe_allow_html=True)

# ── KNOWLEDGE BASE ──
KNOWLEDGE_BASE = [
    {
        "id": 1,
        "topic": "歷史",
        "question": "《大憲章》（Magna Carta）係幾年簽訂？有咩意義？",
        "answer": "1215年，限制君主權力，奠定法治基礎",
        "keywords": ["1215", "大憲章", "約翰王", "法治", "貴族"],
        "emoji": "📜",
        "mnemonic_type": "諧音記憶",
        "mnemonic": "一二一五（1215）→「一而再，一而五」→ 貴族一再要求國王，終於在第五次逼到佢簽字！",
        "acronym": None,
        "story": "1215年，英格蘭貴族忍無可忍，逼迫約翰王（King John）在倫尼米德（Runnymede）簽下《大憲章》。從此，連國王都要受法律約束——即係話，冇人係法律之上！",
        "keyword_chain": ["1215年", "→", "約翰王簽字", "→", "貴族施壓", "→", "法律高於君主", "→", "民主基礎"],
        "visual": "⚔️ 貴族持劍 + 👑 國王低頭 + 📜 羊皮紙 = 法治誕生",
        "rhyme": "一二一五大憲章，約翰國王無法抗，貴族施壓簽協議，法律從此大過王！",
        "tag": "tag-history"
    },
    {
        "id": 2,
        "topic": "政府",
        "question": "英國議會分為上議院同下議院，各有咩功能？",
        "answer": "下議院（選舉產生，立法主導）；上議院（任命，審查法案）",
        "keywords": ["下議院", "上議院", "選舉", "立法", "審查"],
        "emoji": "🏛️",
        "mnemonic_type": "空間記憶",
        "mnemonic": "上面（上議院）= 貴族，老大哥坐喺上面睇住；下面（下議院）= 平民，真正做嘢嘅人！",
        "acronym": "下議院 = 民選做事，上議院 = 監督把關",
        "story": "想像一棟大樓：地下（下議院）係打工仔，每日做嘢立法；樓上（上議院）係退休老闆，坐喺度審批。但最終決定權係喺地下！",
        "keyword_chain": ["民選", "→", "下議院 House of Commons", "→", "立法主導", "→", "上議院 House of Lords", "→", "審查把關"],
        "visual": "🏢 大樓比喻：\n⬆️ 上議院（貴族/任命）= 監督\n⬇️ 下議院（選舉）= 實權立法",
        "rhyme": "下議院民選最實在，立法主導冇人代；上議院任命來監察，兩院合作治天下！",
        "tag": "tag-gov"
    },
    {
        "id": 3,
        "topic": "歷史",
        "question": "維多利亞女王幾時在位？呢個時代有咩特色？",
        "answer": "1837–1901年，工業革命，大英帝國版圖最大",
        "keywords": ["1837", "1901", "工業革命", "大英帝國", "維多利亞"],
        "emoji": "👑",
        "mnemonic_type": "頭字母縮寫",
        "mnemonic": "記住「工帝最長」→ 工業革命、帝國最大、維多利亞在位最長（63年）！",
        "acronym": "工（工業）帝（帝國）最（最大版圖）長（最長在位）",
        "story": "維多利亞女王9歲成為孤兒，18歲登基，在位長達63年！佢見證英國由農業國變成工業強國，版圖橫跨全球1/4土地，包括香港！",
        "keyword_chain": ["1837年登基", "→", "工業革命蓬勃", "→", "1/4地球是英土", "→", "香港1842年歸英", "→", "1901年駕崩"],
        "visual": "👑 維多利亞 (1837-1901)\n🏭 工廠林立\n🗺️ 地圖1/4塗紅 = 英國領土\n🇭🇰 包括香港！",
        "rhyme": "一八三七維多利亞，工業帝國遍天下；六十三年最長治，香港也在版圖下！",
        "tag": "tag-history"
    },
    {
        "id": 4,
        "topic": "文化",
        "question": "莎士比亞係邊個？有咩著名作品？",
        "answer": "1564–1616年，英國最偉大劇作家，著有《哈姆雷特》《羅密歐與朱麗葉》等",
        "keywords": ["莎士比亞", "1564", "劇作家", "哈姆雷特", "史特拉福"],
        "emoji": "🎭",
        "mnemonic_type": "故事聯想",
        "mnemonic": "莎士比亞 = 「沙」士（SARS）比亞洲更有名？唔係！係比任何人更偉大嘅劇作家！記住：生於1564，死於1616，頭尾都係「16」！",
        "acronym": "莎 = 史特拉福出生；士 = 士林頓劇場；比 = 比任何人都有名；亞 = 亞洲人都識佢",
        "story": "莎士比亞出生於英格蘭史特拉福（Stratford-upon-Avon），37部劇作影響西方文化500年。《哈姆雷特》問道：'To be or not to be'——考唔考試都係一個問題！",
        "keyword_chain": ["史特拉福出生", "→", "倫敦環球劇場", "→", "37部劇作", "→", "哈姆雷特/羅密歐", "→", "全球最著名作家"],
        "visual": "🎭 面具 + ✍️ 羽毛筆 + 📖 劇本\n生：1564 死：1616\n(頭尾都係 16！)",
        "rhyme": "莎士比亞生一五六四，死係一六一六年；哈姆雷特問生死，史上劇作第一人！",
        "tag": "tag-culture"
    },
    {
        "id": 5,
        "topic": "地理",
        "question": "英國四個組成國家係咩？各自嘅首都？",
        "answer": "英格蘭(倫敦)、蘇格蘭(愛丁堡)、威爾士(卡迪夫)、北愛爾蘭(貝爾法斯特)",
        "keywords": ["英格蘭", "蘇格蘭", "威爾士", "北愛爾蘭", "四個國家"],
        "emoji": "🗺️",
        "mnemonic_type": "頭韻法",
        "mnemonic": "記住口訣：「英蘇威北」→「英雄蘇武威武北上」！\n或者：London（倫）、Edinburgh（愛）、Cardiff（卡）、Belfast（貝）→「倫愛卡貝」",
        "acronym": "ENCW = England, Northern Ireland, Cardiff(Wales), Scotland → 記住「英北威蘇」",
        "story": "想像UK係一個家庭：英格蘭係老大（最大最有錢）；蘇格蘭係個性獨特嘅二哥（想獨立）；威爾士係文靜嘅細妹（有自己語言）；北愛爾蘭係隔咗海嘅細佬（最複雜）！",
        "keyword_chain": ["英格蘭→倫敦", "蘇格蘭→愛丁堡", "威爾士→卡迪夫", "北愛爾蘭→貝爾法斯特"],
        "visual": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 英格蘭 → 🏙️ 倫敦\n🏴󠁧󠁢󠁳󠁣󠁴󠁿 蘇格蘭 → 🏰 愛丁堡\n🏴󠁧󠁢󠁷󠁬󠁳󠁿 威爾士 → 🐉 卡迪夫\n🍀 北愛爾蘭 → 🚢 貝爾法斯特",
        "rhyme": "英格蘭首都係倫敦，蘇格蘭愛丁堡最靚；威爾士卡迪夫有龍，北愛貝爾法斯特情！",
        "tag": "tag-geo"
    },
    {
        "id": 6,
        "topic": "歷史",
        "question": "二戰期間英國首相係邊個？佢有咩著名說話？",
        "answer": "溫斯頓·邱吉爾（Winston Churchill），著名說話：'We shall never surrender'",
        "keywords": ["邱吉爾", "二戰", "1940", "首相", "永不放棄"],
        "emoji": "✌️",
        "mnemonic_type": "視覺聯想",
        "mnemonic": "邱吉爾 = 肥佬 + 雪茄 + V字手勢 + 鬥牛犬精神！記住：Churchill = Church（教堂）+ Hill（山丘）= 「山上教堂」永遠屹立不倒！",
        "acronym": "邱（丘陵）吉（吉祥）爾（而已）→ 地形吉祥，永不倒下！",
        "story": "1940年，德軍橫掃歐洲，英國孤立無援。邱吉爾發表演講：「我哋唔係嚟講條件，我哋嚟打仗！」呢種不屈精神，最終令英國撐到美國參戰，扭轉局勢。",
        "keyword_chain": ["1940年就任首相", "→", "德軍威脅", "→", "永不放棄演講", "→", "敦克爾克大撤退", "→", "二戰勝利1945"],
        "visual": "🎩 高帽 + 🚬 雪茄 + ✌️ V字手勢\n= 邱吉爾標誌性形象\n💬 'We shall never surrender'",
        "rhyme": "邱吉爾爵士雪茄香，二戰首相保家邦；永不放棄嘅精神，V字手勢傳萬方！",
        "tag": "tag-history"
    },
    {
        "id": 7,
        "topic": "政府",
        "question": "英國採用咩選舉制度？點解有人批評？",
        "answer": "簡單多數決（First Past the Post），批評：少數票可以當選，不成比例",
        "keywords": ["First Past the Post", "選舉", "多數決", "議席", "比例"],
        "emoji": "🗳️",
        "mnemonic_type": "比喻記憶",
        "mnemonic": "First Past the Post = 「賽馬制度」！邊匹馬先過終點線就贏，唔理其他馬差幾遠——所以得最多票就勝！",
        "acronym": "FPTP = First Past The Post = 「快（F）過（P）終（T）點（P）」",
        "story": "想像100人投票：A得40票、B得35票、C得25票——A勝出！但係60%選民係投反對A嘅，呢個就係FPTP嘅爭議所在。",
        "keyword_chain": ["最多票數勝出", "→", "First Past the Post", "→", "唔需要過半", "→", "有爭議但沿用"],
        "visual": "🏇 賽馬比喻\n🥇 A: 40票 ← 勝出！\n🥈 B: 35票\n🥉 C: 25票\n（60%人唔投A）",
        "rhyme": "英國選舉賽馬型，最多票數就係贏；唔需過半有爭議，First Past the Post稱其名！",
        "tag": "tag-gov"
    },
    {
        "id": 8,
        "topic": "文化",
        "question": "英聯邦（Commonwealth）係咩？有幾多成員國？",
        "answer": "前英國殖民地組成的自願聯盟，約54個成員國",
        "keywords": ["英聯邦", "54個", "自願", "殖民地", "香港"],
        "emoji": "🌍",
        "mnemonic_type": "數字記憶",
        "mnemonic": "54個成員國 = 打麻雀54隻牌（筒、索、萬各18隻 = 54）！香港人最識麻雀，咁就記得54喇！",
        "acronym": "Commonwealth = Common（共同）+ Wealth（財富）= 「共同富貴」嘅國家聯盟",
        "story": "英聯邦係大英帝國分崩離析後留低嘅「友誼網絡」。香港雖然1997年回歸，但曾係英聯邦嘅一部分。今日54個成員國，包括印度、加拿大、澳洲等。",
        "keyword_chain": ["英國殖民地", "→", "獨立後自願加入", "→", "54個成員國", "→", "共同價值觀", "→", "非政治軍事聯盟"],
        "visual": "🌍 全球地圖\n54個國家 = 🀄 麻雀54隻牌！\n（筒18 + 索18 + 萬18 = 54）",
        "rhyme": "英聯邦國五十四，麻雀牌數記心窩；共同價值自願入，香港曾是其中個！",
        "tag": "tag-culture"
    },
]

# ── SESSION STATE ──
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_total" not in st.session_state:
    st.session_state.quiz_total = 0
if "current_q" not in st.session_state:
    st.session_state.current_q = None
if "quiz_answered" not in st.session_state:
    st.session_state.quiz_answered = False
if "show_answer" not in st.session_state:
    st.session_state.show_answer = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "ai_memory" not in st.session_state:
    st.session_state.ai_memory = None

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("## 🇬🇧 Life in UK\n### 記憶助手")
    st.markdown("---")
    
    mode = st.radio(
        "選擇學習模式",
        ["🧠 記憶卡片", "🎯 模擬測試", "🤖 AI 生成記憶術", "💬 AI 問答"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    topic_filter = st.multiselect(
        "📚 篩選範疇",
        ["歷史", "政府", "文化", "地理"],
        default=["歷史", "政府", "文化", "地理"]
    )
    
    st.markdown("---")
    
    memory_style = st.selectbox(
        "🧩 記憶技巧偏好",
        ["全部顯示", "🎵 口訣/順口溜", "🔤 縮寫/頭字母", "📖 故事聯想", "🔗 關鍵字鏈", "👁️ 視覺聯想"]
    )
    
    st.markdown("---")
    st.markdown(f"""
    <div style="color:#d4a829; font-size:0.8rem;">
    📊 <b>我的進度</b><br>
    答題：{st.session_state.quiz_total} 題<br>
    答對：{st.session_state.quiz_score} 題<br>
    正確率：{'—' if st.session_state.quiz_total == 0 else f"{int(st.session_state.quiz_score/st.session_state.quiz_total*100)}%"}
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 重置進度", use_container_width=True):
        st.session_state.quiz_score = 0
        st.session_state.quiz_total = 0
        st.rerun()

# ── FILTER ──
filtered_kb = [k for k in KNOWLEDGE_BASE if k["topic"] in topic_filter]

# ══════════════════════════════════════
# MODE 1: 記憶卡片
# ══════════════════════════════════════
if mode == "🧠 記憶卡片":
    st.markdown("## 🧠 記憶卡片")
    st.markdown("每張卡片包含多種記憶技巧，幫你輕鬆記住考試內容。")
    
    if not filtered_kb:
        st.warning("請在側欄選擇至少一個學習範疇。")
    else:
        for item in filtered_kb:
            with st.container():
                col_icon, col_main = st.columns([0.08, 0.92])
                with col_icon:
                    st.markdown(f"<div style='font-size:2rem;text-align:center;padding-top:8px'>{item['emoji']}</div>", unsafe_allow_html=True)
                with col_main:
                    st.markdown(f"""
                    <div class='memory-card'>
                        <h3>【{item['topic']}】 {item['question']}</h3>
                        <p><b>📌 答案：</b>{item['answer']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Tabs for memory techniques
                tabs = st.tabs(["🔑 關鍵字鏈", "🎵 口訣", "📖 故事", "👁️ 視覺", "✍️ 記憶術"])
                
                with tabs[0]:
                    chain = item["keyword_chain"]
                    html_chain = ""
                    for i, node in enumerate(chain):
                        if node in ["→", "→"]:
                            html_chain += f'<span class="keyword-arrow">→</span>'
                        else:
                            html_chain += f'<span class="keyword-node">{node}</span>'
                    st.markdown(f'<div class="keyword-chain">{html_chain}</div>', unsafe_allow_html=True)
                    st.markdown(f"**關鍵字：** {' · '.join(['`'+k+'`' for k in item['keywords']])}")
                
                with tabs[1]:
                    st.markdown(f"""
                    <div class='mnemonic-box'>
                        <div class='mnemonic-title'>🎵 順口溜 / 口訣</div>
                        <div class='mnemonic-text'>{item['rhyme']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with tabs[2]:
                    st.markdown(f"""
                    <div class='story-card'>
                    📖 {item['story']}
                    </div>
                    """, unsafe_allow_html=True)
                
                with tabs[3]:
                    st.markdown(f"""
                    <div class='visual-panel'>
                        <div style='font-size:1.1rem;line-height:2;color:#1a1208;white-space:pre-line'>{item['visual']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with tabs[4]:
                    st.markdown(f"""
                    <div class='mnemonic-box'>
                        <div class='mnemonic-title'>💡 {item['mnemonic_type']}</div>
                        <div class='mnemonic-text'>{item['mnemonic']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if item["acronym"]:
                        st.info(f"🔤 **縮寫法：** {item['acronym']}")
                
                st.markdown("---")

# ══════════════════════════════════════
# MODE 2: 模擬測試
# ══════════════════════════════════════
elif mode == "🎯 模擬測試":
    st.markdown("## 🎯 模擬測試")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ 答對", st.session_state.quiz_score)
    with col2:
        st.metric("📝 已答", st.session_state.quiz_total)
    with col3:
        pct = int(st.session_state.quiz_score / st.session_state.quiz_total * 100) if st.session_state.quiz_total > 0 else 0
        st.metric("🎯 正確率", f"{pct}%", delta="合格線 75%" if pct < 75 else "✓ 已達標")
    
    st.markdown("---")
    
    if not filtered_kb:
        st.warning("請在側欄選擇至少一個學習範疇。")
    else:
        if st.session_state.current_q is None or not st.session_state.quiz_answered:
            if st.session_state.current_q is None:
                st.session_state.current_q = random.choice(filtered_kb)
                st.session_state.quiz_answered = False
        
        q = st.session_state.current_q
        
        # Question card
        st.markdown(f"""
        <div class='memory-card'>
            <h3>{q['emoji']} 【{q['topic']}】</h3>
            <p style='font-size:1.05rem;font-weight:600'>{q['question']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate wrong options
        wrong_pool = [k["answer"] for k in KNOWLEDGE_BASE if k["id"] != q["id"]]
        wrong_opts = random.sample(wrong_pool, min(3, len(wrong_pool)))
        all_opts = wrong_opts + [q["answer"]]
        random.shuffle(all_opts)
        
        opt_key = f"quiz_{q['id']}_{st.session_state.quiz_total}"
        
        if not st.session_state.quiz_answered:
            st.markdown("**請選擇答案：**")
            for i, opt in enumerate(all_opts):
                if st.button(f"　{opt}", key=f"opt_{i}_{opt_key}", use_container_width=True):
                    st.session_state.quiz_total += 1
                    if opt == q["answer"]:
                        st.session_state.quiz_score += 1
                        st.session_state.quiz_answered = True
                        st.session_state.selected_opt = (opt, True)
                    else:
                        st.session_state.quiz_answered = True
                        st.session_state.selected_opt = (opt, False)
                    st.rerun()
        else:
            selected, is_correct = st.session_state.get("selected_opt", ("", False))
            
            if is_correct:
                st.success(f"✅ 答對了！正確答案：**{q['answer']}**")
            else:
                st.error(f"❌ 答錯了！你選：{selected}\n\n✅ 正確答案：**{q['answer']}**")
            
            # Show memory tip
            st.markdown("### 💡 記憶小貼士")
            tab1, tab2, tab3 = st.tabs(["🎵 口訣記憶", "🔗 關鍵字鏈", "📖 故事"])
            with tab1:
                st.markdown(f"""
                <div class='mnemonic-box'>
                    <div class='mnemonic-title'>{q['mnemonic_type']}</div>
                    <div class='mnemonic-text'>{q['mnemonic']}</div>
                </div>
                <div class='mnemonic-box' style='margin-top:10px;background:linear-gradient(135deg,#2d1a30,#1a1208)'>
                    <div class='mnemonic-title'>🎵 順口溜</div>
                    <div class='mnemonic-text'>{q['rhyme']}</div>
                </div>
                """, unsafe_allow_html=True)
            with tab2:
                chain = q["keyword_chain"]
                html_chain = ""
                for node in chain:
                    if node in ["→"]:
                        html_chain += '<span class="keyword-arrow">→</span>'
                    else:
                        html_chain += f'<span class="keyword-node">{node}</span>'
                st.markdown(f'<div class="keyword-chain">{html_chain}</div>', unsafe_allow_html=True)
            with tab3:
                st.markdown(f'<div class="story-card">📖 {q["story"]}</div>', unsafe_allow_html=True)
            
            if st.button("➡️ 下一題", type="primary", use_container_width=True):
                st.session_state.current_q = random.choice(filtered_kb)
                st.session_state.quiz_answered = False
                st.rerun()

# ══════════════════════════════════════
# MODE 3: AI 生成記憶術
# ══════════════════════════════════════
elif mode == "🤖 AI 生成記憶術":
    st.markdown("## 🤖 AI 即時生成記憶術")
    st.markdown("輸入任何 Life in UK 考試內容，AI 會即時為你創作**個人化**記憶技巧！")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        user_topic = st.text_input(
            "輸入想記住嘅內容（廣東話/英文皆可）",
            placeholder="例如：英國國旗嘅組成、工業革命時期、議會制度…",
            label_visibility="visible"
        )
    with col2:
        memory_type_ai = st.selectbox(
            "記憶技巧類型",
            ["全套（口訣+縮寫+故事+視覺）", "🎵 口訣/順口溜", "🔤 縮寫/頭字母", "📖 故事聯想", "👁️ 視覺記憶"]
        )
    
    generate_btn = st.button("✨ 生成記憶術", type="primary", use_container_width=True)
    
    if generate_btn and user_topic:
        type_instruction = {
            "全套（口訣+縮寫+故事+視覺）": "請提供：1)廣東話口訣/順口溜 2)縮寫/頭字母記憶法 3)生動故事聯想 4)視覺圖像描述",
            "🎵 口訣/順口溜": "請重點提供朗朗上口嘅廣東話口訣同順口溜，要押韻",
            "🔤 縮寫/頭字母": "請重點提供縮寫法、頭字母記憶法、諧音記憶",
            "📖 故事聯想": "請重點提供生動有趣嘅故事，幫助記憶",
            "👁️ 視覺記憶": "請重點提供視覺圖像、空間記憶、顏色聯想等視覺化記憶方法"
        }[memory_type_ai]
        
        prompt = f"""你係一個專為香港50歲以上人士設計嘅 Life in UK Test 記憶術專家。

用戶想記住：「{user_topic}」

{type_instruction}

請用廣東話回覆，要：
1. 針對50歲以上香港人，用佢哋熟悉嘅香港文化、食物、地方作比喻
2. 記憶術要生動有趣、朗朗上口
3. 口訣要押韻，容易背誦
4. 解釋點解呢個記憶術有效

格式：
**📌 核心知識點**
[簡單說明正確答案]

**🎵 口訣/順口溜**
[押韻口訣]

**💡 記憶技巧**
[詳細解釋記憶方法，用香港人熟悉嘅例子]

**🔗 關鍵字串連**
[用箭頭串連關鍵字]

**👁️ 視覺圖像**
[描述一個幫助記憶嘅視覺場景]"""
        
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            with st.spinner("🤖 AI 緊係度幫你創作記憶術…"):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
            
            result = response.choices[0].message.content
            st.session_state.ai_memory = result
            
        except Exception as e:
            st.error(f"AI 連線出現問題：{str(e)}\n\n請確保已在 Streamlit Secrets 設定 GROQ_API_KEY。")
    
    if st.session_state.ai_memory:
        st.markdown("---")
        st.markdown("### ✨ AI 生成嘅記憶術")
        
        # Display formatted result
        st.markdown(f"""
        <div style='background:#fffdf7;border:1px solid #c8b89a;border-left:5px solid #d4a829;
                    border-radius:4px;padding:24px;font-size:0.95rem;line-height:1.9;color:#1a1208;'>
        {st.session_state.ai_memory.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 重新生成", use_container_width=True):
                st.session_state.ai_memory = None
                st.rerun()
        with col2:
            if st.button("📋 複製內容", use_container_width=True):
                st.code(st.session_state.ai_memory)
    
    # Quick examples
    st.markdown("---")
    st.markdown("### 💡 快速範例")
    example_topics = [
        "英國國旗（Union Jack）嘅組成",
        "英格蘭玫瑰、蘇格蘭薊花、威爾士龍",
        "英國人均預期壽命",
        "英國脫歐（Brexit）",
        "伊莉莎白二世女王"
    ]
    cols = st.columns(len(example_topics))
    for i, topic in enumerate(example_topics):
        with cols[i]:
            if st.button(topic, key=f"ex_{i}", use_container_width=True):
                st.session_state.ai_memory = None
                # Trigger generation
                st.query_params["topic"] = topic
                st.rerun()

# ══════════════════════════════════════
# MODE 4: AI 問答
# ══════════════════════════════════════
elif mode == "💬 AI 問答":
    st.markdown("## 💬 AI 備考問答")
    st.markdown("用廣東話問我任何關於 Life in UK 考試嘅問題！")
    
    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message("user" if msg["role"] == "user" else "assistant"):
            st.markdown(msg["content"])
    
    # Quick question buttons
    if not st.session_state.chat_history:
        st.markdown("**💡 快速問題：**")
        quick_cols = st.columns(3)
        quick_qs = [
            ("📋 考試基本資料", "Life in UK考試係點考㗎？幾多題？通過標準係咩？"),
            ("🏰 英國歷史重點", "Life in UK考試入面，英國歷史最重要記住咩？"),
            ("🗳️ 政府同選舉", "英國政府制度同選舉有咩係考試必考嘅？"),
            ("📅 備考計劃", "俾我一個針對50歲以上香港人嘅備考計劃"),
            ("🎯 常見錯誤", "考生最常犯咩錯誤？點樣避免？"),
            ("🌍 英聯邦知識", "英聯邦嘅知識點記？有咩記憶技巧？"),
        ]
        for i, (label, q) in enumerate(quick_qs):
            col = quick_cols[i % 3]
            with col:
                if st.button(label, key=f"quick_{i}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": q})
                    st.rerun()
    
    # Chat input
    if prompt_input := st.chat_input("用廣東話問我問題…"):
        st.session_state.chat_history.append({"role": "user", "content": prompt_input})
        st.rerun()
    
    # Generate AI response for last user message
    if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
        system = """你係一個專為香港移英人士（50歲以上）設計嘅 Life in the UK Test 備考助手。
        
        用廣東話回答，要：
        - 清楚易明，照顧年長學員
        - 提供具體記憶技巧（口訣、縮寫、故事、視覺聯想）
        - 用香港人熟悉嘅例子作比喻
        - 重要術語附英文
        
        考試基本資料：24題、45分鐘、答對18題（75%）合格、費用£50"""
        
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            with st.chat_message("assistant"):
                with st.spinner("思考中…"):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        max_tokens=1000,
                        messages=[{"role": "system", "content": system}] +
                                 [{"role": m["role"], "content": m["content"]} 
                                  for m in st.session_state.chat_history]
                    )
                    reply = response.choices[0].message.content
                    st.markdown(reply)
            
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
        
        except Exception as e:
            st.error(f"AI 連線問題：{str(e)}")
    
    if st.session_state.chat_history:
        if st.button("🗑️ 清除對話", use_container_width=False):
            st.session_state.chat_history = []
            st.rerun()
