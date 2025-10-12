#!/usr/bin/env python3
"""
Raga Therapy Integration for RagaSense App
==========================================

This module integrates raga therapy and healing features into the main RagaSense
application, providing users with therapeutic recommendations based on their
health conditions, emotional states, and wellness goals.

Features:
- Health condition-based raga recommendations
- Emotional state therapy
- Chakra healing and alignment
- Quantum physics-based therapy insights
- Personalized wellness plans

Author: RagaSense Team
Date: 2025-01-27
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import numpy as np
from datetime import datetime, timedelta

from raga_therapy_analyzer import RagaTherapyAnalyzer, RagaTherapyProperties

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class UserWellnessProfile:
    """User's wellness profile for personalized therapy"""
    user_id: str
    
    # Health conditions
    current_conditions: List[str]
    chronic_conditions: List[str]
    
    # Emotional state
    current_emotions: List[str]
    emotional_goals: List[str]
    
    # Preferences
    preferred_times: List[str]  # Morning, Afternoon, Evening, Night
    session_duration: int  # minutes
    chakra_focus: Optional[str] = None
    
    # History
    therapy_history: List[Dict[str, Any]] = None
    preferences: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.therapy_history is None:
            self.therapy_history = []
        if self.preferences is None:
            self.preferences = {}

@dataclass
class TherapySession:
    """Individual therapy session"""
    session_id: str
    user_id: str
    raga_name: str
    start_time: datetime
    duration: int  # minutes
    purpose: str  # Health condition, emotional state, etc.
    chakra_focus: Optional[str] = None
    user_feedback: Optional[Dict[str, Any]] = None
    effectiveness_score: Optional[float] = None

class RagaTherapyIntegration:
    """Main integration class for raga therapy features"""
    
    def __init__(self):
        self.therapy_analyzer = RagaTherapyAnalyzer()
        self.user_profiles = {}
        self.therapy_sessions = {}
        self.wellness_plans = {}
        
        # Load existing data
        self._load_user_data()
    
    def _load_user_data(self):
        """Load existing user profiles and therapy sessions"""
        # In a real app, this would load from a database
        # For now, we'll use in-memory storage
        pass
    
    def create_user_profile(self, user_id: str, 
                          current_conditions: List[str] = None,
                          chronic_conditions: List[str] = None,
                          current_emotions: List[str] = None,
                          emotional_goals: List[str] = None,
                          preferred_times: List[str] = None,
                          session_duration: int = 20,
                          chakra_focus: Optional[str] = None) -> UserWellnessProfile:
        """Create a new user wellness profile"""
        
        profile = UserWellnessProfile(
            user_id=user_id,
            current_conditions=current_conditions or [],
            chronic_conditions=chronic_conditions or [],
            current_emotions=current_emotions or [],
            emotional_goals=emotional_goals or [],
            preferred_times=preferred_times or ["Evening"],
            session_duration=session_duration,
            chakra_focus=chakra_focus
        )
        
        self.user_profiles[user_id] = profile
        logger.info(f"Created wellness profile for user {user_id}")
        
        return profile
    
    def get_personalized_recommendations(self, user_id: str) -> Dict[str, Any]:
        """Get personalized raga therapy recommendations for a user"""
        if user_id not in self.user_profiles:
            return {'error': 'User profile not found'}
        
        profile = self.user_profiles[user_id]
        recommendations = {
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'health_recommendations': [],
            'emotional_recommendations': [],
            'chakra_recommendations': [],
            'wellness_plan': None
        }
        
        # Health condition recommendations
        for condition in profile.current_conditions + profile.chronic_conditions:
            health_recs = self.therapy_analyzer.get_healing_recommendations(condition)
            recommendations['health_recommendations'].extend(health_recs)
        
        # Emotional state recommendations
        for emotion in profile.current_emotions:
            emotion_recs = self.therapy_analyzer.get_emotional_state_ragas(emotion)
            recommendations['emotional_recommendations'].extend(emotion_recs)
        
        # Chakra recommendations
        if profile.chakra_focus:
            chakra_recs = self.therapy_analyzer.get_chakra_healing_ragas(profile.chakra_focus)
            recommendations['chakra_recommendations'] = chakra_recs
        
        # Create wellness plan
        recommendations['wellness_plan'] = self._create_wellness_plan(profile)
        
        return recommendations
    
    def _create_wellness_plan(self, profile: UserWellnessProfile) -> Dict[str, Any]:
        """Create a personalized wellness plan"""
        plan = {
            'plan_id': f"wellness_plan_{profile.user_id}_{datetime.now().strftime('%Y%m%d')}",
            'user_id': profile.user_id,
            'created_date': datetime.now().isoformat(),
            'duration_weeks': 4,
            'daily_sessions': [],
            'weekly_goals': [],
            'progress_tracking': {}
        }
        
        # Create daily session recommendations
        for day in range(7):  # One week
            daily_session = {
                'day': day + 1,
                'recommended_ragas': [],
                'session_duration': profile.session_duration,
                'focus_areas': []
            }
            
            # Add health-focused ragas
            if profile.current_conditions:
                for condition in profile.current_conditions[:2]:  # Limit to 2 conditions per day
                    recs = self.therapy_analyzer.get_healing_recommendations(condition)
                    if recs:
                        daily_session['recommended_ragas'].append({
                            'raga_name': recs[0]['raga_name'],
                            'purpose': f'Health: {condition}',
                            'duration': min(15, profile.session_duration // 2)
                        })
            
            # Add emotional state ragas
            if profile.current_emotions:
                for emotion in profile.current_emotions[:1]:  # One emotion per day
                    recs = self.therapy_analyzer.get_emotional_state_ragas(emotion)
                    if recs:
                        daily_session['recommended_ragas'].append({
                            'raga_name': recs[0]['raga_name'],
                            'purpose': f'Emotional: {emotion}',
                            'duration': min(15, profile.session_duration // 2)
                        })
            
            # Add chakra healing
            if profile.chakra_focus:
                chakra_recs = self.therapy_analyzer.get_chakra_healing_ragas(profile.chakra_focus)
                if chakra_recs and day % 3 == 0:  # Every 3rd day
                    daily_session['recommended_ragas'].append({
                        'raga_name': chakra_recs[0]['raga_name'],
                        'purpose': f'Chakra: {profile.chakra_focus}',
                        'duration': profile.session_duration
                    })
            
            plan['daily_sessions'].append(daily_session)
        
        # Set weekly goals
        plan['weekly_goals'] = [
            f"Complete {len(profile.current_conditions)} health-focused sessions",
            f"Address {len(profile.current_emotions)} emotional states",
            "Track mood and energy levels daily",
            "Maintain consistent therapy schedule"
        ]
        
        return plan
    
    def start_therapy_session(self, user_id: str, raga_name: str, 
                            purpose: str, chakra_focus: Optional[str] = None) -> TherapySession:
        """Start a new therapy session"""
        session_id = f"session_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Get user profile for session duration
        duration = 20  # default
        if user_id in self.user_profiles:
            duration = self.user_profiles[user_id].session_duration
        
        session = TherapySession(
            session_id=session_id,
            user_id=user_id,
            raga_name=raga_name,
            start_time=datetime.now(),
            duration=duration,
            purpose=purpose,
            chakra_focus=chakra_focus
        )
        
        self.therapy_sessions[session_id] = session
        
        # Add to user's therapy history
        if user_id in self.user_profiles:
            self.user_profiles[user_id].therapy_history.append({
                'session_id': session_id,
                'raga_name': raga_name,
                'start_time': session.start_time.isoformat(),
                'purpose': purpose
            })
        
        logger.info(f"Started therapy session {session_id} for user {user_id}")
        return session
    
    def end_therapy_session(self, session_id: str, 
                          user_feedback: Dict[str, Any] = None) -> Dict[str, Any]:
        """End a therapy session and collect feedback"""
        if session_id not in self.therapy_sessions:
            return {'error': 'Session not found'}
        
        session = self.therapy_sessions[session_id]
        session.user_feedback = user_feedback
        
        # Calculate effectiveness score based on feedback
        if user_feedback:
            effectiveness_score = self._calculate_effectiveness_score(user_feedback)
            session.effectiveness_score = effectiveness_score
        
        # Update user profile based on session results
        self._update_user_profile_from_session(session)
        
        logger.info(f"Ended therapy session {session_id}")
        
        return {
            'session_id': session_id,
            'duration_completed': (datetime.now() - session.start_time).total_seconds() / 60,
            'effectiveness_score': session.effectiveness_score,
            'recommendations': self._get_session_recommendations(session)
        }
    
    def _calculate_effectiveness_score(self, feedback: Dict[str, Any]) -> float:
        """Calculate effectiveness score from user feedback"""
        score = 0.0
        total_metrics = 0
        
        # Mood improvement (0-10 scale)
        if 'mood_improvement' in feedback:
            score += feedback['mood_improvement'] / 10.0
            total_metrics += 1
        
        # Energy level (0-10 scale)
        if 'energy_level' in feedback:
            score += feedback['energy_level'] / 10.0
            total_metrics += 1
        
        # Pain relief (0-10 scale)
        if 'pain_relief' in feedback:
            score += feedback['pain_relief'] / 10.0
            total_metrics += 1
        
        # Overall satisfaction (0-10 scale)
        if 'overall_satisfaction' in feedback:
            score += feedback['overall_satisfaction'] / 10.0
            total_metrics += 1
        
        return score / total_metrics if total_metrics > 0 else 0.0
    
    def _update_user_profile_from_session(self, session: TherapySession):
        """Update user profile based on session results"""
        if session.user_id not in self.user_profiles:
            return
        
        profile = self.user_profiles[session.user_id]
        
        # Update preferences based on effective sessions
        if session.effectiveness_score and session.effectiveness_score > 0.7:
            if 'effective_ragas' not in profile.preferences:
                profile.preferences['effective_ragas'] = []
            
            if session.raga_name not in profile.preferences['effective_ragas']:
                profile.preferences['effective_ragas'].append(session.raga_name)
    
    def _get_session_recommendations(self, session: TherapySession) -> List[str]:
        """Get recommendations based on session results"""
        recommendations = []
        
        if session.effectiveness_score:
            if session.effectiveness_score > 0.8:
                recommendations.append("Excellent session! Continue with this raga regularly.")
            elif session.effectiveness_score > 0.6:
                recommendations.append("Good session. Consider increasing duration or frequency.")
            else:
                recommendations.append("Try a different raga or adjust session timing.")
        
        # Get therapy properties for additional recommendations
        therapy_props = self.therapy_analyzer.analyze_raga_therapy(session.raga_name)
        if therapy_props:
            if therapy_props.recommended_time:
                recommendations.append(f"Best time for this raga: {therapy_props.recommended_time}")
            
            if therapy_props.chakra_affected:
                recommendations.append(f"Focus on {therapy_props.chakra_affected} chakra during session")
        
        return recommendations
    
    def get_wellness_insights(self, user_id: str) -> Dict[str, Any]:
        """Get wellness insights and progress tracking"""
        if user_id not in self.user_profiles:
            return {'error': 'User profile not found'}
        
        profile = self.user_profiles[user_id]
        insights = {
            'user_id': user_id,
            'total_sessions': len(profile.therapy_history),
            'most_effective_ragas': [],
            'progress_trends': {},
            'recommendations': []
        }
        
        # Analyze therapy history
        if profile.therapy_history:
            # Count raga usage
            raga_usage = {}
            for session in profile.therapy_history:
                raga_name = session['raga_name']
                raga_usage[raga_name] = raga_usage.get(raga_name, 0) + 1
            
            # Get most used ragas
            insights['most_used_ragas'] = sorted(raga_usage.items(), 
                                               key=lambda x: x[1], reverse=True)[:5]
            
            # Get most effective ragas from preferences
            if 'effective_ragas' in profile.preferences:
                insights['most_effective_ragas'] = profile.preferences['effective_ragas']
        
        # Generate recommendations
        if len(profile.therapy_history) < 5:
            insights['recommendations'].append("Start with daily 15-minute sessions")
        elif len(profile.therapy_history) < 20:
            insights['recommendations'].append("Consider increasing session duration to 30 minutes")
        else:
            insights['recommendations'].append("Excellent progress! Maintain consistent practice")
        
        return insights
    
    def export_user_data(self, user_id: str, output_file: str) -> None:
        """Export user's therapy data"""
        if user_id not in self.user_profiles:
            return
        
        profile = self.user_profiles[user_id]
        user_sessions = [s for s in self.therapy_sessions.values() if s.user_id == user_id]
        
        export_data = {
            'user_profile': {
                'user_id': profile.user_id,
                'current_conditions': profile.current_conditions,
                'chronic_conditions': profile.chronic_conditions,
                'current_emotions': profile.current_emotions,
                'emotional_goals': profile.emotional_goals,
                'preferred_times': profile.preferred_times,
                'session_duration': profile.session_duration,
                'chakra_focus': profile.chakra_focus,
                'preferences': profile.preferences
            },
            'therapy_sessions': [
                {
                    'session_id': s.session_id,
                    'raga_name': s.raga_name,
                    'start_time': s.start_time.isoformat(),
                    'duration': s.duration,
                    'purpose': s.purpose,
                    'chakra_focus': s.chakra_focus,
                    'effectiveness_score': s.effectiveness_score
                }
                for s in user_sessions
            ],
            'export_date': datetime.now().isoformat()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported user data to {output_file}")

def main():
    """Main execution function"""
    therapy_integration = RagaTherapyIntegration()
    
    print("🎵 Raga Therapy Integration for RagaSense App")
    print("Personalized healing through Indian classical music")
    
    # Example usage
    user_id = "demo_user_001"
    
    # Create user profile
    profile = therapy_integration.create_user_profile(
        user_id=user_id,
        current_conditions=["Anxiety", "Insomnia"],
        chronic_conditions=["Hypertension"],
        current_emotions=["Stress", "Worry"],
        emotional_goals=["Peace", "Calmness"],
        preferred_times=["Evening", "Night"],
        session_duration=20,
        chakra_focus="Heart"
    )
    
    # Get personalized recommendations
    recommendations = therapy_integration.get_personalized_recommendations(user_id)
    
    print(f"\n📊 Personalized Recommendations for {user_id}:")
    print(f"Health Recommendations: {len(recommendations['health_recommendations'])}")
    print(f"Emotional Recommendations: {len(recommendations['emotional_recommendations'])}")
    print(f"Chakra Recommendations: {len(recommendations['chakra_recommendations'])}")
    
    # Start a therapy session
    session = therapy_integration.start_therapy_session(
        user_id=user_id,
        raga_name="Bhairavi",
        purpose="Anxiety relief",
        chakra_focus="Heart"
    )
    
    print(f"\n🎵 Started therapy session: {session.session_id}")
    print(f"Raga: {session.raga_name}")
    print(f"Purpose: {session.purpose}")
    
    # Simulate ending session with feedback
    feedback = {
        'mood_improvement': 8,
        'energy_level': 7,
        'pain_relief': 6,
        'overall_satisfaction': 8
    }
    
    session_result = therapy_integration.end_therapy_session(session.session_id, feedback)
    print(f"\n✅ Session completed with effectiveness score: {session_result['effectiveness_score']:.2f}")
    
    # Get wellness insights
    insights = therapy_integration.get_wellness_insights(user_id)
    print(f"\n📈 Wellness Insights:")
    print(f"Total sessions: {insights['total_sessions']}")
    print(f"Most effective ragas: {insights['most_effective_ragas']}")

if __name__ == "__main__":
    main()
