from rag import search_health_knowledge_base

EVAL_DATASET = [
    {
        "question": "I feel severe chest pain and dizziness after running, what should I do?",
        "expected_source": "knowledge_base\\01_emergency_red_flags.txt",
    },
    {
        "question": "How quickly should I increase my weekly running mileage safely?",
        "expected_source": "knowledge_base\\02_exercise_safety_progression.txt",
    },
    {
        "question": "What are the signs that I am overtraining and need a rest day?",
        "expected_source": "knowledge_base\\03_overtraining_recovery.txt",
    },
    {
        "question": "How much water and electrolytes should I consume during workouts?",
        "expected_source": "knowledge_base\\04_sleep_hydration_nutrition.txt",
    },
    {
        "question": "I am feeling demotivated and burned out from my workout routine.",
        "expected_source": "knowledge_base\\05_mental_health_burnout.txt",
    },
    {
        "question": "Should I do static stretching before running or dynamic warmups?",
        "expected_source": "knowledge_base\\06_warmup_cooldown_stretching.txt",
    },
    {
        "question": "How do I know if sharp knee pain is muscle soreness or a joint injury?",
        "expected_source": "knowledge_base\\07_joint_pain_vs_muscle_soreness.txt",
    },
    {
        "question": "What is Zone 2 cardio training and how do I pace my long runs?",
        "expected_source": "knowledge_base\\08_cardio_and_strength_pacing.txt",
    },
    {
        "question": "What are the early warning signs of heat stroke while working out?",
        "expected_source": "knowledge_base\\09_environmental_safety_heat_cold.txt",
    },
    {
        "question": "What should I eat right before and immediately after an intense workout?",
        "expected_source": "knowledge_base\\10_nutrition_and_fueling_timing.txt",
    },
]

def run_evaluation():
    hits = 0
    total = len(EVAL_DATASET)

    for idx, item in enumerate(EVAL_DATASET, 1):
        question = item["question"]
        expected = item["expected_source"]
        retrieved_context = search_health_knowledge_base.invoke({"query": question})

        hit = expected in str(retrieved_context)
        if hit:
            hits += 1
            status = "HIT"
        else:
            status = "MISS"

        print(f"Question: {question}")
        print(f"Expected: {expected}")
        print(f"Result: {status}\n")

    hit_rate = (hits / total) * 100
    print(f"Hit Rate: {hits}/{total} ({hit_rate}%)")

if __name__ == "__main__":
    run_evaluation()