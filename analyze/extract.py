import anthropic

def extract_decisions(slack_message):
    client = anthropic.Anthropic()
    
    prompt = f"""
    Analyze this Slack message and extract:
    1. Any decisions made
    2. The reasoning behind them
    3. Who was involved
    4. What alternatives were considered
    
    Message: {slack_message}
    
    Return as JSON.
    """
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return parse_json(response.content[0].text)
