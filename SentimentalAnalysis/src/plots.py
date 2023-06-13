import matplotlib.pyplot as plt
import seaborn as sb

def histogram_plot(result):
    # Histogram
    result["sentiment"].hist()
    plt.xlabel("Sentiments")
    plt.ylabel("Frequency")
    plt.title("Histogram of Sentiment Frequencies")
    return plt

def pie_chart_plot(result):
    # Pie Chart
    value_counts = result['sentiment'].value_counts()
    value_counts = value_counts.sample(frac=1)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', pctdistance=0.75, startangle=315)
    plt.title("Pie Chart of Sentiment Frequencies")
    return plt

def characters_sentiment_plot(result):
    # Sentiment change of characters
    character_counts = result['speaker'].value_counts()

    # Get the top 10 most speaking speakers
    selected_characters = character_counts.nlargest(10).index

    # Filter the results DataFrame
    filtered_results = result[result['speaker'].isin(selected_characters)]

    # Plot the filtered DataFrame
    plt.figure(figsize=(12, 8))
    sb.countplot(data=filtered_results, x='speaker', hue='sentiment')
    plt.xlabel('Speaker')
    plt.ylabel('Count')
    plt.title('Sentiment Distribution by Character')
    plt.xticks(rotation=45)
    plt.legend(title='Sentiment')
    return plt


def sentiment_avg_prob_plot(result):
    # Calculate the average probability for each sentiment
    average_probability = result.groupby('sentiment')['probability'].mean().reset_index()

    # Plot the average probability
    plt.figure(figsize=(8, 6))
    sb.barplot(data=average_probability, x='sentiment', y='probability', palette='Blues')
    plt.xlabel('Sentiment')
    plt.ylabel('Average Probability')
    plt.title('Average Probability for Each Sentiment')
    return plt
