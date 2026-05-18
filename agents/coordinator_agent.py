import time
from google import genai

from agents.resume_agent import analyze_resume
from agents.skill_gap_agent import analyze_skill_gap
from agents.interview_agent import generate_interview_questions


def run_career_workflow(client, resume, role):

    # -----------------------------------
    # RESUME ANALYSIS AGENT
    # -----------------------------------

    resume_result = analyze_resume(
        client,
        resume,
        role
    )
    
    time.sleep(2)

    # -----------------------------------
    # SKILL GAP AGENT
    # -----------------------------------

    skill_result = analyze_skill_gap(
        client,
        resume,
        role
    )
    
    time.sleep(2)

    # -----------------------------------
    # INTERVIEW PREP AGENT
    # -----------------------------------

    interview_result = generate_interview_questions(
        client,
        resume,
        role
    )
    
    time.sleep(2)
    
    # -----------------------------------
    # SYNTHESIS AGENT
    # -----------------------------------
    
    synthesis_prompt = f"""
    Current Year: 2026
    You are a senior AI Career Strategist.

    Analyze all reports carefully.
    
    Your task:
    - identify patterns
    - detect critical weaknesses
    - prioritize improvements
    - give realistic career guidance

    Resume Analysis:
    {resume_result}

    Skill Gap Analysis:
    {skill_result}

    Interview Preparation:
    {interview_result}

    Generate:

    ## Overall Career Readiness Score
    (out of 100)

    ## Critical Weaknesses
    (top 3)

    ## Top 3 Priority Improvements
    
    ## Highest Priority Skills
    (top 5)
    
    ## Top Recommended Certifications for {role}
    - certification name
    - short usefulness reason
    
    ## Suggested Projects
    (3 practical projects)

    ## Final Career Advice
    concise and actionable
    
    Be practical and realistic.
    Avoid generic motivational advice.
    """
    
    
    synthesis_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=synthesis_prompt
    )

    final_summary = synthesis_response.text

    # -----------------------------------
    # FINAL RECOMMENDATION
    # -----------------------------------

    final_recommendation = f"""
# Final Career Recommendation

Based on the complete AI analysis:

- Improve missing technical skills
- Build stronger real-world projects
- Optimize ATS keywords
- Practice interview questions regularly
- Focus on project quality over quantity
- Strengthen problem-solving abilities

## Target Role
**{role}**
"""

    # -----------------------------------
    # RETURN ALL RESULTS
    # -----------------------------------

    return (
        resume_result,
        skill_result,
        interview_result,
        final_summary,
        final_recommendation
    )