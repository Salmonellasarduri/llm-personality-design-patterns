from collections import defaultdict


class DriftState:
    def __init__(self):
        self.daily_counts = defaultdict(lambda: defaultdict(int))

    def add(self, day: str, emotion: str, count: int = 1):
        self.daily_counts[day][emotion] += count

    def drift_days(self) -> int:
        return len(self.daily_counts)

    def total_magnitude(self) -> int:
        return sum(sum(day.values()) for day in self.daily_counts.values())

    def dominant_emotions(self, top_n: int = 2):
        merged = defaultdict(int)
        for day_counts in self.daily_counts.values():
            for k, v in day_counts.items():
                merged[k] += v
        return sorted(merged.items(), key=lambda x: x[1], reverse=True)[:top_n]


def try_crystallize(state: DriftState, min_days: int = 3, threshold: int = 12):
    if state.drift_days() < min_days:
        return None
    if state.total_magnitude() < threshold:
        return None
    return {
        "dominant_emotions": state.dominant_emotions(),
        "days": state.drift_days(),
        "magnitude": state.total_magnitude(),
    }


if __name__ == "__main__":
    state = DriftState()

    state.add("2026-03-01", "joy", 3)
    state.add("2026-03-01", "anticipation", 2)
    state.add("2026-03-02", "joy", 2)
    state.add("2026-03-02", "trust", 2)
    state.add("2026-03-03", "joy", 2)
    state.add("2026-03-03", "anticipation", 2)

    result = try_crystallize(state)

    print("=== Drift summary ===")
    print("days:", state.drift_days())
    print("magnitude:", state.total_magnitude())
    print("dominant:", state.dominant_emotions())

    if result is None:
        print("No crystallization triggered.")
    else:
        print("Crystallization triggered:", result)
