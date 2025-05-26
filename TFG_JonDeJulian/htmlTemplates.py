css = '''
<style>
body, .stApp, .block-container, .main, .st-emotion-cache-1kyxreq, .st-emotion-cache-1v0mbdj {
    background-color: #C1E1C1 !important;
}
</style>
<style>
:root {
    /* Variables compartidas */
    --neon-blue: #00a7ff;
    --neon-purple: #7b2ff7;
    --success-color: #00c170;
    --warning-color: #ff8800;
    --error-color: #ff004c;
    
    /* Variables para tema claro (valores por defecto) */
    --light-bg: #C1E1C1;        /* Verde pastel claro */
    --lighter-bg: #ffffff;
    --glass-bg: rgba(255, 255, 255, 0.7);
    --glass-border: rgba(0, 0, 0, 0.05);
    --text-primary: #1a1f36;
    --text-secondary: rgba(26, 31, 54, 0.7);
    --card-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    --container-bg: rgba(255, 255, 255, 0.85);
    --bot-message-bg: rgba(248, 250, 255, 0.9);
    --input-bg: rgba(255, 255, 255, 0.8);
    --sidebar-bg: rgba(248, 250, 255, 0.9);
    --table-bg: rgba(255, 255, 255, 0.8);
    --expander-bg: rgba(255, 255, 255, 0.8);
    --scrollbar-track: var(--lighter-bg);
}

/* Estilos para el tema oscuro - se aplicarán cuando el body tenga la clase 'dark-theme' */
body.dark-theme {
    --light-bg: #121212;
    --lighter-bg: #1e1e1e;
    --glass-bg: rgba(30, 30, 30, 0.7);
    --glass-border: rgba(255, 255, 255, 0.1);
    --text-primary: #ffffff;
    --text-secondary: rgba(255, 255, 255, 0.7);
    --card-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    --container-bg: rgba(30, 30, 30, 0.85);
    --bot-message-bg: rgba(40, 40, 40, 0.9);
    --input-bg: rgba(40, 40, 40, 0.8);
    --sidebar-bg: rgba(25, 25, 25, 0.9);
    --table-bg: rgba(40, 40, 40, 0.8);
    --expander-bg: rgba(40, 40, 40, 0.8);
    --scrollbar-track: var(--lighter-bg);
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: linear-gradient(125deg, var(--light-bg) 0%, var(--lighter-bg) 100%);
    color: var(--text-primary);
    background-attachment: fixed;
    transition: background 0.3s ease, color 0.3s ease;
}

/* Main container styling */
.main .block-container {
    padding-top: 1rem;
    max-width: 1100px;
    background: var(--container-bg);
    backdrop-filter: blur(10px);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    box-shadow: var(--card-shadow);
    padding: 20px;
    margin-top: 20px;
    transition: background 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}

/* Chat message styling */
.chat-message {
    padding: 1.2rem 1.5rem;
    border-radius: 12px;
    margin-bottom: 1.2rem;
    display: flex;
    box-shadow: var(--card-shadow);
    animation: slideIn 0.3s ease-out;
    backdrop-filter: blur(5px);
    border: 1px solid var(--glass-border);
    transition: background 0.3s ease, border-color 0.3s ease;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

.chat-message.user {
    background: linear-gradient(135deg, var(--neon-purple) 0%, rgba(123, 47, 247, 0.7) 100%);
    margin-left: 40px;
    border-top-right-radius: 4px;
}

.chat-message.bot {
    background: var(--bot-message-bg);
    margin-right: 40px;
    border-top-left-radius: 4px;
    border: 1px solid var(--glass-border);
}

.chat-message .avatar {
    width: 40px;
    height: 40px;
    margin-right: 16px;
    flex-shrink: 0;
    position: relative;
}

.chat-message .avatar::after {
    content: "";
    position: absolute;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    bottom: 0;
    right: 0;
    background-color: var(--success-color);
    box-shadow: 0 0 10px var(--success-color);
}

.chat-message .avatar img {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    object-fit: cover;
    border: 2px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
}

.chat-message .message {
    width: 100%;
    padding: 0 0.5rem;
    font-size: 1rem;
    line-height: 1.5;
    letter-spacing: 0.2px;
}

.chat-message.user .message {
    color: white;
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.3);
}

.chat-message.bot .message {
    color: var(--text-primary);
    transition: color 0.3s ease;
}

/* Button styling */
.stButton>button {
    background: linear-gradient(135deg, var(--neon-blue) 0%, var(--neon-purple) 100%);
    color: white;
    border-radius: 8px;
    padding: 0.6rem 1.8rem;
    font-weight: 600;
    border: none;
    transition: all 0.3s ease;
    box-shadow: 0 0 15px rgba(0, 167, 255, 0.4);
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.9rem;
}

.stButton>button:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 0 25px rgba(0, 167, 255, 0.6);
}

.stButton>button:active {
    transform: translateY(1px);
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-radius: 12px;
    background: var(--glass-bg);
    padding: 6px;
    border: 1px solid var(--glass-border);
    transition: background 0.3s ease, border-color 0.3s ease;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 10px 20px;
    transition: all 0.3s ease;
    color: var(--text-secondary);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--neon-blue) 0%, var(--neon-purple) 100%) !important;
    color: white !important;
    font-weight: 600;
    box-shadow: 0 0 15px rgba(0, 167, 255, 0.4);
}

/* Input fields */
.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    border-radius: 10px;
    border: 1px solid var(--glass-border);
    padding: 14px;
    font-size: 16px;
    background: var(--input-bg);
    color: var(--text-primary);
    transition: all 0.3s ease;
    backdrop-filter: blur(5px);
}

.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
    border-color: var(--neon-blue);
    box-shadow: 0 0 15px rgba(0, 167, 255, 0.3);
}

/* File uploader */
.stFileUploader>div>button {
    background: var(--input-bg);
    color: var(--neon-blue);
    border-radius: 10px;
    border: 1px dashed var(--neon-blue);
    padding: 14px;
    font-weight: 500;
    backdrop-filter: blur(5px);
    transition: all 0.3s ease;
}

.stFileUploader>div>button:hover {
    background: rgba(0, 167, 255, 0.1);
    box-shadow: 0 0 15px rgba(0, 167, 255, 0.2);
}

/* Expander */
.streamlit-expanderHeader {
    font-weight: 600;
    color: var(--neon-blue);
    background: var(--expander-bg);
    border-radius: 10px;
    padding: 10px 14px;
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(5px);
    transition: background 0.3s ease, border-color 0.3s ease;
}

/* Success messages */
.element-container .stAlert {
    border-radius: 10px;
    border: none;
    box-shadow: var(--card-shadow);
    backdrop-filter: blur(5px);
    transition: background 0.3s ease;
}

.element-container .stAlert.success {
    background: rgba(0, 193, 112, 0.1);
    color: var(--success-color);
    border: 1px solid rgba(0, 193, 112, 0.3);
}

/* Info messages */
.element-container .stAlert.info {
    background: rgba(0, 167, 255, 0.1);
    color: var(--neon-blue);
    border: 1px solid rgba(0, 167, 255, 0.3);
}

/* Warning messages */
.element-container .stAlert.warning {
    background: rgba(255, 170, 0, 0.1);
    color: var(--warning-color);
    border: 1px solid rgba(255, 170, 0, 0.3);
}

/* Error messages */
.element-container .stAlert.error {
    background: rgba(255, 0, 76, 0.1);
    color: var(--error-color);
    border: 1px solid rgba(255, 0, 76, 0.3);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--sidebar-bg);
    backdrop-filter: blur(10px);
    border-right: 1px solid var(--glass-border);
    transition: background 0.3s ease, border-color 0.3s ease;
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    padding-top: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

/* Spinner */
.stSpinner > div > div {
    border-color: var(--neon-blue) transparent transparent transparent;
    box-shadow: 0 0 15px var(--neon-blue);
}

/* Subheader styling */
.stSubheader {
    font-weight: 700;
    color: var(--text-primary);
    margin-top: 1.8rem;
    margin-bottom: 1.2rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    font-size: 0.9rem;
    background: linear-gradient(90deg, var(--neon-blue), var(--neon-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
    transition: color 0.3s ease;
}

/* Image styling */
.element-container img {
    border-radius: 12px;
    box-shadow: var(--card-shadow);
    transition: all 0.3s ease;
    border: 1px solid var(--glass-border);
}

.element-container img:hover {
    transform: scale(1.02);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
}

/* Progress bar */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--neon-blue), var(--neon-purple));
    box-shadow: 0 0 10px rgba(0, 167, 255, 0.5);
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--scrollbar-track);
    transition: background 0.3s ease;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(var(--neon-blue), var(--neon-purple));
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--neon-blue);
}

/* Dataframe/table styling */
[data-testid="stTable"], .dataframe {
    background: var(--table-bg);
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--glass-border);
    transition: background 0.3s ease, border-color 0.3s ease;
}

[data-testid="stTable"] th, .dataframe th {
    background: rgba(0, 167, 255, 0.1);
    color: var(--neon-blue);
    font-weight: 600;
    padding: 12px !important;
}

[data-testid="stTable"] td, .dataframe td {
    color: var(--text-primary);
    padding: 10px !important;
    border-bottom: 1px solid var(--glass-border);
    transition: color 0.3s ease;
}

/* Checkbox styling */
[data-testid="stCheckbox"] {
    accent-color: var(--neon-blue);
}

/* Select box styling */
[data-baseweb="select"] {
    background: var(--input-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 10px !important;
    transition: background 0.3s ease, border-color 0.3s ease;
}

[data-baseweb="select"] [data-baseweb="tag"] {
    background: rgba(0, 167, 255, 0.2) !important;
    border-radius: 6px !important;
    color: var(--text-primary) !important;
    transition: color 0.3s ease;
}

/* Tooltip styling */
[data-baseweb="tooltip"] {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 8px !important;
    backdrop-filter: blur(10px) !important;
    color: var(--text-primary) !important;
    box-shadow: var(--card-shadow) !important;
    transition: background 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

/* Headers */
h1, h2, h3 {
    position: relative;
    display: inline-block;
    color: var(--text-primary);
    transition: color 0.3s ease;
}

/* Tema selector styling */
.theme-toggle {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
}

.theme-toggle-label {
    font-weight: 600;
    margin-right: 10px;
    color: var(--text-primary);
    transition: color 0.3s ease;
}

/* Radio buttons personalizados para el selector de tema */
.stRadio > div {
    display: flex;
    flex-direction: row !important;
    gap: 10px;
}

.stRadio > div > div {
    flex: 1;
}

.stRadio > div > div > label {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px 16px;
    background: var(--glass-bg);
    border-radius: 10px;
    border: 1px solid var(--glass-border);
    transition: all 0.3s ease;
    cursor: pointer;
}

.stRadio > div > div > label:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Estilo para el tema activo */
.stRadio > div > div > label[data-baseweb="radio"] > span:first-child {
    background-color: var(--neon-blue);
    border-color: var(--neon-blue);
}

/* Script para cambiar el tema */
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Función para aplicar el tema
    function applyTheme(theme) {
        if (theme === 'dark') {
            document.body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.classList.remove('dark-theme');
            localStorage.setItem('theme', 'light');
        }
    }
    
    // Verificar si hay un tema guardado
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        applyTheme(savedTheme);
    }
    
    // Observar cambios en los radio buttons
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'data-testid') {
                const radios = document.querySelectorAll('input[type="radio"][name="theme"]');
                radios.forEach(function(radio) {
                    radio.addEventListener('change', function(e) {
                        if (e.target.value === 'Oscuro') {
                            applyTheme('dark');
                        } else {
                            applyTheme('light');
                        }
                    });
                });
            }
        });
    });
    
    // Configurar el observador
    observer.observe(document.body, { 
        childList: true, 
        subtree: true, 
        attributes: true,
        attributeFilter: ['data-testid'] 
    });
});
</script>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://static.vecteezy.com/system/resources/previews/016/774/583/original/3d-user-icon-on-transparent-background-free-png.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''



