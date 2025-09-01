import streamlit as st
import google.generativeai as genai
import random
import time

# Configure Streamlit page
st.set_page_config(
    page_title="⚡ Instant Tech Story Generator",
    page_icon="🚀",
    layout="wide"
)

# Get API key from secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ Please add GEMINI_API_KEY to your Streamlit secrets")
    st.stop()

# 100+ High-Engagement Tech Topics
VIRAL_TECH_TOPICS = [
    # AI & Machine Learning
    "The day AI became smarter than my professor",
    "I asked ChatGPT to write my resume and got 5 job offers",
    "My AI girlfriend broke up with me (seriously)",
    "I trained an AI to predict my mood and it's scary accurate",
    "Why AI will replace teachers in 5 years (and I'm not mad about it)",
    "I let AI plan my entire week and it changed my life",
    "The AI that saved my failing startup",
    "I discovered my roommate is secretly an AI researcher",
    "How I used AI to ace every exam without studying",
    "The creepiest thing AI told me about my future",
    
    # Quantum & Physics
    "Quantum physics explained like you're 5 (and why it matters)",
    "I accidentally discovered time travel in my physics lab",
    "Why quantum computers will break the internet (soon)",
    "The multiverse theory that keeps me awake at night",
    "I met a quantum physicist and my mind exploded",
    "How quantum entanglement is like my toxic relationship",
    "The Schrödinger's cat experiment that changed everything",
    "Why parallel universes might explain my bad luck",
    "I tried to build a quantum computer in my dorm",
    "The quantum mystery that scientists can't solve",
    
    # Space & Universe
    "What I learned from staring at stars for 100 nights",
    "The day we discovered we're not alone in the universe",
    "I calculated how long it takes to reach Mars (spoiler: too long)",
    "Why black holes are actually portals to other dimensions",
    "The space mission that failed but taught us everything",
    "I applied to be an astronaut and here's what happened",
    "The asteroid that almost ended everything",
    "Why we need to colonize Mars before 2030",
    "The alien signal that changed everything we know",
    "I witnessed a UFO and no one believes me",
    
    # Future Technology
    "I lived in a smart home for 30 days and here's what happened",
    "The day robots took over my job (and why I'm grateful)",
    "I tried brain-computer interface and read minds",
    "Why we'll all be cyborgs by 2035",
    "The technology that will make death optional",
    "I experienced virtual reality so real I forgot reality",
    "The app that predicts your death date (and it's accurate)",
    "Why flying cars are finally happening in 2025",
    "I tested Neuralink and became superhuman",
    "The technology that reads your thoughts",
    
    # Blockchain & Crypto
    "I lost $10,000 in crypto and learned this valuable lesson",
    "The blockchain technology that will revolutionize everything",
    "Why NFTs are making teenagers millionaires",
    "I created my own cryptocurrency in my dorm room",
    "The crypto scam that taught me about human nature",
    "How I became a blockchain developer in 30 days",
    "The decentralized future that's coming whether we like it or not",
    "I tried living on Bitcoin for a month",
    "Why Web3 will replace the internet as we know it",
    "The DeFi protocol that changed my life",
    
    # Biotechnology & Life Sciences
    "I edited my own DNA using CRISPR (true story)",
    "The day we cured aging (and why it's terrifying)",
    "I cloned myself and met my clone",
    "Why synthetic biology will feed 10 billion people",
    "The biotech breakthrough that ended depression",
    "I grew organs in a lab and saved lives",
    "The genetic modification that made me superhuman",
    "Why we'll all live to 150 years old",
    "I discovered the secret to immortality in bacteria",
    "The bioengineering project that went too far",
    
    # Consciousness & Mind
    "I uploaded my consciousness to the cloud",
    "The day we proved consciousness is just code",
    "I experienced ego death through technology",
    "Why your thoughts aren't actually yours",
    "The meditation app that showed me the universe",
    "I connected my brain to the internet for 24 hours",
    "The consciousness transfer experiment that worked",
    "Why free will is an illusion (and science proves it)",
    "I communicated with my subconscious mind",
    "The technology that measures your soul",
    
    # Social Technology Impact
    "How social media rewired my brain (the scary truth)",
    "I deleted all social media for a year and this happened",
    "The algorithm that knows you better than yourself",
    "Why TikTok is actually mind control",
    "I studied the psychology of viral content",
    "The social experiment that revealed human nature",
    "How technology is making us lonelier",
    "I lived like it's 1995 for a month (no internet)",
    "The app addiction that almost ruined my life",
    "Why Gen Z is the last purely human generation",
    
    # Energy & Environment
    "I built a fusion reactor in my garage (almost)",
    "The renewable energy breakthrough that changes everything",
    "How I powered my house with my footsteps",
    "The climate technology that will save Earth",
    "I lived off-grid for 6 months using only solar",
    "The energy source that governments don't want you to know",
    "How I turned CO2 into money",
    "The battery technology that powers the future",
    "I created energy from thin air",
    "Why nuclear fusion is finally here",
    
    # Philosophy of Technology
    "The day I realized we're living in a simulation",
    "Technology killed God (and here's what replaced Him)",
    "I discovered the meaning of life through code",
    "Why humans are becoming obsolete",
    "The technological singularity started yesterday",
    "I found proof we're in the Matrix",
    "The ethics of playing God with technology",
    "Why the future belongs to AI, not humans",
    "I solved the meaning of existence using quantum mechanics",
    "The philosophy that will guide our digital future"
]

# Viral writing styles for maximum engagement
VIRAL_STYLES = [
    "Shocked college student sharing mind-blowing discovery",
    "Confused but curious person explaining complex stuff simply", 
    "Excited researcher who just made a breakthrough",
    "Skeptical student who became a believer",
    "Ordinary person experiencing extraordinary technology",
    "Failed experiment that taught valuable lessons",
    "Accidental discovery that changed everything",
    "Personal journey into deep tech rabbit hole"
]

# Main App
st.title("🚀 ⚡ INSTANT TECH STORY GENERATOR")
st.markdown("**One-click viral tech stories that make money** • No inputs needed • Maximum engagement")

# The magic button
if st.button("🎯 GENERATE VIRAL TECH STORY", type="primary", use_container_width=True):
    with st.spinner("🧠 AI is crafting your viral story... ⚡"):
        try:
            # Randomly select topic and style
            topic = random.choice(VIRAL_TECH_TOPICS)
            style = random.choice(VIRAL_STYLES)
            
            # Initialize model
            model = genai.GenerativeModel('gemini-2.0-flash-lite')
            
            # Ultra-humanized prompt for maximum engagement
            story_prompt = f"""
            Write an extremely engaging, human story about: "{topic}"
            
            Writing style: {style}
            
            CRITICAL REQUIREMENTS FOR VIRAL SUCCESS:
            - Write like a real college student who just experienced something mind-blowing
            - Use simple language with natural imperfections and typos
            - Include personal emotions, reactions, and "holy shit" moments
            - Add specific details that make it feel 100% authentic
            - Use conversational tone with contractions, casual language
            - Include relatable struggles and "aha" moments
            - Make it addictive to read - each paragraph should hook for the next
            - Add subtle cliffhangers and curiosity gaps
            - Include personal thoughts in parentheses
            - Use varied sentence lengths naturally
            - Add some informal expressions and reactions
            - Make it shareable and discussion-worthy
            
            Structure for maximum engagement:
            1. Hook opening (something shocking/unexpected)
            2. Personal context (why this matters to me)
            3. The journey/discovery (with emotions and reactions)
            4. The revelation/breakthrough (mind-blown moment)
            5. Impact on life/worldview (what this means)
            6. Call for discussion (question/thought for readers)
            
            Write EXACTLY 500 words. Make it impossible to stop reading.
            """
            
            # Generate story
            story_response = model.generate_content(story_prompt)
            story = story_response.text
            
            # Generate viral title
            title_prompt = f"""
            Create the most clickable, viral title for this story about: {topic}
            
            Make it:
            - Curiosity-driven and impossible to ignore
            - Personal and emotional
            - Uses numbers or specific claims when possible
            - Sounds like a real person wrote it
            - 6-12 words maximum
            - Creates FOMO or surprise
            
            Examples of viral style:
            "This AI Discovery Made Me Question Reality"
            "I Found Proof We're Living in a Simulation"
            "Scientists Hate This One Quantum Trick"
            
            Story context: {story[:150]}
            """
            
            title_response = model.generate_content(title_prompt)
            title = title_response.text.strip().replace('"', '')
            
            # Generate engaging description
            desc_prompt = f"""
            Write a compelling 2-3 sentence description that makes people NEED to read this story.
            
            Make it:
            - Create curiosity and FOMO
            - Personal and relatable
            - Tease the main revelation without giving it away
            - Sound like the author wrote it themselves
            
            Story: {story}
            """
            
            desc_response = model.generate_content(desc_prompt)
            description = desc_response.text.strip()
            
            # Generate authentic disclaimer
            disclaimers = [
                "This is my personal experience and opinion. Everyone's journey with technology is different, and yours might be too.",
                "Based on my real experience. I'm not a expert, just someone who got curious and went down a rabbit hole.",
                "This reflects my personal experience and research. I'm still learning, and technology evolves fast.",
                "My personal take on this tech topic. I might be wrong about some things, but this is what I experienced.",
                "Just sharing my personal journey and thoughts. Technology affects everyone differently."
            ]
            
            disclaimer = random.choice(disclaimers)
            
            # Display results
            st.success("✅ Viral tech story generated! Ready to copy-paste to Milyin")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("📝 Generated Content")
                
                st.markdown("**1. TITLE:**")
                st.code(title, language=None)
                
                st.markdown("**2. STORY (500 words):**")
                st.text_area("Copy this story:", story, height=300, key="story")
                
            with col2:
                st.subheader("📋 Additional Fields")
                
                st.markdown("**3. DESCRIPTION:**")
                st.text_area("Copy this description:", description, height=100, key="desc")
                
                st.markdown("**4. DISCLAIMER:**")
                st.text_area("Copy this disclaimer:", disclaimer, height=80, key="disclaimer")
                
                # Stats
                word_count = len(story.split())
                st.info(f"📊 Word count: {word_count}")
                st.info(f"🎯 Topic: {topic}")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Quick stats and tips
st.markdown("---")
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.metric("🔥 Viral Topics", "100+", "Tech focused")

with col_b:
    st.metric("⚡ Generation Time", "~30s", "Instant results")

with col_c:
    st.metric("💰 Engagement Level", "High", "Money making")

# Pro tips
with st.expander("💡 VIRAL STRATEGY TIPS"):
    st.markdown("""
    **🚀 For Maximum Money-Making Success:**
    
    • **Post 2-3 stories daily** during peak hours (7-9 AM, 6-8 PM)
    • **Engage in comments** within first hour of posting
    • **Use trending hashtags** related to AI, tech, future
    • **Cross-promote** on social media with story snippets
    • **Create series** - "Part 1 of my AI journey..."
    • **Ask questions** at the end to boost comments
    • **Share personal failures** - people love authenticity
    • **Use numbers** in titles when possible
    • **Create controversy** (respectfully) for more engagement
    • **Follow up** on popular stories with related content
    
    **🎯 Best performing topics:** AI consciousness, simulation theory, future predictions, personal tech experiments
    """)

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p><strong>⚡ FASTEST • MOST VIRAL • MAXIMUM ENGAGEMENT</strong></p>
        <p>Built for serious content creators who want to make money fast 🚀💰</p>
    </div>
    """, 
    unsafe_allow_html=True
)
