from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from weekend_fun.event_finder import Event


class EventRanker:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini", max_retries=3)

    def rank_events(self, events: list[Event], interests: list[str]) -> list[Event]:
        events_and_scores = []
        for event in events:
            score = self._calculate_interest_score(event, interests)
            events_and_scores.append((event, score))

        ranked_events = sorted(events_and_scores, key=lambda x: x[1], reverse=True)
        return [ranked_event[0] for ranked_event in ranked_events]

    def _calculate_interest_score(self, event: Event, interests: list[str]) -> float:
        """Calculate an interest score for an event based on user interests."""

        _ranker_instructions = f"""
        Event Title: {event.name}
        Event Description: {event.description}
        User Interests: {", ".join(interests)}
        
        On a scale of 0 to 1, how well does this event match the user's interests?
        Provide only the numerical score and nothing else.
        """

        response = self.llm.invoke(
            [SystemMessage(content=_ranker_instructions.format(event=event))]
        )

        try:
            assert isinstance(response.content, str)
            score = float(response.content.strip())
            return min(max(score, 0), 1)  # Ensure score is between 0 and 1
        except ValueError:
            return 0.0
