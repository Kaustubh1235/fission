import streamlit as st
from googletrans import Translator
from google.cloud import translate_v2 as gct

# objects
translator = Translator()
cloud = gct.Client()

# config
st.set_page_config(page_title="EN ↔ AR Translator", page_icon="🔄", layout="centered")

# UI language selector
ui_lang = st.sidebar.radio("🌐 Select Page Language / اختر لغة الصفحة", ["English", "العربية"], index=0)

# labels
LABELS = {
    "English": {
        "title": "English ↔ Arabic Translator ",
        "prompt": "Enter text in any language:",
        "translate": "Translate",
        "detected": "Detected",
        "to": "to",
        "gt": "googletrans result",
        "gc": "Google Cloud result",
        "error": "Only English and Arabic are supported as target languages.",
        "target": "Target language",
        "lang_options": ["English", "Arabic"],
        "caption": "googletrans (unofficial) · Google Cloud Translation (official). Set GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_API_KEY for Cloud access."
    },
    "العربية": {
        "title": "مترجم عربي ↔ إنجليزي 📝",
        "prompt": "أدخل نصًا بأي لغة:",
        "translate": "ترجمة",
        "detected": "اكتُشِف",
        "to": "إلى",
        "gt": "نتيجة googletrans",
        "gc": "نتيجة Google Cloud",
        "error": "يُسمح بالترجمة إلى الإنجليزية أو العربية فقط.",
        "target": "اللغة الهدف",
        "lang_options": ["الإنجليزية", "العربية"],
        "caption": "googletrans (غير رسمي) · ترجمة Google Cloud (رسمية). قم بتعيين GOOGLE_APPLICATION_CREDENTIALS أو GOOGLE_API_KEY للوصول إلى Google Cloud."
    }
}
T = LABELS[ui_lang]

st.title(T["title"])
text = st.text_area(T["prompt"], height=120)
target_choice = st.radio(T["target"], T["lang_options"], horizontal=True)
lang_map = {
    "English": "en",
    "Arabic": "ar",
    "الإنجليزية": "en",
    "العربية": "ar"
}


if st.button(T["translate"]) and text.strip():
    try:
      
        src_lang = translator.detect(text).lang

      
        target_lang = lang_map.get(target_choice, "en")

        if src_lang == target_lang:
            st.warning("Source and target languages are the same. No translation needed.")
            st.stop()

        st.write(f"{T['detected']}: **{src_lang}** {T['to']} **{target_lang}**")

      
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(T["gt"])
            try:
                gt_text = translator.translate(text, src=src_lang, dest=target_lang).text
                st.write(gt_text)
            except Exception as e:
                st.error(f"googletrans error: {e}")

        with col2:
            st.subheader(T["gc"])
            try:
                gc_text = cloud.translate(
                    text, source_language=src_lang, target_language=target_lang
                )["translatedText"]
                st.write(gc_text)
            except Exception as e:
                st.error(f"Google Cloud error: {e}")

    except Exception as e:
        st.error(f"Language detection failed: {e}")

st.caption(T["caption"])
