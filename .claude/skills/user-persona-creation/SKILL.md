---
name: user-persona-creation
description: Create detailed user personas based on research and data. Develop realistic representations of target users to guide product decisions and ensure user-centered design.
---

# User Persona Creation

## Overview

User personas synthesize research into realistic user profiles that guide design, development, and marketing decisions.

## When to Use

- Starting product design
- Feature prioritization
- Marketing messaging
- User research synthesis
- Team alignment on users
- Journey mapping
- Success metrics definition

## Instructions

### 1. **Research & Data Collection**

```python
# Gather data for persona development

class PersonaResearch:
    def conduct_interviews(self, target_sample_size=12):
        """Interview target users"""
        interview_guide = {
            'demographics': [
                'Age, gender, location',
                'Job title, industry, company size',
                'Experience level, education',
                'Salary range, purchasing power'
            ],
            'goals': [
                'What are you trying to achieve?',
                'What's most important to you?',
                'What does success look like?'
            ],
            'pain_points': [
                'What frustrates you about current solutions?',
                'What takes too long or is complicated?',
                'What prevents you from achieving goals?'
            ],
            'behaviors': [
                'How do you currently solve this problem?',
                'What tools do you use?',
                'How do you learn about new solutions?'
            ],
            'preferences': [
                'How do you prefer to communicate?',
                'What communication channels do you use?',
                'When are you most responsive?'
            ]
        }

        return {
            'sample_size': target_sample_size,
            'interview_guide': interview_guide,
            'output': 'Interview transcripts, notes, recordings'
        }

    def analyze_survey_data(self, survey_data):
        """Synthesize survey responses"""
        return {
            'demographics': self.segment_demographics(survey_data),
            'pain_points': self.extract_pain_points(survey_data),
            'goals': self.identify_goals(survey_data),
            'needs': self.map_needs(survey_data),
            'frequency_distribution': self.calculate_frequencies(survey_data)
        }

    def analyze_user_data(self):
        """Use product analytics data"""
        return {
            'feature_usage': 'Which features are most used',
            'user_segments': 'Behavioral groupings',
            'conversion_paths': 'How users achieve goals',
            'churn_patterns': 'Why users leave',
            'usage_frequency': 'Active vs inactive users'
        }

    def synthesize_data(self, interview_data, survey_data, usage_data):
        """Combine all data sources"""
        return {
            'primary_personas': self.identify_primary_personas(interview_data),
            'secondary_personas': self.identify_secondary_personas(survey_data),
            'persona_groups': self.cluster_similar_users(usage_data),
            'confidence_level': 'Based on data sources and sample size'
        }
```

### 2. **Persona Template**

```yaml
User Persona: Premium SaaS Buyer

---

## Demographics

Name: Sarah Chen
Age: 34
Location: San Francisco, CA
Job Title: VP Product Management
Company: Series B SaaS startup (50 employees)
Experience: 8 years in product management
Education: MBA from Stanford, BS in Computer Science
Income: $180K salary + 0.5% equity

---

## Professional Context

Industry: B2B SaaS (Project Management)
Company Size: 50-200 employees
Budget Authority: Can approve purchases up to $50K
Buying Process: 60% solo decisions, 40% committee
Evaluation Time: 4-6 weeks average

---

## Goals & Motivations

Primary Goals:
  1. Improve team productivity by 25%
  2. Reduce project delivery time by 30%
  3. Increase visibility into project status
  4. Improve team collaboration across remote locations

Success Definition:
  - Team using tool daily
  - 20% reduction in status meetings
  - Faster decision-making
  - Higher team satisfaction

---

## Pain Points

Current Challenges:
