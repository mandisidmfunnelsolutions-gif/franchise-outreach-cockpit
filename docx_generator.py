"""
DOCX Report Generator for SA Franchise AI Adoption Study.
University of Pretoria — BCom (Hons) Strategic Business Management.
Generates academic-grade Word documents (.docx) showing questions, responses,
and explicit percentages for all slider ratings.
"""

import io
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

# Color Palette
NAVY_PRIMARY = RGBColor(30, 58, 138)       # #1E3A8A - Deep Academic Navy
INDIGO_ACCENT = RGBColor(67, 56, 202)      # #4338CA - Royal Indigo
SLATE_DARK = RGBColor(15, 23, 42)          # #0F172A - Body text
SLATE_MUTED = RGBColor(100, 116, 139)      # #64748B - Muted/Metadata
EMERALD_GREEN = RGBColor(5, 150, 105)      # #059669 - High rating
AMBER_WARNING = RGBColor(217, 119, 6)      # #D97706 - Moderate rating
HEX_LIGHT_BG = "F1F5F9"                    # Slate 100
HEX_NAVY_BG = "1E3A8A"                     # Navy
HEX_BORDER = "CBD5E1"                      # Slate 300

def set_cell_background(cell, hex_color):
    """Set background color for a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner padding for a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)

def add_header_banner(doc, title="SURVEY RESPONSE & INTERVIEW TRANSCRIPT"):
    """Adds the University of Pretoria academic header block."""
    p_inst = doc.add_paragraph()
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(2)
    run_inst = p_inst.add_run("UNIVERSITY OF PRETORIA")
    run_inst.bold = True
    run_inst.font.name = "Calibri"
    run_inst.font.size = Pt(13)
    run_inst.font.color.rgb = NAVY_PRIMARY

    p_dept = doc.add_paragraph()
    p_dept.paragraph_format.space_before = Pt(0)
    p_dept.paragraph_format.space_after = Pt(2)
    run_dept = p_dept.add_run("Faculty of Economic and Management Sciences | Department of Business Management")
    run_dept.font.name = "Calibri"
    run_dept.font.size = Pt(9.5)
    run_dept.font.color.rgb = SLATE_MUTED

    p_topic = doc.add_paragraph()
    p_topic.paragraph_format.space_before = Pt(2)
    p_topic.paragraph_format.space_after = Pt(8)
    run_topic = p_topic.add_run("BCom (Honours) Strategic Business Management Research Study:\n")
    run_topic.bold = True
    run_topic.font.name = "Calibri"
    run_topic.font.size = Pt(10)
    run_topic.font.color.rgb = SLATE_DARK
    
    run_sub = p_topic.add_run("“The adoption of artificial intelligence for operational efficiency in food and beverage franchises in Gauteng, South Africa”")
    run_sub.italic = True
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(10)
    run_sub.font.color.rgb = INDIGO_ACCENT

    # Title Banner
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(12)
    p_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run(f"— {title} —")
    run_title.bold = True
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(14)
    run_title.font.color.rgb = NAVY_PRIMARY

def add_section_header(doc, section_title):
    """Adds a bold styled section divider."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(section_title)
    run.bold = True
    run.font.name = "Calibri"
    run.font.size = Pt(12)
    run.font.color.rgb = NAVY_PRIMARY

def add_question_block(doc, question_num_text, response_text, is_slider=False, slider_val=None, slider_scale=5, interpretation=""):
    """Adds a question and formatted answer block with explicit percentage for sliders."""
    # Question line
    p_q = doc.add_paragraph()
    p_q.paragraph_format.space_before = Pt(6)
    p_q.paragraph_format.space_after = Pt(2)
    p_q.paragraph_format.left_indent = Inches(0.1)
    p_q.paragraph_format.keep_with_next = True
    
    run_q = p_q.add_run(f"Q: {question_num_text}")
    run_q.bold = True
    run_q.font.name = "Calibri"
    run_q.font.size = Pt(10)
    run_q.font.color.rgb = SLATE_DARK

    # If slider, append badge with exact percentage
    if is_slider and slider_val is not None:
        try:
            val_int = int(slider_val)
            pct = round((val_int / slider_scale) * 100)
            
            p_badge = doc.add_paragraph()
            p_badge.paragraph_format.space_before = Pt(1)
            p_badge.paragraph_format.space_after = Pt(2)
            p_badge.paragraph_format.left_indent = Inches(0.3)
            p_badge.paragraph_format.keep_with_next = True

            run_lbl = p_badge.add_run("Quantitative Scale Rating: ")
            run_lbl.font.name = "Calibri"
            run_lbl.font.size = Pt(9.5)
            run_lbl.font.color.rgb = SLATE_MUTED

            run_score = p_badge.add_run(f"{val_int} / {slider_scale}  ({pct}%)")
            run_score.bold = True
            run_score.font.name = "Calibri"
            run_score.font.size = Pt(10)
            run_score.font.color.rgb = INDIGO_ACCENT

            if interpretation:
                run_interp = p_badge.add_run(f"  [{interpretation}]")
                run_interp.italic = True
                run_interp.font.name = "Calibri"
                run_interp.font.size = Pt(9.5)
                run_interp.font.color.rgb = SLATE_MUTED
        except (ValueError, TypeError):
            pass

    # Response line
    p_ans = doc.add_paragraph()
    p_ans.paragraph_format.space_before = Pt(1)
    p_ans.paragraph_format.space_after = Pt(6)
    p_ans.paragraph_format.left_indent = Inches(0.3)

    run_ans_prefix = p_ans.add_run("Response: ")
    run_ans_prefix.bold = True
    run_ans_prefix.font.name = "Calibri"
    run_ans_prefix.font.size = Pt(10)
    run_ans_prefix.font.color.rgb = INDIGO_ACCENT

    clean_text = str(response_text).strip() if response_text is not None and str(response_text).strip() else "[No qualitative answer provided]"
    run_ans = p_ans.add_run(clean_text)
    run_ans.font.name = "Calibri"
    run_ans.font.size = Pt(10)
    run_ans.font.color.rgb = SLATE_DARK
    if clean_text == "[No qualitative answer provided]":
        run_ans.italic = True
        run_ans.font.color.rgb = SLATE_MUTED

def format_date_str(iso_str):
    """Safely converts ISO timestamp to readable date string."""
    if not iso_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%B %d, %Y at %H:%M SAST")
    except Exception:
        return str(iso_str)

def get_employee_response_label(scale_val):
    labels = {
        1: "1 / 5 (20%) — Highly Resistant",
        2: "2 / 5 (40%) — Hesitant / Cautious",
        3: "3 / 5 (60%) — Neutral / Moderate",
        4: "4 / 5 (80%) — Receptive / Enthusiastic",
        5: "5 / 5 (100%) — Highly Enthusiastic / Champions"
    }
    return labels.get(int(scale_val), f"{scale_val} / 5 ({int(scale_val)*20}%)")

def build_single_survey_docx(record):
    """
    Builds an academic .docx for a single survey response record.
    Returns: BytesIO object of the generated .docx file.
    """
    doc = Document()
    
    # Set page margins to 1 inch standard
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    data = record.get("response_data", {})
    record_id = record.get("id", "N/A")
    created_at = record.get("created_at", "")

    # 1. Header Banner
    add_header_banner(doc, title="ACADEMIC INTERVIEW & SURVEY RECORD")

    # 2. Participant Profile Table
    add_section_header(doc, "PARTICIPANT & ORGANISATION PROFILE")
    
    table = doc.add_table(rows=5, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    profile_data = [
        ("Full Name (Confidential):", data.get("participantName", "Anonymous Respondent")),
        ("Franchise / Organisation Name:", data.get("franchiseName", "Not Specified")),
        ("Role in the Business:", data.get("role", "Not Specified")),
        ("Contact Verification (Email / Tel):", data.get("contactInfo", "N/A")),
        ("Submission Timestamp & Record ID:", f"{format_date_str(created_at)}  (ID: {record_id[:8]})")
    ]

    for idx, (label, val) in enumerate(profile_data):
        cell_lbl, cell_val = table.rows[idx].cells
        cell_lbl.width = Inches(2.5)
        cell_val.width = Inches(4.3)
        
        set_cell_background(cell_lbl, HEX_LIGHT_BG)
        set_cell_margins(cell_lbl, top=80, bottom=80, left=120, right=120)
        set_cell_margins(cell_val, top=80, bottom=80, left=120, right=120)
        
        p_l = cell_lbl.paragraphs[0]
        p_l.paragraph_format.space_before = Pt(2)
        p_l.paragraph_format.space_after = Pt(2)
        r_l = p_l.add_run(label)
        r_l.bold = True
        r_l.font.name = "Calibri"
        r_l.font.size = Pt(9.5)
        r_l.font.color.rgb = SLATE_DARK

        p_v = cell_val.paragraphs[0]
        p_v.paragraph_format.space_before = Pt(2)
        p_v.paragraph_format.space_after = Pt(2)
        r_v = p_v.add_run(str(val))
        r_v.font.name = "Calibri"
        r_v.font.size = Pt(9.5)
        r_v.font.color.rgb = SLATE_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # 3. Section 1: AI Usage & Adoption
    add_section_header(doc, "1. AI USAGE & ADOPTION")
    add_question_block(
        doc,
        "1.1 What are the types of AI-tools or AI-systems that you use?",
        data.get("q1_1_toolsUsed")
    )
    add_question_block(
        doc,
        "1.2 Who in the business use the AI tools?",
        data.get("q1_2_whoUsesTools")
    )
    add_question_block(
        doc,
        "1.3 When did your franchise or business start to use AI?",
        data.get("q1_3_whenStarted")
    )

    # 4. Section 2: Daily Operations
    add_section_header(doc, "2. DAILY OPERATIONS")
    add_question_block(
        doc,
        "2. How is AI used in the daily operations of your franchise?",
        data.get("q2_dailyOperations")
    )
    activities_list = data.get("q2_1_activities", [])
    activities_str = ", ".join(activities_list) if isinstance(activities_list, list) and activities_list else str(activities_list)
    add_question_block(
        doc,
        "2.1 Do you use AI for activities such as stock management, ordering, customer service, scheduling of staff or marketing?",
        f"Selected Activities: {activities_str or 'None'}"
    )
    add_question_block(
        doc,
        "2.1 (Qualitative Details) Please elaborate on the activities selected above:",
        data.get("q2_1_activitiesDetails")
    )

    # 5. Section 3: Operational Efficiency
    add_section_header(doc, "3. OPERATIONAL EFFICIENCY")
    add_question_block(
        doc,
        "3. How do you understand the role of AI improving the organisation's operational efficiency?",
        data.get("q3_roleInEfficiency")
    )
    improvements_list = data.get("q3_1_improvements", [])
    improvements_str = ", ".join(improvements_list) if isinstance(improvements_list, list) and improvements_list else str(improvements_list)
    add_question_block(
        doc,
        "3.1 Has AI helped saved time, improve processes, reduce errors or support decision making?",
        f"Selected Improvements: {improvements_str or 'None'}"
    )
    add_question_block(
        doc,
        "3.1 (Qualitative Details) Please elaborate on the improvements selected above:",
        data.get("q3_1_improvementsDetails")
    )

    # 6. Section 4: Benefits and Challenges (WITH SLIDER PERCENTAGE)
    add_section_header(doc, "4. BENEFITS & CHALLENGES")
    add_question_block(
        doc,
        "4.1 What are the main benefits your business has experienced from the adoption of AI?",
        data.get("q4_1_benefits")
    )
    add_question_block(
        doc,
        "4.2 What are the challenges that have affected the use of AI such as costs, employee skills, technology limitations or training?",
        data.get("q4_2_challenges")
    )
    
    # Slider 4.3 with explicit percentage
    emp_scale = data.get("q4_3_employeeResponseScale", 3)
    emp_interp = get_employee_response_label(emp_scale)
    add_question_block(
        doc,
        "4.3 How do the employees respond to using AI? (Slider Scale: 1 = Resistant, 5 = Enthusiastic)",
        f"Quantitative Employee Sentiment: {emp_interp}",
        is_slider=True,
        slider_val=emp_scale,
        slider_scale=5,
        interpretation=emp_interp
    )
    add_question_block(
        doc,
        "4.3 (Qualitative Context) Please provide more qualitative context regarding the employees' response:",
        data.get("q4_3_employeeResponseText")
    )

    # 7. Section 5: External & Organisational Factors (WITH SLIDER PERCENTAGES)
    add_section_header(doc, "5. EXTERNAL & ORGANISATIONAL FACTORS")
    
    p_fac_intro = doc.add_paragraph()
    p_fac_intro.paragraph_format.space_before = Pt(4)
    p_fac_intro.paragraph_format.space_after = Pt(4)
    p_fac_intro.paragraph_format.left_indent = Inches(0.1)
    r_fac = p_fac_intro.add_run("Q: 5.1 Do factors such as internet reliability, tech access, staff skills, and cost influence adoption? (Scale 1–5):")
    r_fac.bold = True
    r_fac.font.name = "Calibri"
    r_fac.font.size = Pt(10)
    r_fac.font.color.rgb = SLATE_DARK

    factors = data.get("q5_1_factors", {})
    factor_items = [
        ("Internet Reliability", factors.get("internet", 3)),
        ("Access to Technology", factors.get("techAccess", 3)),
        ("Skills of Staff", factors.get("skills", 3)),
        ("Operational / Software Costs", factors.get("cost", 3))
    ]

    # Clean styled table for Section 5.1 Factors
    f_table = doc.add_table(rows=5, cols=3)
    f_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    f_table.autofit = False

    # Header Row
    headers = ["Adoption Factor / Dynamic", "Rating (1 - 5)", "Influence Percentage (%)"]
    for c_idx, h_text in enumerate(headers):
        c = f_table.rows[0].cells[c_idx]
        set_cell_background(c, HEX_NAVY_BG)
        set_cell_margins(c, top=80, bottom=80, left=120, right=120)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, (factor_name, rating_val) in enumerate(factor_items, start=1):
        row = f_table.rows[r_idx]
        val_int = int(rating_val) if rating_val is not None else 3
        pct_val = round((val_int / 5) * 100)

        c0, c1, c2 = row.cells
        c0.width = Inches(3.2)
        c1.width = Inches(1.8)
        c2.width = Inches(1.8)

        for cell in (c0, c1, c2):
            set_cell_background(cell, HEX_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=60, bottom=60, left=120, right=120)

        # Factor name
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(factor_name)
        r0.font.name = "Calibri"
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = SLATE_DARK

        # Score
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(f"{val_int} / 5")
        r1.bold = True
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = INDIGO_ACCENT

        # Percentage
        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_before = Pt(2)
        p2.paragraph_format.space_after = Pt(2)
        r2 = p2.add_run(f"{pct_val}%  Influence")
        r2.bold = True
        r2.font.name = "Calibri"
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = EMERALD_GREEN if pct_val >= 70 else (AMBER_WARNING if pct_val >= 40 else SLATE_MUTED)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_question_block(
        doc,
        "5.1 (Explanation) Please explain how these factors have influenced adoption:",
        data.get("q5_1_factorsExplanation")
    )

    support_bool = data.get("q5_2_franchisorSupport")
    support_str = "Yes" if support_bool is True else ("No" if support_bool is False else "Not Specified")
    add_question_block(
        doc,
        "5.2 Does the franchisor provide any support or guidance regarding the adoption of AI?",
        f"{support_str} — {data.get('q5_2_franchisorSupportDetails', '')}"
    )

    add_question_block(
        doc,
        "5.3 Are franchisees able to choose their own tools or are tools controlled by franchisors?",
        data.get("q5_3_toolChoiceControl")
    )

    # 8. Section 6: Conclusion
    add_section_header(doc, "6. CONCLUSION & FINAL REMARKS")
    add_question_block(
        doc,
        "Is there anything else you would like to add regarding your experience with the adoption of AI in your franchise?",
        data.get("conclusion")
    )

    # 9. Confidentiality Notice & Ethics Footer
    p_foot = doc.add_paragraph()
    p_foot.paragraph_format.space_before = Pt(20)
    p_foot.paragraph_format.space_after = Pt(4)
    run_foot = p_foot.add_run(
        "CONFIDENTIALITY & ACADEMIC INTEGRITY NOTICE:\n"
        "This document contains qualitative and quantitative empirical research data collected for the University of Pretoria "
        "BCom (Honours) Strategic Business Management degree. All personal identifiers are strictly masked in final academic dissertations "
        "and peer-reviewed publications in accordance with the UP Research Ethics Policy."
    )
    run_foot.font.name = "Calibri"
    run_foot.font.size = Pt(8.5)
    run_foot.font.color.rgb = SLATE_MUTED
    run_foot.italic = True

    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio

def build_consolidated_survey_docx(records):
    """
    Builds a single consolidated dossier containing all survey responses
    separated by page breaks.
    Returns: BytesIO object of the generated .docx file.
    """
    doc = Document()
    
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Title Cover Page
    add_header_banner(doc, title="CONSOLIDATED RESEARCH DOSSIER — ALL SURVEY RESPONSES")
    
    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.space_before = Pt(12)
    p_intro.paragraph_format.space_after = Pt(12)
    r_intro = p_intro.add_run(
        f"This master document compiles all empirical responses ({len(records)} total submissions) "
        f"captured via the South African Food & Beverage Franchise AI Adoption Web Survey.\n"
        f"Export Generated: {datetime.now().strftime('%B %d, %Y at %H:%M SAST')}"
    )
    r_intro.font.name = "Calibri"
    r_intro.font.size = Pt(11)
    r_intro.font.color.rgb = SLATE_DARK

    doc.add_page_break()

    for idx, record in enumerate(records):
        data = record.get("response_data", {})
        record_id = record.get("id", "N/A")
        created_at = record.get("created_at", "")
        participant_name = data.get("participantName", f"Participant #{idx+1}")
        franchise_name = data.get("franchiseName", "Franchise")

        # Header for individual record
        p_num = doc.add_paragraph()
        p_num.paragraph_format.space_before = Pt(6)
        p_num.paragraph_format.space_after = Pt(2)
        r_num = p_num.add_run(f"RESPONSE #{idx+1} — {participant_name} ({franchise_name})")
        r_num.bold = True
        r_num.font.name = "Calibri"
        r_num.font.size = Pt(13)
        r_num.font.color.rgb = NAVY_PRIMARY

        # Profile table
        table = doc.add_table(rows=5, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        profile_data = [
            ("Full Name:", participant_name),
            ("Franchise / Organisation:", franchise_name),
            ("Role in Business:", data.get("role", "Not Specified")),
            ("Contact Verification:", data.get("contactInfo", "N/A")),
            ("Submission Timestamp:", f"{format_date_str(created_at)}  (ID: {record_id[:8]})")
        ]

        for p_idx, (label, val) in enumerate(profile_data):
            cell_lbl, cell_val = table.rows[p_idx].cells
            cell_lbl.width = Inches(2.5)
            cell_val.width = Inches(4.3)
            set_cell_background(cell_lbl, HEX_LIGHT_BG)
            set_cell_margins(cell_lbl, top=60, bottom=60, left=100, right=100)
            set_cell_margins(cell_val, top=60, bottom=60, left=100, right=100)

            p_l = cell_lbl.paragraphs[0]
            p_l.paragraph_format.space_before = Pt(1)
            p_l.paragraph_format.space_after = Pt(1)
            r_l = p_l.add_run(label)
            r_l.bold = True
            r_l.font.name = "Calibri"
            r_l.font.size = Pt(9)
            r_l.font.color.rgb = SLATE_DARK

            p_v = cell_val.paragraphs[0]
            p_v.paragraph_format.space_before = Pt(1)
            p_v.paragraph_format.space_after = Pt(1)
            r_v = p_v.add_run(str(val))
            r_v.font.name = "Calibri"
            r_v.font.size = Pt(9)
            r_v.font.color.rgb = SLATE_DARK

        doc.add_paragraph().paragraph_format.space_after = Pt(2)

        # Questions
        add_section_header(doc, "1. AI Adoption & Tools Used")
        add_question_block(doc, "1.1 Tools/Systems Used:", data.get("q1_1_toolsUsed"))
        add_question_block(doc, "1.2 Users in Business:", data.get("q1_2_whoUsesTools"))
        add_question_block(doc, "1.3 When Adoption Started:", data.get("q1_3_whenStarted"))

        add_section_header(doc, "2. Daily Operations & Impact")
        add_question_block(doc, "2. Daily Operations Usage:", data.get("q2_dailyOperations"))
        activities_list = data.get("q2_1_activities", [])
        act_str = ", ".join(activities_list) if isinstance(activities_list, list) else str(activities_list)
        add_question_block(doc, "2.1 Activities Supported:", f"Activities: {act_str or 'None'}")
        add_question_block(doc, "2.1 Activities Details:", data.get("q2_1_activitiesDetails"))

        add_section_header(doc, "3. Operational Efficiency")
        add_question_block(doc, "3. Role in Efficiency:", data.get("q3_roleInEfficiency"))
        improvements_list = data.get("q3_1_improvements", [])
        imp_str = ", ".join(improvements_list) if isinstance(improvements_list, list) else str(improvements_list)
        add_question_block(doc, "3.1 Improvements Observed:", f"Observed: {imp_str or 'None'}")
        add_question_block(doc, "3.1 Improvements Details:", data.get("q3_1_improvementsDetails"))

        add_section_header(doc, "4. Benefits, Challenges & Employee Sentiment")
        add_question_block(doc, "4.1 Key Benefits:", data.get("q4_1_benefits"))
        add_question_block(doc, "4.2 Challenges Encountered:", data.get("q4_2_challenges"))
        emp_scale = data.get("q4_3_employeeResponseScale", 3)
        emp_interp = get_employee_response_label(emp_scale)
        add_question_block(
            doc,
            "4.3 Employee Response Rating (1 = Resistant, 5 = Enthusiastic):",
            f"Sentiment: {emp_interp}",
            is_slider=True,
            slider_val=emp_scale,
            slider_scale=5,
            interpretation=emp_interp
        )
        add_question_block(doc, "4.3 Employee Response Context:", data.get("q4_3_employeeResponseText"))

        add_section_header(doc, "5. External Factors & Franchisor Dynamics")
        factors = data.get("q5_1_factors", {})
        factor_items = [
            ("Internet Reliability", factors.get("internet", 3)),
            ("Access to Technology", factors.get("techAccess", 3)),
            ("Skills of Staff", factors.get("skills", 3)),
            ("Costs", factors.get("cost", 3))
        ]
        
        # Summary line for factors
        fac_ratings = [f"{name}: {rating}/5 ({int(rating)*20}%)" for name, rating in factor_items if rating is not None]
        add_question_block(doc, "5.1 External Factors Ratings:", " | ".join(fac_ratings))
        add_question_block(doc, "5.1 Factors Explanation:", data.get("q5_1_factorsExplanation"))
        
        support_bool = data.get("q5_2_franchisorSupport")
        support_str = "Yes" if support_bool is True else ("No" if support_bool is False else "Not Specified")
        add_question_block(doc, "5.2 Franchisor Guidance/Support:", f"{support_str} — {data.get('q5_2_franchisorSupportDetails', '')}")
        add_question_block(doc, "5.3 Tool Choice Control:", data.get("q5_3_toolChoiceControl"))

        add_section_header(doc, "6. Concluding Remarks")
        add_question_block(doc, "Final Experience & Feedback:", data.get("conclusion"))

        if idx < len(records) - 1:
            doc.add_page_break()

    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio
