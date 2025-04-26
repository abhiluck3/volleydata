import streamlit as st
import pandas as pd
import plotly.express as px
from file_manager import load_sheet, add_entry, update_entry
from data_config import tabs_config

st.set_page_config(page_title="Tournament Manager", layout="wide")
st.title("🏓 Tournament Data Entry & Analysis")

tab_names = list(tabs_config.keys()) + ["Analysis", "Player Match Record"]
tabs = st.tabs(tab_names)

for i, name in enumerate(tabs_config.keys()):
    with tabs[i]:
        st.subheader(name)
        df = load_sheet(tabs_config[name]['sheet'])
        st.dataframe(df, use_container_width=True)

        st.markdown("### ➕ Add New Entry")
        with st.form(f"add_form_{i}", clear_on_submit=True):
            new_data = {}
            for f in tabs_config[name]['fields']:
                if "Date" in f:
                    new_data[f] = st.date_input(f)
                elif f in ["Gender"]:
                    new_data[f] = st.selectbox(f, ["Male", "Female", "Other"])
                elif f in ["Player 1", "Player 2", "Winner"]:
                    players = load_sheet("TeamsPlayers")["Player Name"].dropna().tolist()
                    new_data[f] = st.selectbox(f, players)
                else:
                    new_data[f] = st.text_input(f)
            if st.form_submit_button("Add Entry"):
                data_str = {k: str(v) for k, v in new_data.items()}
                if all(v.strip() for v in data_str.values()):
                    add_entry(tabs_config[name]['sheet'], data_str)
                    st.success("Entry added! Refresh to see update.")
                else:
                    st.error("Fill all fields.")

        st.markdown("---")
        st.markdown("### ✏️ Edit Existing Entry")
        if not df.empty:
            idx = st.number_input(f"Row to edit (0-{len(df)-1})", 0, len(df)-1)
            if st.button(f"Load row {idx}", key=f"load_{i}"):
                ed = {}
                for f in tabs_config[name]['fields']:
                    ed[f] = st.text_input(f, value=str(df.at[idx, f]))
                if st.button(f"Save row {idx}", key=f"save_{i}"):
                    update_entry(tabs_config[name]['sheet'], idx, ed)
                    st.success("Row updated! Refresh.")

with tabs[-2]:
    st.header("📊 Analysis Dashboard")
    ms = load_sheet("MatchScores")
    if not ms.empty:
        st.subheader("Match Results")
        st.dataframe(ms, use_container_width=True)
        wc = ms["Winner"].value_counts().reset_index()
        wc.columns = ["Player", "Wins"]
        st.subheader("🏆 Wins per Player")
        st.plotly_chart(px.bar(wc, x="Player", y="Wins", text_auto=True), use_container_width=True)
        st.metric("Total Matches", len(ms), delta=None)
        st.success(f"Top: {wc.iloc[0]['Player']} ({wc.iloc[0]['Wins']} wins)")
    tp = load_sheet("TeamsPlayers")
    if not tp.empty:
        st.subheader("Players per Team")
        st.plotly_chart(px.pie(tp, names="Team Name"), use_container_width=True)

with tabs[-1]:
    st.header("📊 Player Match Record")
    tp = load_sheet("TeamsPlayers")
    ms = load_sheet("MatchScores")
    if not tp.empty and not ms.empty:
        stats = {}
        for _, m in ms.iterrows():
            p1, p2, w = m["Player 1"], m["Player 2"], m["Winner"]
            for p in [p1, p2]:
                stats.setdefault(p, {"matches":0, "wins":0})
                stats[p]["matches"] += 1
            stats[w]["wins"] += 1
        df_stats = pd.DataFrame([{
            "Player": p,
            "Matches Played": v["matches"],
            "Wins": v["wins"],
            "Losses": v["matches"]-v["wins"],
            "Win %": round(v["wins"]/v["matches"]*100 if v["matches"]>0 else 0,2)
        } for p,v in stats.items()])
        st.dataframe(df_stats, use_container_width=True)
        st.plotly_chart(px.bar(df_stats, x="Player", y="Win %", text_auto=True), use_container_width=True)
    else:
        st.warning("Add players & match scores first.")
