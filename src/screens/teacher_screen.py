import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout

from src.components.header import header_dashboard

from src.components.subject_card import subject_card
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects, get_attendance_for_teacher
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog

from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_results import attendance_result_dialog
import numpy as np

from datetime import datetime

import pandas as pd

from src.database.config import supabase


from src.components.dialog_voice_attendance import voice_attendance_dialog
def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()





def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns([3, 2], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        st.markdown(f"""
            <div style="text-align:right;">
                <span style="font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#64748b;">authenticated educator</span>
                <div style="font-size:1.4rem; font-weight:800; color:#0b0f19; letter-spacing:-0.03em;">welcome, {teacher_data['name'].lower()}</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
        col_dummy, col_logout = st.columns([1, 1])
        with col_logout:
            if st.button("log out", type='secondary', key='loginbackbtn', shortcut="control+backspace", width='stretch'):
                st.session_state['is_logged_in'] = False
                del st.session_state.teacher_data 
                st.rerun()

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'
    
    # Sofi Health Pill Navigation Switcher
    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('take attendance', type=type1, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('manage subjects', type=type2, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('attendance records', type=type3, width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    st.markdown("<div style='margin-bottom:1.5rem;'></div>", unsafe_allow_html=True)

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    




def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')


    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You havent created any subjects yet! Please create one to begin!')
        return
    
    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3,1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4 ]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')
    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear all photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()


    with c2:
        
        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:', disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)


                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id',selected_subject_id ).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                else:

                    results, attendance_to_log  = [], []

                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


                    for node in enrolled_students:
                        student = node.get('students')
                        if not student:
                            continue
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present = len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button('Use Voice Attendance', type='primary', width='stretch', icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)











def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header('Manage Subjects', width='stretch')

    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)


    # LIST all SUBJECTS
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]
            def make_share_btn(current_sub):
                def share_btn():
                    if st.button(f"Share Code: {current_sub['name']}", key=f"share_{current_sub['subject_code']}", icon=":material/share:"):
                        share_subject_dialog(current_sub['name'], current_sub['subject_code'])
                    st.space()
                return share_btn

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=make_share_btn(sub)
            )
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")


def teacher_tab_attendance_records():
    st.header('Attendance Records')

    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("No attendance records found yet. Take attendance using Face Analysis or Voice Attendance to generate logs.")
        return
    
    data = []

    for r in records:
        ts = r.get('timestamp')

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N'A",
            "Subject": r['subjects']['name'],
            "Subject Code":r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })


    df = pd.DataFrame(data)



    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count = ('is_present', 'sum'),
            Total_Count =('is_present', 'count')
        ).reset_index()

    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " /"
        + summary['Total_Count'].astype(str) + ' Students'
    )

    display_df = ( summary.sort_values(by='ts_group' ,ascending=False)
                  [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
                  )
    
    st.dataframe(display_df, width='stretch', hide_index=True)


def login_teacher(username, password):
    if not username or not password:
        return False
    
    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role ='teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    

    return False
def teacher_screen_login():
    c1, c2 = st.columns([3, 2], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        col_space, col_back = st.columns([1, 2])
        with col_back:
            if st.button("← back to home", type='secondary', key='loginbackbtn', shortcut="control+backspace", width='stretch'):
                st.session_state['login_type'] = None
                st.rerun()

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # Centered Sofi Card Container
    left_col, center_col, right_col = st.columns([1, 3, 1])

    with center_col:
        st.markdown("""
            <div style="background:rgba(255, 255, 255, 0.9); backdrop-filter:blur(24px); border-radius:28px; padding:2.5rem 2.8rem; border:1px solid rgba(15, 23, 42, 0.08); box-shadow:0 20px 45px -15px rgba(0,0,0,0.06); animation:fadeSlideUp 0.6s ease both;">
                <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(241, 245, 249, 0.8); border:1px solid rgba(15, 23, 42, 0.08); padding:5px 14px; border-radius:9999px; margin-bottom:1rem;">
                    <span style="width:6px; height:6px; background:#3b82f6; border-radius:50%;"></span>
                    <span style="font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#475569;">educator portal</span>
                </div>
                <h2 style="font-size:2.2rem; font-weight:800; color:#0b0f19; margin:0 0 6px 0; letter-spacing:-0.04em; line-height:1.1;">sign in to snapclass</h2>
                <p style="font-size:0.95rem; color:#64748b; margin:0 0 1.8rem 0; line-height:1.5;">enter your educator credentials to manage course rosters and launch ai roll call</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        teacher_username = st.text_input("Username", placeholder='e.g. ananyaroy', key="t_login_user")
        teacher_pass = st.text_input("Password", type='password', placeholder="••••••••••••", key="t_login_pass")

        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

        btnc1, btnc2 = st.columns(2)
        with btnc1:
            if st.button('sign in →', type='primary', shortcut='control+enter', width='stretch'):
                if login_teacher(teacher_username, teacher_pass):
                    st.toast("welcome back!", icon="👋")
                    import time
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("invalid username or password combination")

        with btnc2:
            if st.button('create account', type="secondary", width='stretch'):
                st.session_state.teacher_login_type = 'register'
                st.rerun()


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "all fields are required"
    if check_teacher_exists(teacher_username):
        return False, "username is already taken"
    if teacher_pass != teacher_pass_confirm:
        return False, "passwords do not match"
    
    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "educator account created successfully! please sign in."
    except Exception as e:
        return False, "unexpected error occurred"
    

def teacher_screen_register():
    c1, c2 = st.columns([3, 2], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        col_space, col_back = st.columns([1, 2])
        with col_back:
            if st.button("← back to home", type='secondary', key='loginbackbtn', shortcut="control+backspace", width='stretch'):
                st.session_state['login_type'] = None
                st.rerun()

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # Centered Sofi Card Container
    left_col, center_col, right_col = st.columns([1, 3, 1])

    with center_col:
        st.markdown("""
            <div style="background:rgba(255, 255, 255, 0.9); backdrop-filter:blur(24px); border-radius:28px; padding:2.5rem 2.8rem; border:1px solid rgba(15, 23, 42, 0.08); box-shadow:0 20px 45px -15px rgba(0,0,0,0.06); animation:fadeSlideUp 0.6s ease both;">
                <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(241, 245, 249, 0.8); border:1px solid rgba(15, 23, 42, 0.08); padding:5px 14px; border-radius:9999px; margin-bottom:1rem;">
                    <span style="width:6px; height:6px; background:#10b981; border-radius:50%;"></span>
                    <span style="font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#475569;">educator onboarding</span>
                </div>
                <h2 style="font-size:2.2rem; font-weight:800; color:#0b0f19; margin:0 0 6px 0; letter-spacing:-0.04em; line-height:1.1;">create teacher account</h2>
                <p style="font-size:0.95rem; color:#64748b; margin:0 0 1.8rem 0; line-height:1.5;">set up your teaching profile to organize subjects and track attendance</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        teacher_username = st.text_input("Choose username", placeholder='e.g. ananyaroy', key="t_reg_user")
        teacher_name = st.text_input("Full name", placeholder='e.g. Dr. Ananya Roy', key="t_reg_name")
        teacher_pass = st.text_input("Create password", type='password', placeholder="••••••••••••", key="t_reg_pass")
        teacher_pass_confirm = st.text_input("Confirm password", type='password', placeholder="••••••••••••", key="t_reg_pass2")

        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

        btnc1, btnc2 = st.columns(2)
        with btnc1:
            if st.button('register profile →', type='primary', shortcut='control+enter', width='stretch'):
                success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
                if success:
                    st.success(message)
                    import time
                    time.sleep(1.2)
                    st.session_state.teacher_login_type = "login"
                    st.rerun()
                else:
                    st.error(message)

        with btnc2:
            if st.button('already registered? sign in', type="secondary", width='stretch'):
                st.session_state.teacher_login_type = 'login'
                st.rerun()
