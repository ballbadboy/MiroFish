"""
配置管理
统一从项目根目录的 .env 文件加载配置
"""

import os
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
# 路径: MiroFish/.env (相对于 backend/app/config.py)
project_root_env = os.path.join(os.path.dirname(__file__), '../../.env')

if os.path.exists(project_root_env):
    load_dotenv(project_root_env, override=True)
else:
    # 如果根目录没有 .env，尝试加载环境变量（用于生产环境）
    load_dotenv(override=True)


class Config:
    """Flask配置类"""
    
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        # Allow dev mode without setting SECRET_KEY only when DEBUG env is set
        SECRET_KEY = 'dev-only-insecure-key' if os.environ.get('FLASK_DEBUG', '').lower() == 'true' else None
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # JSON配置 - 禁用ASCII转义，让中文直接显示（而不是 \uXXXX 格式）
    JSON_AS_ASCII = False
    
    # LLM配置（统一使用OpenAI格式）— default / backward-compat
    LLM_API_KEY = os.environ.get('LLM_API_KEY')
    LLM_BASE_URL = os.environ.get('LLM_BASE_URL', 'https://api.openai.com/v1')
    LLM_MODEL_NAME = os.environ.get('LLM_MODEL_NAME', 'gpt-4o-mini')

    # ── Model Roles ──────────────────────────────────────────────────────────
    # Each role falls back to the default LLM_* values when not explicitly set.
    #
    # "strong" — quality-critical tasks: report generation, ontology building
    #   Set MODEL_STRONG_NAME=gpt-4o or claude-3-5-sonnet-20241022 etc.
    MODEL_STRONG_API_KEY  = os.environ.get('MODEL_STRONG_API_KEY')  or os.environ.get('LLM_API_KEY')
    MODEL_STRONG_BASE_URL = os.environ.get('MODEL_STRONG_BASE_URL') or os.environ.get('LLM_BASE_URL', 'https://api.openai.com/v1')
    MODEL_STRONG_NAME     = os.environ.get('MODEL_STRONG_NAME')     or os.environ.get('LLM_MODEL_NAME', 'gpt-4o-mini')

    # "fast" — bulk / cheap tasks: agent-profile generation, simulation config
    #   Set MODEL_FAST_NAME=gpt-4o-mini or gemini-1.5-flash etc.
    MODEL_FAST_API_KEY    = os.environ.get('MODEL_FAST_API_KEY')    or os.environ.get('LLM_API_KEY')
    MODEL_FAST_BASE_URL   = os.environ.get('MODEL_FAST_BASE_URL')   or os.environ.get('LLM_BASE_URL', 'https://api.openai.com/v1')
    MODEL_FAST_NAME       = os.environ.get('MODEL_FAST_NAME')       or os.environ.get('LLM_MODEL_NAME', 'gpt-4o-mini')

    # "local" — dev / testing via Ollama (or any OpenAI-compatible local server)
    #   Set MODEL_LOCAL_NAME=llama3.2 (or whatever model you pulled)
    MODEL_LOCAL_API_KEY   = os.environ.get('MODEL_LOCAL_API_KEY',  'ollama')
    MODEL_LOCAL_BASE_URL  = os.environ.get('MODEL_LOCAL_BASE_URL', 'http://localhost:11434/v1')
    MODEL_LOCAL_NAME      = os.environ.get('MODEL_LOCAL_NAME',     'llama3.2')
    # ─────────────────────────────────────────────────────────────────────────
    
    # Zep配置
    ZEP_API_KEY = os.environ.get('ZEP_API_KEY')
    # ZEP_BASE_URL: ถ้าใส่ → ชี้ไป Zep CE local, ถ้าว่าง → ใช้ Zep Cloud default
    ZEP_BASE_URL = os.environ.get('ZEP_BASE_URL')
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'md', 'txt', 'markdown'}
    
    # 文本处理配置
    DEFAULT_CHUNK_SIZE = 500  # 默认切块大小
    DEFAULT_CHUNK_OVERLAP = 50  # 默认重叠大小
    
    # OASIS模拟配置
    OASIS_DEFAULT_MAX_ROUNDS = int(os.environ.get('OASIS_DEFAULT_MAX_ROUNDS', '10'))
    OASIS_SIMULATION_DATA_DIR = os.path.join(os.path.dirname(__file__), '../uploads/simulations')
    
    # OASIS平台可用动作配置
    OASIS_TWITTER_ACTIONS = [
        'CREATE_POST', 'LIKE_POST', 'REPOST', 'FOLLOW', 'DO_NOTHING', 'QUOTE_POST'
    ]
    OASIS_REDDIT_ACTIONS = [
        'LIKE_POST', 'DISLIKE_POST', 'CREATE_POST', 'CREATE_COMMENT',
        'LIKE_COMMENT', 'DISLIKE_COMMENT', 'SEARCH_POSTS', 'SEARCH_USER',
        'TREND', 'REFRESH', 'DO_NOTHING', 'FOLLOW', 'MUTE'
    ]
    
    # Report Agent配置
    REPORT_AGENT_MAX_TOOL_CALLS = int(os.environ.get('REPORT_AGENT_MAX_TOOL_CALLS', '5'))
    REPORT_AGENT_MAX_REFLECTION_ROUNDS = int(os.environ.get('REPORT_AGENT_MAX_REFLECTION_ROUNDS', '2'))
    REPORT_AGENT_TEMPERATURE = float(os.environ.get('REPORT_AGENT_TEMPERATURE', '0.5'))
    
    @classmethod
    def validate(cls):
        """验证必要配置"""
        errors = []
        if not cls.LLM_API_KEY:
            errors.append("LLM_API_KEY 未配置")
        if not cls.ZEP_API_KEY:
            errors.append("ZEP_API_KEY 未配置")
        if not cls.SECRET_KEY and not cls.DEBUG:
            errors.append("SECRET_KEY env var is required in production (set FLASK_DEBUG=True for dev)")
        return errors

