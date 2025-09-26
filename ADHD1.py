# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="Parent ADHD Screening", layout="centered")

# --- Language selection ---
lang = st.sidebar.selectbox(
    "Select Language / भाषा चुनें / ਭਾਸ਼ਾ ਚੁਣੋ",
    ["English", "हिन्दी", "ਪੰਜਾਬੀ"]
)

# --- Translations ---
TEXTS = {
    "English": {
        "title": "ADHD Screening Questionnaire (Parent Version)",
        "instructions": "Please rate your child’s behavior over the past 6 months.",
        "inattention": "Inattention Symptoms",
        "hyper": "Hyperactivity & Impulsivity Symptoms",
        "results": "📊 Screening Results",
        "interpret": "Interpretation",
        "download": "📥 Download Responses",
        "score_label": "Total Score",
        "interpret_low": "Likely typical behavior (no ADHD symptoms).",
        "interpret_mid": "Some ADHD-like traits present. Monitoring recommended.",
        "interpret_high": "High number of ADHD symptoms. Clinical evaluation recommended.",
    },
    "हिन्दी": {
        "title": "एडीएचडी स्क्रीनिंग प्रश्नावली (माता-पिता संस्करण)",
        "instructions": "कृपया पिछले 6 महीनों में अपने बच्चे के व्यवहार को रेट करें।",
        "inattention": "ध्यान की कमी से संबंधित लक्षण",
        "hyper": "अत्यधिक सक्रियता और आवेगशीलता के लक्षण",
        "results": "📊 परिणाम",
        "interpret": "व्याख्या",
        "download": "📥 उत्तर डाउनलोड करें",
        "score_label": "कुल स्कोर",
        "interpret_low": "सामान्य व्यवहार (एडीएचडी के लक्षण नहीं)।",
        "interpret_mid": "कुछ एडीएचडी जैसे लक्षण मौजूद हैं। निगरानी की सलाह दी जाती है।",
        "interpret_high": "एडीएचडी के लक्षणों की संख्या अधिक है। क्लिनिकल मूल्यांकन की आवश्यकता है।",
    },
    "ਪੰਜਾਬੀ": {
        "title": "ADHD ਸਕ੍ਰੀਨਿੰਗ ਪ੍ਰਸ਼ਨਾਵਲੀ (ਮਾਪਿਆਂ ਲਈ)",
        "instructions": "ਕਿਰਪਾ ਕਰਕੇ ਪਿਛਲੇ 6 ਮਹੀਨਿਆਂ ਵਿੱਚ ਆਪਣੇ ਬੱਚੇ ਦੇ ਵਿਵਹਾਰ ਨੂੰ ਦਰਜ ਕਰੋ।",
        "inattention": "ਧਿਆਨ ਦੀ ਘਾਟ ਦੇ ਲੱਛਣ",
        "hyper": "ਅਤਿਅਧਿਕ ਸਰਗਰਮੀ ਅਤੇ ਜਜ਼ਬਾਤੀ ਲੱਛਣ",
        "results": "📊 ਨਤੀਜੇ",
        "interpret": "ਵਿਆਖਿਆ",
        "download": "📥 ਜਵਾਬ ਡਾਊਨਲੋਡ ਕਰੋ",
        "score_label": "ਕੁੱਲ ਸਕੋਰ",
        "interpret_low": "ਸਧਾਰਣ ਵਿਵਹਾਰ (ADHD ਦੇ ਲੱਛਣ ਨਹੀਂ)।",
        "interpret_mid": "ਕੁਝ ADHD ਵਰਗੇ ਲੱਛਣ ਮੌਜੂਦ ਹਨ। ਨਿਗਰਾਨੀ ਦੀ ਲੋੜ ਹੈ।",
        "interpret_high": "ADHD ਦੇ ਲੱਛਣ ਵੱਧ ਹਨ। ਕਲੀਨਿਕਲ ਮੁਲਾਂਕਣ ਦੀ ਸਿਫ਼ਾਰਸ਼ ਹੈ।",
    },
}

QUESTIONS = {
    "English": {
        "inattention": [
            "Makes careless mistakes or doesn’t pay close attention to details.",
            "Has trouble sustaining attention in tasks or play.",
            "Doesn’t seem to listen when spoken to directly.",
            "Doesn’t follow instructions or finish tasks.",
            "Has trouble organizing tasks and activities.",
            "Avoids or dislikes tasks requiring mental effort.",
            "Often loses things (books, pencils, toys).",
            "Easily distracted by outside stimuli.",
            "Forgetful in daily activities.",
        ],
        "hyper": [
            "Fidgets or squirms in seat.",
            "Leaves seat when expected to remain seated.",
            "Runs or climbs in inappropriate situations.",
            "Unable to play quietly.",
            "Acts as if 'driven by a motor'.",
            "Talks excessively.",
            "Blurts out answers before questions are finished.",
            "Has trouble waiting turn.",
            "Interrupts or intrudes on others.",
        ],
    },
    "हिन्दी": {
        "inattention": [
            "लापरवाही से गलतियाँ करता है या विवरण पर ध्यान नहीं देता।",
            "काम या खेल में ध्यान बनाए रखने में कठिनाई होती है।",
            "सीधे बात करने पर भी नहीं सुनता लगता है।",
            "निर्देशों का पालन नहीं करता या कार्य पूरे नहीं करता।",
            "कार्यों और गतिविधियों को व्यवस्थित करने में कठिनाई होती है।",
            "मानसिक प्रयास वाले कार्यों से बचता है।",
            "अक्सर चीजें खो देता है (किताबें, पेंसिल, खिलौने)।",
            "बाहरी चीजों से आसानी से विचलित हो जाता है।",
            "दैनिक गतिविधियों में भूल जाता है।",
        ],
        "hyper": [
            "बैठे-बैठे हिलता-डुलता है।",
            "जब बैठना चाहिए तब सीट छोड़ देता है।",
            "अनुचित स्थितियों में दौड़ता या चढ़ता है।",
            "शांतिपूर्वक खेल नहीं सकता।",
            "हमेशा सक्रिय रहता है जैसे मोटर चला रही हो।",
            "बहुत अधिक बोलता है।",
            "प्रश्न पूरा होने से पहले ही उत्तर दे देता है।",
            "अपनी बारी का इंतजार करने में कठिनाई होती है।",
            "दूसरों की बात काट देता है या बीच में टोकता है।",
        ],
    },
    "ਪੰਜਾਬੀ": {
        "inattention": [
            "ਲਾਪਰਵਾਹੀ ਨਾਲ ਗਲਤੀਆਂ ਕਰਦਾ ਹੈ ਜਾਂ ਵੇਰਵਿਆਂ ਤੇ ਧਿਆਨ ਨਹੀਂ ਦਿੰਦਾ।",
            "ਕੰਮ ਜਾਂ ਖੇਡ ਵਿੱਚ ਧਿਆਨ ਬਣਾਈ ਰੱਖਣ ਵਿੱਚ ਮੁਸ਼ਕਲ ਹੁੰਦੀ ਹੈ।",
            "ਸਿੱਧਾ ਗੱਲ ਕਰਨ 'ਤੇ ਵੀ ਨਹੀਂ ਸੁਣਦਾ।",
            "ਨਿਰਦੇਸ਼ਾਂ ਦੀ ਪਾਲਣਾ ਨਹੀਂ ਕਰਦਾ ਜਾਂ ਕੰਮ ਪੂਰਾ ਨਹੀਂ ਕਰਦਾ।",
            "ਕੰਮਾਂ ਅਤੇ ਗਤੀਵਿਧੀਆਂ ਨੂੰ ਸੁਧਾਰਨ ਵਿੱਚ ਮੁਸ਼ਕਲ ਹੁੰਦੀ ਹੈ।",
            "ਮਾਨਸਿਕ ਯਤਨ ਵਾਲੇ ਕੰਮਾਂ ਤੋਂ ਬਚਦਾ ਹੈ।",
            "ਅਕਸਰ ਚੀਜ਼ਾਂ ਗੁਆ ਲੈਂਦਾ ਹੈ (ਕਿਤਾਬਾਂ, ਪੈਨਸਿਲਾਂ, ਖਿਡੌਣੇ)।",
            "ਬਾਹਰੀ ਚੀਜ਼ਾਂ ਨਾਲ ਅਸਾਨੀ ਨਾਲ ਧਿਆਨ ਭੰਗ ਕਰ ਲੈਂਦਾ ਹੈ।",
            "ਰੋਜ਼ਾਨਾ ਕਾਰਜਾਂ ਵਿੱਚ ਭੁੱਲ ਜਾਂਦਾ ਹੈ।",
        ],
        "hyper": [
            "ਬੈਠਿਆਂ ਹਿਲਦਾ-ਡੁੱਲਦਾ ਹੈ।",
            "ਜਦੋਂ ਬੈਠਣਾ ਚਾਹੀਦਾ ਹੈ ਉਸ ਵੇਲੇ ਸੀਟ ਛੱਡ ਦਿੰਦਾ ਹੈ।",
            "ਗਲਤ ਸਮੇਂ ਦੌੜਦਾ ਜਾਂ ਚੜ੍ਹਦਾ ਹੈ।",
            "ਸ਼ਾਂਤੀ ਨਾਲ ਖੇਡ ਨਹੀਂ ਸਕਦਾ।",
            "ਹਮੇਸ਼ਾਂ ਸਰਗਰਮ ਰਹਿੰਦਾ ਹੈ ਜਿਵੇਂ ਮੋਟਰ ਚਲਾ ਰਹੀ ਹੋਵੇ।",
            "ਬਹੁਤ ਜ਼ਿਆਦਾ ਬੋਲਦਾ ਹੈ।",
            "ਪ੍ਰਸ਼ਨ ਪੂਰਾ ਹੋਣ ਤੋਂ ਪਹਿਲਾਂ ਹੀ ਜਵਾਬ ਦੇ ਦਿੰਦਾ ਹੈ।",
            "ਆਪਣੀ ਵਾਰੀ ਦੀ ਉਡੀਕ ਕਰਨ ਵਿੱਚ ਮੁਸ਼ਕਲ ਹੁੰਦੀ ਹੈ।",
            "ਹੋਰਾਂ ਦੀ ਗੱਲ ਵਿਚਕਾਰ ਕੱਟ ਦਿੰਦਾ ਹੈ।",
        ],
    },
}

# --- Scale labels ---
scale_options = {
    0: {"English": "0 — Never or Rarely", "हिन्दी": "0 — कभी नहीं / बहुत कम", "ਪੰਜਾਬੀ": "0 — ਕਦੇ ਨਹੀਂ / ਬਹੁਤ ਘੱਟ"},
    1: {"English": "1 — Sometimes", "हिन्दी": "1 — कभी-कभी", "ਪੰਜਾਬੀ": "1 — ਕਦੇ-ਕਦੇ"},
    2: {"English": "2 — Often", "हिन्दी": "2 — अक्सर", "ਪੰਜਾਬੀ": "2 — ਅਕਸਰ"},
    3: {"English": "3 — Very Often", "हिन्दी": "3 — बहुत बार", "ਪੰਜਾਬੀ": "3 — ਬਹੁਤ ਵਾਰ"},
}

# --- UI ---
st.title(TEXTS[lang]["title"])
st.write(TEXTS[lang]["instructions"])

responses = {}

# Inattention
st.subheader(TEXTS[lang]["inattention"])
for i, q in enumerate(QUESTIONS[lang]["inattention"], 1):
    responses[f"Inattention {i}"] = st.radio(
        q, [scale_options[x][lang] for x in range(4)], horizontal=True, key=f"inatt_{i}"
    )

# Hyperactivity/Impulsivity
st.subheader(TEXTS[lang]["hyper"])
for i, q in enumerate(QUESTIONS[lang]["hyper"], 1):
    responses[f"Hyperactivity {i}"] = st.radio(
        q, [scale_options[x][lang] for x in range(4)], horizontal=True, key=f"hyper_{i}"
    )

# Submit
if st.button("Submit / सबमिट / ਜਮ੍ਹਾਂ ਕਰੋ"):
    # convert responses to numeric
    scores = []
    for ans in responses.values():
        for k, v in scale_options.items():
            if v[lang] == ans:
                scores.append(k)
    total_score = sum(scores)

    st.subheader(TEXTS[lang]["results"])
    st.metric(TEXTS[lang]["score_label"], total_score)

    st.subheader(TEXTS[lang]["interpret"])
    if total_score <= 12:
        st.success(TEXTS[lang]["interpret_low"])
    elif total_score <= 24:
        st.warning(TEXTS[lang]["interpret_mid"])
    else:
        st.error(TEXTS[lang]["interpret_high"])

    # Save to CSV
    df = pd.DataFrame([responses])
    df["Total Score"] = total_score
    df["Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button(
        label=TEXTS[lang]["download"],
        data=csv_buffer.getvalue(),
        file_name="adhd_screening.csv",
        mime="text/csv",
    )
