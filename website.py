import uuid

import streamlit as st
import json
import os
import plotly.express as px
import pandas as pd
import login


st.set_page_config(layout="wide")
st.title("Cornball Ranking")
st.set_page_config(page_title='Cornball Ranking')

col1, col2 = st.columns([0.2, 0.7], gap="large")

def load_state(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)
    return f"Error: No {file_name} file"

def save_state(state, file_name):
    with open(file_name, "w") as f:
        json.dump(state, f)





if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'UUID' not in st.session_state:
    st.session_state['UUID'] = ""

# Login page
if not st.session_state['logged_in']:
    with col1:
        username = st.text_input("Username")
        password = st.text_input("Password")
        if st.button("Log in"):
            log_in = login.log_in(username, password)
            if log_in != "Failed":
                st.session_state['UUID'] = log_in
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.session_state['logged_in'] = False
                st.rerun()

        if st.button("Create account"):
            create_acct = login.create_account(username, password)
            if create_acct != "Failed":
                st.session_state['UUID'] = create_acct
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.session_state['logged_in'] = False
                st.rerun()

state = load_state("state.json")
events = load_state("events.json")


if st.session_state['UUID'] in state:
    session_events = state.get(st.session_state['UUID'])
else:
    state.update({st.session_state['UUID']: events})
    session_events = state.get(st.session_state['UUID'])



if st.session_state['logged_in']:

    with col1:
        for event in session_events:
            st.text(event)
            val = st.slider(label="", label_visibility='collapsed', min_value=0.0, max_value=10.0, step=0.5, value=float(state.get(st.session_state['UUID']).get(event)), key=event, format="%g")
            session_events.update({event: val})

        if st.button("Submit"):
            state.update({st.session_state['UUID']: session_events})
            save_state(state, "state.json")





    # {event: [user 1 rating, user 2 rating, ... ]}
    event_state_total = {}

    state = load_state("state.json")

    with col2:

        for event in events:
            value = 0
            for user in state:
                value += state.get(user).get(event)
            event_state_total.update({event: value / (len(state) - 1)})

        df = pd.DataFrame(list(event_state_total.items()), columns=['Event', 'Value'])

        df_sorted = df.sort_values(by=['Value'], ascending=True)

        fig = px.bar(df_sorted, x='Value', y='Event', orientation="h", text_auto=True)

        fig.update_xaxes(range=[0,10])

        podium = st.container()
        top_3 = df.nlargest(3, 'Value').reset_index(drop=True)

        with podium:
            second, first, third = st.columns(3)

            with first:
                st.markdown(f"""
                                    <style>

                                        .empty-space-a {{
                                            width: 500px;
                                            height: 50px;
                                            border-radius: 10px;
                                            margin: auto; /* This centers the rectangle horizontally */
                                        }}

                                        /* Style for the text above the rectangle */
                                        .title-text-a {{
                                            text-align: center;
                                            font-weight: bold;
                                            font-size: 18px;
                                            color: #FFD700;
                                            margin-bottom: 8px; /* Space between text and rectangle */
                                        }}

                                        /* Style for the gold rectangle */
                                        .gold-rectangle {{
                                            width: 500px;
                                            height: 250px;
                                            background-color: #FFD700 !important;
                                            border-radius: 10px;
                                            margin: auto; /* This centers the rectangle horizontally */
                                        }}
                                    </style>

                                    <div class="empty-space-a">
                                    </div>

                                    <!-- This div holds our styled text -->
                                    <div class="title-text-a">
                                        {top_3.at[0, 'Event']}    {round(top_3.at[0, 'Value'], 1)}/10
                                    </div>

                                    <!-- This div is our styled rectangle -->
                                    <div class="gold-rectangle">
                                    </div>
                                    """, unsafe_allow_html=True)
            with second:
                st.markdown(f"""
                                    <style>
                                        /* Style for the text above the rectangle */

                                        .empty-space-b {{
                                            width: 500px;
                                            height: 100px;
                                            border-radius: 10px;
                                            margin: auto; /* This centers the rectangle horizontally */
                                        }}

                                        .title-text-b {{
                                            text-align: center;
                                            font-weight: bold;
                                            font-size: 18px;
                                            color: #C0C0C0;
                                            margin-bottom: 8px; /* Space between text and rectangle */
                                        }}

                                        /* Style for the red rectangle */
                                        .silver-rectangle {{
                                            width: 500px;
                                            height: 200px;
                                            background-color: #C0C0C0 !important;
                                            border-radius: 10px;
                                            margin: auto; /* This centers the rectangle horizontally */
                                        }}
                                    </style>

                                    <!-- This div holds our styled text -->

                                    <div class="empty-space-b">
                                    </div>

                                    <div class="title-text-b">
                                        {top_3.at[1, 'Event']}    {round(top_3.at[1, 'Value'], 1)}/10.
                                    </div>

                                    <!-- This div is our styled rectangle -->
                                    <div class="silver-rectangle">
                                    </div>
                                    """, unsafe_allow_html=True)
            with third:
                st.markdown(f"""
                                        <style>

                                            .empty-space-c {{
                                                width: 500px;
                                                height: 150px;
                                                border-radius: 10px;
                                                margin: auto; /* This centers the rectangle horizontally */
                                            }}

                                            /* Style for the text above the rectangle */
                                            .title-text-c {{
                                                text-align: center;
                                                font-weight: bold;
                                                font-size: 18px;
                                                color: #CD7F32;
                                                margin-bottom: 8px; /* Space between text and rectangle */
                                            }}

                                            /* Style for the blue rectangle */
                                            .bronze-rectangle {{
                                                width: 500px;
                                                height: 150px;
                                                background-color: #CD7F32 !important;
                                                border-radius: 10px;
                                                margin: auto; /* This centers the rectangle horizontally */
                                            }}
                                        </style>

                                        <div class="empty-space-c">
                                        </div>

                                        <!-- This div holds our styled text -->
                                        <div class="title-text-c">
                                            {top_3.at[2, 'Event']}    {round(top_3.at[2, 'Value'], 1)}/10.
                                        </div>

                                        <!-- This div is our styled rectangle -->
                                        <div class="bronze-rectangle">
                                        </div>
                                        """, unsafe_allow_html=True)

        st.plotly_chart(fig, config={"staticPlot": True})



