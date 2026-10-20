import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout

from src.components.header import header_dashboard

from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
import time

from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card

def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    c1, c2 = st.columns([3, 2], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        st.markdown(f"""
            <div style="text-align:right;">
                <span style="font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#64748b;">enrolled student</span>
                <div style="font-size:1.4rem; font-weight:800; color:#0b0f19; letter-spacing:-0.03em;">welcome, {student_data['name'].lower()}</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
        col_dummy, col_logout = st.columns([1, 1])
        with col_logout:
            if st.button("log out", type='secondary', key='loginbackbtn', shortcut="control+backspace", width='stretch'):
                st.session_state['is_logged_in'] = False
                del st.session_state.student_data 
                st.rerun()

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1], vertical_alignment='center')
    with c1:
        st.markdown("""
            <div>
                <h2 style="font-size:2rem; font-weight:800; color:#0b0f19; margin:0; letter-spacing:-0.04em;">enrolled subjects</h2>
                <p style="font-size:0.92rem; color:#64748b; margin:4px 0 0 0;">view verified attendance logs and course status</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        if st.button('+ enroll in subject', type='primary', width='stretch'):
            enroll_dialog()

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    with st.spinner('loading your enrolled subjects..'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {"total":0, "attended": 0}

        stats_map[sid]['total'] +=1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    if not subjects:
        st.info("you are not enrolled in any subjects yet. click '+ enroll in subject' above to get started!")

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']

        stats = stats_map.get(sid,{"total":0, "attended": 0} )
        def unenroll_button():
                if st.button("unenroll from course", type='tertiary', width='stretch', icon=':material/delete_forever:'):
                    unenroll_student_to_subject(student_id, sid)
                    st.toast(f"unenrolled from {sub['name']} successfully!")
                    st.rerun()

        with cols[i % 2]:
            subject_card(
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats = [
                    ('📅', 'total sessions', stats['total']),
                    ('✅', 'attended', stats['attended']),
                ],
                footer_callback=unenroll_button
            )


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return
    
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

    # Sofi Health Title Card
    st.markdown("""
        <div style="background:rgba(255, 255, 255, 0.9); backdrop-filter:blur(24px); border-radius:28px; padding:2rem 2.5rem; border:1px solid rgba(15, 23, 42, 0.08); box-shadow:0 15px 35px -10px rgba(0,0,0,0.05); margin-bottom:2rem; animation:fadeSlideUp 0.6s ease both;">
            <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(241, 245, 249, 0.8); border:1px solid rgba(15, 23, 42, 0.08); padding:5px 14px; border-radius:9999px; margin-bottom:0.8rem;">
                <span style="width:6px; height:6px; background:#10b981; border-radius:50%; box-shadow:0 0 6px #10b981;"></span>
                <span style="font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#475569;">instant faceid check-in</span>
            </div>
            <h2 style="font-size:2.2rem; font-weight:800; color:#0b0f19; margin:0 0 4px 0; letter-spacing:-0.04em;">biometric attendance verification</h2>
            <p style="font-size:0.95rem; color:#64748b; margin:0; line-height:1.5;">align your face with the camera or upload a clear photo for neural recognition</p>
        </div>
    """, unsafe_allow_html=True)
    
    cam_col, upload_col = st.columns(2)
    with cam_col:
        cam_photo = st.camera_input("center face in camera", key="student_cam")
    with upload_col:
        upload_photo = st.file_uploader("or upload a face photo (jpg, png)", type=['jpg', 'jpeg', 'png'], key="student_upload")

    photo_source = cam_photo if cam_photo is not None else upload_photo

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    with st.expander("🎓 **quick access: select student profile directly**", expanded=False):
        all_students = get_all_students()
        if all_students:
            s_map = {f"{s['name']} (ID: {s['student_id']})": s for s in all_students}
            chosen = st.selectbox("Select Student Profile", options=list(s_map.keys()), key="direct_s_choice")
            if st.button("log in as selected student →", type="primary", key="direct_s_btn"):
                st.session_state.is_logged_in = True
                st.session_state.user_role = 'student'
                st.session_state.student_data = s_map[chosen]
                st.toast(f"welcome back {s_map[chosen]['name']}!")
                st.rerun()

    show_registration = False
    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner('AI is scanning..'):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning('Face not found!')
            elif num_faces >1:
                st.warning('Multiple faces found')
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id']==student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f'Welcome Back {student['name']}')
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not recognized! You might be a new student!')
                    show_registration = True
    if show_registration:
        with st.container(border=True):
            st.header('Register new Profile')
            new_name = st.text_input("Enter your name", placeholder='E.g. Hamza Rizvi')

            st.subheader('Optional : Voice Enrollment')
            st.info("Enroll your for voice only attendance")


            audio_data = None

            try:
                audio_data = st.audio_input('Record a short phrase like I am present, My name is Akash.')
            except Exception:
                st.error('Audio Data failed!')

            if st.button('Create Account', type='primary'):
                if new_name:
                    with st.spinner('Creating profile..'):
                        img = np.array(Image.open(photo_source))
                        encodings= get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f'Profile Created! Hi {new_name}!')
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error('Couldnt capture your facial features for registration')

                else:
                    st.warning('Please enter your name!')


        