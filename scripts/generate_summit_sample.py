from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "docs" / "summit-liaison-sample.pdf"

PAGE_W, PAGE_H = A4
PAPER = colors.HexColor("#F5F2EA")
PAPER_DEEP = colors.HexColor("#E8E2D5")
INK = colors.HexColor("#171614")
INK_SOFT = colors.HexColor("#3A3731")
MUTED = colors.HexColor("#6F6A60")
LINE = colors.HexColor("#CFC8BA")
ACCENT = colors.HexColor("#3F7778")
ACCENT_DEEP = colors.HexColor("#245456")
ACCENT_WASH = colors.HexColor("#DCEBE7")
WHITE = colors.HexColor("#FFFDF8")

UNICODE_FONT_PATH = Path("/System/Library/Fonts/STHeiti Medium.ttc")
pdfmetrics.registerFont(TTFont("PortfolioUnicode", str(UNICODE_FONT_PATH), subfontIndex=0))
FONT = "PortfolioUnicode"

body_style = ParagraphStyle(
    "body",
    fontName=FONT,
    fontSize=9.4,
    leading=16,
    textColor=INK_SOFT,
    wordWrap="CJK",
)
small_style = ParagraphStyle(
    "small",
    fontName=FONT,
    fontSize=7.6,
    leading=12,
    textColor=MUTED,
    wordWrap="CJK",
)
label_style = ParagraphStyle(
    "label",
    fontName=FONT,
    fontSize=6.8,
    leading=10,
    textColor=ACCENT_DEEP,
    wordWrap="CJK",
)


def paragraph(c, text, x, y, width, style=body_style, gap=4):
    p = Paragraph(text, style)
    _, height = p.wrap(width, PAGE_H)
    p.drawOn(c, x, y - height)
    return y - height - gap


def text(c, value, x, y, size=9, color=INK, font=FONT):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, y, value)


def right_text(c, value, x, y, size=9, color=INK, font=FONT):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawRightString(x, y, value)


def rule(c, x1, y1, x2, y2= None, color=LINE, width=0.6):
    y2 = y1 if y2 is None else y2
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)


def rounded_box(c, x, y, w, h, fill, stroke=None, radius=8):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(0.6)
        c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
    else:
        c.roundRect(x, y, w, h, radius, fill=1, stroke=0)


def page_header(c, page, section):
    left = 18 * mm
    right = PAGE_W - 18 * mm
    text(c, "郑文凤  /  峰会对接与活动执行", left, PAGE_H - 14 * mm, 7.5, MUTED)
    right_text(c, f"{section}  ·  {page:02d} / 04", right, PAGE_H - 14 * mm, 7.2, MUTED)
    rule(c, left, PAGE_H - 18 * mm, right, color=LINE)


def page_footer(c):
    left = 18 * mm
    right = PAGE_W - 18 * mm
    rule(c, left, 15 * mm, right, color=LINE)
    text(c, "PORTFOLIO 2026  /  PUBLIC VERSION", left, 10 * mm, 6.5, MUTED)
    right_text(c, "所有嘉宾信息均已脱敏", right, 10 * mm, 6.5, MUTED)


def cover(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    margin = 18 * mm
    panel_w = 92 * mm
    c.setFillColor(ACCENT_DEEP)
    c.rect(0, 0, panel_w, PAGE_H, fill=1, stroke=0)

    text(c, "LIAISON", 16 * mm, PAGE_H - 28 * mm, 8, ACCENT_WASH, "Helvetica")
    text(c, "/ OPERATIONS", 16 * mm, PAGE_H - 34 * mm, 8, ACCENT_WASH, "Helvetica")
    text(c, "05", 16 * mm, PAGE_H - 57 * mm, 66, WHITE, "Helvetica-Bold")
    text(c, "商务对接", 16 * mm, PAGE_H - 90 * mm, 28, WHITE)
    text(c, "与会务统筹", 16 * mm, PAGE_H - 104 * mm, 28, WHITE)

    paragraph(
        c,
        "从第一次触达，到嘉宾顺利落座、上台、返程。把多线程沟通变成可检查的交付。",
        16 * mm,
        PAGE_H - 122 * mm,
        panel_w - 32 * mm,
        ParagraphStyle(
            "cover-copy",
            fontName=FONT,
            fontSize=10.5,
            leading=21,
            textColor=ACCENT_WASH,
            wordWrap="CJK",
        ),
    )

    text(c, "2026", 16 * mm, 34 * mm, 9, ACCENT_WASH, "Helvetica")
    text(c, "第三届中国主题公园战略营销峰会", 16 * mm, 26 * mm, 8.5, WHITE)
    text(c, "嘉宾指引手册 × 共享协作表 × 主持与颁奖台本", 16 * mm, 19 * mm, 7.5, ACCENT_WASH)

    x = panel_w + 18 * mm
    right_edge = PAGE_W - 18 * mm
    text(c, "PUBLIC SAMPLE", x, PAGE_H - 28 * mm, 7, ACCENT_DEEP, "Helvetica")
    right_text(c, "PORTFOLIO 2026", right_edge, PAGE_H - 28 * mm, 7, MUTED, "Helvetica")
    rule(c, x, PAGE_H - 33 * mm, right_edge, color=LINE)

    title_style = ParagraphStyle(
        "cover-title",
        fontName=FONT,
        fontSize=22,
        leading=36,
        textColor=INK,
        wordWrap="CJK",
    )
    paragraph(c, "峰会对接与<br/>主持执行样例", x, PAGE_H - 49 * mm, 70 * mm, title_style, 12)
    paragraph(
        c,
        "这是一份面向公开招聘的脱敏工作样张。保留真实项目的流程、交付结构与执行方法，移除所有嘉宾姓名、机构、联络方式及现场识别信息。",
        x,
        PAGE_H - 87 * mm,
        70 * mm,
        ParagraphStyle(
            "cover-body",
            fontName=FONT,
            fontSize=9.5,
            leading=19,
            textColor=INK_SOFT,
            wordWrap="CJK",
        ),
    )

    meta_y = 111 * mm
    rows = [
        ("ROLE", "嘉宾对接 / 会务统筹"),
        ("SCALE", "300+ 行业高管"),
        ("CONTACT", "数十位专家与嘉宾"),
        ("OUTPUT", "4 类核心协作文件"),
    ]
    for i, (key, value) in enumerate(rows):
        y = meta_y - i * 17 * mm
        rule(c, x, y + 9 * mm, right_edge, color=LINE)
        text(c, key, x, y, 6.5, ACCENT_DEEP, "Helvetica")
        text(c, value, x + 31 * mm, y, 9.2, INK)

    rounded_box(c, x, 24 * mm, right_edge - x, 42 * mm, ACCENT_WASH, radius=10)
    text(c, "PRIVACY NOTE", x + 8 * mm, 52 * mm, 6.5, ACCENT_DEEP, "Helvetica")
    paragraph(
        c,
        "本样张不包含任何真实嘉宾资料、私人联系方式或未公开议程。现场照片另经不可逆遮挡处理。",
        x + 8 * mm,
        44 * mm,
        right_edge - x - 16 * mm,
        small_style,
    )
    page_footer(c)


def spread_1(c):
    page_header(c, 2, "METHOD / 01")
    left = 18 * mm
    right = PAGE_W - 18 * mm
    content_w = right - left

    text(c, "01", left, PAGE_H - 35 * mm, 9, ACCENT, "Helvetica")
    text(c, "对接不是传话，", left, PAGE_H - 47 * mm, 23, INK)
    text(c, "而是把承诺推到落地。", left, PAGE_H - 59 * mm, 23, INK)
    paragraph(
        c,
        "核心工作不是“通知到了”，而是确认对方收到、理解、能按时到场，并在临时变化发生时快速完成跨团队交接。",
        left,
        PAGE_H - 70 * mm,
        132 * mm,
        body_style,
    )

    stages = [
        ("01", "提前摸底", "身份、角色、需求与敏感点一次问清"),
        ("02", "行程确认", "车次、入住、用餐、到场时间逐项核对"),
        ("03", "现场交付", "手册、动线、座位、催场与临时需求"),
        ("04", "会后闭环", "感谢、采访素材与反馈统一归档"),
    ]
    gap = 4 * mm
    col_w = (content_w - gap * 3) / 4
    y = PAGE_H - 132 * mm
    h = 49 * mm
    for i, (num, title, desc) in enumerate(stages):
        x = left + i * (col_w + gap)
        rounded_box(c, x, y, col_w, h, WHITE, LINE, 7)
        text(c, num, x + 5 * mm, y + h - 10 * mm, 8, ACCENT_DEEP, "Helvetica-Bold")
        text(c, title, x + 5 * mm, y + h - 20 * mm, 10.2, INK)
        paragraph(c, desc, x + 5 * mm, y + h - 26 * mm, col_w - 10 * mm, small_style)
        if i < 3:
            c.setStrokeColor(ACCENT)
            c.setLineWidth(1)
            c.line(x + col_w + 1 * mm, y + h / 2, x + col_w + 3 * mm, y + h / 2)

    text(c, "两天现场 / 一条时间线", left, PAGE_H - 151 * mm, 12, INK)
    timeline_top = PAGE_H - 160 * mm
    timeline_items = [
        ("D-7", "信息收集", "确认角色、议程、住宿与交通"),
        ("D-3", "材料交付", "发送路线、签到、用餐与联系人文件"),
        ("D-1", "最终确认", "复核到场时间、演讲稿与现场需求"),
        ("DAY", "现场流转", "签到、落座、催场、媒体采访与合影"),
        ("D+1", "资料归档", "感谢、照片、反馈与复盘表统一整理"),
    ]
    for i, (day, title, desc) in enumerate(timeline_items):
        y = timeline_top - i * 20 * mm
        c.setFillColor(ACCENT if i == 3 else ACCENT_WASH)
        c.circle(left + 2.2 * mm, y, 2.2 * mm, fill=1, stroke=0)
        if i < 4:
            rule(c, left + 2.2 * mm, y - 2.2 * mm, left + 2.2 * mm, y - 17.8 * mm, color=LINE, width=0.9)
        text(c, day, left + 8 * mm, y - 1.5 * mm, 7, ACCENT_DEEP, "Helvetica")
        text(c, title, left + 25 * mm, y - 1.5 * mm, 9.2, INK)
        text(c, desc, left + 56 * mm, y - 1.5 * mm, 8.6, MUTED)

    box_x = left + 121 * mm
    box_w = right - box_x
    rounded_box(c, box_x, 31 * mm, box_w, 55 * mm, ACCENT_DEEP, radius=9)
    text(c, "ONE-PAGE RULE", box_x + 7 * mm, 76 * mm, 6.5, ACCENT_WASH, "Helvetica")
    paragraph(
        c,
        "一页内看清：<br/>谁 / 在哪 / 几点 / 找谁。",
        box_x + 7 * mm,
        67 * mm,
        box_w - 14 * mm,
        ParagraphStyle(
            "rule",
            fontName=FONT,
            fontSize=13,
            leading=21,
            textColor=WHITE,
            wordWrap="CJK",
        ),
    )
    text(c, "信息越集中，现场越从容。", box_x + 7 * mm, 38 * mm, 7.8, ACCENT_WASH)
    page_footer(c)


def spread_2(c):
    page_header(c, 3, "SYSTEM / 02")
    left = 18 * mm
    right = PAGE_W - 18 * mm
    content_w = right - left

    text(c, "02", left, PAGE_H - 35 * mm, 9, ACCENT, "Helvetica")
    text(c, "共享文档，", left, PAGE_H - 47 * mm, 23, INK)
    text(c, "把信息差降到最低。", left, PAGE_H - 59 * mm, 23, INK)
    paragraph(
        c,
        "把嘉宾状态、交通、住宿、演讲需求、现场负责人和变更记录放进同一套协作逻辑。主办方、会务、媒体与当事人看到的是同一份最新版本。",
        left,
        PAGE_H - 70 * mm,
        132 * mm,
        body_style,
    )

    table_x = left
    table_y = PAGE_H - 99 * mm
    table_w = content_w
    row_h = 9 * mm
    widths = [20, 38, 60, 43]
    headers = ["ID", "阶段", "关键字段", "状态"]
    c.setFillColor(ACCENT_DEEP)
    c.rect(table_x, table_y, table_w, row_h, fill=1, stroke=0)
    text(c, "ID", table_x + 4 * mm, table_y + 3.7 * mm, 7, WHITE, "Helvetica")
    text(c, "阶段", table_x + widths[0] * mm + 4 * mm, table_y + 3.7 * mm, 7, WHITE)
    text(c, "关键字段", table_x + (widths[0] + widths[1]) * mm + 4 * mm, table_y + 3.7 * mm, 7, WHITE)
    text(c, "状态", table_x + (widths[0] + widths[1] + widths[2]) * mm + 4 * mm, table_y + 3.7 * mm, 7, WHITE)

    rows = [
        ("A-01", "邀约确认", "角色 / 分享主题 / 时间窗口", "已完成"),
        ("A-02", "行程确认", "到达时间 / 入住 / 用餐 / 用车", "跟进中"),
        ("A-03", "材料交付", "指引手册 / 座位 / 联系人", "待回执"),
        ("A-04", "现场执行", "签到 / 催场 / 采访 / 合影", "待执行"),
    ]
    for i, row in enumerate(rows):
        y = table_y - (i + 1) * row_h
        c.setFillColor(WHITE if i % 2 == 0 else PAPER_DEEP)
        c.rect(table_x, y, table_w, row_h, fill=1, stroke=0)
        text(c, row[0], table_x + 4 * mm, y + 3.5 * mm, 7.7, ACCENT_DEEP, "Helvetica-Bold")
        text(c, row[1], table_x + widths[0] * mm + 4 * mm, y + 3.5 * mm, 8, INK)
        text(c, row[2], table_x + (widths[0] + widths[1]) * mm + 4 * mm, y + 3.5 * mm, 7.7, MUTED)
        text(c, row[3], table_x + (widths[0] + widths[1] + widths[2]) * mm + 4 * mm, y + 3.5 * mm, 7.7, ACCENT_DEEP)
    rule(c, table_x, table_y - len(rows) * row_h, table_x + table_w, table_y - len(rows) * row_h, color=LINE)
    text(c, "示例为字段结构，不含真实嘉宾数据。", left, table_y - len(rows) * row_h - 6 * mm, 6.8, MUTED)

    card_y = 69 * mm
    card_h = 74 * mm
    col_gap = 5 * mm
    col_w = (content_w - col_gap) / 2
    rounded_box(c, left, card_y, col_w, card_h, WHITE, LINE, 9)
    text(c, "嘉宾指引手册", left + 6 * mm, card_y + card_h - 12 * mm, 11, INK)
    text(c, "INPUT  →  ACTION  →  RECEIPT", left + 6 * mm, card_y + card_h - 19 * mm, 6.3, ACCENT_DEEP, "Helvetica")
    handbook_lines = [
        "• 会议日期、地点与天气提醒",
        "• 入住、签到、用餐、交通动线",
        "• 发言时间、催场节点与现场支持",
        "• 变更渠道与紧急联络机制",
    ]
    paragraph(c, "<br/>".join(handbook_lines), left + 6 * mm, card_y + card_h - 26 * mm, col_w - 12 * mm, small_style)
    rounded_box(c, left + 6 * mm, card_y + 7 * mm, col_w - 12 * mm, 15 * mm, ACCENT_WASH, radius=5)
    text(c, "目标：对方打开一页，就知道下一步。", left + 10 * mm, card_y + 13 * mm, 8.3, ACCENT_DEEP)

    x2 = left + col_w + col_gap
    rounded_box(c, x2, card_y, col_w, card_h, INK, radius=9)
    text(c, "主持 / 颁奖台本节选", x2 + 6 * mm, card_y + card_h - 12 * mm, 11, WHITE)
    text(c, "CUE  ·  TRANSITION  ·  RECOVERY", x2 + 6 * mm, card_y + card_h - 19 * mm, 6.3, ACCENT_WASH, "Helvetica")
    script_lines = [
        "[开场]  欢迎语 → 安全提示 → 议程总览",
        "[串场]  上一位收束 → 下一位介绍 → 掌声引导",
        "[仪式]  嘉宾站位 → 物料确认 → 倒数与合影",
        "[应急]  延迟 / 空场 / 临时调整的替代话术",
    ]
    paragraph(
        c,
        "<br/>".join(script_lines),
        x2 + 6 * mm,
        card_y + card_h - 26 * mm,
        col_w - 12 * mm,
        ParagraphStyle(
            "script",
            fontName=FONT,
            fontSize=7.7,
            leading=14,
            textColor=ACCENT_WASH,
            wordWrap="CJK",
        ),
    )
    text(c, "台本不是台词堆叠，而是现场状态机。", x2 + 6 * mm, card_y + 9 * mm, 8.2, ACCENT_WASH)
    page_footer(c)


def spread_3(c):
    page_header(c, 4, "PROOF / 03")
    left = 18 * mm
    right = PAGE_W - 18 * mm
    content_w = right - left

    text(c, "03", left, PAGE_H - 35 * mm, 9, ACCENT, "Helvetica")
    text(c, "把沟通结果，", left, PAGE_H - 47 * mm, 23, INK)
    text(c, "变成可验证的现场。", left, PAGE_H - 59 * mm, 23, INK)
    paragraph(
        c,
        "我关注的不是“聊得好不好”，而是对方是否准时出现、是否知道下一步、临时需求是否有人接住，以及会后是否能留下可复用的关系与内容。",
        left,
        PAGE_H - 70 * mm,
        132 * mm,
        body_style,
    )

    stats = [
        ("300+", "行业高管顺利出席"),
        ("数十位", "专家与嘉宾独立接洽"),
        ("4 SET", "核心协作与内容文件"),
        ("4500+", "峰会线上直播观看"),
    ]
    gap = 3 * mm
    stat_w = (content_w - gap * 3) / 4
    y = PAGE_H - 111 * mm
    for i, (number, label) in enumerate(stats):
        x = left + i * (stat_w + gap)
        rounded_box(c, x, y, stat_w, 31 * mm, WHITE, LINE, 8)
        text(c, number, x + 5 * mm, y + 15 * mm, 21 if i not in (1, 2) else 16, INK, "Helvetica-Bold" if i not in (1, 2) else FONT)
        paragraph(c, label, x + 5 * mm, y + 9 * mm, stat_w - 10 * mm, small_style)

    text(c, "我实际承担的对接链路", left, PAGE_H - 131 * mm, 12, INK)
    flow = [
        ("01", "商务接洽", "确认参会意向与嘉宾角色"),
        ("02", "需求梳理", "行程、发言、采访与特殊安排"),
        ("03", "文件交付", "手册、动线、日程与回执"),
        ("04", "现场统筹", "签到、催场、环节衔接与救场"),
        ("05", "会后收束", "感谢、素材、反馈与关系维护"),
    ]
    flow_y = 95 * mm
    col_w = content_w / len(flow)
    for i, (num, title, desc) in enumerate(flow):
        x = left + i * col_w
        text(c, num, x, flow_y + 25 * mm, 7, ACCENT_DEEP, "Helvetica-Bold")
        text(c, title, x, flow_y + 17 * mm, 9.2, INK)
        paragraph(c, desc, x, flow_y + 13 * mm, col_w - 4 * mm, small_style)
        if i < len(flow) - 1:
            rule(c, x + col_w - 3 * mm, flow_y + 21 * mm, x + col_w - 1 * mm, color=ACCENT, width=1)
    rule(c, left, flow_y + 10 * mm, right, color=LINE)

    note_y = 28 * mm
    note_h = 32 * mm
    rounded_box(c, left, note_y, content_w, note_h, ACCENT_WASH, radius=8)
    paragraph(
        c,
        "公开版本处理规则",
        left + 7 * mm,
        note_y + note_h - 7 * mm,
        70 * mm,
        label_style,
    )
    paragraph(
        c,
        "嘉宾姓名、机构、电话、微信/二维码、证件与桌面桌牌全部移除；现场照片中的嘉宾面部、胸牌与文件信息做二次遮挡。本页只展示工作方法与匿名化样例。",
        left + 7 * mm,
        note_y + note_h - 14 * mm,
        content_w - 14 * mm,
        small_style,
    )
    page_footer(c)


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=A4)
    c.setTitle("峰会对接与主持执行样例 - 脱敏版")
    c.setAuthor("郑文凤")
    c.setSubject("商务对接、嘉宾服务与会务统筹能力样张")
    cover(c)
    c.showPage()
    spread_1(c)
    c.showPage()
    spread_2(c)
    c.showPage()
    spread_3(c)
    c.showPage()
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    main()
