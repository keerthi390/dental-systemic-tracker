import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime
import os
import base64
from PIL import Image
import io

st.set_page_config(page_title="Gingival Systems Health Tracker", layout="wide")
st.title("🦷 Gingival Systems Health Tracker")
st.caption("Photo Upload | Gum-Brain | Gum-Heart | Gum-Gut | Gum-Hormonal | Gum-Sleep | Gum-Stress | Gum-Skin | Gum-Hair | Gum-Muscle | Gum-Bone | Gum-Aging")
st.markdown("---")

# Create photo directory if not exists
PHOTO_DIR = "user_photos"
if not os.path.exists(PHOTO_DIR):
    os.makedirs(PHOTO_DIR)

# Initialize session state
if "logs" not in st.session_state:
    st.session_state.logs = pd.DataFrame(columns=[
        "Date", "Age",
        # Hygiene
        "Brushing (1-5)", "Flossing (1-5)",
        # Diet
        "Sugar_Intake_g", "Sticky_Carbs (0/1)", "Calcium_Food (0/1)", "Water_Intake_cups",
        # Oral
        "Bad_Breath (1-5)", "Dry_Mouth (0/1)", "Gums_Bleed (0/1)", "Gum_Color (0=pink,1=red)", "Tooth_Sensitivity (1-5)",
        # Lifestyle
        "Last_Dental_Visit_months", "Tobacco (0/1)", "Alcohol_Weekly", "Teeth_Grinding (0/1)",
        # Gum-Brain
        "Brain_Fog (0-3)", "Memory_Issues (0-3)",
        # Gum-Heart
        "High_BP (0/1)", "Heart_Disease (0/1)",
        # Gum-Gut
        "Digestive_Issues (0/1)",
        # Gum-Hormonal
        "Menstrual_Phase (0=follicular,1=luteal,2=NA)", "Pregnant (0/1)", "PCOS (0/1)", "Menopause (0/1)", "Thyroid_Issue (0/1)", "High_Cortisol (0/1)",
        # Gum-Sleep
        "Sleep_Hours", "Sleep_Quality (1-5)",
        # Gum-Stress
        "Stress_Level (1-10)",
        # Gum-Skin
        "Acne (0/1)", "Rosacea (0/1)", "Slow_Healing (0/1)",
        # Gum-Hair
        "Hair_Thinning (0/1)",
        # Gum-Muscle
        "Fatigue (1-5)", "Poor_Muscle_Recovery (0/1)",
        # Gum-Bone
        "Osteoporosis (0/1)", "Joint_Pain (0/1)",
        # Medical Conditions
        "Diabetes (0/1)", "GERD (0/1)", "Autoimmune (0/1)",
        # Photo tracking
        "Has_Photos (0/1)"
    ])

if "photo_metadata" not in st.session_state:
    st.session_state.photo_metadata = pd.DataFrame(columns=[
        "Date", "Tooth_Number", "Angle", "Photo_Path", "Notes"
    ])

# Tooth number helper
def get_tooth_selector():
    tooth_options = {
        "Upper Right": [1,2,3,4,5,6,7,8],
        "Upper Left": [9,10,11,12,13,14,15,16],
        "Lower Left": [17,18,19,20,21,22,23,24],
        "Lower Right": [25,26,27,28,29,30,31,32]
    }
    quadrant = st.selectbox("Select quadrant", list(tooth_options.keys()))
    tooth = st.selectbox("Select tooth number", tooth_options[quadrant])
    return tooth, quadrant

# Sidebar – Daily Log
st.sidebar.header("📝 Log Today")
with st.sidebar.form("log_form"):
    age = st.number_input("Your age", 18, 100, 30)
    
    st.subheader("🪥 Hygiene")
    brushing = st.slider("Brushing (1=poor,5=excellent)", 1, 5, 4)
    flossing = st.slider("Flossing (1=poor,5=excellent)", 1, 5, 3)
    
    st.subheader("🍎 Diet")
    sugar = st.number_input("Sugar (grams)", 0, 150, 25)
    sticky = st.checkbox("Sticky carbs? (rice, bread, chapati, noodles)")
    calcium = st.checkbox("Calcium-rich food? (dairy, tofu, greens)")
    water = st.slider("Water (cups)", 0, 12, 6)
    
    st.subheader("👃 Oral")
    bad_breath = st.slider("Bad breath (1=fresh,5=very bad)", 1, 5, 2)
    dry_mouth = st.checkbox("Dry mouth today?")
    gums_bleed = st.checkbox("Gums bleed while brushing?")
    gum_color = st.radio("Gum color", ["Healthy pink", "Red/swollen"], index=0)
    sensitivity = st.slider("Tooth sensitivity (1=none,5=severe)", 1, 5, 2)
    
    st.subheader("🏥 Lifestyle")
    last_visit = st.number_input("Months since last dental visit", 0, 60, 12)
    tobacco = st.checkbox("Use tobacco/smoke?")
    alcohol = st.number_input("Alcoholic drinks per week", 0, 50, 2)
    grinding = st.checkbox("Teeth grinding (day or night)?")
    
    st.subheader("🧠 Gum-Brain Axis")
    brain_fog = st.select_slider("Brain fog (0=none,3=severe)", options=[0,1,2,3], value=0)
    memory = st.select_slider("Memory issues (0=none,3=severe)", options=[0,1,2,3], value=0)
    
    st.subheader("❤️ Gum-Heart Axis")
    high_bp = st.checkbox("High blood pressure")
    heart_disease = st.checkbox("Heart disease history")
    
    st.subheader("🦠 Gum-Gut Axis")
    digestive = st.checkbox("Digestive issues (bloating, IBS, acidity)")
    
    st.subheader("🌸 Gum-Hormonal Axis")
    menstrual = st.selectbox("Menstrual phase", ["Not applicable", "Follicular", "Luteal"], index=0)
    pregnant = st.checkbox("Pregnant")
    pcos = st.checkbox("PCOS")
    menopause = st.checkbox("Menopause")
    thyroid = st.checkbox("Thyroid disorder")
    high_cortisol = st.checkbox("High cortisol / chronic stress")
    
    st.subheader("😴 Gum-Sleep Axis")
    sleep_hours = st.slider("Hours slept last night", 0, 12, 7)
    sleep_quality = st.slider("Sleep quality (1=poor,5=excellent)", 1, 5, 3)
    
    st.subheader("⚡ Gum-Stress Axis")
    stress = st.slider("Stress level (1=low,10=high)", 1, 10, 5)
    
    st.subheader("🧴 Gum-Skin Axis")
    acne = st.checkbox("Acne")
    rosacea = st.checkbox("Rosacea")
    slow_healing = st.checkbox("Slow wound healing")
    
    st.subheader("💇 Gum-Hair Axis")
    hair_thinning = st.checkbox("Hair thinning or loss")
    
    st.subheader("💪 Gum-Muscle Axis")
    fatigue = st.slider("Fatigue (1=none,5=severe)", 1, 5, 2)
    poor_recovery = st.checkbox("Poor muscle recovery after exercise")
    
    st.subheader("🦴 Gum-Bone Axis")
    osteoporosis = st.checkbox("Osteoporosis")
    joint_pain = st.checkbox("Chronic joint pain")
    
    st.subheader("🏥 Medical Conditions")
    diabetes = st.checkbox("Diabetes (Type 1 or 2)")
    gerd = st.checkbox("GERD / acid reflux")
    autoimmune = st.checkbox("Autoimmune disease (Lupus, RA, Crohn's, etc.)")
    
    submitted = st.form_submit_button("Save Entry")
    
    if submitted:
        menstrual_map = {"Not applicable": 2, "Follicular": 0, "Luteal": 1}
        gum_color_map = {"Healthy pink": 0, "Red/swollen": 1}
        
        new_entry = pd.DataFrame([{
            "Date": date.today(),
            "Age": age,
            "Brushing (1-5)": brushing,
            "Flossing (1-5)": flossing,
            "Sugar_Intake_g": sugar,
            "Sticky_Carbs (0/1)": 1 if sticky else 0,
            "Calcium_Food (0/1)": 1 if calcium else 0,
            "Water_Intake_cups": water,
            "Bad_Breath (1-5)": bad_breath,
            "Dry_Mouth (0/1)": 1 if dry_mouth else 0,
            "Gums_Bleed (0/1)": 1 if gums_bleed else 0,
            "Gum_Color (0=pink,1=red)": gum_color_map[gum_color],
            "Tooth_Sensitivity (1-5)": sensitivity,
            "Last_Dental_Visit_months": last_visit,
            "Tobacco (0/1)": 1 if tobacco else 0,
            "Alcohol_Weekly": alcohol,
            "Teeth_Grinding (0/1)": 1 if grinding else 0,
            "Brain_Fog (0-3)": brain_fog,
            "Memory_Issues (0-3)": memory,
            "High_BP (0/1)": 1 if high_bp else 0,
            "Heart_Disease (0/1)": 1 if heart_disease else 0,
            "Digestive_Issues (0/1)": 1 if digestive else 0,
            "Menstrual_Phase (0=follicular,1=luteal,2=NA)": menstrual_map[menstrual],
            "Pregnant (0/1)": 1 if pregnant else 0,
            "PCOS (0/1)": 1 if pcos else 0,
            "Menopause (0/1)": 1 if menopause else 0,
            "Thyroid_Issue (0/1)": 1 if thyroid else 0,
            "High_Cortisol (0/1)": 1 if high_cortisol else 0,
            "Sleep_Hours": sleep_hours,
            "Sleep_Quality (1-5)": sleep_quality,
            "Stress_Level (1-10)": stress,
            "Acne (0/1)": 1 if acne else 0,
            "Rosacea (0/1)": 1 if rosacea else 0,
            "Slow_Healing (0/1)": 1 if slow_healing else 0,
            "Hair_Thinning (0/1)": 1 if hair_thinning else 0,
            "Fatigue (1-5)": fatigue,
            "Poor_Muscle_Recovery (0/1)": 1 if poor_recovery else 0,
            "Osteoporosis (0/1)": 1 if osteoporosis else 0,
            "Joint_Pain (0/1)": 1 if joint_pain else 0,
            "Diabetes (0/1)": 1 if diabetes else 0,
            "GERD (0/1)": 1 if gerd else 0,
            "Autoimmune (0/1)": 1 if autoimmune else 0,
            "Has_Photos (0/1)": 0
        }])
        st.session_state.logs = pd.concat([st.session_state.logs, new_entry], ignore_index=True)
        st.sidebar.success("✅ Daily log saved!")

# Photo Upload Section (Separate)
st.sidebar.markdown("---")
st.sidebar.header("📸 Upload Tooth Photo")

with st.sidebar.form("photo_form"):
    photo_date = st.date_input("Photo date", date.today())
    tooth_num, quadrant = get_tooth_selector()
    angle = st.selectbox("Camera angle", [
        "Front (facing camera)",
        "Left side (buccal)", 
        "Right side (buccal)",
        "Top (occlusal)",
        "Bottom (occlusal)",
        "Close-up (specific tooth)"
    ])
    photo_notes = st.text_area("Notes (e.g., redness, swelling, cavity visible)", height=68)
    uploaded_file = st.file_uploader("Choose photo", type=["jpg", "jpeg", "png"])
    
    photo_submitted = st.form_submit_button("Save Photo")
    
    if photo_submitted and uploaded_file is not None:
        # Save photo with unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tooth_{tooth_num}_{angle.replace(' ', '_')}_{timestamp}.jpg"
        filepath = os.path.join(PHOTO_DIR, filename)
        
        # Save image
        image = Image.open(uploaded_file)
        image.save(filepath)
        
        # Save metadata
        new_photo = pd.DataFrame([{
            "Date": photo_date,
            "Tooth_Number": tooth_num,
            "Angle": angle,
            "Photo_Path": filepath,
            "Notes": photo_notes
        }])
        st.session_state.photo_metadata = pd.concat([st.session_state.photo_metadata, new_photo], ignore_index=True)
        
        # Update main log that photos exist
        if len(st.session_state.logs) > 0:
            st.session_state.logs.loc[st.session_state.logs.index[-1], "Has_Photos (0/1)"] = 1
        
        st.sidebar.success(f"✅ Photo saved for tooth #{tooth_num} ({angle})")

# Main Dashboard
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "🧬 Axis Scores", "📸 Photo Gallery", "🩺 Health Summary", "📜 History"])

with tab1:
    if len(st.session_state.logs) > 0:
        df = st.session_state.logs.copy()
        df["Date"] = pd.to_datetime(df["Date"])
        latest = df.iloc[-1]
        
        # Composite Scores
        hygiene = (latest["Brushing (1-5)"] * 0.4 + latest["Flossing (1-5)"] * 0.6) * 10
        nutrition = 100 - min(100, (latest["Sugar_Intake_g"] / 15) * 60 + latest["Sticky_Carbs (0/1)"] * 20 - latest["Calcium_Food (0/1)"] * 20 + (8 - latest["Water_Intake_cups"]) * 2)
        inflammation_score = (
            latest["Gums_Bleed (0/1)"] * 15 +
            latest["Gum_Color (0=pink,1=red)"] * 10 +
            latest["Stress_Level (1-10)"] * 3 +
            (6 - latest["Sleep_Quality (1-5)"]) * 5 +
            latest["Fatigue (1-5)"] * 4
        )
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🪥 Hygiene", f"{hygiene:.0f}/50")
        col2.metric("🍎 Nutrition", f"{nutrition:.0f}/100")
        col3.metric("🔥 Inflammation Risk", f"{min(100, inflammation_score):.0f}/100", help="Higher = more systemic inflammation")
        col4.metric("📸 Photos Saved", f"{len(st.session_state.photo_metadata)}")
        
        st.subheader("💡 Systemic Recommendations")
        recs = []
        if latest["Gums_Bleed (0/1)"] or latest["Gum_Color (0=pink,1=red)"]:
            recs.append("🔹 Bleeding/red gums → inflammation. See dentist. Links to heart & brain health.")
        if latest["Brain_Fog (0-3)"] >= 2:
            recs.append("🔹 Brain fog + gum inflammation → possible Gum-Brain axis activation")
        if latest["High_BP (0/1)"] or latest["Heart_Disease (0/1)"]:
            recs.append("🔹 Gum disease increases cardiovascular risk — manage both")
        if latest["Stress_Level (1-10)"] >= 7:
            recs.append("🔹 High stress elevates cortisol → worsens gum healing")
        if latest["Sleep_Quality (1-5)"] <= 2:
            recs.append("🔹 Poor sleep impairs gum repair and increases inflammation")
        if latest["Diabetes (0/1)"]:
            recs.append("🔹 Diabetes + gum disease = bidirectional. Control both.")
        if latest["Autoimmune (0/1)"]:
            recs.append("🔹 Autoimmune conditions worsen periodontal inflammation")
        if latest["Pregnant (0/1)"]:
            recs.append("🔹 Pregnancy gingivitis is common — gentle brushing, see dentist")
        if not recs:
            recs.append("✅ Good systemic profile. Maintain hygiene & manage stress.")
        for r in recs:
            st.write(r)
    else:
        st.info("Log your first day using the sidebar.")

with tab2:
    if len(st.session_state.logs) > 0:
        latest = df.iloc[-1]
        axes = {
            "Gum-Brain": 100 - (latest["Brain_Fog (0-3)"] + latest["Memory_Issues (0-3)"]) * 12.5,
            "Gum-Heart": 100 - (latest["High_BP (0/1)"] + latest["Heart_Disease (0/1)"]) * 25,
            "Gum-Gut": 100 - latest["Digestive_Issues (0/1)"] * 30,
            "Gum-Hormonal": 100 - (latest["PCOS (0/1)"] + latest["Thyroid_Issue (0/1)"]) * 20,
            "Gum-Sleep": 100 - ((8 - latest["Sleep_Hours"]) * 5 + (5 - latest["Sleep_Quality (1-5)"]) * 5),
            "Gum-Stress": 100 - (latest["Stress_Level (1-10)"] - 1) * 11,
            "Gum-Skin": 100 - (latest["Acne (0/1)"] + latest["Rosacea (0/1)"]) * 25,
            "Gum-Hair": 100 - latest["Hair_Thinning (0/1)"] * 30,
            "Gum-Muscle": 100 - (latest["Fatigue (1-5)"] * 5 + latest["Poor_Muscle_Recovery (0/1)"] * 20),
            "Gum-Bone": 100 - (latest["Osteoporosis (0/1)"] + latest["Joint_Pain (0/1)"]) * 25,
        }
        axes_df = pd.DataFrame(list(axes.items()), columns=["Axis", "Score"])
        fig = px.bar(axes_df, x="Axis", y="Score", title="Gingival Systems Axis Scores (Higher = Better)", color="Score", color_continuous_scale="RdYlGn", range_color=[0,100])
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Based on Gingival Systems Axis framework — gum health connected to whole body")
        
        # Show most affected axis
        min_axis = min(axes, key=axes.get)
        st.warning(f"⚠️ Lowest scoring axis: **{min_axis}** ({axes[min_axis]:.0f}/100) — focus on improving this area")
    else:
        st.info("Log data to see axis scores")

with tab3:
    st.subheader("📸 Tooth Photo Gallery")
    
    if len(st.session_state.photo_metadata) > 0:
        # Filters
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filter_tooth = st.selectbox("Filter by tooth number", ["All"] + sorted(st.session_state.photo_metadata["Tooth_Number"].unique().tolist()))
        with col_f2:
            filter_angle = st.selectbox("Filter by angle", ["All"] + st.session_state.photo_metadata["Angle"].unique().tolist())
        
        filtered_photos = st.session_state.photo_metadata
        if filter_tooth != "All":
            filtered_photos = filtered_photos[filtered_photos["Tooth_Number"] == filter_tooth]
        if filter_angle != "All":
            filtered_photos = filtered_photos[filtered_photos["Angle"] == filter_angle]
        
        # Display photos
        for idx, row in filtered_photos.iterrows():
            with st.expander(f"📸 Tooth #{row['Tooth_Number']} - {row['Angle']} - {row['Date']}"):
                if os.path.exists(row["Photo_Path"]):
                    image = Image.open(row["Photo_Path"])
                    st.image(image, caption=f"Tooth #{row['Tooth_Number']} ({row['Angle']})", use_container_width=True)
                else:
                    st.warning("Image file not found")
                if row["Notes"]:
                    st.caption(f"📝 Notes: {row['Notes']}")
                st.caption(f"📅 Uploaded: {row['Date']}")
        
        # Timeline view
        st.subheader("📅 Photo Timeline")
        timeline_df = st.session_state.photo_metadata.sort_values("Date")
        fig = px.scatter(timeline_df, x="Date", y="Tooth_Number", color="Angle", 
                         title="Tooth Photos Over Time", hover_data=["Notes"])
        st.plotly_chart(fig, use_container_width=True)
        
        # Download all photos as zip (placeholder - would need zipfile library)
        st.info("📦 To download all photos, photos are stored in the 'user_photos' folder on the server")
        
        # Share with dentist
        st.subheader("👨‍⚕️ Share with Dentist")
        if st.button("📧 Generate Shareable Report"):
            # Create summary
            report = f"""
            DENTAL HEALTH REPORT
            Date: {date.today()}
            Total Photos: {len(st.session_state.photo_metadata)}
            Recent Inflammation: {"Yes" if latest['Gums_Bleed (0/1)'] else "No"}
            Overall Health Score: {100 - (latest.get('Nutrition_Risk', 50) if 'Nutrition_Risk' in latest else 50):.0f}/100
            """
            st.text_area("Copy this report to share with your dentist:", report, height=200)
            st.success("Show this report and your photo gallery during your next dental visit")
    else:
        st.info("No photos uploaded yet. Use the sidebar to upload photos of your teeth from different angles.")
        st.markdown("""
        ### 📸 Recommended Angles:
        1. **Front** – Smile with teeth together
        2. **Left side** – Turn head left, open slightly
        3. **Right side** – Turn head right, open slightly
        4. **Top (occlusal)** – Upper teeth, looking down
        5. **Bottom (occlusal)** – Lower teeth, looking up
        6. **Close-up** – Any specific tooth of concern
        """)

with tab4:
    if len(st.session_state.logs) > 0:
        latest = df.iloc[-1]
        st.subheader("🩺 Active Medical Conditions")
        conditions = []
        if latest["Diabetes (0/1)"]: conditions.append("Diabetes")
        if latest["GERD (0/1)"]: conditions.append("GERD / Acid reflux")
        if latest["Autoimmune (0/1)"]: conditions.append("Autoimmune disease")
        if latest["High_BP (0/1)"]: conditions.append("High blood pressure")
        if latest["Heart_Disease (0/1)"]: conditions.append("Heart disease")
        if latest["Thyroid_Issue (0/1)"]: conditions.append("Thyroid disorder")
        if latest["PCOS (0/1)"]: conditions.append("PCOS")
        if latest["Osteoporosis (0/1)"]: conditions.append("Osteoporosis")
        if conditions:
            for c in conditions:
                st.write(f"• {c}")
        else:
            st.write("No major conditions logged")
        
        st.subheader("🦷 Oral Health Summary")
        if latest["Gums_Bleed (0/1)"] or latest["Gum_Color (0=pink,1=red)"]:
            st.warning("⚠️ Active gum inflammation detected — links to heart, brain, and systemic health")
        else:
            st.success("✅ Gums appear healthy")
        
        st.subheader("📸 Photo Summary")
        st.write(f"Total tooth photos: {len(st.session_state.photo_metadata)}")
        if len(st.session_state.photo_metadata) > 0:
            teeth_with_photos = st.session_state.photo_metadata["Tooth_Number"].unique()
            st.write(f"Teeth documented: {sorted(teeth_with_photos)}")
    else:
        st.info("Log data to see health summary")

with tab5:
    if len(st.session_state.logs) > 0:
        st.dataframe(st.session_state.logs.sort_values("Date", ascending=False))
        csv = st.session_state.logs.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export CSV", csv, "gingival_health_log.csv", "text/csv")
        
        if len(st.session_state.photo_metadata) > 0:
            photo_csv = st.session_state.photo_metadata.to_csv(index=False).encode('utf-8')
            st.download_button("📸 Export Photo Metadata", photo_csv, "photo_metadata.csv", "text/csv")
    else:
        st.write("No history yet")

st.sidebar.markdown("---")
st.sidebar.info("""
**🌏 Complete Oral-Systemic Health Tracker**

Tracks:
• 🪥 Oral hygiene
• 🍎 Nutrition
• 👃 Bad breath & dry mouth
• 🧠 Brain fog (Gum-Brain axis)
• ❤️ Heart health (Gum-Heart axis)
• 🦠 Gut health (Gum-Gut axis)
• 🌸 Hormones (Gum-Hormonal axis)
• 😴 Sleep (Gum-Sleep axis)
• ⚡ Stress (Gum-Stress axis)
• 🧴 Skin (Gum-Skin axis)
• 💇 Hair (Gum-Hair axis)
• 💪 Muscle (Gum-Muscle axis)
• 🦴 Bone (Gum-Bone axis)
• 🏥 Medical conditions
• 📸 Tooth photos with angles

Based on Gingival Systems Axis research framework
""")
