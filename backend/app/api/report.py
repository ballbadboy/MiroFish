"""
Report API路由
提供模拟报告生成、获取、对话等接口
"""

import os
import re
import html as html_mod
import traceback
import threading
from flask import request, jsonify, send_file, Response

from . import report_bp
from ..config import Config
from ..services.report_agent import ReportAgent, ReportManager, ReportStatus
from ..services.simulation_manager import SimulationManager
from ..models.project import ProjectManager
from ..models.task import TaskManager, TaskStatus
from ..utils.logger import get_logger
from ..utils.locale import t, get_locale, set_locale

logger = get_logger('endora.api.report')


# ============== HTML Export Helpers ==============

def _inline_md(text: str) -> str:
    """Apply inline markdown transforms to already-HTML-escaped text."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    return text


def _md_to_html(text: str) -> str:
    """
    Lightweight markdown→HTML converter for LLM report output.
    Handles: fenced code blocks, headings, hr, bold/italic/code,
    unordered/ordered lists, blockquotes, and paragraphs.
    """
    # ── Pass 1: extract fenced code blocks ──────────────────────────────
    code_blocks: dict[str, str] = {}
    out_lines: list[str] = []
    in_code = False
    code_buf: list[str] = []
    code_lang = ''
    code_idx = 0

    for line in text.split('\n'):
        fence = re.match(r'^```(\w*)$', line.strip())
        if fence and not in_code:
            in_code = True
            code_lang = fence.group(1)
            code_buf = []
        elif line.strip() == '```' and in_code:
            in_code = False
            placeholder = f'\x00CODE{code_idx}\x00'
            lang_attr = f' class="language-{code_lang}"' if code_lang else ''
            escaped = html_mod.escape('\n'.join(code_buf))
            code_blocks[placeholder] = f'<pre><code{lang_attr}>{escaped}</code></pre>'
            out_lines.append(placeholder)
            code_idx += 1
        elif in_code:
            code_buf.append(line)
        else:
            out_lines.append(line)

    # ── Pass 2: paragraph-level processing ──────────────────────────────
    paragraphs = re.split(r'\n{2,}', '\n'.join(out_lines))
    parts: list[str] = []

    ul_re = re.compile(r'^[-*]\s+(.+)$')
    ol_re = re.compile(r'^\d+\.\s+(.+)$')

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Code block placeholder (single line)
        if para in code_blocks:
            parts.append(code_blocks[para])
            continue

        para_lines = para.split('\n')
        first = para_lines[0]

        # Headings (only when the whole paragraph is a single heading line)
        h_match = re.match(r'^(#{1,4})\s+(.+)$', first) if len(para_lines) == 1 else None
        if h_match:
            lvl = len(h_match.group(1))
            parts.append(f'<h{lvl}>{_inline_md(html_mod.escape(h_match.group(2)))}</h{lvl}>')
            continue

        # Horizontal rule
        if len(para_lines) == 1 and re.match(r'^-{3,}$', first):
            parts.append('<hr>')
            continue

        # Blockquote
        if first.startswith('> '):
            content = ' '.join(l.lstrip('> ') for l in para_lines)
            parts.append(f'<blockquote><p>{_inline_md(html_mod.escape(content))}</p></blockquote>')
            continue

        # Unordered list
        if ul_re.match(first):
            items = ''.join(
                f'<li>{_inline_md(html_mod.escape(m.group(1)))}</li>'
                for line in para_lines
                if (m := ul_re.match(line))
            )
            parts.append(f'<ul>{items}</ul>')
            continue

        # Ordered list
        if ol_re.match(first):
            items = ''.join(
                f'<li>{_inline_md(html_mod.escape(m.group(1)))}</li>'
                for line in para_lines
                if (m := ol_re.match(line))
            )
            parts.append(f'<ol>{items}</ol>')
            continue

        # Regular paragraph (join multi-lines with a space)
        content = ' '.join(para_lines)
        parts.append(f'<p>{_inline_md(html_mod.escape(content))}</p>')

    return '\n'.join(parts)


_EXPORT_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__ — Endora Report</title>
<style>
:root{--font-body:'Space Grotesk',system-ui,sans-serif;--font-mono:'JetBrains Mono',monospace;--color-muted:#666;--color-border:#eaeaea;--color-surface:#fafafa;}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
body{font-family:var(--font-body);color:#0d0d0d;background:#fff;line-height:1.75;font-size:15px;}
.print-bar{position:fixed;top:0;left:0;right:0;background:#000;color:#fff;padding:10px 32px;display:flex;justify-content:space-between;align-items:center;z-index:100;font-size:11px;font-family:var(--font-mono);letter-spacing:.06em;}
.print-btn{background:#fff;color:#000;border:none;padding:6px 18px;font-family:var(--font-body);font-size:11px;font-weight:700;cursor:pointer;border-radius:2px;text-transform:uppercase;letter-spacing:.05em;}
.report-wrapper{max-width:860px;margin:60px auto 80px;padding:0 48px;}
.report-header{padding:40px 0 32px;border-bottom:2px solid #000;margin-bottom:40px;}
.report-tag{display:block;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--color-muted);font-family:var(--font-mono);margin-bottom:12px;}
.report-title{font-size:30px;font-weight:700;line-height:1.25;color:#000;margin-bottom:12px;}
.report-summary{font-size:16px;color:var(--color-muted);line-height:1.6;max-width:640px;}
.report-meta{margin-top:20px;display:flex;gap:24px;font-size:11px;font-family:var(--font-mono);color:#999;flex-wrap:wrap;}
.report-meta strong{color:#333;}
.report-content h1{font-size:24px;font-weight:700;margin:48px 0 14px;}
.report-content h2{font-size:20px;font-weight:600;margin:40px 0 12px;padding-bottom:8px;border-bottom:1px solid var(--color-border);}
.report-content h3{font-size:17px;font-weight:600;margin:32px 0 10px;}
.report-content h4{font-size:13px;font-weight:700;margin:24px 0 8px;text-transform:uppercase;letter-spacing:.05em;color:#555;}
.report-content p{margin-bottom:16px;}
.report-content ul,.report-content ol{margin:10px 0 18px 28px;}
.report-content li{margin-bottom:6px;}
.report-content hr{border:none;border-top:1px solid var(--color-border);margin:32px 0;}
.report-content blockquote{border-left:3px solid #000;padding:8px 20px;margin:16px 0;background:var(--color-surface);color:#444;}
.report-content code{font-family:var(--font-mono);font-size:13px;background:#f0f0f0;padding:2px 6px;border-radius:2px;color:#c0392b;}
.report-content pre{background:#0d0d0d;color:#e0e0e0;padding:20px 24px;border-radius:4px;margin:20px 0;overflow-x:auto;}
.report-content pre code{background:transparent;color:inherit;padding:0;font-size:13px;}
.report-content strong{font-weight:600;}
.report-content em{font-style:italic;color:#555;}
.report-content a{color:#000;text-decoration:underline;}
.report-footer{margin-top:64px;padding-top:20px;border-top:1px solid var(--color-border);font-size:10px;font-family:var(--font-mono);color:#bbb;display:flex;justify-content:space-between;}
@media print{
  .print-bar{display:none!important;}
  body{font-size:13px;}
  .report-wrapper{margin:0;padding:24px 40px;max-width:100%;}
  .report-content pre{border:1px solid #ddd;background:#f9f9f9;color:#000;}
  h1,h2,h3,h4{page-break-after:avoid;}
  p,li{page-break-inside:avoid;}
}
</style>
</head>
<body>
<div class="print-bar">
  <span>ENDORA &nbsp;/&nbsp; __REPORT_ID__</span>
  <button class="print-btn" onclick="window.print()">&#8595; Save as PDF</button>
</div>
<div class="report-wrapper">
  <header class="report-header">
    <span class="report-tag">Simulation Analysis Report</span>
    <h1 class="report-title">__TITLE__</h1>
    <p class="report-summary">__SUMMARY__</p>
    <div class="report-meta">
      <span>ID:&nbsp;<strong>__REPORT_ID__</strong></span>
      <span>Simulation:&nbsp;<strong>__SIM_ID__</strong></span>
      <span>Generated:&nbsp;<strong>__GENERATED_AT__</strong></span>
    </div>
  </header>
  <div class="report-content">
__CONTENT_HTML__
  </div>
  <footer class="report-footer">
    <span>Generated by Endora &middot; Multi-Agent Social Simulation</span>
    <span>__REPORT_ID__</span>
  </footer>
</div>
</body>
</html>"""


def _build_export_html(report) -> str:
    """Assemble a fully self-contained HTML export from a report object."""
    outline = report.outline or {}
    title   = html_mod.escape(str(outline.get('title', report.report_id)))
    summary = html_mod.escape(str(outline.get('summary', '')))
    generated_at = str(getattr(report, 'completed_at', None) or
                       getattr(report, 'created_at', 'N/A'))[:19].replace('T', ' ')

    content_html = _md_to_html(report.markdown_content or '')

    return (
        _EXPORT_TEMPLATE
        .replace('__TITLE__', title)
        .replace('__SUMMARY__', summary)
        .replace('__REPORT_ID__', html_mod.escape(report.report_id))
        .replace('__SIM_ID__', html_mod.escape(str(report.simulation_id or '')))
        .replace('__GENERATED_AT__', html_mod.escape(generated_at))
        .replace('__CONTENT_HTML__', content_html)
    )


# ============== 报告生成接口 ==============

@report_bp.route('/generate', methods=['POST'])
def generate_report():
    """
    生成模拟分析报告（异步任务）
    
    这是一个耗时操作，接口会立即返回task_id，
    使用 GET /api/report/generate/status 查询进度
    
    请求（JSON）：
        {
            "simulation_id": "sim_xxxx",    // 必填，模拟ID
            "force_regenerate": false        // 可选，强制重新生成
        }
    
    返回：
        {
            "success": true,
            "data": {
                "simulation_id": "sim_xxxx",
                "task_id": "task_xxxx",
                "status": "generating",
                "message": "报告生成任务已启动"
            }
        }
    """
    try:
        data = request.get_json() or {}
        
        simulation_id = data.get('simulation_id')
        if not simulation_id:
            return jsonify({
                "success": False,
                "error": t('api.requireSimulationId')
            }), 400

        force_regenerate = data.get('force_regenerate', False)
        
        # 获取模拟信息
        manager = SimulationManager()
        state = manager.get_simulation(simulation_id)
        
        if not state:
            return jsonify({
                "success": False,
                "error": t('api.simulationNotFound', id=simulation_id)
            }), 404

        # 检查是否已有报告
        if not force_regenerate:
            existing_report = ReportManager.get_report_by_simulation(simulation_id)
            if existing_report and existing_report.status == ReportStatus.COMPLETED:
                return jsonify({
                    "success": True,
                    "data": {
                        "simulation_id": simulation_id,
                        "report_id": existing_report.report_id,
                        "status": "completed",
                        "message": t('api.reportAlreadyExists'),
                        "already_generated": True
                    }
                })
        
        # 获取项目信息
        project = ProjectManager.get_project(state.project_id)
        if not project:
            return jsonify({
                "success": False,
                "error": t('api.projectNotFound', id=state.project_id)
            }), 404
        
        graph_id = state.graph_id or project.graph_id
        if not graph_id:
            return jsonify({
                "success": False,
                "error": t('api.missingGraphIdEnsure')
            }), 400
        
        simulation_requirement = project.simulation_requirement
        if not simulation_requirement:
            return jsonify({
                "success": False,
                "error": t('api.missingSimRequirement')
            }), 400
        
        # 提前生成 report_id，以便立即返回给前端
        import uuid
        report_id = f"report_{uuid.uuid4().hex[:12]}"
        
        # 创建异步任务
        task_manager = TaskManager()
        task_id = task_manager.create_task(
            task_type="report_generate",
            metadata={
                "simulation_id": simulation_id,
                "graph_id": graph_id,
                "report_id": report_id
            }
        )
        
        # Capture locale before spawning background thread
        current_locale = get_locale()

        # 定义后台任务
        def run_generate():
            set_locale(current_locale)
            try:
                task_manager.update_task(
                    task_id,
                    status=TaskStatus.PROCESSING,
                    progress=0,
                    message=t('api.initReportAgent')
                )
                
                # 创建Report Agent
                agent = ReportAgent(
                    graph_id=graph_id,
                    simulation_id=simulation_id,
                    simulation_requirement=simulation_requirement
                )
                
                # 进度回调
                def progress_callback(stage, progress, message):
                    task_manager.update_task(
                        task_id,
                        progress=progress,
                        message=f"[{stage}] {message}"
                    )
                
                # 生成报告（传入预先生成的 report_id）
                report = agent.generate_report(
                    progress_callback=progress_callback,
                    report_id=report_id
                )
                
                # 保存报告
                ReportManager.save_report(report)
                
                if report.status == ReportStatus.COMPLETED:
                    task_manager.complete_task(
                        task_id,
                        result={
                            "report_id": report.report_id,
                            "simulation_id": simulation_id,
                            "status": "completed"
                        }
                    )
                else:
                    task_manager.fail_task(task_id, report.error or t('api.reportGenerateFailed'))
                
            except Exception as e:
                logger.error(f"报告生成失败: {str(e)}")
                task_manager.fail_task(task_id, str(e))
        
        # 启动后台线程
        thread = threading.Thread(target=run_generate, daemon=True)
        thread.start()
        
        return jsonify({
            "success": True,
            "data": {
                "simulation_id": simulation_id,
                "report_id": report_id,
                "task_id": task_id,
                "status": "generating",
                "message": t('api.reportGenerateStarted'),
                "already_generated": False
            }
        })
        
    except Exception as e:
        logger.error(f"启动报告生成任务失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@report_bp.route('/generate/status', methods=['POST'])
def get_generate_status():
    """
    查询报告生成任务进度
    
    请求（JSON）：
        {
            "task_id": "task_xxxx",         // 可选，generate返回的task_id
            "simulation_id": "sim_xxxx"     // 可选，模拟ID
        }
    
    返回：
        {
            "success": true,
            "data": {
                "task_id": "task_xxxx",
                "status": "processing|completed|failed",
                "progress": 45,
                "message": "..."
            }
        }
    """
    try:
        data = request.get_json() or {}
        
        task_id = data.get('task_id')
        simulation_id = data.get('simulation_id')
        
        # 如果提供了simulation_id，先检查是否已有完成的报告
        if simulation_id:
            existing_report = ReportManager.get_report_by_simulation(simulation_id)
            if existing_report and existing_report.status == ReportStatus.COMPLETED:
                return jsonify({
                    "success": True,
                    "data": {
                        "simulation_id": simulation_id,
                        "report_id": existing_report.report_id,
                        "status": "completed",
                        "progress": 100,
                        "message": t('api.reportGenerated'),
                        "already_completed": True
                    }
                })
        
        if not task_id:
            return jsonify({
                "success": False,
                "error": t('api.requireTaskOrSimId')
            }), 400
        
        task_manager = TaskManager()
        task = task_manager.get_task(task_id)
        
        if not task:
            return jsonify({
                "success": False,
                "error": t('api.taskNotFound', id=task_id)
            }), 404
        
        return jsonify({
            "success": True,
            "data": task.to_dict()
        })
        
    except Exception as e:
        logger.error(f"查询任务状态失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============== 报告获取接口 ==============

@report_bp.route('/<report_id>', methods=['GET'])
def get_report(report_id: str):
    """
    获取报告详情
    
    返回：
        {
            "success": true,
            "data": {
                "report_id": "report_xxxx",
                "simulation_id": "sim_xxxx",
                "status": "completed",
                "outline": {...},
                "markdown_content": "...",
                "created_at": "...",
                "completed_at": "..."
            }
        }
    """
    try:
        report = ReportManager.get_report(report_id)
        
        if not report:
            return jsonify({
                "success": False,
                "error": t('api.reportNotFound', id=report_id)
            }), 404
        
        return jsonify({
            "success": True,
            "data": report.to_dict()
        })
        
    except Exception as e:
        logger.error(f"获取报告失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@report_bp.route('/by-simulation/<simulation_id>', methods=['GET'])
def get_report_by_simulation(simulation_id: str):
    """
    根据模拟ID获取报告
    
    返回：
        {
            "success": true,
            "data": {
                "report_id": "report_xxxx",
                ...
            }
        }
    """
    try:
        report = ReportManager.get_report_by_simulation(simulation_id)
        
        if not report:
            return jsonify({
                "success": False,
                "error": t('api.noReportForSim', id=simulation_id),
                "has_report": False
            }), 404
        
        return jsonify({
            "success": True,
            "data": report.to_dict(),
            "has_report": True
        })
        
    except Exception as e:
        logger.error(f"获取报告失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@report_bp.route('/list', methods=['GET'])
def list_reports():
    """
    列出所有报告
    
    Query参数：
        simulation_id: 按模拟ID过滤（可选）
        limit: 返回数量限制（默认50）
    
    返回：
        {
            "success": true,
            "data": [...],
            "count": 10
        }
    """
    try:
        simulation_id = request.args.get('simulation_id')
        limit = request.args.get('limit', 50, type=int)
        
        reports = ReportManager.list_reports(
            simulation_id=simulation_id,
            limit=limit
        )
        
        return jsonify({
            "success": True,
            "data": [r.to_dict() for r in reports],
            "count": len(reports)
        })
        
    except Exception as e:
        logger.error(f"列出报告失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@report_bp.route('/<report_id>/download', methods=['GET'])
def download_report(report_id: str):
    """
    下载报告（Markdown格式）
    
    返回Markdown文件
    """
    try:
        report = ReportManager.get_report(report_id)
        
        if not report:
            return jsonify({
                "success": False,
                "error": t('api.reportNotFound', id=report_id)
            }), 404
        
        md_path = ReportManager._get_report_markdown_path(report_id)
        
        if not os.path.exists(md_path):
            # 如果MD文件不存在，生成一个临时文件
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                f.write(report.markdown_content)
                temp_path = f.name
            
            return send_file(
                temp_path,
                as_attachment=True,
                download_name=f"{report_id}.md"
            )
        
        return send_file(
            md_path,
            as_attachment=True,
            download_name=f"{report_id}.md"
        )
        
    except Exception as e:
        logger.error(f"下载报告失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@report_bp.route('/<report_id>/export/html', methods=['GET'])
def export_report_html(report_id: str):
    """
    导出报告为独立 HTML 文件（可在浏览器直接打印/存为 PDF）

    返回：自包含的 HTML 文件（text/html）
    """
    try:
        report = ReportManager.get_report(report_id)

        if not report:
            return jsonify({
                "success": False,
                "error": t('api.reportNotFound', id=report_id)
            }), 404

        if not report.markdown_content:
            return jsonify({
                "success": False,
                "error": "Report content is not yet available"
            }), 400

        html_content = _build_export_html(report)

        return Response(
            html_content,
            status=200,
            mimetype='text/html',
            headers={
                'Content-Disposition': f'attachment; filename="{report_id}.html"',
                'Content-Type': 'text/html; charset=utf-8',
            }
        )

    except Exception as e:
        logger.error(f"导出报告 HTML 失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@report_bp.route('/<report_id>', methods=['DELETE'])
def delete_report(report_id: str):
    """删除报告"""
    try:
        success = ReportManager.delete_report(report_id)
        
        if not success:
            return jsonify({
                "success": False,
                "error": t('api.reportNotFound', id=report_id)
            }), 404
        
        return jsonify({
            "success": True,
            "message": t('api.reportDeleted', id=report_id)
        })
        
    except Exception as e:
        logger.error(f"删除报告失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


# ============== Report Agent对话接口 ==============

@report_bp.route('/chat', methods=['POST'])
def chat_with_report_agent():
    """
    与Report Agent对话
    
    Report Agent可以在对话中自主调用检索工具来回答问题
    
    请求（JSON）：
        {
            "simulation_id": "sim_xxxx",        // 必填，模拟ID
            "message": "请解释一下舆情走向",    // 必填，用户消息
            "chat_history": [                   // 可选，对话历史
                {"role": "user", "content": "..."},
                {"role": "assistant", "content": "..."}
            ]
        }
    
    返回：
        {
            "success": true,
            "data": {
                "response": "Agent回复...",
                "tool_calls": [调用的工具列表],
                "sources": [信息来源]
            }
        }
    """
    try:
        data = request.get_json() or {}
        
        simulation_id = data.get('simulation_id')
        message = data.get('message')
        chat_history = data.get('chat_history', [])
        
        if not simulation_id:
            return jsonify({
                "success": False,
                "error": t('api.requireSimulationId')
            }), 400

        if not message:
            return jsonify({
                "success": False,
                "error": t('api.requireMessage')
            }), 400
        
        # 获取模拟和项目信息
        manager = SimulationManager()
        state = manager.get_simulation(simulation_id)
        
        if not state:
            return jsonify({
                "success": False,
                "error": t('api.simulationNotFound', id=simulation_id)
            }), 404

        project = ProjectManager.get_project(state.project_id)
        if not project:
            return jsonify({
                "success": False,
                "error": t('api.projectNotFound', id=state.project_id)
            }), 404
        
        graph_id = state.graph_id or project.graph_id
        if not graph_id:
            return jsonify({
                "success": False,
                "error": t('api.missingGraphId')
            }), 400
        
        simulation_requirement = project.simulation_requirement or ""
        
        # 创建Agent并进行对话
        agent = ReportAgent(
            graph_id=graph_id,
            simulation_id=simulation_id,
            simulation_requirement=simulation_requirement
        )
        
        result = agent.chat(message=message, chat_history=chat_history)
        
        return jsonify({
            "success": True,
            "data": result
        })
        
    except Exception as e:
        logger.error(f"对话失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


# ============== 报告进度与分章节接口 ==============

@report_bp.route('/<report_id>/progress', methods=['GET'])
def get_report_progress(report_id: str):
    """
    获取报告生成进度（实时）
    
    返回：
        {
            "success": true,
            "data": {
                "status": "generating",
                "progress": 45,
                "message": "正在生成章节: 关键发现",
                "current_section": "关键发现",
                "completed_sections": ["执行摘要", "模拟背景"],
                "updated_at": "2025-12-09T..."
            }
        }
    """
    try:
        progress = ReportManager.get_progress(report_id)
        
        if not progress:
            return jsonify({
                "success": False,
                "error": t('api.reportProgressNotAvail', id=report_id)
            }), 404
        
        return jsonify({
            "success": True,
            "data": progress
        })
        
    except Exception as e:
        logger.error(f"获取报告进度失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@report_bp.route('/<report_id>/sections', methods=['GET'])
def get_report_sections(report_id: str):
    """
    获取已生成的章节列表（分章节输出）
    
    前端可以轮询此接口获取已生成的章节内容，无需等待整个报告完成
    
    返回：
        {
            "success": true,
            "data": {
                "report_id": "report_xxxx",
                "sections": [
                    {
                        "filename": "section_01.md",
                        "section_index": 1,
                        "content": "## 执行摘要\\n\\n..."
                    },
                    ...
                ],
                "total_sections": 3,
                "is_complete": false
            }
        }
    """
    try:
        sections = ReportManager.get_generated_sections(report_id)
        
        # 获取报告状态
        report = ReportManager.get_report(report_id)
        is_complete = report is not None and report.status == ReportStatus.COMPLETED
        
        return jsonify({
            "success": True,
            "data": {
                "report_id": report_id,
                "sections": sections,
                "total_sections": len(sections),
                "is_complete": is_complete
            }
        })
        
    except Exception as e:
        logger.error(f"获取章节列表失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@report_bp.route('/<report_id>/section/<int:section_index>', methods=['GET'])
def get_single_section(report_id: str, section_index: int):
    """
    获取单个章节内容
    
    返回：
        {
            "success": true,
            "data": {
                "filename": "section_01.md",
                "content": "## 执行摘要\\n\\n..."
            }
        }
    """
    try:
        section_path = ReportManager._get_section_path(report_id, section_index)
        
        if not os.path.exists(section_path):
            return jsonify({
                "success": False,
                "error": t('api.sectionNotFound', index=f"{section_index:02d}")
            }), 404
        
        with open(section_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            "success": True,
            "data": {
                "filename": f"section_{section_index:02d}.md",
                "section_index": section_index,
                "content": content
            }
        })
        
    except Exception as e:
        logger.error(f"获取章节内容失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


# ============== 报告状态检查接口 ==============

@report_bp.route('/check/<simulation_id>', methods=['GET'])
def check_report_status(simulation_id: str):
    """
    检查模拟是否有报告，以及报告状态
    
    用于前端判断是否解锁Interview功能
    
    返回：
        {
            "success": true,
            "data": {
                "simulation_id": "sim_xxxx",
                "has_report": true,
                "report_status": "completed",
                "report_id": "report_xxxx",
                "interview_unlocked": true
            }
        }
    """
    try:
        report = ReportManager.get_report_by_simulation(simulation_id)
        
        has_report = report is not None
        report_status = report.status.value if report else None
        report_id = report.report_id if report else None
        
        # 只有报告完成后才解锁interview
        interview_unlocked = has_report and report.status == ReportStatus.COMPLETED
        
        return jsonify({
            "success": True,
            "data": {
                "simulation_id": simulation_id,
                "has_report": has_report,
                "report_status": report_status,
                "report_id": report_id,
                "interview_unlocked": interview_unlocked
            }
        })
        
    except Exception as e:
        logger.error(f"检查报告状态失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


# ============== Agent 日志接口 ==============

@report_bp.route('/<report_id>/agent-log', methods=['GET'])
def get_agent_log(report_id: str):
    """
    获取 Report Agent 的详细执行日志
    
    实时获取报告生成过程中的每一步动作，包括：
    - 报告开始、规划开始/完成
    - 每个章节的开始、工具调用、LLM响应、完成
    - 报告完成或失败
    
    Query参数：
        from_line: 从第几行开始读取（可选，默认0，用于增量获取）
    
    返回：
        {
            "success": true,
            "data": {
                "logs": [
                    {
                        "timestamp": "2025-12-13T...",
                        "elapsed_seconds": 12.5,
                        "report_id": "report_xxxx",
                        "action": "tool_call",
                        "stage": "generating",
                        "section_title": "执行摘要",
                        "section_index": 1,
                        "details": {
                            "tool_name": "insight_forge",
                            "parameters": {...},
                            ...
                        }
                    },
                    ...
                ],
                "total_lines": 25,
                "from_line": 0,
                "has_more": false
            }
        }
    """
    try:
        from_line = request.args.get('from_line', 0, type=int)
        
        log_data = ReportManager.get_agent_log(report_id, from_line=from_line)
        
        return jsonify({
            "success": True,
            "data": log_data
        })
        
    except Exception as e:
        logger.error(f"获取Agent日志失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@report_bp.route('/<report_id>/agent-log/stream', methods=['GET'])
def stream_agent_log(report_id: str):
    """
    获取完整的 Agent 日志（一次性获取全部）
    
    返回：
        {
            "success": true,
            "data": {
                "logs": [...],
                "count": 25
            }
        }
    """
    try:
        logs = ReportManager.get_agent_log_stream(report_id)
        
        return jsonify({
            "success": True,
            "data": {
                "logs": logs,
                "count": len(logs)
            }
        })
        
    except Exception as e:
        logger.error(f"获取Agent日志失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


# ============== 控制台日志接口 ==============

@report_bp.route('/<report_id>/console-log', methods=['GET'])
def get_console_log(report_id: str):
    """
    获取 Report Agent 的控制台输出日志
    
    实时获取报告生成过程中的控制台输出（INFO、WARNING等），
    这与 agent-log 接口返回的结构化 JSON 日志不同，
    是纯文本格式的控制台风格日志。
    
    Query参数：
        from_line: 从第几行开始读取（可选，默认0，用于增量获取）
    
    返回：
        {
            "success": true,
            "data": {
                "logs": [
                    "[19:46:14] INFO: 搜索完成: 找到 15 条相关事实",
                    "[19:46:14] INFO: 图谱搜索: graph_id=xxx, query=...",
                    ...
                ],
                "total_lines": 100,
                "from_line": 0,
                "has_more": false
            }
        }
    """
    try:
        from_line = request.args.get('from_line', 0, type=int)
        
        log_data = ReportManager.get_console_log(report_id, from_line=from_line)
        
        return jsonify({
            "success": True,
            "data": log_data
        })
        
    except Exception as e:
        logger.error(f"获取控制台日志失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@report_bp.route('/<report_id>/console-log/stream', methods=['GET'])
def stream_console_log(report_id: str):
    """
    获取完整的控制台日志（一次性获取全部）
    
    返回：
        {
            "success": true,
            "data": {
                "logs": [...],
                "count": 100
            }
        }
    """
    try:
        logs = ReportManager.get_console_log_stream(report_id)
        
        return jsonify({
            "success": True,
            "data": {
                "logs": logs,
                "count": len(logs)
            }
        })
        
    except Exception as e:
        logger.error(f"获取控制台日志失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


# ============== 工具调用接口（供调试使用）==============

@report_bp.route('/tools/search', methods=['POST'])
def search_graph_tool():
    """
    图谱搜索工具接口（供调试使用）
    
    请求（JSON）：
        {
            "graph_id": "endora_xxxx",
            "query": "搜索查询",
            "limit": 10
        }
    """
    try:
        data = request.get_json() or {}
        
        graph_id = data.get('graph_id')
        query = data.get('query')
        limit = data.get('limit', 10)
        
        if not graph_id or not query:
            return jsonify({
                "success": False,
                "error": t('api.requireGraphIdAndQuery')
            }), 400
        
        from ..services.zep_tools import ZepToolsService
        
        tools = ZepToolsService()
        result = tools.search_graph(
            graph_id=graph_id,
            query=query,
            limit=limit
        )
        
        return jsonify({
            "success": True,
            "data": result.to_dict()
        })
        
    except Exception as e:
        logger.error(f"图谱搜索失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@report_bp.route('/tools/statistics', methods=['POST'])
def get_graph_statistics_tool():
    """
    图谱统计工具接口（供调试使用）
    
    请求（JSON）：
        {
            "graph_id": "endora_xxxx"
        }
    """
    try:
        data = request.get_json() or {}
        
        graph_id = data.get('graph_id')
        
        if not graph_id:
            return jsonify({
                "success": False,
                "error": t('api.requireGraphId')
            }), 400
        
        from ..services.zep_tools import ZepToolsService
        
        tools = ZepToolsService()
        result = tools.get_graph_statistics(graph_id)
        
        return jsonify({
            "success": True,
            "data": result
        })
        
    except Exception as e:
        logger.error(f"获取图谱统计失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500
