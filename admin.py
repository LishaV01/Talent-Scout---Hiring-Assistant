"""
Admin Dashboard for TalentScout Hiring Assistant
View and export candidate data
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json
from database import DatabaseManager

def main():
    st.set_page_config(
        page_title="TalentScout Admin Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 TalentScout Admin Dashboard")
    st.markdown("---")
    
    # Initialize database
    db = DatabaseManager()
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Select Page",
            ["Overview", "Candidate Details", "Export Data"]
        )
        
        st.markdown("---")
        st.caption("TalentScout Admin Panel v1.0")
    
    if page == "Overview":
        # Get all candidates
        candidates = db.get_all_candidates(limit=1000)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Candidates", len(candidates))
        
        with col2:
            avg_exp = sum(c['years_experience'] for c in candidates if c['years_experience']) / len(candidates) if candidates else 0
            st.metric("Avg. Experience", f"{avg_exp:.1f} years")
        
        with col3:
            completed = len([c for c in candidates if c['email'] and c['phone']])
            st.metric("Completed Profiles", completed)
        
        with col4:
            today_count = len([c for c in candidates if c['created_at'] and c['created_at'].startswith(datetime.now().strftime('%Y-%m-%d'))])
            st.metric("Today's Candidates", today_count)
        
        st.markdown("---")
        
        # Candidates table
        st.subheader("Recent Candidates")
        
        if candidates:
            # Convert to DataFrame for display
            df = pd.DataFrame(candidates)
            
            # Format datetime columns
            for col in ['created_at', 'updated_at']:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d %H:%M')
            
            # Display table
            st.dataframe(
                df[['id', 'full_name', 'email', 'phone', 'years_experience', 
                    'current_location', 'created_at']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No candidates found in the database.")
    
    elif page == "Candidate Details":
        st.subheader("View Candidate Details")
        
        # Get candidate list for selection
        candidates = db.get_all_candidates(limit=1000)
        
        if candidates:
            # Create selection dropdown
            candidate_options = {
                f"{c['full_name']} ({c['email']})": c['id'] 
                for c in candidates 
                if c['full_name'] and c['email']
            }
            
            selected = st.selectbox(
                "Select a candidate:",
                options=list(candidate_options.keys())
            )
            
            if selected:
                candidate_id = candidate_options[selected]
                
                # Get full candidate data
                candidate_data = db.get_candidate_full_data(candidate_id)
                
                if candidate_data:
                    # Display candidate info
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 👤 Personal Information")
                        st.write(f"**Name:** {candidate_data['full_name']}")
                        st.write(f"**Email:** {candidate_data['email']}")
                        st.write(f"**Phone:** {candidate_data['phone']}")
                        st.write(f"**Location:** {candidate_data['current_location']}")
                    
                    with col2:
                        st.markdown("### 💼 Professional Details")
                        st.write(f"**Experience:** {candidate_data['years_experience']} years")
                        st.write(f"**Desired Positions:** {', '.join(candidate_data['desired_positions'])}")
                        st.write(f"**Tech Stack:** {', '.join(candidate_data['tech_stack'])}")
                    
                    st.markdown("---")
                    
                    # Technical Q&A
                    st.markdown("### 📝 Technical Interview")
                    
                    qa_data = candidate_data.get('technical_qa', [])
                    if qa_data:
                        for qa in qa_data:
                            with st.expander(f"Question {qa['question_index'] + 1}"):
                                st.write(f"**Question:** {qa['question']}")
                                if qa['answer']:
                                    st.write(f"**Answer:** {qa['answer']}")
                                    st.caption(f"Answered at: {qa['answered_at']}")
                                else:
                                    st.warning("No answer provided")
                    else:
                        st.info("No technical questions found for this candidate.")
                    
                    # Conversation History
                    with st.expander("💬 Full Conversation History"):
                        logs = candidate_data.get('conversation_logs', [])
                        if logs:
                            for log in logs:
                                role_emoji = "👤" if log['role'] == 'user' else "🤖"
                                st.markdown(f"**{role_emoji} {log['role'].title()}** ({log['timestamp']})")
                                st.write(log['content'])
                                st.markdown("---")
                        else:
                            st.info("No conversation logs found.")
        else:
            st.info("No candidates found in the database.")
    
    elif page == "Export Data":
        st.subheader("Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Export to JSON")
            st.write("Export all candidate data to a JSON file.")
            
            if st.button("Export JSON", type="primary"):
                with st.spinner("Exporting data..."):
                    filename = f"candidates_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    success = db.export_to_json(filename)
                    
                    if success:
                        st.success(f"Data exported successfully to {filename}")
                        
                        # Read and offer download
                        with open(filename, 'r') as f:
                            json_data = f.read()
                        
                        st.download_button(
                            label="Download JSON",
                            data=json_data,
                            file_name=filename,
                            mime="application/json"
                        )
                    else:
                        st.error("Failed to export data")
        
        with col2:
            st.markdown("### Export to CSV")
            st.write("Export candidate summary to CSV.")
            
            if st.button("Export CSV", type="primary"):
                candidates = db.get_all_candidates(limit=10000)
                
                if candidates:
                    df = pd.DataFrame(candidates)
                    csv = df.to_csv(index=False)
                    
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"candidates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No data to export")
        
        st.markdown("---")
        st.markdown("### Database Statistics")
        
        # Show database stats
        try:
            import os
            db_size = os.path.getsize("talentscout.db") / 1024 / 1024  # MB
            st.metric("Database Size", f"{db_size:.2f} MB")
        except:
            pass

if __name__ == "__main__":
    main()