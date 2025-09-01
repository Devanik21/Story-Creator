import streamlit as st
import google.generativeai as genai
import random
import re

# Configure Streamlit page
st.set_page_config(
    page_title="Story Generator ",
    page_icon="📝",
    layout="wide"
)

# Title
st.title("📝 Milyin Story Generator")
st.markdown("Generate humanized, engaging stories for content monetization")

# Sidebar for API key and settings
with st.sidebar:
    st.header("🔧 Settings")
    
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    
    if api_key:
        genai.configure(api_key=api_key)
        st.success("✅ API Key configured!")
    
    st.header("📊 Story Parameters")
    story_genre = st.selectbox(
        "Story Genre:",
        ["Personal Experience", "College Life", "Friendship", "Travel", "Learning", 
         "Motivation", "Life Lessons", "Funny Moments", "Challenges", "Success Stories"]
    )
    
    writing_style = st.selectbox(
        "Writing Style:",
        ["Casual & Conversational", "Simple & Direct", "Emotional & Personal", 
         "Humorous", "Reflective"]
    )
    
    target_audience = st.selectbox(
        "Target Audience:",
        ["College Students", "Young Adults", "General Readers", "Professionals"]
    )

# Main content area
if api_key:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Generate Story")
        
        # Topic input
        topic = st.text_input(
            "Enter a story topic or theme:",
            placeholder="e.g., My first day at college, A lesson learned from failure, etc."
        )
        
        # Keywords for SEO
        keywords = st.text_input(
            "Keywords (for better engagement):",
            placeholder="e.g., college, students, friendship, success"
        )
        
        if st.button("🚀 Generate Story", type="primary"):
            if topic:
                with st.spinner("Crafting your humanized story... ✨"):
                    try:
                        # Initialize the model
                        model = genai.GenerativeModel('gemini-2.0-flash-lite')
                        
                        # Humanization techniques in the prompt
                        humanization_prompt = f"""
                        Write a very human, authentic story about: {topic}
                        
                        IMPORTANT HUMANIZATION REQUIREMENTS:
                        - Write like a real {target_audience.lower()} would write
                        - Use simple, natural language with slight imperfections
                        - Include personal thoughts, emotions, and relatable experiences
                        - Add casual expressions, contractions, and conversational tone
                        - Include specific details that feel lived-in and authentic
                        - Vary sentence lengths naturally
                        - Use transition words organically
                        - Include some informal language and personal observations
                        - Make it feel like someone sharing a real experience
                        
                        Style: {writing_style}
                        Genre: {story_genre}
                        Keywords to naturally include: {keywords}
                        
                        The story should be exactly 500 words and feel completely human-written.
                        """
                        
                        # Generate the main story
                        story_response = model.generate_content(humanization_prompt)
                        story_content = story_response.text
                        
                        # Generate title
                        title_prompt = f"""
                        Create a catchy, human-sounding title for this story about {topic}.
                        The title should be:
                        - Engaging and clickable
                        - Natural, not overly optimized
                        - Relatable to {target_audience.lower()}
                        - Between 5-10 words
                        
                        Story context: {story_content[:200]}...
                        """
                        
                        title_response = model.generate_content(title_prompt)
                        title = title_response.text.strip().replace('"', '')
                        
                        # Generate description/summary
                        description_prompt = f"""
                        Write a short, engaging summary (2-3 sentences) for this story.
                        Make it sound natural and human-written, like someone describing their own story.
                        Avoid marketing language - keep it personal and authentic.
                        
                        Story: {story_content}
                        """
                        
                        description_response = model.generate_content(description_prompt)
                        description = description_response.text.strip()
                        
                        # Generate disclaimer
                        disclaimer_options = [
                            "This story is based on my personal experience and perspective. Different people might have different experiences in similar situations.",
                            "The events described in this story are from my personal experience. Names and some details may have been changed for privacy.",
                            "This is my personal story and reflects my own experience. Your experience might be different, and that's completely okay.",
                            "This story shares my personal journey and thoughts. Everyone's experience is unique, so yours might be different.",
                            "Based on my personal experience - everyone's journey is different, and this is just my perspective on things."
                        ]
                        
                        disclaimer = random.choice(disclaimer_options)
                        
                        # Store in session state
                        st.session_state.generated_title = title
                        st.session_state.generated_story = story_content
                        st.session_state.generated_description = description
                        st.session_state.generated_disclaimer = disclaimer
                        
                    except Exception as e:
                        st.error(f"Error generating story: {str(e)}")
            else:
                st.warning("Please enter a topic for your story.")
    
    with col2:
        st.header("📋 Generated Content")
        
        if 'generated_title' in st.session_state:
            # Display generated content
            st.subheader("1. Title")
            title_container = st.container()
            with title_container:
                st.text_area("Copy this title:", st.session_state.generated_title, height=60, key="title_output")
            
            st.subheader("2. Story Body (500 words)")
            story_container = st.container()
            with story_container:
                st.text_area("Copy this story:", st.session_state.generated_story, height=300, key="story_output")
            
            st.subheader("3. Description/Summary")
            desc_container = st.container()
            with desc_container:
                st.text_area("Copy this description:", st.session_state.generated_description, height=80, key="desc_output")
            
            st.subheader("4. Disclaimer/Notice")
            disclaimer_container = st.container()
            with disclaimer_container:
                st.text_area("Copy this disclaimer:", st.session_state.generated_disclaimer, height=80, key="disclaimer_output")
            
            # Word count
            word_count = len(st.session_state.generated_story.split())
            st.info(f"📊 Story word count: {word_count} words")
            
            # Quick copy buttons
            st.markdown("---")
            st.subheader("🚀 Quick Actions")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("🔄 Generate New Story"):
                    # Clear session state to generate new content
                    for key in ['generated_title', 'generated_story', 'generated_description', 'generated_disclaimer']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
            
            with col_b:
                # Download as text file
                full_content = f"""TITLE:
{st.session_state.generated_title}

STORY:
{st.session_state.generated_story}

DESCRIPTION:
{st.session_state.generated_description}

DISCLAIMER:
{st.session_state.generated_disclaimer}"""
                
                st.download_button(
                    label="📥 Download All Content",
                    data=full_content,
                    file_name=f"story_{st.session_state.generated_title[:20].replace(' ', '_')}.txt",
                    mime="text/plain"
                )

else:
    st.warning("👈 Please enter your Gemini API key in the sidebar to start generating stories.")
    
    with st.expander("ℹ️ How to get a Gemini API Key"):
        st.markdown("""
        1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Sign in with your Google account
        3. Click "Create API Key"
        4. Copy the generated API key
        5. Paste it in the sidebar
        """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>💡 <strong>Tips for Success:</strong></p>
        <p>• Use specific, relatable topics • Engage with your audience • Post consistently • Focus on authentic storytelling</p>
        <p>Built for content creators who want to monetize through engaging stories 🚀</p>
    </div>
    """, 
    unsafe_allow_html=True
)
