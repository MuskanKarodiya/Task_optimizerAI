import os
import json
from typing import Dict, List, Optional
import random

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def get_openai_client():
    if OPENAI_AVAILABLE and OPENAI_API_KEY:
        return OpenAI(api_key=OPENAI_API_KEY)
    return None


def analyze_emotion(text: str) -> Dict:
    client = get_openai_client()
    
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-5",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an emotion detection expert. Analyze the emotional state "
                        + "from the text and provide: emotion (happy/neutral/stressed/anxious/motivated), "
                        + "stress_level (1-10), mood_score (1-100), and a brief insight. "
                        + "Respond with JSON in this format: "
                        + "{'emotion': string, 'stress_level': number, 'mood_score': number, 'insight': string}",
                    },
                    {"role": "user", "content": text},
                ],
                response_format={"type": "json_object"},
            )
            result = json.loads(response.choices[0].message.content)
            return {
                "emotion": result.get("emotion", "neutral"),
                "stress_level": max(1, min(10, result.get("stress_level", 5))),
                "mood_score": max(1, min(100, result.get("mood_score", 50))),
                "insight": result.get("insight", "No specific insight available."),
                "ai_powered": True
            }
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return fallback_emotion_analysis(text)
    else:
        return fallback_emotion_analysis(text)


def fallback_emotion_analysis(text: str) -> Dict:
    text_lower = text.lower()
    
    positive_words = ['happy', 'great', 'excellent', 'good', 'love', 'enjoy', 'excited', 'wonderful', 'amazing']
    negative_words = ['stressed', 'tired', 'difficult', 'hard', 'overwhelmed', 'anxious', 'worried', 'exhausted']
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        emotion = "happy"
        stress_level = random.randint(1, 4)
        mood_score = random.randint(70, 95)
    elif negative_count > positive_count:
        emotion = "stressed"
        stress_level = random.randint(6, 9)
        mood_score = random.randint(30, 55)
    else:
        emotion = "neutral"
        stress_level = random.randint(4, 6)
        mood_score = random.randint(50, 70)
    
    return {
        "emotion": emotion,
        "stress_level": stress_level,
        "mood_score": mood_score,
        "insight": f"Basic analysis detected {emotion} sentiment. Add OpenAI API key for detailed AI-powered insights.",
        "ai_powered": False
    }


def suggest_tasks(member_name: str, emotion: str, stress_level: int, available_tasks: List[Dict]) -> List[Dict]:
    client = get_openai_client()
    
    if client and available_tasks:
        try:
            tasks_desc = "\n".join([f"- {t['title']} (Priority: {t['priority']}, Complexity: {t.get('complexity', 'medium')})" 
                                    for t in available_tasks])
            
            response = client.chat.completions.create(
                model="gpt-5",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a task assignment expert. Based on the team member's current "
                        + "emotional state and stress level, suggest which tasks would be most suitable. "
                        + "Respond with JSON containing an array of task recommendations with reasoning: "
                        + "{'recommendations': [{'task_title': string, 'reason': string, 'suitability_score': number}]}",
                    },
                    {
                        "role": "user", 
                        "content": f"Team member: {member_name}\nEmotion: {emotion}\nStress Level: {stress_level}/10\n\nAvailable tasks:\n{tasks_desc}"
                    },
                ],
                response_format={"type": "json_object"},
            )
            result = json.loads(response.choices[0].message.content)
            return result.get("recommendations", fallback_task_suggestions(emotion, stress_level, available_tasks))
        except Exception as e:
            print(f"Task suggestion error: {e}")
            return fallback_task_suggestions(emotion, stress_level, available_tasks)
    else:
        return fallback_task_suggestions(emotion, stress_level, available_tasks)


def fallback_task_suggestions(emotion: str, stress_level: int, available_tasks: List[Dict]) -> List[Dict]:
    recommendations = []
    
    for task in available_tasks[:3]:
        complexity = task.get('complexity', 'medium')
        
        if stress_level <= 4:
            if complexity == 'high':
                reason = "Low stress level - perfect time for complex challenges"
                score = 90
            else:
                reason = "Good energy for steady progress"
                score = 75
        elif stress_level <= 7:
            if complexity == 'low':
                reason = "Moderate stress - lighter tasks recommended"
                score = 80
            else:
                reason = "Manageable with focus"
                score = 60
        else:
            if complexity == 'low':
                reason = "High stress - focus on simple, achievable tasks"
                score = 95
            else:
                reason = "Consider postponing until stress reduces"
                score = 40
        
        recommendations.append({
            "task_title": task['title'],
            "reason": reason,
            "suitability_score": score
        })
    
    recommendations.sort(key=lambda x: x['suitability_score'], reverse=True)
    return recommendations


def generate_mood_insight(team_data: List[Dict]) -> str:
    client = get_openai_client()
    
    if client and team_data:
        try:
            summary = "\n".join([f"- {m['name']}: {m['emotion']}, stress {m['stress_level']}/10" 
                                for m in team_data])
            
            response = client.chat.completions.create(
                model="gpt-5",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a team wellness advisor. Analyze the overall team mood and "
                        + "provide actionable insights and recommendations.",
                    },
                    {"role": "user", "content": f"Team Status:\n{summary}\n\nProvide brief insights."},
                ],
                max_completion_tokens=200,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Insight generation error: {e}")
            return fallback_team_insight(team_data)
    else:
        return fallback_team_insight(team_data)


def fallback_team_insight(team_data: List[Dict]) -> str:
    if not team_data:
        return "No team data available for analysis."
    
    avg_stress = sum(m.get('stress_level', 5) for m in team_data) / len(team_data)
    stressed_count = sum(1 for m in team_data if m.get('stress_level', 5) > 7)
    
    if avg_stress > 7:
        return f"⚠️ Team stress is elevated (avg: {avg_stress:.1f}/10). {stressed_count} members need support. Consider workload redistribution."
    elif avg_stress > 5:
        return f"📊 Team stress is moderate (avg: {avg_stress:.1f}/10). Monitor closely and maintain work-life balance."
    else:
        return f"✅ Team is performing well (avg stress: {avg_stress:.1f}/10). Great environment for tackling challenges!"
