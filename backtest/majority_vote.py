def majority_vote(signals_list):
    combined_signals = []
    for i in range(len(signals_list[0])):
        votes = [s[i] for s in signals_list]
        vote_result = sum(votes)
        if vote_result >= 2:
            combined_signals.append(1)  # Buy
        elif vote_result <= -2:
            combined_signals.append(-1)  # Sell
        else:
            combined_signals.append(0)  # No Action
    return combined_signals
