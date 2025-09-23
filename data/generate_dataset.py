import pandas as pdc
from faker import Faker
import uuid
import random

# Initialize Faker
fake = Faker()
Faker.seed(42)  # For reproducible results
random.seed(42)

# Define custom data for realistic startup ecosystem
ROLES = ["Founder", "Co-founder", "Engineer", "PM", "Investor", "Other"]
STAGES = ["none", "pre-seed", "seed", "series A", "growth"]

# Startup keywords by category
KEYWORDS_POOL = [
    "healthtech", "AI", "marketplace", "fintech", "edtech", "SaaS", "blockchain", 
    "e-commerce", "mobile", "IoT", "cybersecurity", "cleantech", "biotech", "adtech",
    "proptech", "foodtech", "logistics", "automation", "analytics", "cloud",
    "developer tools", "productivity", "social", "gaming", "VR", "AR", "robotics",
    "energy", "agriculture", "retail", "travel", "fitness", "beauty", "fashion"
]

# Business ideas templates by category
IDEA_TEMPLATES = {
    "healthtech": [
        "AI-powered diagnostic platform for early disease detection",
        "Telemedicine app connecting rural patients with specialists",
        "Wearable device for continuous health monitoring",
        "Digital therapy platform for mental health support",
        "Remote patient monitoring system for chronic conditions",
        "DNA-based personalized nutrition platform",
        "Mobile app for medication adherence tracking",
        "Virtual physiotherapy sessions with motion tracking",
        "AI chatbot for mental health triage",
        "Blockchain-based medical record storage",
        "Voice-enabled app for elderly health management",
        "Predictive analytics for hospital resource allocation",
        "IoT-enabled smart pill dispenser",
        "Crowdsourced platform for clinical trial recruitment",
        "Genomics-based disease risk prediction",
        "Remote ultrasound device controlled by specialists",
        "Smart glasses for visually impaired assistance",
        "Digital twin of the human body for simulation",
        "On-demand mobile lab testing services",
        "AI tool for early detection of rare diseases",
        "Wearable hydration and nutrition tracker",
        "Health gamification app for lifestyle improvement",
        "Robotic exoskeleton for physical rehabilitation",
        "VR-based pain distraction therapy",
        "Home diagnostics kit with AI interpretation",
        "EHR-integrated AI drug interaction alerts",
        "Personalized fertility tracking and planning app",
        "AI-powered triage system for emergency rooms",
        "Subscription-based preventive health checkups",
        "Marketplace for at-home caregivers and nurses",
        "IoT air quality monitor linked to respiratory health",
        "Mobile app for postpartum support and recovery",
        "AI system for optimizing clinical trial design",
        "Platform for secure doctor-patient second opinions"
    ],
    "fintech": [
        "Blockchain-based payment solution for cross-border transfers",
        "AI investment advisor for retail investors",
        "Digital banking platform for small businesses",
        "Cryptocurrency trading app with social features",
        "Peer-to-peer lending platform for underserved markets",
        "AI tool for credit scoring of gig workers",
        "Voice-enabled banking assistant",
        "Micro-investing app for spare change",
        "Blockchain-based insurance claims management",
        "Robo-advisor with ESG investment options",
        "Buy-now-pay-later service for education expenses",
        "Crowdfunding platform for local businesses",
        "AI-driven fraud detection for e-commerce",
        "Mobile-first neobank for teenagers",
        "DeFi yield optimization platform",
        "Real-time FX rate locking app for travelers",
        "Invoice factoring platform for freelancers",
        "Smart contract-based property rental payments",
        "Gamified savings app for children",
        "Rural-focused mobile wallet with offline payments",
        "Tokenized real estate investment marketplace",
        "AI chatbot for personal finance coaching",
        "Blockchain-based loyalty rewards exchange",
        "Small-ticket insurance platform for gig workers",
        "P2P remittance service using stablecoins",
        "Biometric-based mobile payments",
        "Community-driven investment syndicate platform",
        "Carbon credit trading fintech platform",
        "AI platform for regulatory compliance automation",
        "Crypto-backed lending platform",
        "Open banking API for fintech startups",
        "App for dynamic utility bill splitting among roommates",
        "Wealth tracking dashboard with AI recommendations",
        "Smart pension planning and automation tool"
    ],
    "AI": [
        "Machine learning platform for business process automation",
        "Computer vision solution for quality control in manufacturing",
        "Natural language processing tool for customer service",
        "Predictive analytics platform for supply chain optimization",
        "AI-powered resume screening tool",
        "Generative AI for personalized marketing campaigns",
        "AI-based code review assistant",
        "Voice synthesis platform for realistic dubbing",
        "AI scheduling assistant for enterprises",
        "Fraud detection system using anomaly detection",
        "AI-powered real estate price prediction engine",
        "Computer vision app for plant disease detection",
        "AI-powered creative design suggestion tool",
        "Speech-to-text platform with multilingual support",
        "AI forecasting tool for energy consumption",
        "Virtual AI influencer creation platform",
        "AI-based negotiation bot for procurement",
        "Synthetic data generation platform",
        "AI music composition for content creators",
        "AI engine for personalized fitness plans",
        "Emotion recognition for video conferencing",
        "AI writing assistant for legal documents",
        "AI tutor for STEM education",
        "AI moderation tool for online communities",
        "AI-powered sports performance analytics",
        "AI-powered cybersecurity intrusion detection",
        "Voice cloning as a service",
        "Predictive AI maintenance for industrial equipment",
        "AI-powered weather prediction for agriculture",
        "AI for automated video editing",
        "AI coach for public speaking training",
        "AI-powered news summarization tool",
        "AI co-pilot for e-commerce merchandising"
    ],
    "marketplace": [
        "B2B marketplace connecting manufacturers with suppliers",
        "Peer-to-peer platform for sharing professional equipment",
        "Online marketplace for sustainable and eco-friendly products",
        "Digital platform connecting freelancers with enterprise clients",
        "Local farm-to-table produce marketplace",
        "Marketplace for secondhand luxury goods authentication",
        "Online platform for renting sports gear",
        "Digital art and NFT marketplace for creators",
        "Marketplace for verified home repair professionals",
        "Subscription-based book swap platform",
        "Marketplace for custom 3D printing services",
        "Online skills barter exchange",
        "Marketplace for refurbished electronics",
        "Peer-to-peer parking space rental platform",
        "Marketplace for on-demand photography services",
        "Marketplace for ethically sourced handmade crafts",
        "Online car-sharing marketplace for communities",
        "Marketplace for short-term warehouse rentals",
        "On-demand catering marketplace",
        "Marketplace for eco-friendly fashion rentals",
        "Marketplace for personalized coaching sessions",
        "Marketplace for zero-waste products",
        "Student-to-student tutoring marketplace",
        "Marketplace for adventure travel guides",
        "Digital marketplace for corporate wellness services",
        "Marketplace for secondhand office furniture",
        "Community-driven local event ticket exchange",
        "Marketplace for plant swapping and sales",
        "Freelance marketplace for AI and data science talent",
        "Marketplace for drone photography services",
        "Marketplace for pop-up retail spaces",
        "Marketplace for pet sitting and dog walking",
        "Marketplace for curated subscription boxes"
    ],
    "edtech": [
        "Interactive learning platform using gamification",
        "AI-powered tutoring system for personalized education",
        "Virtual reality training platform for technical skills",
        "Online coding bootcamp with job placement guarantee",
        "Peer-to-peer language learning platform",
        "AI writing assistant for academic research",
        "Gamified math learning app for kids",
        "VR history immersion experiences for students",
        "Adaptive test preparation platform",
        "Online debate practice community",
        "Platform for project-based STEM learning",
        "App for soft skills microlearning",
        "AI-driven plagiarism detection tool",
        "Marketplace for online music lessons",
        "Digital portfolio builder for students",
        "AI co-pilot for lesson planning",
        "VR-based surgical training platform",
        "Collaborative note-taking platform for classrooms",
        "AI teaching assistant chatbot",
        "Global mentorship matching platform",
        "Digital flashcard app with spaced repetition",
        "Immersive storytelling platform for education",
        "Micro-courses for professionals with certifications",
        "Edtech platform for special needs learning",
        "Blockchain credential verification system",
        "AI grading tool for essays and exams",
        "Virtual classroom with real-time collaboration",
        "App for parental engagement in student progress",
        "Skill-based certification marketplace",
        "Personalized career guidance using AI",
        "AR app for science experiments",
        "AI engine for learning style diagnostics",
        "Collaborative research network for students"
    ]
}

def generate_founder_data():
    """Generate a single founder record"""
    
    # Basic info
    founder_id = str(uuid.uuid4())
    gender = random.choice(['male', 'female'])
    first_name = fake.first_name_male() if gender == 'male' else fake.first_name_female()
    last_name = fake.last_name()
    founder_name = f"{first_name} {last_name}"
    
    # Role and stage
    role = random.choice(ROLES)
    stage = random.choice(STAGES)
    
    # Company and location
    company_name = fake.company()
    city = fake.city()
    country = fake.country()
    location = f"{city}, {country}"
    
    # Email (realistic looking)
    company_domain = company_name.lower().replace(' ', '').replace(',', '').replace('.', '').replace("'", '')[:15]
    email_formats = [
        f"{first_name.lower()}.{last_name.lower()}@{company_domain}",
        f"{first_name.lower()}@{company_domain}",
        f"{first_name[0].lower()}{last_name.lower()}@{company_domain}"
    ]
    email = random.choice(email_formats) + random.choice(['.com', '.io', '.ai', '.co'])
    
    # Keywords (2-5 relevant keywords)
    num_keywords = random.randint(2, 5)
    keywords = random.sample(KEYWORDS_POOL, num_keywords)
    keywords_str = ", ".join(keywords)
    
    # Generate idea based on primary keyword
    primary_keyword = keywords[0]
    if primary_keyword in IDEA_TEMPLATES:
        idea = random.choice(IDEA_TEMPLATES[primary_keyword])
    else:
        # Generic ideas for other keywords
        generic_ideas = [
            f"Innovative {primary_keyword} solution for enterprise clients",
            f"Consumer-focused {primary_keyword} platform with mobile-first approach",
            f"B2B {primary_keyword} tool that increases operational efficiency",
            f"AI-enhanced {primary_keyword} service for modern businesses"
        ]
        idea = random.choice(generic_ideas)
    
    # Background experiences
    backgrounds = [
        "Former Google engineer", "Ex-McKinsey consultant", "Stanford MBA graduate",
        "Serial entrepreneur", "Former startup CTO", "Investment banking background",
        "PhD in Computer Science", "Y Combinator alum", "Former Facebook PM",
        "Ex-Tesla engineer", "Harvard Business School graduate", "Former Uber executive",
        "MIT graduate", "Former Amazon manager", "Berkeley PhD", "Ex-Apple designer",
        "Former SpaceX engineer", "Oxford MBA graduate", "Ex-Deloitte consultant",
        "Former Airbnb product lead", "Ex-Salesforce executive", "Former Goldman Sachs analyst",
        "PhD in Neuroscience", "Former Microsoft AI researcher", "London School of Economics graduate",
        "Former Stripe engineer", "Ex-Boston Consulting Group consultant", "Former Dropbox designer",
        "Ex-Adobe product manager", "Wharton School MBA graduate", "Former Palantir data scientist",
        "Former NASA researcher", "Cambridge PhD", "Ex-Snapchat growth lead",
        "Former Lyft operations manager", "Ex-Intel hardware engineer", "Carnegie Mellon graduate",
        "Former Shopify product manager", "Ex-NASA software engineer", "INSEAD MBA graduate",
        "Former IBM researcher", "Ex-Reddit community manager", "Former Twitter engineer",
        "Former Bain & Company consultant", "Ex-Sequoia Capital associate", "Former ByteDance AI researcher"
    ]

    # Skills
    skills = [
        "machine learning", "product management", "software development", "data science",
        "business development", "fundraising", "team building", "go-to-market strategy",
        "user experience design", "growth hacking", "artificial intelligence", "blockchain development",
        "cybersecurity", "cloud architecture", "mobile development", "marketing automation",
        "natural language processing", "computer vision", "quantitative analysis",
        "financial modeling", "UX research", "data engineering", "full-stack development",
        "deep learning", "hardware prototyping", "AR/VR development", "game design",
        "sales strategy", "enterprise partnerships", "bioinformatics", "robotics engineering",
        "supply chain optimization", "digital advertising", "no-code development",
        "operations management", "customer success", "tokenomics design", "network security",
        "data visualization", "human-computer interaction", "API design", "quantum computing",
        "SaaS growth strategy", "distributed systems", "edge computing", "open-source contributions",
        "product-led growth", "brand strategy"
    ]

    # Outcomes
    outcomes = [
        "raised $2M seed round", "grew user base to 100K+", "achieved $1M ARR",
        "successful exit via acquisition", "led team of 50+ engineers", "launched in 15 countries",
        "built platform serving 1M+ users", "generated $10M+ in revenue", "filed 5 patents",
        "scaled from 0 to 100 employees", "achieved break-even in 18 months",
        "closed $10M Series A", "expanded operations to 25+ cities", "partnered with Fortune 500 companies",
        "achieved 95% customer retention", "recognized on Forbes 30 Under 30", 
        "featured in TechCrunch and Wired", "won industry innovation award", "grew ARR to $50M+",
        "bootstrapped to profitability", "built developer community of 200K+", 
        "secured government contracts", "launched IPO on NASDAQ", "acquired by global tech giant",
        "reduced churn by 40%", "opened offices in 3 continents", "built a marketplace with 500K sellers",
        "launched app downloaded 5M+ times", "patented novel AI algorithm", "scaled cloud infrastructure to millions of users",
        "raised $100M+ across funding rounds", "achieved unicorn status ($1B valuation)", 
        "recognized as industry thought leader", "grew social media following to 1M+", 
        "launched SaaS product used by Fortune 100 companies", "reduced operational costs by 60%", 
        "expanded team to 500+ employees", "hit $200M GMV in 2 years", "launched in emerging markets with 10M+ users"
    ]

    
    # Create bio (2-4 sentences)
    background = random.choice(backgrounds)
    skill_set = random.sample(skills, random.randint(2, 3))
    outcome = random.choice(outcomes) if random.random() > 0.3 else None  # 70% chance of outcome
    
    bio_parts = [f"{background} with expertise in {', '.join(skill_set)}."]
    
    if role in ["Founder", "Co-founder"]:
        bio_parts.append(f"Currently building {company_name} to revolutionize the {primary_keyword} industry.")
    elif role == "Engineer":
        bio_parts.append(f"Lead engineer at {company_name} focusing on scalable {primary_keyword} solutions.")
    elif role == "PM":
        bio_parts.append(f"Product manager at {company_name} driving {primary_keyword} product strategy.")
    elif role == "Investor":
        bio_parts.append(f"Angel investor and advisor specializing in {primary_keyword} startups.")
    else:
        bio_parts.append(f"Working in the {primary_keyword} space with focus on innovation and growth.")
    
    if outcome:
        bio_parts.append(f"Previously {outcome}.")
    
    about = " ".join(bio_parts)
    
    # LinkedIn URL
    linkedin_url = f"https://linkedin.com/in/{first_name.lower()}-{last_name.lower()}-{random.randint(100, 999)}"
    
    # Notes (optional, 60% chance of having notes)
    notes = ""
    if random.random() > 0.4:
        note_options = [
            "Looking for technical co-founder",
            "Open to advisory roles", 
            "Available for consulting",
            "Seeking Series A funding",
            "Interested in partnerships",
            "Building remote team",
            "Focus on sustainable tech",
            "Expanding to European markets",
            "Former YC S21 cohort",
            "Angel investor in 10+ startups"
        ]
        notes = random.choice(note_options)
    
    return {
        'id': founder_id,
        'founder_name': founder_name,
        'email': email,
        'role': role,
        'company': company_name,
        'location': location,
        'idea': idea,
        'about': about,
        'keywords': keywords_str,
        'stage': stage,
        'linkedin': linkedin_url,
        'notes': notes
    }

def main():
    """Generate the complete dataset"""
    print("Generating 700 founder records...")
    
    # Generate all records
    founders_data = []
    for i in range(700):
        founder = generate_founder_data()
        founders_data.append(founder)
        
        if (i + 1) % 100 == 0:
            print(f"Generated {i + 1} records...")
    
    # Create DataFrame
    df = pd.DataFrame(founders_data)
    
    # Save to CSV
    df.to_csv('founders_dataset.csv', index=False)
    print(f"Dataset saved as 'founders_dataset.csv'")
    print(f"Dataset shape: {df.shape}")
    
    # Display first few rows for verification
    print("\nFirst 5 rows:")
    print(df.head())
    
    # Show data quality stats
    print(f"\nDataset Statistics:")
    print(f"Total records: {len(df)}")
    print(f"Unique companies: {df['company'].nunique()}")
    print(f"Role distribution:")
    print(df['role'].value_counts())
    print(f"\nStage distribution:")
    print(df['stage'].value_counts())

if __name__ == "__main__":
    main()
