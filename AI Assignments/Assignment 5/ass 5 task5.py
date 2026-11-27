COURSES = [
	{
		"name": "Python Fundamentals",
		"category": "programming",
		"level": "beginner",
		"topics": {"python", "coding", "automation"},
	},
	{
		"name": "Data Analysis with Python",
		"category": "data",
		"level": "intermediate",
		"topics": {"python", "data", "visualization"},
	},
	{
		"name": "Web Development Basics",
		"category": "programming",
		"level": "beginner",
		"topics": {"html", "css", "coding"},
	},
]


def recommend_courses(preferences, courses=COURSES):
	"""Return course recommendations and explain why each one matched."""
	recommendations = []

	for course in courses:
		score = 0
		reasons = []

		if preferences.get("category") == course["category"]:
			score += 2
			reasons.append(f"matches your {course['category']} category")

		if preferences.get("level") == course["level"]:
			score += 2
			reasons.append(f"matches your {course['level']} level")

		matching_topics = preferences.get("topics", set()) & course["topics"]
		if matching_topics:
			score += len(matching_topics)
			topics = ", ".join(sorted(matching_topics))
			reasons.append(f"covers your interests: {topics}")

		if reasons:
			recommendations.append(
				{"course": course["name"], "score": score, "reasons": reasons}
			)

	return sorted(recommendations, key=lambda recommendation: recommendation["score"], reverse=True)


user_preferences = {
	"category": "programming",
	"level": "beginner",
	"topics": {"python", "coding"},
}

for recommendation in recommend_courses(user_preferences):
	print(f"\nRecommendation: {recommendation['course']}")
	print("Reasons:")
	for reason in recommendation["reasons"]:
		print(f"- {reason}")
