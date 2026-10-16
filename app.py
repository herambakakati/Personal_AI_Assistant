# ============================================================
# AI PERSONAL ASSISTANT
# Premium Bright UI | Streamlit | LangChain Agents
# ============================================================

import os
import streamlit as st
from dotenv import load_dotenv
from tools import check_due_reminders
import streamlit.components.v1 as components

# ============================================================
# ENVIRONMENT CONFIGURATION
# ============================================================

# Load environment variables BEFORE importing the agent
load_dotenv()

from agent import create_personal_agent

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Personal Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# PREMIUM UI STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       GLOBAL THEME
    -------------------------------------------------------- */

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    :root {
        --primary: #0078FF;
        --secondary: #4F46E5;
        --accent: #00C6FF;
        --background: #F4F8FF;
        --text: #172554;
        --muted: #64748B;
        --card: #FFFFFF;
        --border: #E2EAF5;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ============================================================
   FULL-PAGE BACKGROUND BANNER
   ============================================================ */

    .stApp {
        background-image:
            linear-gradient(
                115deg,
                rgba(244, 248, 255, 0.70) 0%,
                rgba(239, 246, 255, 0.60) 48%,
                rgba(245, 243, 255, 0.70) 100%
            ),
            radial-gradient(
                circle at 8% 12%,
                rgba(0, 198, 255, 0.12),
                transparent 32%
            ),
            radial-gradient(
                circle at 92% 18%,
                rgba(79, 70, 229, 0.10),
                transparent 34%
            ),
            url(
               "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=2400&q=85"
            );

        background-size: cover, cover, cover, cover;
        background-position: center, center, center, center;
        background-repeat: no-repeat;
        background-attachment: fixed;

        color: var(--text);
    }

    /* Keep the main page transparent so the background remains visible. */

    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        background: transparent !important;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1rem;
        padding-bottom: 0.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Hide Streamlit header and unnecessary decorations */

    [data-testid="stHeader"] {
        display: none !important;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    /* Remove the space previously occupied by the header */

    [data-testid="stAppViewBlockContainer"] {
        padding-top: 1rem !important;
    }

    /* --------------------------------------------------------
       HERO BANNER
    -------------------------------------------------------- */

    .hero-banner {
        position: relative;
        overflow: hidden;
        isolation: isolate;
        padding: 44px 42px;
        border-radius: 26px;
        margin-bottom: 28px;

        background-image:
            linear-gradient(
                110deg,
                rgba(0, 91, 220, 0.94),
                rgba(37, 99, 235, 0.90) 48%,
                rgba(79, 70, 229, 0.82)
            ),
            url(
                "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1800&q=85"
            );

        background-size: cover;
        background-position: center;

        box-shadow:
            0 18px 45px rgba(37, 99, 235, 0.18);
    }

    .hero-banner::before {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        top: -115px;
        right: 8%;
        border-radius: 50%;
        border: 1px solid rgba(255, 255, 255, 0.22);
        z-index: -1;
    }

    .hero-banner::after {
        content: "";
        position: absolute;
        width: 190px;
        height: 190px;
        bottom: -125px;
        right: 22%;
        border-radius: 50%;
        background: rgba(0, 198, 255, 0.20);
        filter: blur(3px);
        z-index: -1;
    }

    .hero-badge {
        display: inline-block;
        padding: 8px 14px;
        margin-bottom: 17px;

        background: rgba(255, 255, 255, 0.16);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 30px;

        color: #FFFFFF;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.3px;
        text-transform: uppercase;
    }

    .hero-title {
        color: #FFFFFF !important;
        font-size: clamp(32px, 4vw, 48px);
        line-height: 1.16;
        font-weight: 800;
        letter-spacing: -1.6px;
        margin: 0 0 16px 0;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
    }

    .hero-subtitle {
        color: #FFFFFF !important;
        font-size: 16px;
        line-height: 1.9;
        max-width: 760px;
        margin: 0;
        text-shadow: 0 1px 5px rgba(0, 0, 0, 0.12);
    }

    .hero-footer {
        margin-top: 24px;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }

    .hero-tag {
        display: inline-block;
        padding: 8px 13px;
        border-radius: 10px;

        background: rgba(255, 255, 255, 0.14);
        border: 1px solid rgba(255, 255, 255, 0.18);

        color: #FFFFFF;
        font-size: 12px;
        font-weight: 600;
    }

    /* --------------------------------------------------------
       SECTION HEADINGS
    -------------------------------------------------------- */

    .section-heading {
        font-size: 25px;
        font-weight: 800;
        color: #0B1F44 !important;
        letter-spacing: -0.5px;
        margin: 8px 0 8px 0;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.75);
    }

    .section-description {
        font-size: 17px;
        font-weight: 500;
        line-height: 1.8;
        color: #0B1F44 !important;
        margin-bottom: 18px;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.85);
    }

    /* --------------------------------------------------------
       FEATURE CARDS
    -------------------------------------------------------- */

    .feature-card {
        display: flex;
        align-items: center;
        gap: 12px;

        height: 85px;
        padding: 10px 13px;
        margin-bottom: 6px;

        background: linear-gradient(
            145deg,
            #FFFFFF,
            #F8FBFF
        );

        border: 1px solid #E3ECF8;
        border-radius: 14px;

        box-shadow: 0 3px 10px rgba(31, 64, 120, 0.04);

        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease,
            border-color 0.25s ease;
    }

    .feature-card:hover {
        transform: translateY(-4px);
        border-color: #B8D5FF;

        box-shadow:
            0 13px 28px rgba(37, 99, 235, 0.10);
    }

    .feature-icon {
        width: 32px;
        height: 32px;
        flex-shrink: 0;

        display: flex;
        align-items: center;
        justify-content: center;

        background: linear-gradient(
            135deg,
            #EAF3FF,
            #DDF8FF
        );

        border-radius: 9px;
        font-size: 18px;
        margin-bottom: 0;
    }

    .feature-content {
        flex: 1;
        min-width: 0;
    }

    .feature-title {
        color: #1E3A8A;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .feature-description {
        color: #64748B;
        font-size: 11px;
        line-height: 1.5;
        overflow-wrap: anywhere;
    }

    /* --------------------------------------------------------
       CHAT AREA
    -------------------------------------------------------- */

    /* Clean inline chat input */

    [data-testid="stForm"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin-top: 12px !important;
        margin-bottom: 12px !important;
        box-shadow: none !important;
    }

    [data-testid="stForm"] input {
        background: #FFFFFF !important;
        color: #172554 !important;
        border: 1px solid #D9E5F5 !important;
        border-radius: 14px !important;
        min-height: 44px;
    }

    /* Light grey placeholder text */
    [data-testid="stForm"] input::placeholder {
        color: #B0BAC9 !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #B0BAC9 !important;
    }

    /* Keep user-entered text dark and readable */
    [data-testid="stForm"] input {
        color: #172554 !important;
        -webkit-text-fill-color: #172554 !important;
    }

    [data-testid="stForm"] button {
        min-height: 44px;
        border-radius: 12px;
        background: #2563EB;
        color: #FFFFFF;
        border: none;
        font-weight: 600;
    }

    [data-testid="stForm"] button:hover {
        background: #1D4ED8;
        color: #FFFFFF;
    }

    /* One shared conversation card */

    /* One shared, scrollable conversation card */

    .st-key-conversation {
        background: #FFFFFF;
        border: 1px solid #E2EAF5;
        border-radius: 18px;

        padding: 12px 20px;
        margin: 10px 0 16px 0;

        max-height: 420px;
        overflow-y: auto;
        overflow-x: hidden;

        box-shadow: 0 5px 18px rgba(31, 64, 120, 0.04);
        scroll-behavior: smooth;
    }

    /* Remove individual message cards */

    .st-key-conversation [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;

        padding: 8px 4px !important;
        margin: 0 !important;
    }

    /* Conversation text */

    .st-key-conversation [data-testid="stChatMessage"] p {
        color: #24334D;
        font-size: 14px;
        line-height: 1.7;
    }

    /* Remove individual message cards */

    .st-key-conversation [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        padding: 10px 4px !important;
        margin: 0 !important;
    }

    /* Keep conversation text readable */

    .st-key-conversation [data-testid="stChatMessage"] p {
        color: #24334D;
        font-size: 14px;
        line-height: 1.7;
    }

    [data-testid="stChatMessage"] p {
        color: #24334D;
        font-size: 14px;
        line-height: 1.9;
    }

    [data-testid="stChatInput"] {
        border-radius: 16px;
    }

    [data-testid="stChatInput"] textarea {
        background: #FFFFFF;
        border-radius: 16px;
        border: 1px solid #D9E5F5;
        font-size: 15px;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #60A5FA;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.08);
    }

    /* --------------------------------------------------------
       SIDEBAR
    -------------------------------------------------------- */

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #FFFFFF 0%,
            #F0F7FF 100%
        );

        border-right: 1px solid #E2EAF5;
    }

    /* Reduce sidebar vertical spacing */

    [data-testid="stSidebar"] .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }

    [data-testid="stSidebar"] hr {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }

    [data-testid="stSidebar"] h3 {
        margin-top: 0.3rem !important;
        margin-bottom: 0.2rem !important;
    }

    [data-testid="stSidebar"] h2 {
        color: #1E3A8A;
        font-size: 19px;
        font-weight: 800;
    }

    [data-testid="stSidebar"] h3 {
        color: #2563EB;
        font-size: 15px;
        font-weight: 750;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li {
        color: #475569;
        font-size: 13px;
        line-height: 1.9;
    }

    /* --------------------------------------------------------
       BUTTONS
    -------------------------------------------------------- */

    .stButton > button {
        min-height: 43px;
        border-radius: 12px;

        border: 1px solid #D8E7FA;
        background: #FFFFFF;

        color: #1D4ED8;
        font-weight: 650;
        font-size: 13px;

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: #EFF6FF;
        border-color: #93C5FD;
        color: #1D4ED8;
        transform: translateY(-1px);
    }

    /* --------------------------------------------------------
       STATUS MESSAGES
    -------------------------------------------------------- */

    [data-testid="stAlert"] {
        border-radius: 14px;
    }

    /* ============================================================
    REMINDER NOTIFICATION — CLEAN, HIGH-CONTRAST DESIGN
    ============================================================ */

    [data-testid="stAlert"] {
        background: rgba(255, 255, 255, 0.97) !important;
        border: 1px solid #B8D8FF !important;
        border-left: 5px solid #2563EB !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.10) !important;
    }

    /* Reminder message */
    [data-testid="stAlert"] p {
        color: #102A56 !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        line-height: 1.6 !important;
        opacity: 1 !important;
    }

    /* Scheduled date and time */
    [data-testid="stCaptionContainer"] p {
        color: #334155 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        line-height: 1.6 !important;
        opacity: 1 !important;
    }

    /* Keep reminder content clearly separated */
    [data-testid="stAlert"] + [data-testid="stCaptionContainer"] {
        margin-top: 4px !important;
        margin-bottom: 14px !important;
    }

    /* --------------------------------------------------------
       FOOTER
    -------------------------------------------------------- */

    .app-footer {
        margin-top: 5px;
        padding-top: 5px;
        border-top: 1px solid #DFE8F4;

        text-align: center;
        color: #64748B;

        font-size: 12px;
        line-height: 1.2;
    }

    .footer-brand {
        color: #2563EB;
        font-weight: 800;
    }

    /* --------------------------------------------------------
       RESPONSIVE DESIGN
    -------------------------------------------------------- */

    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
        }

        .hero-banner {
            padding: 28px 22px;
            border-radius: 20px;
        }

        .hero-title {
            font-size: 32px;
            letter-spacing: -0.8px;
        }

        .hero-subtitle {
            font-size: 14px;
        }

        .feature-card {
            height: 100px;
            min-height: 100px;
            padding: 10px;
        }
    }

    /* Hide sidebar for a clean chat interface */
    [data-testid="stSidebar"] {
        display: none !important;
    }

    /* Remove the sidebar collapse control */
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }


    /* ============================================================
    FORCE CHAT TEXT TO BLACK
    ============================================================ */

    /* User questions and AI responses */
    .st-key-conversation [data-testid="stChatMessage"],
    .st-key-conversation [data-testid="stChatMessage"] p,
    .st-key-conversation [data-testid="stChatMessage"] span,
    .st-key-conversation [data-testid="stChatMessage"] div,
    .st-key-conversation [data-testid="stChatMessage"] li,
    .st-key-conversation [data-testid="stChatMessage"] strong,
    .st-key-conversation [data-testid="stChatMessage"] em,
    .st-key-conversation [data-testid="stChatMessage"] h1,
    .st-key-conversation [data-testid="stChatMessage"] h2,
    .st-key-conversation [data-testid="stChatMessage"] h3,
    .st-key-conversation [data-testid="stChatMessage"] h4,
    .st-key-conversation [data-testid="stChatMessage"] h5,
    .st-key-conversation [data-testid="stChatMessage"] h6 {
        color: #000000 !important;
    }

    /* Inline code and code blocks */
    .st-key-conversation [data-testid="stChatMessage"] code,
    .st-key-conversation [data-testid="stChatMessage"] pre {
        color: #000000 !important;
    }

    /* Tables */
    .st-key-conversation [data-testid="stChatMessage"] table,
    .st-key-conversation [data-testid="stChatMessage"] th,
    .st-key-conversation [data-testid="stChatMessage"] td {
        color: #000000 !important;
    }

    /* Links */
    .st-key-conversation [data-testid="stChatMessage"] a {
        color: #000000 !important;
        text-decoration: underline;
    }

    /* ============================================================
    IMPROVE TEXT READABILITY
    ============================================================ */

    /* Main headings */
    h1, h2, h3 {
        color: #102a56 !important;
        font-weight: 750 !important;
        text-shadow: none !important;
    }

    /* Paragraphs and descriptions */
    .stApp p,
    .stApp label,
    .stApp .stMarkdown {
        color: #243b5a;
    }

    /* Section heading and description */
    .stApp h2 {
        color: #102a56 !important;
    }

    .stApp [data-testid="stCaptionContainer"] p {
        color: #425875 !important;
        opacity: 1 !important;
    }

    /* Improve text inside feature cards */
    .feature-card h3,
    .feature-card p {
        color: #173b75 !important;
        text-shadow: none !important;
    }

    /* Chat input text */
    .stChatInput textarea,
    .stTextInput input {
        color: #172b4d !important;
        background-color: #ffffff !important;
        -webkit-text-fill-color: #172b4d !important;
    }

    /* Chat input placeholder */
    .stChatInput textarea::placeholder,
    .stTextInput input::placeholder {
        color: #718096 !important;
        opacity: 1 !important;
    }

    /* Footer readability */
    footer,
    footer p {
        color: #425875 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HERO BANNER
# ============================================================

st.html(
    """
    <div class="hero-banner">

        <div class="hero-badge">
            ✦ YOUR INTELLIGENT DIGITAL COMPANION
        </div>

        <h1 class="hero-title">
            AI Personal Assistant
        </h1>

        <p class="hero-subtitle">
            Your everyday AI companion for quick answers and everyday tasks.
            Check the weather, convert currencies, set reminders, search the web,
            get the current time, and solve math problems - all through simple conversation.
        </p>

        <div class="hero-footer">
            <span class="hero-tag">💬 Ask Questions Naturally</span>
            <span class="hero-tag">⚡ Get Quick Responses</span>
            <span class="hero-tag">🧠 AI-Powered Assistance</span>
            <span class="hero-tag">✨ Simplify Daily Tasks</span>
        </div>

    </div>
    """,
    
)


# ============================================================
# AGENT INITIALIZATION
# ============================================================

@st.cache_resource(show_spinner=False)
def load_personal_agent():
    return create_personal_agent()


# Check API key before initializing the agent
if not os.getenv("OPENAI_API_KEY"):
    st.error(
        "OpenAI API key not found. Please add OPENAI_API_KEY "
        "to your .env file in the project directory."
    )

    st.code(
        "OPENAI_API_KEY=your_actual_openai_api_key",
        language="text"
    )

    st.stop()


try:
    agent = load_personal_agent()

    from datetime import datetime
    import streamlit.components.v1 as components

except Exception as exc:
    st.error(
        "The AI assistant could not be initialized. "
        "Check your API key, package dependencies, and terminal error."
    )

    with st.expander("Technical details"):
        st.code(str(exc))

    st.stop()


# ============================================================
# FEATURE OVERVIEW
# ============================================================

st.html(
    """
    <div class="section-heading">
        Everything You Need, In One Assistant
    </div>

    <div class="section-description">
        Choose a capability below, then ask your question in the
        chat area. You can also use the example questions in the sidebar.
    </div>
    """,
    
)


features = [
    (
        "🌤️",
        "Weather Intelligence",
        "Check weather conditions and forecasts for different locations."
    ),
    (
        "💱",
        "Currency Converter",
        "Convert currencies and check exchange-rate information."
    ),
    (
        "🕒",
        "Time & Date",
        "Get the current date and time for supported locations."
    ),
    (
        "🔔",
        "Smart Reminders",
        "Create reminders and retrieve your saved reminder list."
    ),
    (
        "🌍",
        "Web Search",
        "Find information on people, companies, technology, and more."
    ),
    (
        "🧮",
        "Math Assistant",
        "Calculate expressions and solve supported mathematical problems."
    )
]


feature_columns = st.columns(3, gap="medium")

for index, feature in enumerate(features):

    icon, title, description = feature

    with feature_columns[index % 3]:

        st.html(
            f"""
            <div class="feature-card">

                <div class="feature-icon">
                    {icon}
                </div>

                <div class="feature-content">

                    <div class="feature-title">
                        {title}
                    </div>

                    <div class="feature-description">
                        {description}
                    </div>

                </div>

            </div>
            """
        )

# ============================================================
# AUTOMATIC REMINDER CHECKER — WITHOUT FULL APP REFRESH
# ============================================================

@st.fragment(run_every="5s")
def reminder_panel():

    # Initialize notification storage for this browser session.
    if "due_notifications" not in st.session_state:
        st.session_state.due_notifications = []

    # Check for reminders that have reached their scheduled time.
    due_reminders = check_due_reminders()

    # Store each newly triggered reminder once.
    for reminder in due_reminders:
        st.session_state.due_notifications.append(reminder)

    # Display notifications only when reminders are due.
    for index, reminder in enumerate(
        st.session_state.due_notifications
    ):

        st.warning(
            f"🔔 Reminder: {reminder['task']}",
            icon="🔔"
        )

        st.caption(
            "Scheduled for "
            + reminder["time"].strftime(
                "%d %B %Y, %I:%M %p"
            )
            + " IST"
        )


# Start the independently refreshing reminder section.
reminder_panel()


# ============================================================
# CHAT MEMORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# DISPLAY PREVIOUS CONVERSATION
# ============================================================

if not st.session_state.messages:

    st.html(
        """
        <div style="
            background: linear-gradient(135deg, #FFFFFF, #EFF6FF);
            border: 1px solid #DFEAF8;
            border-radius: 20px;
            padding: 16px 20px;
            text-align: center;
            margin: 4px 0 8px 0;
        ">

            <div style="font-size: 39px; margin-bottom: 4px;">
                💬
            </div>

            <div style="
                color: #1E3A8A;
                font-size: 21px;
                font-weight: 800;
                margin-bottom: 4px;
            ">
                How can I help you today?
            </div>

            <div style="
                color: #64748B;
                font-size: 14px;
                line-height: 1.2;
            ">
                Discover how I can help you work smarter, simplify everyday tasks, and find the information you need.
            </div>

        </div>
        """,
        
    )

# ============================================================
# DISPLAY CONVERSATION ONLY WHEN MESSAGES EXIST
# ============================================================

# Display the latest 5 question-and-answer pairs.
visible_messages = st.session_state.messages[-10:]

# Do not render an empty conversation container.
if visible_messages:

    with st.container(key="conversation", border=True):

        for msg in visible_messages:

            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])


# ============================================================
# CHAT INPUT — INLINE ABOVE FOOTER
# ============================================================

with st.form("chat_form", clear_on_submit=True):

    input_col, button_col = st.columns([8, 1])

    with input_col:
        user_input = st.text_input(
            "Message",
            placeholder="Ask anything... e.g. Convert 100 USD to INR",
            label_visibility="collapsed"
        )

    with button_col:
        submitted = st.form_submit_button(
            "➤ Send",
            use_container_width=True
        )
# ============================================================
# PROCESS USER MESSAGE — RELIABLE RESPONSE HANDLING
# ============================================================

if submitted and user_input and user_input.strip():

    question = user_input.strip()

    # Add the user's question to the conversation.
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    try:
        with st.spinner("Thinking... Please wait."):

            response = agent.invoke({
                "messages": st.session_state.messages
            })

        # Get the messages returned by the agent.
        response_messages = response.get("messages", [])

        # Find the final AI response.
        answer = None

        for message in reversed(response_messages):

            message_type = getattr(message, "type", None)

            # Also support message dictionaries if returned.
            if isinstance(message, dict):
                message_type = message.get("type")
                message_content = message.get("content", "")
                tool_calls = message.get("tool_calls", [])
            else:
                message_content = getattr(message, "content", "")
                tool_calls = getattr(message, "tool_calls", [])

            if message_type in ("ai", "assistant") and not tool_calls:

                # Convert structured content into readable text.
                if isinstance(message_content, list):

                    parts = []

                    for block in message_content:

                        if isinstance(block, dict):
                            if block.get("type") == "text":
                                parts.append(block.get("text", ""))

                        elif isinstance(block, str):
                            parts.append(block)

                    message_content = "\n\n".join(parts)

                if message_content and str(message_content).strip():
                    answer = str(message_content).strip()
                    break

        # Do not silently leave the question unanswered.
        if not answer:
            raise ValueError(
                "The agent finished without returning a readable answer."
            )

        # Save the assistant response.
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        # Clear any previous error.
        st.session_state.pop("chat_error", None)

    except Exception as exc:

        # Save the error so it remains visible after rerunning.
        st.session_state.chat_error = str(exc)

        st.session_state.messages.append({
            "role": "assistant",
            "content": (
                "I couldn't complete that request. "
                "Please try again or check the technical details below."
            )
        })

    # Refresh the page in both success and failure cases.
    st.rerun()


# Display technical errors after the rerun.
if st.session_state.get("chat_error"):

    with st.expander("Chatbot technical details", expanded=True):
        st.code(st.session_state.chat_error)


# ============================================================
# CLEAR CONVERSATION
# ============================================================

if st.session_state.messages:

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

        
# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="app-footer" style="
        margin-top: 5px;
        padding-top: 5px;
        line-height: 1.2;
    ">

        <div style="margin-bottom: 3px;">
            <span class="footer-brand">AI Personal Assistant</span>
        </div>

        <div style="margin-bottom: 3px;">
            Your everyday tasks, made easier with AI.
        </div>

        <div>
            Developed by
            <strong style="color: #2563EB;">
                Heramba Kakati
            </strong>
        </div>

    </div>
    """
)