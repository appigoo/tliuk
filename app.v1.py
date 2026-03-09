import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import random

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
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@300;400;600;700&family=Lora:ital,wght@0,400;0,600;1,400&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap');

html, body, [class*="css"] { font-family: 'Noto Serif TC', serif; }
.stApp { background: #f7f2e8; }

[data-testid="stSidebar"] { background: #1a1208 !important; }
[data-testid="stSidebar"] * { color: #e8dfc8 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label { color: #d4a829 !important; font-weight: 600; }
h1, h2, h3 { font-family: 'Lora', serif !important; color: #1a1208; }

.bilingual-term {
    display: inline-flex; flex-direction: column; align-items: center;
    background: linear-gradient(135deg, #1a1208, #2d2010);
    border-radius: 6px; padding: 10px 18px; margin: 4px;
    min-width: 140px; text-align: center;
}
.term-zh { color: #f7f2e8; font-size: 1rem; font-weight: 600; line-height: 1.3; }
.term-en { color: #d4a829; font-size: 0.8rem; font-style: italic; margin-top: 3px; letter-spacing: 0.03em; }

.bilingual-card {
    background: #fffdf7; border: 1px solid #c8b89a; border-radius: 6px;
    overflow: hidden; margin: 14px 0; box-shadow: 0 2px 14px rgba(26,18,8,0.08);
}
.card-header {
    background: linear-gradient(90deg, #1a1208, #2d2010);
    padding: 10px 20px; display: flex; align-items: center; gap: 10px;
}
.card-header .topic-badge { color: #d4a829; font-size: 0.75rem; letter-spacing: 0.1em; font-weight: 700; }
.card-body { padding: 20px 24px; }

.question-block {
    display: grid; grid-template-columns: 1fr 1fr; gap: 0;
    border: 1px solid #e0d4b8; border-radius: 4px; overflow: hidden; margin-bottom: 14px;
}
.question-zh {
    padding: 14px 16px; background: #fffdf7;
    font-size: 0.95rem; line-height: 1.75; color: #1a1208;
    border-right: 1px solid #e0d4b8;
}
.question-en {
    padding: 14px 16px; background: #f0ead8;
    font-size: 0.9rem; line-height: 1.75; color: #3a2a10;
    font-family: 'Source Serif 4', serif;
}
.lang-label {
    font-size: 0.65rem; letter-spacing: 0.1em; font-weight: 700;
    margin-bottom: 6px; display: block;
}
.lang-label-zh { color: #b8860b; }
.lang-label-en { color: #8b6020; }

.answer-block {
    display: grid; grid-template-columns: 1fr 1fr; gap: 0;
    border: 1px solid #b8e0b8; border-radius: 4px; overflow: hidden;
}
.answer-zh {
    padding: 12px 16px; background: #f0faf0;
    font-size: 0.9rem; line-height: 1.7; color: #1a4a1a;
    border-right: 1px solid #b8e0b8; font-weight: 600;
}
.answer-en {
    padding: 12px 16px; background: #e4f5e4;
    font-size: 0.88rem; line-height: 1.7; color: #1a4a1a;
    font-family: 'Source Serif 4', serif; font-weight: 600;
}

.keyword-chain { display: flex; align-items: center; flex-wrap: wrap; gap: 6px; margin: 10px 0; }
.keyword-node {
    display: flex; flex-direction: column; align-items: center;
    background: #1a1208; padding: 6px 12px; border-radius: 4px; min-width: 80px;
}
.kn-zh { color: #d4a829; font-size: 0.78rem; font-weight: 700; }
.kn-en { color: rgba(232,223,200,0.75); font-size: 0.65rem; font-style: italic; margin-top: 1px; }
.keyword-arrow { color: #b8860b; font-size: 1.3rem; }

.mnemonic-box {
    background: linear-gradient(135deg, #1a1208, #2d2010);
    border-radius: 8px; padding: 20px 24px; margin: 10px 0; color: #f7f2e8;
}
.mnemonic-title { color: #d4a829; font-weight: 700; font-size: 0.82rem; letter-spacing: 0.1em; margin-bottom: 10px; }
.mnemonic-text { font-size: 1.05rem; line-height: 1.9; white-space: pre-line; }

.vocab-table { width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 0.88rem; }
.vocab-table th {
    background: #1a1208; color: #d4a829; padding: 8px 14px;
    text-align: left; font-weight: 700; font-size: 0.75rem; letter-spacing: 0.08em;
}
.vocab-table td { padding: 9px 14px; border-bottom: 1px solid #e8dfc8; vertical-align: top; }
.vocab-table tr:nth-child(even) td { background: #f7f2e8; }
.vocab-table tr:hover td { background: #f0e8d0; }
.vocab-en { font-family: 'Source Serif 4', serif; color: #1a4a6b; font-weight: 600; }
.vocab-zh { color: #1a1208; }
.vocab-note { color: #8b6020; font-size: 0.78rem; font-style: italic; }

.story-card {
    background: #fff8ee; border: 1px solid #e8d0a0; border-radius: 6px;
    padding: 18px 20px; font-size: 0.9rem; line-height: 1.9; color: #3a2a10;
}

div[data-testid="metric-container"] {
    background: #fffdf7; border: 1px solid #c8b89a; border-radius: 4px; padding: 12px;
}
.stButton > button { border-radius: 3px !important; font-family: 'Noto Serif TC', serif !important; transition: all 0.2s !important; }
.stButton > button:hover { border-color: #b8860b !important; color: #b8860b !important; }

/* XP / streak bar */
.xp-bar-wrap { background: #e8dfc8; border-radius: 99px; height: 10px; overflow: hidden; margin: 6px 0; }
.xp-bar-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #d4a829, #f0c040); transition: width 0.6s ease; }

/* Fun celebration box */
.celebrate-box {
    background: linear-gradient(135deg, #1a4a1a, #2d6a2d);
    border: 2px solid #4a9a4a; border-radius: 10px;
    padding: 18px 24px; text-align: center;
    animation: popIn 0.4s cubic-bezier(0.175,0.885,0.32,1.275);
}
@keyframes popIn { from{transform:scale(0.8);opacity:0} to{transform:scale(1);opacity:1} }
.celebrate-text { color: #a0f0a0; font-size: 1.2rem; font-weight: 700; }
.celebrate-sub { color: rgba(160,240,160,0.7); font-size: 0.85rem; margin-top: 4px; }

.oops-box {
    background: linear-gradient(135deg, #3a1a08, #5a2a10);
    border: 2px solid #c87840; border-radius: 10px;
    padding: 18px 24px; text-align: center;
    animation: shake 0.4s ease;
}
@keyframes shake { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-6px)} 75%{transform:translateX(6px)} }
.oops-text { color: #f0c090; font-size: 1.1rem; font-weight: 700; }
.oops-sub { color: rgba(240,192,144,0.7); font-size: 0.85rem; margin-top: 4px; }

/* Streak badge */
.streak-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: linear-gradient(135deg, #8b1a1a, #c03030);
    color: white; padding: 6px 14px; border-radius: 99px;
    font-size: 0.85rem; font-weight: 700;
    box-shadow: 0 2px 8px rgba(192,48,48,0.4);
    animation: pulse 1.5s infinite;
}
@keyframes pulse { 0%,100%{box-shadow:0 2px 8px rgba(192,48,48,0.4)} 50%{box-shadow:0 2px 16px rgba(192,48,48,0.7)} }

/* Fun fact box */
.funfact-box {
    background: linear-gradient(135deg, #0a2a4a, #1a3a6a);
    border: 1px solid #4a7ab8; border-radius: 8px;
    padding: 16px 20px; margin: 12px 0;
}
.funfact-title { color: #7ab8f0; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.1em; margin-bottom: 6px; }
.funfact-text { color: #c8e0f8; font-size: 0.88rem; line-height: 1.7; }

/* Option buttons states */
.opt-correct { background: #e8f8e8 !important; border-color: #4a9a4a !important; }
.opt-wrong { background: #f8e8e8 !important; border-color: #c84a4a !important; }

/* Welcome banner */
.welcome-banner {
    background: linear-gradient(135deg, #1a1208 0%, #3a2a10 50%, #1a1208 100%);
    border-radius: 12px; padding: 28px 32px; margin-bottom: 24px;
    text-align: center; position: relative; overflow: hidden;
}
.welcome-banner::before {
    content: "🇬🇧"; position: absolute; font-size: 8rem; opacity: 0.05;
    top: -10px; right: -10px;
}
.welcome-title { color: #d4a829; font-family: "Lora", serif; font-size: 1.6rem; margin-bottom: 8px; }
.welcome-sub { color: rgba(232,223,200,0.7); font-size: 0.9rem; }

/* Progress ring text */
.progress-text { font-size: 2rem; font-weight: 700; color: #b8860b; font-family: "Lora", serif; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# KNOWLEDGE BASE — fully bilingual
# ══════════════════════════════════════
KNOWLEDGE_BASE = [
    {
        "id": 1,
        "topic": "歷史 History",
        "question_zh": "《大憲章》係幾年簽訂？有咩意義？",
        "question_en": "When was the Magna Carta signed, and what was its significance?",
        "answer_zh": "1215年，限制君主權力，奠定法治基礎",
        "answer_en": "1215 — limited the monarch's power and established the rule of law",
        "emoji": "📜",
        "vocab": [
            ("Magna Carta", "大憲章", "拉丁文，意思係『大憲章』"),
            ("rule of law", "法治", "法律高於一切，包括國王"),
            ("monarch", "君主 / 國王", "King 或 Queen"),
            ("baron / noble", "貴族", "逼國王簽憲章嘅人"),
            ("Runnymede", "倫尼米德", "簽署地點，倫敦附近"),
        ],
        "keyword_chain": [
            ("1215年", "Year 1215"), ("→", ""), ("約翰王", "King John"),
            ("→", ""), ("貴族施壓", "Barons' Revolt"), ("→", ""),
            ("大憲章", "Magna Carta"), ("→", ""), ("法律高於君主", "Rule of Law"),
        ],
        "mnemonic_type": "諧音記憶",
        "mnemonic": "一二一五（1215）→「一而再，一而五」→ 貴族（Barons）一再要求，終於第五次逼到國王（King John）簽字！\n\nMagna Carta = 「馬嘎 卡他」→ 馬（King）嘎（無聲嘅）被卡（Carta）住，簽晒！",
        "rhyme": "一二一五大憲章，Magna Carta 限君王；\n貴族 Barons 施壓力，Rule of Law 奠基礎長！",
        "story_zh": "1215年，英格蘭貴族忍無可忍，逼迫約翰王在倫尼米德簽下《大憲章》。從此，連國王都要受法律約束——即係話，冇人係法律之上！",
        "story_en": "In 1215, English barons forced King John to sign the Magna Carta at Runnymede. For the first time, even the king was subject to the law — no one was above it.",
        "en_key_phrases": ["Magna Carta (1215)", "King John", "rule of law", "barons", "Runnymede"],
    },
    {
        "id": 2,
        "topic": "政府 Government",
        "question_zh": "英國議會分為上議院同下議院，各有咩功能？",
        "question_en": "What are the roles of the House of Commons and the House of Lords?",
        "answer_zh": "下議院（民選，立法主導）；上議院（任命，審查法案）",
        "answer_en": "House of Commons (elected, leads legislation); House of Lords (appointed, reviews bills)",
        "emoji": "🏛️",
        "vocab": [
            ("House of Commons", "下議院", "民選議員，實際立法"),
            ("House of Lords", "上議院", "貴族/任命，審查法案"),
            ("MP (Member of Parliament)", "國會議員", "下議院選出嘅代表"),
            ("legislation / bill", "法案", "Law 通過前叫 Bill"),
            ("General Election", "大選", "選出下議院議員"),
        ],
        "keyword_chain": [
            ("民選", "Elected"), ("→", ""), ("下議院", "House of Commons"),
            ("→", ""), ("立法", "Legislation"), ("→", ""),
            ("上議院", "House of Lords"), ("→", ""), ("審查", "Review Bills"),
        ],
        "mnemonic_type": "空間記憶",
        "mnemonic": "上面（House of Lords）= 舊貴族坐喺上面睇住；\n下面（House of Commons）= 「Common」= 平民百姓，真正做嘢！\n\nCommons → Common people（平民）→ 民選！\nLords → Lord（老爺）→ 任命貴族！",
        "rhyme": "Commons 下院民選出，立法做嘢最實在；\nLords 上院來審查，Bills 法案兩院過！",
        "story_zh": "想像一棟大廈：地下（House of Commons）係打工仔，每日做嘢立法；樓上（House of Lords）係退休老闆，坐喺度審批。但最終決定權係喺地下！",
        "story_en": "Think of Parliament as a building: the ground floor (House of Commons) is where elected MPs do the real legislative work; upstairs (House of Lords) the Lords review their decisions — but ultimate power lies with the Commons.",
        "en_key_phrases": ["House of Commons", "House of Lords", "MP", "elected", "appointed", "legislation"],
    },
    {
        "id": 3,
        "topic": "歷史 History",
        "question_zh": "維多利亞女王幾時在位？呢個時代有咩特色？",
        "question_en": "When did Queen Victoria reign, and what characterised her era?",
        "answer_zh": "1837–1901年，工業革命，大英帝國版圖最大",
        "answer_en": "1837–1901; Industrial Revolution, British Empire at its largest",
        "emoji": "👑",
        "vocab": [
            ("Queen Victoria", "維多利亞女王", "在位63年"),
            ("Industrial Revolution", "工業革命", "蒸汽機、工廠、鐵路"),
            ("British Empire", "大英帝國", "版圖達地球1/4"),
            ("reign", "在位 / 統治", "國王或女王執政嘅期間"),
            ("colony", "殖民地", "包括香港（1842年起）"),
        ],
        "keyword_chain": [
            ("1837登基", "Crowned 1837"), ("→", ""), ("工業革命", "Industrial Revolution"),
            ("→", ""), ("大英帝國", "British Empire"), ("→", ""),
            ("1/4地球", "¼ of Earth"), ("→", ""), ("1901駕崩", "Died 1901"),
        ],
        "mnemonic_type": "頭字母縮寫",
        "mnemonic": "記住「工帝最長」= Industrial Revolution, Empire biggest, Longest reign（63年）！\n\nVictoria = Victory（勝利）→ 大英帝國最強盛嘅時代！\n1837 → 「一八（18歲）登基，三七（37）年後統治中期」",
        "rhyme": "一八三七 Victoria，Industrial Revolution 起；\nBritish Empire 遍天下，香港 colony 係其一！",
        "story_zh": "維多利亞女王18歲登基，在位長達63年！佢見證英國由農業國變成工業強國，版圖橫跨全球1/4土地，包括香港！",
        "story_en": "Queen Victoria ascended aged 18 and reigned for 63 years. She witnessed Britain transform through the Industrial Revolution, with the British Empire covering a quarter of the globe — including Hong Kong.",
        "en_key_phrases": ["Queen Victoria", "1837–1901", "Industrial Revolution", "British Empire", "colony"],
    },
    {
        "id": 4,
        "topic": "文化 Culture",
        "question_zh": "莎士比亞係邊個？有咩著名作品？",
        "question_en": "Who was William Shakespeare and what is he known for?",
        "answer_zh": "1564–1616年，英國最偉大劇作家，著有《哈姆雷特》等",
        "answer_en": "1564–1616; Britain's greatest playwright, wrote Hamlet, Romeo and Juliet, etc.",
        "emoji": "🎭",
        "vocab": [
            ("playwright", "劇作家", "寫舞台劇嘅人"),
            ("William Shakespeare", "莎士比亞", "史上最著名英語作家"),
            ("Hamlet", "哈姆雷特", "'To be or not to be'"),
            ("Globe Theatre", "環球劇場", "莎士比亞喺倫敦嘅劇院"),
            ("Stratford-upon-Avon", "史特拉福", "莎士比亞嘅出生地"),
        ],
        "keyword_chain": [
            ("史特拉福", "Stratford-upon-Avon"), ("→", ""), ("1564出生", "Born 1564"),
            ("→", ""), ("環球劇場", "Globe Theatre"), ("→", ""),
            ("37部劇作", "37 plays"), ("→", ""), ("1616逝世", "Died 1616"),
        ],
        "mnemonic_type": "數字記憶",
        "mnemonic": "生於1564，死於1616 → 頭尾都係「16」！\n\nShakespeare = Shake（搖）+ Spear（矛）→ 「搖住支矛寫劇本」嘅人！\nGlobe Theatre → 全個地球（Globe）都識佢！",
        "rhyme": "一五六四 Shakespeare 生，Globe Theatre 寫劇情；\nHamlet 問 to be or not，一六一六 完成名！",
        "story_zh": "莎士比亞出生於英格蘭史特拉福（Stratford-upon-Avon），37部劇作影響西方文化500年。《哈姆雷特》問道：'To be or not to be'——考唔考試都係一個問題！",
        "story_en": "Born in Stratford-upon-Avon, Shakespeare wrote 37 plays that shaped Western culture for 500 years. Hamlet's 'To be or not to be' remains one of history's most famous lines.",
        "en_key_phrases": ["William Shakespeare", "playwright", "Stratford-upon-Avon", "Globe Theatre", "Hamlet"],
    },
    {
        "id": 5,
        "topic": "地理 Geography",
        "question_zh": "英國四個組成國家係咩？各自嘅首都？",
        "question_en": "What are the four nations of the UK and their capitals?",
        "answer_zh": "英格蘭(倫敦)、蘇格蘭(愛丁堡)、威爾士(卡迪夫)、北愛爾蘭(貝爾法斯特)",
        "answer_en": "England (London), Scotland (Edinburgh), Wales (Cardiff), Northern Ireland (Belfast)",
        "emoji": "🗺️",
        "vocab": [
            ("England", "英格蘭", "首都 London 倫敦"),
            ("Scotland", "蘇格蘭", "首都 Edinburgh 愛丁堡"),
            ("Wales", "威爾士", "首都 Cardiff 卡迪夫"),
            ("Northern Ireland", "北愛爾蘭", "首都 Belfast 貝爾法斯特"),
            ("United Kingdom (UK)", "英國", "四個國家嘅聯合王國"),
        ],
        "keyword_chain": [
            ("England", "英格蘭"), ("→", ""), ("London", "倫敦"),
            ("Scotland", "蘇格蘭"), ("→", ""), ("Edinburgh", "愛丁堡"),
            ("Wales", "威爾士"), ("→", ""), ("Cardiff", "卡迪夫"),
            ("N. Ireland", "北愛爾蘭"), ("→", ""), ("Belfast", "貝爾法斯特"),
        ],
        "mnemonic_type": "頭韻法",
        "mnemonic": "英文首字母：E-S-W-N → 「Every Student Will Note」\nEngland, Scotland, Wales, Northern Ireland\n\n首都記憶法：\nLondon = 大家都識！\nEdinburgh = E 開頭（但係蘇格蘭，唔係英格蘭！）\nCardiff = C → 威爾士（Wales）有 C\nBelfast = B → 北（North）→ B！",
        "rhyme": "England London 大城市，Scotland Edinburgh 靚；\nWales Cardiff 有條龍，Northern Ireland Belfast 情！",
        "story_zh": "想像UK係一個家庭：英格蘭係老大（最大）；蘇格蘭係個性獨特嘅二哥（想獨立）；威爾士係文靜嘅細妹（有自己語言Welsh）；北愛爾蘭係隔咗海嘅細佬！",
        "story_en": "The UK is like a family: England is the eldest; Scotland is the independent-minded sibling; Wales has its own language (Welsh); and Northern Ireland, across the Irish Sea, has the most complex history.",
        "en_key_phrases": ["England", "Scotland", "Wales", "Northern Ireland", "London", "Edinburgh", "Cardiff", "Belfast"],
    },
    {
        "id": 6,
        "topic": "歷史 History",
        "question_zh": "二戰期間英國首相係邊個？佢有咩貢獻？",
        "question_en": "Who was the UK Prime Minister during World War II and what was his contribution?",
        "answer_zh": "溫斯頓·邱吉爾（Winston Churchill），帶領英國抵抗納粹德國",
        "answer_en": "Winston Churchill; led Britain's resistance against Nazi Germany and inspired the nation",
        "emoji": "✌️",
        "vocab": [
            ("Prime Minister (PM)", "首相", "英國政府首腦"),
            ("Winston Churchill", "溫斯頓·邱吉爾", "二戰英雄首相"),
            ("World War II", "第二次世界大戰", "1939–1945年"),
            ("Nazi Germany", "納粹德國", "由希特拉領導"),
            ("Dunkirk", "敦克爾克", "著名大撤退，1940年"),
        ],
        "keyword_chain": [
            ("1940就任", "PM from 1940"), ("→", ""), ("納粹威脅", "Nazi Threat"),
            ("→", ""), ("永不放棄", "'Never Surrender'"), ("→", ""),
            ("敦克爾克", "Dunkirk 1940"), ("→", ""), ("1945勝利", "Victory 1945"),
        ],
        "mnemonic_type": "視覺聯想",
        "mnemonic": "Churchill = Church（教堂）+ Hill（山丘）= 山上教堂永遠屹立不倒！\n\n標誌：🎩 高帽 + 🚬 雪茄 + ✌️ V字手勢\n名言：'We shall never surrender'（我哋永不放棄）\n\nNever Surrender = 永不放棄 = 邱吉爾精神！",
        "rhyme": "Churchill 邱吉爾二戰雄，Prime Minister 保英城；\nNever Surrender 永不降，V 字手勢傳萬方！",
        "story_zh": "1940年，德軍橫掃歐洲，英國孤立無援。邱吉爾發表著名演講：「我哋永不放棄！」（We shall never surrender）此精神令英國撐到美國參戰，最終勝利。",
        "story_en": "In 1940, with Nazi Germany sweeping Europe, Churchill rallied Britain with 'We shall never surrender.' His leadership sustained Britain until the Allies achieved victory in 1945.",
        "en_key_phrases": ["Winston Churchill", "Prime Minister", "World War II", "never surrender", "Dunkirk"],
    },
    {
        "id": 7,
        "topic": "政府 Government",
        "question_zh": "英國採用咩選舉制度？",
        "question_en": "What electoral system does the UK use for general elections?",
        "answer_zh": "簡單多數決（First Past the Post），得最多票嘅候選人勝出",
        "answer_en": "First Past the Post (FPTP) — the candidate with the most votes wins the constituency seat",
        "emoji": "🗳️",
        "vocab": [
            ("First Past the Post (FPTP)", "簡單多數決", "最多票即勝，唔需過半"),
            ("constituency", "選區", "每區選出一名 MP"),
            ("candidate", "候選人", "競選嘅人"),
            ("ballot / ballot paper", "選票", "投票用嘅紙"),
            ("general election", "大選", "全國性選舉，選出下議院"),
        ],
        "keyword_chain": [
            ("選區", "Constituency"), ("→", ""), ("候選人競選", "Candidates stand"),
            ("→", ""), ("最多票勝出", "Most votes wins"), ("→", ""),
            ("FPTP 制度", "First Past the Post"), ("→", ""), ("議員當選", "MP elected"),
        ],
        "mnemonic_type": "比喻記憶",
        "mnemonic": "First Past the Post = 賽馬制度 🏇\n邊匹馬先過終點線（the Post）就贏（First）！\n唔理其他馬差幾遠，唔需要過半！\n\nFPTP → Fast Person Takes Prize（最快嘅人攞獎）",
        "rhyme": "First Past the Post 賽馬型，最多選票 constituency 贏；\n唔需過半 majority，FPTP 英國行！",
        "story_zh": "想像100人投票：A得40票、B得35票、C得25票——A勝出！但係60%選民係投反對A嘅，呢個就係FPTP嘅爭議。",
        "story_en": "Imagine 100 voters: A gets 40, B gets 35, C gets 25 — A wins! Yet 60% voted against A. This is the key controversy of the First Past the Post system.",
        "en_key_phrases": ["First Past the Post", "FPTP", "constituency", "candidate", "general election", "ballot"],
    },
    {
        "id": 8,
        "topic": "文化 Culture",
        "question_zh": "英聯邦（Commonwealth）係咩？有幾多個成員國？",
        "question_en": "What is the Commonwealth of Nations and how many member states does it have?",
        "answer_zh": "前英國殖民地組成嘅自願聯盟，約54個成員國",
        "answer_en": "A voluntary association of former British territories; approximately 54 member states",
        "emoji": "🌍",
        "vocab": [
            ("Commonwealth of Nations", "英聯邦", "前殖民地自願組成嘅聯盟"),
            ("member state", "成員國", "目前約有54個"),
            ("voluntary", "自願", "唔係強制加入"),
            ("former colony", "前殖民地", "曾係英國殖民地"),
            ("Head of the Commonwealth", "英聯邦元首", "英國國王擔任"),
        ],
        "keyword_chain": [
            ("英國殖民地", "British colonies"), ("→", ""), ("獨立後", "Post-independence"),
            ("→", ""), ("自願加入", "Voluntary membership"), ("→", ""),
            ("54成員國", "54 member states"), ("→", ""), ("共同價值", "Shared values"),
        ],
        "mnemonic_type": "數字記憶",
        "mnemonic": "54個成員國 = 打麻雀54隻牌（筒索萬各18隻）！🀄\n香港人最識麻雀，54就記得喇！\n\nCommonwealth = Common（共同）+ Wealth（財富）\n= 共同富貴嘅國家聯盟！",
        "rhyme": "Commonwealth 英聯邦，五十四國 voluntary；\nFormer colonies 自願入，共同 values 連繫強！",
        "story_zh": "英聯邦係大英帝國分崩離析後留低嘅「友誼網絡」。香港雖然1997年回歸，但曾係英聯邦嘅一部分。今日54個成員國，包括印度、加拿大、澳洲等。",
        "story_en": "The Commonwealth is the friendship network that emerged from the fall of the British Empire. Its 54 member states include India, Canada and Australia — all voluntary members united by shared values.",
        "en_key_phrases": ["Commonwealth of Nations", "54 member states", "voluntary", "former colony", "shared values"],
    },
]

# ── SESSION STATE ──
for k, v in {
    "quiz_score": 0, "quiz_total": 0,
    "current_q": None, "quiz_answered": False,
    "selected_opt": None, "chat_history": [],
    "ai_memory": None, "flashcard_idx": 0,
    "streak": 0, "best_streak": 0, "show_confetti": False,
    "last_was_correct": None, "xp": 0,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── ENCOURAGEMENT MESSAGES ──
CORRECT_MSGS = [
    "🎉 叻仔叻女！答啱喇！", "🌟 正！你真係得！", "💪 勁！繼續加油！",
    "🏆 完美！狀態正好！", "👏 好嘢！學到喇！", "🎊 哇！好醒目！",
    "⭐ 滿分！你好犀利！", "🦁 獅子山精神！答對！", "🍵 飲杯茶休息下，你做得好好！",
    "🎯 一矢中的！正確！",
]
WRONG_MSGS = [
    "😅 差少少！下次一定得！", "🤔 冇問題，溫多次就記得！",
    "💡 唔緊要，睇吓下面嘅記憶術！", "🌱 學習係一個過程，繼續！",
    "☕ 飲杯茶，再睇多次！", "🐢 慢慢嚟，熟能生巧！",
    "📖 溫書唔係一日之功，你做得到！", "💪 跌倒再爬起，你最叻！",
]
STREAK_MSGS = {3: "🔥 連中3題！", 5: "🔥🔥 連中5題！超勁！", 8: "🔥🔥🔥 連中8題！你係高手！", 10: "👑 連中10題！準備考試啦！"}


def render_keyword_chain(chain):
    html = '<div class="keyword-chain">'
    for zh, en in chain:
        if zh == "→":
            html += '<span class="keyword-arrow">→</span>'
        else:
            html += (f'<span class="keyword-node">'
                     f'<span class="kn-zh">{zh}</span>'
                     f'<span class="kn-en">{en}</span>'
                     f'</span>')
    html += '</div>'
    return html


def tts_button(text: str, label: str = "🔊 讀出", key: str = "tts", rate: float = 0.85, pitch: float = 1.0):
    """Render a speak button using browser Web Speech API."""
    # Escape for JS string — handle quotes and backslashes
    safe = (text.replace("\\", "\\\\")
                .replace("'", "\\'")
                .replace("\n", " ")
                .replace("\r", ""))
    uid = abs(hash(key + text)) % 99999
    components.html(f"""
    <style>
      .tts-btn-{uid} {{
        display: inline-flex; align-items: center; gap: 7px;
        background: linear-gradient(135deg, #1a1208, #3a2a10);
        color: #d4a829; border: 1.5px solid #b8860b; border-radius: 6px;
        padding: 8px 18px; font-size: 0.9rem; font-family: serif;
        cursor: pointer; transition: all 0.2s; user-select: none;
        box-shadow: 0 2px 8px rgba(184,134,11,0.2);
      }}
      .tts-btn-{uid}:hover {{ background: #2d2010; box-shadow: 0 3px 12px rgba(184,134,11,0.4); transform: translateY(-1px); }}
      .tts-btn-{uid}.speaking {{ background: linear-gradient(135deg, #1a3a1a, #2d5a2d); border-color: #4a9a4a; color: #80d880; animation: tts-pulse 0.8s infinite; }}
      @keyframes tts-pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:0.7}} }}
      .tts-wave-{uid} {{ display:none; gap:2px; align-items:center; }}
      .tts-wave-{uid}.show {{ display:inline-flex; }}
      .tts-wave-{uid} span {{ width:3px; background:#80d880; border-radius:2px; animation:wave 0.8s infinite ease-in-out; }}
      .tts-wave-{uid} span:nth-child(1){{height:6px;animation-delay:0s}}
      .tts-wave-{uid} span:nth-child(2){{height:12px;animation-delay:0.15s}}
      .tts-wave-{uid} span:nth-child(3){{height:8px;animation-delay:0.3s}}
      .tts-wave-{uid} span:nth-child(4){{height:14px;animation-delay:0.1s}}
      .tts-wave-{uid} span:nth-child(5){{height:6px;animation-delay:0.25s}}
      @keyframes wave {{ 0%,100%{{transform:scaleY(1)}} 50%{{transform:scaleY(1.8)}} }}
    </style>
    <button class="tts-btn-{uid}" id="btn-{uid}" onclick="speakText_{uid}()">
      <span id="icon-{uid}">🔊</span>
      <span id="lbl-{uid}">{label}</span>
      <div class="tts-wave-{uid}" id="wave-{uid}">
        <span></span><span></span><span></span><span></span><span></span>
      </div>
    </button>
    <script>
    var synth_{uid} = window.speechSynthesis;
    var utt_{uid} = null;
    function speakText_{uid}() {{
      var btn = document.getElementById('btn-{uid}');
      var wave = document.getElementById('wave-{uid}');
      var icon = document.getElementById('icon-{uid}');
      var lbl = document.getElementById('lbl-{uid}');
      if (synth_{uid}.speaking) {{
        synth_{uid}.cancel();
        btn.classList.remove('speaking');
        wave.classList.remove('show');
        icon.textContent = '🔊';
        lbl.textContent = '{label}';
        return;
      }}
      utt_{uid} = new SpeechSynthesisUtterance('{safe}');
      utt_{uid}.lang = 'en-GB';
      utt_{uid}.rate = {rate};
      utt_{uid}.pitch = {pitch};
      // Prefer a British English voice
      var voices = synth_{uid}.getVoices();
      var preferred = voices.find(v => v.lang === 'en-GB') ||
                      voices.find(v => v.lang.startsWith('en')) || null;
      if (preferred) utt_{uid}.voice = preferred;
      utt_{uid}.onstart = function() {{
        btn.classList.add('speaking');
        wave.classList.add('show');
        icon.textContent = '⏹';
        lbl.textContent = '停止朗讀';
      }};
      utt_{uid}.onend = utt_{uid}.onerror = function() {{
        btn.classList.remove('speaking');
        wave.classList.remove('show');
        icon.textContent = '🔊';
        lbl.textContent = '{label}';
      }};
      synth_{uid}.speak(utt_{uid});
    }}
    // Pre-load voices on mobile browsers
    if (synth_{uid}.onvoiceschanged !== undefined) {{
      synth_{uid}.onvoiceschanged = function() {{ synth_{uid}.getVoices(); }};
    }}
    </script>
    """, height=52)


# ══════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════
with st.sidebar:
    st.markdown("## 🇬🇧 Life in UK\n### 中英對照記憶助手")
    st.markdown("---")
    mode = st.radio(
        "學習模式 Learning Mode",
        ["🧠 記憶卡片", "📖 英文詞彙表", "🎯 模擬測試", "🤖 AI 記憶術", "💬 AI 問答"],
        label_visibility="visible"
    )
    st.markdown("---")
    topic_filter = st.multiselect(
        "篩選範疇 Topics",
        ["歷史 History", "政府 Government", "文化 Culture", "地理 Geography"],
        default=["歷史 History", "政府 Government", "文化 Culture", "地理 Geography"]
    )
    st.markdown("---")
    st.markdown(f"""
    <div style="color:#d4a829;font-size:0.8rem;line-height:1.9">
    📊 <b>學習進度</b><br>
    答題：{st.session_state.quiz_total}<br>
    答對：{st.session_state.quiz_score}<br>
    正確率：{'—' if st.session_state.quiz_total==0 else f"{int(st.session_state.quiz_score/st.session_state.quiz_total*100)}%"}<br>
    合格線 Pass mark：75%
    </div>
    """, unsafe_allow_html=True)
    # XP display
    xp = st.session_state.xp
    xp_level = xp // 100 + 1
    xp_pct = (xp % 100)
    st.markdown(f"""
    <div style="color:#d4a829;font-size:0.75rem;margin-top:4px">
    ⚡ <b>XP：{xp}</b> · 等級 Level {xp_level}
    </div>
    <div class="xp-bar-wrap"><div class="xp-bar-fill" style="width:{xp_pct}%"></div></div>
    """, unsafe_allow_html=True)
    if st.session_state.streak > 0:
        st.markdown(f'<div class="streak-badge">🔥 連對 {st.session_state.streak} 題</div>', unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🔄 重置進度 Reset", use_container_width=True):
        st.session_state.quiz_score = 0
        st.session_state.quiz_total = 0
        st.session_state.streak = 0
        st.session_state.xp = 0
        st.rerun()

filtered_kb = [k for k in KNOWLEDGE_BASE if k["topic"] in topic_filter]

# ══════════════════════════════════════
# MODE 1: 記憶卡片
# ══════════════════════════════════════
if mode == "🧠 記憶卡片":
    st.markdown("""
    <div class="welcome-banner">
      <div class="welcome-title">🧠 中英對照記憶卡片</div>
      <div class="welcome-sub">每張卡片有5種記憶技巧 · 廣東話理解 + 英文考試用語<br>
      點擊展開任何卡片開始學習！</div>
    </div>
    """, unsafe_allow_html=True)

    if not filtered_kb:
        st.warning("請在側欄選擇至少一個學習範疇。")
    else:
        for item in filtered_kb:
            label = f"{item['emoji']}  **{item['topic']}** ── {item['question_zh']}"
            with st.expander(label, expanded=False):

                st.markdown(f"""
                <div class="question-block">
                  <div class="question-zh">
                    <span class="lang-label lang-label-zh">🇭🇰 廣東話（理解用）</span>
                    {item['question_zh']}
                  </div>
                  <div class="question-en">
                    <span class="lang-label lang-label-en">🇬🇧 English（考試用）</span>
                    {item['question_en']}
                  </div>
                </div>
                <div class="answer-block">
                  <div class="answer-zh">
                    <span class="lang-label lang-label-zh">✅ 答案（中文）</span>
                    {item['answer_zh']}
                  </div>
                  <div class="answer-en">
                    <span class="lang-label lang-label-en">✅ Answer (English)</span>
                    {item['answer_en']}
                  </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("**🔑 考試英文關鍵詞 Key Exam Terms**")
                terms_html = "".join([
                    f'<span class="bilingual-term"><span class="term-en">{en}</span><span class="term-zh">{zh}</span></span>'
                    for en, zh, _ in item["vocab"]
                ])
                st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:6px;margin:8px 0">{terms_html}</div>', unsafe_allow_html=True)

                # TTS for question and answer
                _c1, _c2 = st.columns(2)
                with _c1:
                    tts_button(item["question_en"], label="🔊 讀出題目", key=f"tts_card_q_{item['id']}", rate=0.8)
                with _c2:
                    tts_button(item["answer_en"], label="🔊 讀出答案", key=f"tts_card_a_{item['id']}", rate=0.75)

                tabs = st.tabs(["🔗 關鍵字鏈", "🎵 口訣", "📖 雙語故事", "💡 記憶術"])

                with tabs[0]:
                    st.markdown(render_keyword_chain(item["keyword_chain"]), unsafe_allow_html=True)
                    st.markdown("**英文必記短語 Key English Phrases:**")
                    st.markdown("  ".join([f"`{p}`" for p in item["en_key_phrases"]]))
                    tts_button(". ".join(item["en_key_phrases"]), label="🔊 讀出關鍵詞", key=f"tts_kp_{item['id']}", rate=0.7)

                with tabs[1]:
                    st.markdown(f"""
                    <div class='mnemonic-box'>
                      <div class='mnemonic-title'>🎵 順口溜（英文關鍵詞已標出）</div>
                      <div class='mnemonic-text'>{item['rhyme']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with tabs[2]:
                    col_zh, col_en = st.columns(2)
                    with col_zh:
                        st.markdown("**🇭🇰 廣東話故事**")
                        st.markdown(f'<div class="story-card">{item["story_zh"]}</div>', unsafe_allow_html=True)
                    with col_en:
                        st.markdown("**🇬🇧 English Story**")
                        st.markdown(f'<div class="story-card" style="font-family:\'Source Serif 4\',serif;font-size:0.88rem">{item["story_en"]}</div>', unsafe_allow_html=True)
                        tts_button(item["story_en"], label="🔊 讀出英文故事", key=f"tts_story_{item['id']}", rate=0.78)

                with tabs[3]:
                    st.markdown(f"""
                    <div class='mnemonic-box'>
                      <div class='mnemonic-title'>💡 {item['mnemonic_type']}</div>
                      <div class='mnemonic-text'>{item['mnemonic']}</div>
                    </div>
                    """, unsafe_allow_html=True)

# ══════════════════════════════════════
# MODE 2: 英文詞彙表
# ══════════════════════════════════════
elif mode == "📖 英文詞彙表":
    st.markdown("""
    <div class="welcome-banner">
      <div class="welcome-title">📖 英文詞彙對照表</div>
      <div class="welcome-sub">考試係英文作答 · 熟讀英文術語係通過考試嘅關鍵<br>
      下面仲有閃卡練習，幫你鞏固記憶！</div>
    </div>
    """, unsafe_allow_html=True)

    search = st.text_input("🔍 搜尋詞彙 Search", placeholder="輸入中文或英文…")

    all_vocab = []
    for item in KNOWLEDGE_BASE:
        if item["topic"] in topic_filter:
            for en, zh, note in item["vocab"]:
                all_vocab.append((en, zh, note, item["topic"], item["emoji"]))

    if search:
        all_vocab = [v for v in all_vocab if search.lower() in v[0].lower() or search in v[1]]

    seen, unique_vocab = set(), []
    for v in all_vocab:
        if v[0] not in seen:
            seen.add(v[0])
            unique_vocab.append(v)

    rows = "".join([
        f'<tr><td class="vocab-en">{en}</td><td class="vocab-zh">{zh}</td>'
        f'<td class="vocab-note">{note}</td>'
        f'<td style="font-size:0.75rem;color:#6b5e4a">{emoji} {topic}</td></tr>'
        for en, zh, note, topic, emoji in unique_vocab
    ])
    st.markdown(f"""
    <table class="vocab-table">
      <thead><tr>
        <th>🇬🇧 English Term（考試用）</th>
        <th>🇭🇰 中文解釋</th>
        <th>📝 記憶提示</th>
        <th>📚 範疇</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)
    st.markdown(f"**共 {len(unique_vocab)} 個詞彙 · {len(unique_vocab)} terms**")

    # English Flashcard Drill
    st.markdown("---")
    st.markdown("### 🃏 英文閃卡練習 English Flashcard Drill")
    st.markdown("""
    <div class="funfact-box">
      <div class="funfact-title">🎮 點玩</div>
      <div class="funfact-text">睇住中文 → 喺心入面諗一諗英文答案 → 再按「顯示英文」核對！
      重複練習直到唔使睇答案為止。考試係英文，所以要熟悉英文用法！</div>
    </div>
    """, unsafe_allow_html=True)

    if unique_vocab:
        idx = st.session_state.flashcard_idx % len(unique_vocab)
        card = unique_vocab[idx]
        show_key = f"show_flash_{idx}"
        if show_key not in st.session_state:
            st.session_state[show_key] = False

        _, col, _ = st.columns([1, 2, 1])
        with col:
            answer_html = (
                f"<div style='font-size:1.15rem;color:#1a4a6b;font-family:\"Source Serif 4\",serif;"
                f"font-weight:700;border-top:1px solid #e0d4b8;padding-top:12px;margin-top:8px'>"
                f"{card[0]}</div>"
            ) if st.session_state[show_key] else (
                "<div style='color:#c8b89a;font-size:0.85rem'>點擊「顯示英文」→ Click 'Show English'</div>"
            )
            st.markdown(f"""
            <div style="background:linear-gradient(145deg,#fffdf7,#f0e8d0);
                        border:2px solid #b8860b;border-radius:8px;padding:28px;
                        text-align:center;box-shadow:4px 4px 0 #b8860b;min-height:160px;
                        display:flex;flex-direction:column;justify-content:center;align-items:center">
              <div style="font-size:0.72rem;color:#8b6020;letter-spacing:0.1em;margin-bottom:8px">中文 CHINESE</div>
              <div style="font-size:1.3rem;color:#1a1208;margin-bottom:4px;font-weight:600">{card[1]}</div>
              <div style="font-size:0.78rem;color:#8b6020;margin-bottom:12px">{card[2]}</div>
              <div style="font-size:0.72rem;color:#b8860b;letter-spacing:0.1em;margin-bottom:4px">ENGLISH ANSWER 英文答案</div>
              {answer_html}
            </div>
            """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("👁️ 顯示英文 Show EN", use_container_width=True):
                st.session_state[show_key] = True
                st.rerun()
        with c2:
            if st.button("⏭️ 下一張 Next", use_container_width=True):
                st.session_state.flashcard_idx = idx + 1
                st.rerun()
        with c3:
            if st.button("🔀 隨機 Random", use_container_width=True):
                st.session_state.flashcard_idx = random.randint(0, len(unique_vocab) - 1)
                st.rerun()

        # TTS — always show; reads the EN term aloud
        tts_button(
            f"{card[0]}. {card[2]}",
            label="🔊 讀出英文術語",
            key=f"tts_flash_{idx}",
            rate=0.75
        )
        st.caption(f"詞彙 {idx+1} / {len(unique_vocab)}")

# ══════════════════════════════════════
# MODE 3: 模擬測試 (English questions)
# ══════════════════════════════════════
elif mode == "🎯 模擬測試":
    # Fun facts shown while studying
    FUN_FACTS = [
        "💡 你知唔知：Life in UK考試喺英國超過1,500個考試中心都可以考！",
        "💡 趣聞：Magna Carta 係拉丁文，意思係「Great Charter」大憲章！",
        "💡 你知唔知：英國國歌係 God Save the King（或 Queen），視乎當時嘅君主！",
        "💡 趣聞：莎士比亞發明咗超過1,700個英文新詞，包括 bedroom、lonely、generous！",
        "💡 你知唔知：英國係全球第一個工業化國家，喺18世紀引領工業革命！",
        "💡 趣聞：英聯邦嘅54個成員國，合共有24億人口，佔全球1/3！",
        "💡 你知唔知：英國議會係全球最古老嘅議會之一，有超過700年歷史！",
    ]
    if "fun_fact_idx" not in st.session_state:
        st.session_state.fun_fact_idx = random.randint(0, len(FUN_FACTS)-1)

    st.markdown(f"""
    <div class="welcome-banner">
      <div class="welcome-title">🎯 模擬測試</div>
      <div class="welcome-sub">英文題目 · 答題後即睇記憶技巧 · 連對有獎勵！</div>
    </div>
    <div class="funfact-box">
      <div class="funfact-title">📚 學習趣聞 FUN FACT</div>
      <div class="funfact-text">{FUN_FACTS[st.session_state.fun_fact_idx]}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("✅ 答對", st.session_state.quiz_score)
    with c2:
        st.metric("📝 已答", st.session_state.quiz_total)
    with c3:
        pct = int(st.session_state.quiz_score / st.session_state.quiz_total * 100) if st.session_state.quiz_total > 0 else 0
        delta_color = "normal"
        st.metric("🎯 正確率", f"{pct}%", delta="✓ 合格！" if pct >= 75 else f"差 {75-pct}%")
    with c4:
        st.metric("🔥 連對", f"{st.session_state.streak} 題", delta=f"最高 {st.session_state.best_streak}")
    # Progress bar toward pass mark
    if st.session_state.quiz_total > 0:
        bar_color = "#4a9a4a" if pct >= 75 else "#b8860b"
        st.markdown(f"""
        <div style="margin:4px 0 12px">
          <div style="font-size:0.72rem;color:#6b5e4a;margin-bottom:3px">
            合格進度 Pass Progress ({pct}% / 75%)
          </div>
          <div class="xp-bar-wrap" style="height:14px">
            <div class="xp-bar-fill" style="width:{min(pct,100)}%;background:{bar_color}"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    if not filtered_kb:
        st.warning("請在側欄選擇至少一個學習範疇。")
    else:
        # Reset if stale question from old data structure
        if st.session_state.current_q is None or "question_en" not in st.session_state.current_q:
            st.session_state.current_q = random.choice(filtered_kb)
            st.session_state.quiz_answered = False

        q = st.session_state.current_q

        st.markdown(f"""
        <div class="bilingual-card">
          <div class="card-header">
            <span style="font-size:1.4rem">{q['emoji']}</span>
            <span class="topic-badge">{q['topic']}</span>
          </div>
          <div class="card-body">
            <div style="font-size:0.7rem;color:#d4a829;letter-spacing:0.1em;font-weight:700;margin-bottom:8px">
              🇬🇧 EXAM QUESTION (English — as it appears in the real test)
            </div>
            <div style="font-family:'Source Serif 4',serif;font-size:1.1rem;line-height:1.75;color:#1a1208;margin-bottom:12px">
              {q['question_en']}
            </div>
            <div style="font-size:0.82rem;color:#8b6020;border-top:1px solid #e0d4b8;padding-top:8px">
              🇭🇰 廣東話參考：{q['question_zh']}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        tts_button(q['question_en'], label="🔊 讀出題目", key=f"tts_q_{q['id']}", rate=0.8)

        # Use seeded RNG so options are identical before and after rerun
        rng = random.Random(q["id"])
        wrong_pool = [k["answer_en"] for k in KNOWLEDGE_BASE if k["id"] != q["id"]]
        wrong_opts = rng.sample(wrong_pool, min(3, len(wrong_pool)))
        all_opts = wrong_opts + [q["answer_en"]]
        rng.shuffle(all_opts)
        opt_key = f"quiz_{q['id']}_{st.session_state.quiz_total}"

        if not st.session_state.quiz_answered:
            st.markdown("**Select the correct answer / 選擇正確答案：**")
            letters = ["A", "B", "C", "D"]
            for i, opt in enumerate(all_opts):
                if st.button(f"　{letters[i]}.  {opt}", key=f"opt_{i}_{opt_key}", use_container_width=True):
                    st.session_state.quiz_total += 1
                    # Store only selected text; re-derive correctness at render time
                    st.session_state.selected_opt = opt
                    if opt == q["answer_en"]:
                        st.session_state.quiz_score += 1
                        st.session_state.streak += 1
                        st.session_state.xp += 20
                        if st.session_state.streak > st.session_state.best_streak:
                            st.session_state.best_streak = st.session_state.streak
                        st.session_state.fun_fact_idx = random.randint(0, 6)
                    else:
                        st.session_state.streak = 0
                        st.session_state.xp = max(0, st.session_state.xp - 5)
                    st.session_state.quiz_answered = True
                    st.rerun()
        else:
            selected = st.session_state.selected_opt
            # Re-derive correctness at render time — avoids stale tuple bug
            is_correct = isinstance(selected, str) and selected == q["answer_en"]
            if is_correct:
                enc_msg = random.choice(CORRECT_MSGS)
                streak_msg = STREAK_MSGS.get(st.session_state.streak, "")
                st.markdown(f"""
                <div class="celebrate-box">
                  <div class="celebrate-text">{enc_msg}</div>
                  <div class="celebrate-sub">🇬🇧 {q["answer_en"]}</div>
                  {("<div style='color:#ffdd80;font-size:1rem;margin-top:6px'>" + streak_msg + "</div>") if streak_msg else ""}
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"🇭🇰 中文答案：**{q['answer_zh']}**")
                tts_button(
                    f"Correct! The answer is: {q['answer_en']}",
                    label="🔊 讀出答案",
                    key=f"tts_ans_c_{q['id']}_{st.session_state.quiz_total}",
                    rate=0.8
                )
            else:
                enc_msg = random.choice(WRONG_MSGS)
                st.markdown(f"""
                <div class="oops-box">
                  <div class="oops-text">{enc_msg}</div>
                  <div class="oops-sub">你選：{selected}</div>
                  <div style="color:#f0d090;font-weight:700;margin-top:8px">✅ 正確答案：{q["answer_en"]}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"🇭🇰 中文答案：**{q['answer_zh']}**")
                tts_button(
                    f"The correct answer is: {q['answer_en']}",
                    label="🔊 讀出正確答案",
                    key=f"tts_ans_w_{q['id']}_{st.session_state.quiz_total}",
                    rate=0.8
                )

            st.markdown("### 💡 記憶技巧 Memory Tips")
            t1, t2, t3, t4 = st.tabs(["🔑 英文關鍵詞", "🔗 關鍵字鏈", "🎵 口訣", "📖 雙語故事"])
            with t1:
                vocab_rows = "".join([
                    f'<tr><td class="vocab-en">{en}</td><td class="vocab-zh">{zh}</td><td class="vocab-note">{note}</td></tr>'
                    for en, zh, note in q["vocab"]
                ])
                st.markdown(f"""
                <table class="vocab-table">
                  <thead><tr>
                    <th>🇬🇧 English Term</th>
                    <th>🇭🇰 中文意思</th>
                    <th>📝 記憶提示</th>
                  </tr></thead>
                  <tbody>{vocab_rows}</tbody>
                </table>
                """, unsafe_allow_html=True)
            with t2:
                st.markdown(render_keyword_chain(q["keyword_chain"]), unsafe_allow_html=True)
            with t3:
                st.markdown(f"""
                <div class='mnemonic-box'>
                  <div class='mnemonic-title'>{q['mnemonic_type']}</div>
                  <div class='mnemonic-text'>{q['mnemonic']}</div>
                </div>
                <div class='mnemonic-box' style='margin-top:8px;background:linear-gradient(135deg,#2d1a30,#1a1208)'>
                  <div class='mnemonic-title'>🎵 順口溜</div>
                  <div class='mnemonic-text'>{q['rhyme']}</div>
                </div>
                """, unsafe_allow_html=True)
            with t4:
                ca, cb = st.columns(2)
                with ca:
                    st.markdown("**🇭🇰 廣東話**")
                    st.markdown(f'<div class="story-card">{q["story_zh"]}</div>', unsafe_allow_html=True)
                with cb:
                    st.markdown("**🇬🇧 English**")
                    st.markdown(f'<div class="story-card" style="font-family:\'Source Serif 4\',serif;font-size:0.88rem">{q["story_en"]}</div>', unsafe_allow_html=True)

            next_labels = ["➡️ 繼續！下一題！", "💪 唔怕！下一題！", "🚀 衝！下一題！", "🎯 再試！下一題！"]
            if st.button(random.choice(next_labels), type="primary", use_container_width=True):
                st.session_state.current_q = random.choice(filtered_kb)
                st.session_state.quiz_answered = False
                st.rerun()

# ══════════════════════════════════════
# MODE 4: AI 記憶術
# ══════════════════════════════════════
elif mode == "🤖 AI 記憶術":
    st.markdown("""
    <div class="welcome-banner">
      <div class="welcome-title">🤖 AI 即時生成記憶術</div>
      <div class="welcome-sub">輸入任何考試內容 · AI 即時創作廣東話口訣 + 英文詞彙 + 故事！<br>
      係你專屬嘅記憶術，其他人冇得用！</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        user_topic = st.text_input(
            "輸入想記住嘅內容",
            placeholder="例如：the Union Jack / 女性投票權 / the Domesday Book…"
        )
    with col2:
        memory_type_ai = st.selectbox(
            "重點技巧",
            ["全套（口訣+詞彙表+故事+視覺）", "🎵 廣東話口訣", "🔤 英文縮寫法", "📖 雙語故事", "📋 英文詞彙表"]
        )

    if st.button("✨ 生成記憶術 Generate", type="primary", use_container_width=True) and user_topic:
        prompt = f"""你係一個專為香港50歲以上移英人士設計嘅 Life in UK Test 記憶術專家。

用戶想記住：「{user_topic}」

考試係英文作答，所以必須提供中英對照。請按以下格式回覆：

**📌 核心知識點 Core Knowledge**
中文解釋：[廣東話解釋]
English answer：[英文答案，考試用語，要準確]

**🔑 英文關鍵詞表 Key English Terms**
（至少5個，用表格：English | 中文意思 | 記憶提示）

**🎵 廣東話口訣（含英文關鍵詞）**
[押韻口訣，英文詞用大楷寫出]

**💡 記憶技巧**
[廣東話解釋，用香港人熟悉嘅例子，幫助記住英文術語]

**🔗 中英對照關鍵字鏈**
中文鏈：詞1 → 詞2 → 詞3
English：Word1 → Word2 → Word3

**👁️ 視覺記憶圖像**
[幫助記憶英文術語嘅視覺聯想]"""

        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            with st.spinner("🤖 AI 緊係度幫你創作記憶術…"):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    max_tokens=1200,
                    messages=[{"role": "user", "content": prompt}]
                )
            st.session_state.ai_memory = response.choices[0].message.content
        except Exception as e:
            st.error(f"AI 連線出現問題：{e}\n\n請確保 Streamlit Secrets 已設定 GROQ_API_KEY。")

    if st.session_state.ai_memory:
        st.markdown("---")
        st.markdown("### ✨ AI 生成嘅中英對照記憶術")
        st.markdown(st.session_state.ai_memory)
        if st.button("🔄 重新生成 Regenerate", use_container_width=False):
            st.session_state.ai_memory = None
            st.rerun()

    st.markdown("---")
    st.markdown("### 💡 快速範例 Quick Examples")
    examples = [
        "The Union Jack 英國國旗", "The Suffragettes 女性參政",
        "The NHS 國家醫療服務", "Guy Fawkes / Gunpowder Plot",
        "The Domesday Book", "The Battle of Hastings 1066",
    ]
    cols = st.columns(3)
    for i, ex in enumerate(examples):
        with cols[i % 3]:
            if st.button(ex, key=f"ex_{i}", use_container_width=True):
                st.session_state.ai_memory = None
                try:
                    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    with st.spinner("生成中…"):
                        resp = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            max_tokens=1000,
                            messages=[{"role": "user", "content":
                                f"你係Life in UK Test記憶術專家，幫香港50歲以上移英人士。"
                                f"記住「{ex}」，提供：廣東話口訣（含英文術語）、英文關鍵詞表（中英對照）、雙語故事、視覺記憶。"
                                f"考試係英文，英文術語要準確。"}]
                        )
                    st.session_state.ai_memory = resp.choices[0].message.content
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

# ══════════════════════════════════════
# MODE 5: AI 問答
# ══════════════════════════════════════
elif mode == "💬 AI 問答":
    st.markdown("""
    <div class="welcome-banner">
      <div class="welcome-title">💬 AI 備考問答</div>
      <div class="welcome-sub">用廣東話問我任何問題 · 我會提供廣東話解釋 + 英文考試用語<br>
      隨時問，唔怕蠢問題，只怕唔問！</div>
    </div>
    """, unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        with st.chat_message("user" if msg["role"] == "user" else "assistant"):
            st.markdown(msg["content"])

    if not st.session_state.chat_history:
        st.markdown("**💡 快速問題：**")
        quick_cols = st.columns(3)
        quick_qs = [
            ("📋 考試資料", "Life in UK考試係點考㗎？幾多題？幫我列出重要英文術語。"),
            ("🏰 歷史重點", "英國歷史最重要嘅英文詞彙係咩？幫我做中英對照表。"),
            ("🗳️ 政府制度", "英國政府制度嘅重要英文詞彙，考試最常考哪幾個？"),
            ("📅 備考計劃", "俾我一個4星期備考計劃，附英文詞彙學習安排。"),
            ("🎯 英文詞彙", "Life in UK考試最常出現嘅重要英文詞彙係咩？"),
            ("🌍 英聯邦", "Commonwealth相關嘅英文詞彙同知識點，幫我整理。"),
        ]
        for i, (label, q) in enumerate(quick_qs):
            with quick_cols[i % 3]:
                if st.button(label, key=f"quick_{i}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": q})
                    st.rerun()

    if prompt_input := st.chat_input("用廣東話問我問題…"):
        st.session_state.chat_history.append({"role": "user", "content": prompt_input})
        st.rerun()

    if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
        system = """你係一個專為香港移英人士（50歲以上）設計嘅 Life in the UK Test 備考助手。

核心原則：考試係英文作答，所以每次回答都要：
1. 廣東話解釋（易明易記）
2. 提供相關英文考試術語（要準確，用**粗體**標示）
3. 盡量列出中英對照詞彙
4. 提供記憶技巧（口訣、縮寫、故事）
5. 用香港人熟悉嘅例子作比喻

考試基本資料：24題、45分鐘、答對18題（75%）合格、費用£50"""

        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            with st.chat_message("assistant"):
                with st.spinner("思考中…"):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        max_tokens=1200,
                        messages=[{"role": "system", "content": system}] +
                                 [{"role": m["role"], "content": m["content"]}
                                  for m in st.session_state.chat_history]
                    )
                    reply = response.choices[0].message.content
                    st.markdown(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"AI 連線問題：{e}")

    if st.session_state.chat_history:
        if st.button("🗑️ 清除對話 Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
