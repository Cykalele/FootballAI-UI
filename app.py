import streamlit as st
import requests

st.set_page_config(page_title="Football Analyzer", layout="centered")

st.title("⚽ Football Video Analyzer")

# -- Teamkonfiguration
st.markdown("### 🔧 Teamkonfiguration")

team1_name = st.text_input("Team 1 Name", value="VFB")
team1_color = st.color_picker("Team 1 Farbe", value="#FF0000")

team2_name = st.text_input("Team 2 Name", value="Team Blue")
team2_color = st.color_picker("Team 2 Farbe", value="#0000FF")

st.markdown("---")

# -- Video Upload oder Linkwahl
st.markdown("### 🎥 Halbzeit-Video bereitstellen")
upload_method = st.radio("Wie möchtest du dein Video bereitstellen?", ["Upload", "Cloud-Link (z. B. Google Drive, OneDrive)"])

video_file = None
cloud_link = None
API_BASE = "https://1910-2a00-1e-d383-4201-818a-61d-c40a-a808.ngrok-free.app"  # <- NGROK API URL

if upload_method == "Upload":
    video_file = st.file_uploader("🎞️ MP4-Datei hochladen", type=["mp4"])
    st.info("Bitte lade **nur eine Halbzeit** als MP4 hoch. Optimale Größe: <300 MB.")
else:
    cloud_link = st.text_input("🔗 Freigabelink einfügen (z. B. OneDrive, Google Drive)")
    st.warning("⚠️ Stelle sicher, dass der Link öffentlich zugänglich ist und direkt auf das Video verweist.")

# -- Run-Optionen
if video_file or cloud_link:
    st.success("✅ Videoquelle erkannt.")

    col1, col2 = st.columns(2)
    with col1:
        run_tracking = st.checkbox("Run Tracking", value=True)
    with col2:
        run_assignment = st.checkbox("Run Team Assignment", value=True)

    if st.button("🚀 Analyse starten"):
        with st.spinner("Sende Daten an Backend..."):

            # -- Konfigdaten
            payload = {
                "team1_name": team1_name,
                "team1_color": team1_color,
                "team2_name": team2_name,
                "team2_color": team2_color,
                "run_tracking": run_tracking,
                "run_assignment": run_assignment,
            }

            if cloud_link:
                payload["video_url"] = cloud_link
                try:
                    r = requests.post(f"{API_BASE}/process-link", json=payload)
                    if r.status_code == 200:
                        st.success("🚀 Verarbeitung erfolgreich gestartet (Cloud-Link).")
                    else:
                        st.error(f"❌ Fehler beim Senden des Links: {r.status_code}")
                except Exception as e:
                    st.error(f"❌ Ausnahmefehler: {e}")

            elif video_file:
                try:
                    files = {
                        "file": (video_file.name, video_file, "video/mp4")
                    }
                    r = requests.post(f"{API_BASE}/upload", files=files, data=payload)
                    if r.status_code == 200:
                        st.success("🚀 Verarbeitung erfolgreich gestartet (Upload).")
                    else:
                        st.error(f"❌ Fehler beim Hochladen: {r.status_code}")
                except Exception as e:
                    st.error(f"❌ Ausnahmefehler: {e}")
