import streamlit as st
###
import os, json, tempfile, streamlit as st


from deep_translator import GoogleTranslator
##as sir metioned
import speech_recognition as sr
##for audio
from langdetect import detect, DetectorFactory
##en or ar and viseversa
from google.cloud import translate_v2 as translate
##api
import os
##input ot output
import time

try:
    from pydub import AudioSegment
    pydub_available = True
except ImportError:
    pydub_available = False

# Set deterministic language detection for beter GUESS
DetectorFactory.seed = 0


st.set_page_config(
    page_title=" Arabic-English Translator",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .main {
        font-family: 'Poppins', sans-serif;
            color:black;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Card styling */
    .translator-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid #e1e8ed;
        margin-bottom: 1.5rem;
    }
    
    /* Language indicator */
    .language-badge {
        display: inline-block;
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    /* Translation output styling */
    .translation-output {
        background: linear-gradient(135deg, #e3f2fd, #f3e5f5);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        font-size: 1.1rem;
        line-height: 1.6;
            color:black;
    }
    
    /* Comparison cards */
    .comparison-container {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .translation-card {
        flex: 1;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid transparent;
        transition: all 0.3s ease;
            color:black;
    }
    
    .deep-translator-card {
        background: linear-gradient(135deg, #a8edea, #fed6e3);
        border-color: #667eea;
               color:black;
    }
    
    .google-translator-card {
        background: linear-gradient(135deg, #ffecd2, #fcb69f);
        border-color: #764ba2;
               color:black;
    }
    
    .translation-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* File uploader styling */
    .uploadedFile {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: linear-gradient(135deg, #f8f9ff, #fff);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #667eea, #764ba2);
    }
    
    /* Progress bar */
    .progress-container {
        background: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Feature highlights */
    .feature-box {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    /* Status messages */
    .status-success {
        background: linear-gradient(135deg, #56c596, #3dd5f3);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #ffa726, #ff7043);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Audio visualization */
    .audio-indicator {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 5px;
        margin: 1rem 0;
    }
    
    .audio-bar {
        width: 4px;
        height: 20px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 2px;
        animation: audioWave 1s ease-in-out infinite alternate;
    }
    
    @keyframes audioWave {
        0% { height: 10px; }
        100% { height: 30px; }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="main-header">
    <div class="main-title">Arabic ↔ English Translator</div>
    <div class="main-subtitle">Advanced AI-Powered Translation with Speech Recognition</div>
</div>
""", unsafe_allow_html=True)


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>🔤 Text Translation</h3>
        <p>Instant text translation with AI accuracy</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h3>🎤 Speech Recognition</h3>
        <p>Convert audio to text and translate</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h3>🧠 Auto-Detection</h3>
        <p>Automatic language detection</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-box">
        <h3>⚡ Dual Validation</h3>
        <p>Compare multiple translation engines</p>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.2)); 
           padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem;">
    <h2 style="color: white; text-align: center; margin-bottom: 1rem;">📖 Instructions</h2>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
###  Text Mode
- Enter Arabic or English text
- Click **Translate Text** button
- View dual translation results

### Audio Mode  
- Upload WAV/MP3 file
- Clear speech recommended
- Supports Arabic & English

### Features
- **Auto-detection** using advanced AI
- **Dual validation** with Google API
- **Real-time** translation
- **High accuracy** results
""")




input_mode = st.radio(
    " Choose your input method:",
    ["Text Translation", " Audio Translation"],
    horizontal=True
)

if input_mode == "Text Translation":
    st.markdown("""
    <div class="translator-card"><h3 style="margin-bottom: 1rem; color: #667eea;">Enter Text to Translate</h3></div>
    """, unsafe_allow_html=True)
    
    text_input = st.text_area(
        "",
        placeholder="Type",
        height=120,
        help="Support for both Arabic and English text"
    )
    

    if st.button("Translate Text", key="translate_btn"):
        if not text_input.strip():
            st.markdown("""
            <div class="status-warning">
                 Please enter some text to translate.
            </div>
            """, unsafe_allow_html=True)
        else:
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
        
            status_text.text("Detecting language...")
            progress_bar.progress(20)
    
            try:
                lang_code = detect(text_input)
                time.sleep(0.5)  
            except Exception as e:
                st.error(f"Language detection error: {e}")
                lang_code = None

            if lang_code:
                
                if lang_code.startswith('ar'):
                    source_lang, target_lang = 'ar', 'en'
                    lang_display = "Arabic → English"
                    flag_emoji = "🇸🇦 → 🇺🇸"
                else:
                    source_lang, target_lang = 'en', 'ar'
                    lang_display = "English → Arabic"
                    flag_emoji = "🇺🇸 → 🇸🇦"
                
                st.markdown(f"""
                <div class="language-badge">
                    {flag_emoji} Detected: {lang_display}
                </div>
                """, unsafe_allow_html=True)
            else:
                source_lang, target_lang = 'en', 'ar'
                lang_display = "English → Arabic (Default)"

        
            status_text.text("Initializing translator...")
            progress_bar.progress(40)
            
            try:
                translator = GoogleTranslator(source=source_lang, target=target_lang)
                time.sleep(0.3)
            except Exception as e:
                st.error(f"Translator initialization failed: {e}")
                translator = None

            if translator:
                
                status_text.text("Translating text...")
                progress_bar.progress(70)
                
                paras = [p for p in text_input.splitlines() if p.strip()]
                
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div class="translation-card deep-translator-card">
                        <h4 style="margin-bottom: 1rem; color: #667eea;">Deep Translator</h4>
                    """, unsafe_allow_html=True)
                    
                    for para in paras:
                        try:
                            translated_para = translator.translate(para)
                            st.markdown(f"""
                            <div class="translation-output">
                                {translated_para}
                            </div>
                            """, unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Translation error: {e}")
                    
                    st.markdown("</div>", unsafe_allow_html=True)

            
                status_text.text("Validating with Google API...")
                progress_bar.progress(90)
                
                with col2:
                    st.markdown("""
                    <div class="translation-card google-translator-card">
                        <h4 style="margin-bottom: 1rem; color: black;"> Google Translate</h4>
                    """, unsafe_allow_html=True)
                    
                    try:
                        client = translate.Client()
                        for para in paras:
                            try:
                                result = client.translate(para, target_language=target_lang, format_='text')
                                google_text = result.get('translatedText', '')
                                st.markdown(f"""
                                <div class="translation-output">
                                    {google_text}
                                </div>
                                """, unsafe_allow_html=True)
                            except Exception as e:
                                st.error(f"Google API error: {e}")
                    except Exception as e:
                        st.markdown(f"""
                        <div class="translation-output">
                            Google Cloud API not available: {e}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)

            
            progress_bar.progress(100)
            status_text.text("✅ Translation completed!")
            time.sleep(1)
            progress_bar.empty()
            status_text.empty()

elif input_mode == " Audio Translation":
    st.markdown("""
    <div class="translator-card">
        <h3 style="margin-bottom: 1rem; color: #667eea;"> Upload Audio for Translation</h3>
        <p style="color: #666; margin-bottom: 1rem;">Supported formats: WAV, MP3 | Recommended: Clear speech, minimal background noise</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose audio file",
        type=["wav", "mp3"],
        help="Upload a clear audio file with speech in Arabic or English"
    )
    
    if uploaded_file is not None:
        
        file_size = len(uploaded_file.getvalue()) / 1024 / 1024  # Size in MB
        st.markdown(f"""
        <div class="status-success">
            **File uploaded:** {uploaded_file.name}<br>
            **Size:** {file_size:.2f} MB<br>
            **Type:** {uploaded_file.type}
        </div>
        """, unsafe_allow_html=True)
        
    
        st.markdown("""
        <div class="audio-indicator">
            <div class="audio-bar" style="animation-delay: 0s;"></div>
            <div class="audio-bar" style="animation-delay: 0.1s;"></div>
            <div class="audio-bar" style="animation-delay: 0.2s;"></div>
            <div class="audio-bar" style="animation-delay: 0.3s;"></div>
            <div class="audio-bar" style="animation-delay: 0.4s;"></div>
            <span style="margin-left: 10px; color: #667eea; font-weight: 500;">Audio Ready</span>
        </div>
        """, unsafe_allow_html=True)
    
    if uploaded_file is not None and st.button("Translate Audio", key="audio_btn"):
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        
        status_text.text("Processing audio file...")
        progress_bar.progress(10)
        
        ext = uploaded_file.name.split('.')[-1].lower()
        temp_path = f"temp_input.{ext}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        
        if ext == "mp3":
            status_text.text("Converting MP3 to WAV...")
            progress_bar.progress(25)
            
            if pydub_available:
                try:
                    sound = AudioSegment.from_mp3(temp_path)
                    wav_path = "temp_audio.wav"
                    sound.export(wav_path, format="wav")
                    audio_file = sr.AudioFile(wav_path)
                except Exception as e:
                    st.error(f"❌ Audio conversion failed: {e}")
                    audio_file = sr.AudioFile(temp_path)
            else:
                st.markdown("""
                <div class="status-warning">
                     pydub not available; using MP3 directly (may have issues)
                </div>
                """, unsafe_allow_html=True)
                audio_file = sr.AudioFile(temp_path)
        else:
            audio_file = sr.AudioFile(temp_path)

    
        status_text.text("🎧 Recognizing speech...")
        progress_bar.progress(50)
        
        recognizer = sr.Recognizer()
        with audio_file as source:
            try:
                audio_data = recognizer.record(source)
                time.sleep(0.5)
            except Exception as e:
                st.error(f" Audio processing failed: {e}")
                audio_data = None

        recognized_text = ""
        if audio_data:
            status_text.text("Converting speech to text...")
            progress_bar.progress(75)
            
            try:
                recognized_text = recognizer.recognize_google(audio_data)
                time.sleep(0.5)
            except sr.UnknownValueError:
                st.markdown("""
                <div class="status-warning">
                    Could not understand the audio speech. Please try with clearer audio.
                </div>
                """, unsafe_allow_html=True)
            except sr.RequestError as e:
                st.error(f"🌐 Speech Recognition API error: {e}")

        if recognized_text:
            
            st.markdown(f"""
            <div class="translator-card">
                <h4 style="color: #667eea; margin-bottom: 1rem;">🎯 Recognized Speech</h4>
                <div class="translation-output">
                    {recognized_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

            
            status_text.text("🔍 Detecting language and translating...")
            progress_bar.progress(90)
            
            try:
                lang_code = detect(recognized_text)
            except Exception as e:
                st.error(f"Language detection error: {e}")
                lang_code = None

            if lang_code:
                if lang_code.startswith('ar'):
                    source_lang, target_lang = 'ar', 'en'
                    lang_display = "Arabic → English"
                    flag_emoji = "🇸🇦 → 🇺🇸"
                else:
                    source_lang, target_lang = 'en', 'ar'
                    lang_display = "English → Arabic"
                    flag_emoji = "🇺🇸 → 🇸🇦"
                
                st.markdown(f"""
                <div class="language-badge">
                    {flag_emoji} Detected: {lang_display}
                </div>
                """, unsafe_allow_html=True)
            else:
                source_lang, target_lang = 'en', 'ar'


            translator = GoogleTranslator(source=source_lang, target=target_lang)
            paras = [p for p in recognized_text.splitlines() if p.strip()]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="translation-card deep-translator-card">
                    <h4 style="margin-bottom: 1rem; color: #667eea;">🧠 Deep Translator</h4>
                """, unsafe_allow_html=True)
                
                for para in paras:
                    try:
                        trans_para = translator.translate(para)
                        st.markdown(f"""
                        <div class="translation-output">
                            {trans_para}
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Translation error: {e}")
                
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div class="translation-card google-translator-card">
                    <h4 style="margin-bottom: 1rem; color: #764ba2;">🌐 Google Translate</h4>
                """, unsafe_allow_html=True)
                
                try:
                    client = translate.Client()
                    for para in paras:
                        try:
                            result = client.translate(para, target_language=target_lang, format_='text')
                            google_text = result.get('translatedText', '')
                            st.markdown(f"""
                            <div class="translation-output">
                                {google_text}
                            </div>
                            """, unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Google API error: {e}")
                except Exception as e:
                    st.markdown(f"""
                    <div class="translation-output">
                        ⚠️ Google Cloud API not available: {e}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

        # Cleanup
        progress_bar.progress(100)
        status_text.text("🧹 Cleaning up temporary files...")
        time.sleep(0.5)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if ext == "mp3" and os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")
            
        progress_bar.empty()
        status_text.empty()


st.markdown("""
---
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea, #764ba2); 
           border-radius: 15px; color: white; margin-top: 2rem;">
    <h3 style="margin-bottom: 1rem;">Advanced Translation Technology</h3>
    <p style="margin-bottom: 0.5rem;">Powered by Google Translate API & Deep Translator</p>
    <p style="margin-bottom: 0; opacity: 0.8;">Built with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)


st.sidebar.markdown("""
---
###  Technical Notes
**DetectorFactory.seed = 0** ensures:
- Consistent language detection results
- Reproducible behavior across runs
- Eliminates randomness in detection
- Better reliability for the same input
""")
