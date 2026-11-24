import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase

import time


@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write('Enter the subject code provided by your teacher to enroll.')
    join_code = st.text_input('Subject Code', placeholder='e.g. CS101').strip().upper()

    if join_code:
        # Look up ALL subjects matching this code (case-insensitive via UPPER normalisation)
        res = supabase.table('subjects').select(
            'subject_id, name, subject_code, section, teacher_id'
        ).execute()

        matches = [s for s in (res.data or []) if s['subject_code'].strip().upper() == join_code]

        if not matches:
            st.error(f'No subject found with code **{join_code}**. Check the code and try again.')
        else:
            # If multiple subjects share the same code, let the student pick
            if len(matches) == 1:
                subject = matches[0]
            else:
                options = {f"{s['name']} (Section {s['section']})": s for s in matches}
                chosen_label = st.selectbox('Multiple subjects found — select one:', list(options.keys()))
                subject = options[chosen_label]

            st.info(f"**{subject['name']}** · Section {subject['section']} · Code `{subject['subject_code']}`")

            if st.button('Confirm Enroll', type='primary', width='stretch'):
                student_id = st.session_state.student_data['student_id']
                check = supabase.table('subject_students').select('id').eq(
                    'subject_id', subject['subject_id']
                ).eq('student_id', student_id).execute()

                if check.data:
                    st.warning('You are already enrolled in this subject.')
                else:
                    enroll_student_to_subject(student_id, subject['subject_id'])
                    st.success(f"Successfully enrolled in **{subject['name']}**!")
                    time.sleep(1)
                    st.rerun()
    else:
        if st.button('Enroll now', type='primary', width='stretch'):
            st.warning('Please enter a subject code.')
