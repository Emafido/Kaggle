import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

df = pd.read_csv("StudentsPerformance.csv")

simulation_data = []
for idx, row in df.iterrows():
    base_math = row['math score']
    base_reading = row['reading score']
    base_writing = row['writing score']

    for attempt_num in range(1, 6):
        simulation_data.append({
            'user_id': idx,
            'gender': row['gender'],
            'attempt': attempt_num,
            'math_score': min(100, base_math + np.random.normal(attempt_num * 2, 1)),
            'reading_score': min(100, base_reading + np.random.normal(attempt_num * 2, 1)),
            'writing_score': min(100, base_writing + np.random.normal(attempt_num * 2, 1))
        })

df_simulated = pd.DataFrame(simulation_data)


def calculate_slope(score_values, attempt_values):
    if len(score_values) < 2:
        return 0
    slope_value, _ = np.polyfit(attempt_values, score_values, 1)
    return slope_value


learning_data = []
for user_id, user_df in df_simulated.groupby('user_id'):
    user_gender = user_df['gender'].iloc[0]
    attempt_nums = user_df['attempt'].values

    for subject_name in ['math_score', 'reading_score', 'writing_score']:
        subject_scores = user_df[subject_name].values
        user_slope = calculate_slope(subject_scores, attempt_nums)
        learning_data.append({
            'user_id': user_id,
            'gender': user_gender,
            'subject': subject_name,
            'learning_rate': user_slope
        })

slopes_data = pd.DataFrame(learning_data)
speed_summary = slopes_data.groupby(['gender', 'subject'])['learning_rate'].mean().unstack()

results_dict = {}
for subject_name in ['math_score', 'reading_score', 'writing_score']:
    male_slopes = slopes_data[(slopes_data['gender'] == 'male') & (slopes_data['subject'] == subject_name)][
        'learning_rate']
    female_slopes = slopes_data[(slopes_data['gender'] == 'female') & (slopes_data['subject'] == subject_name)][
        'learning_rate']

    t_statistic, p_val = ttest_ind(male_slopes, female_slopes)
    is_significant = p_val < 0.05
    faster_gender = "male" if male_slopes.mean() > female_slopes.mean() else "female"

    results_dict[subject_name] = {
        'p_value': p_val,
        'significant': is_significant,
        'faster_gender': faster_gender,
        'male_slope': male_slopes.mean(),
        'female_slope': female_slopes.mean(),
        'male_std': male_slopes.std(),
        'female_std': female_slopes.std()
    }

plt.figure(figsize=(15, 10))
subject_titles = ['Mathematics', 'Reading Comprehension', 'Writing Skills']
color_palette = {'female': '#E64C80', 'male': '#4C78A8'}

for idx, subject in enumerate(['math_score', 'reading_score', 'writing_score']):
    plt.subplot(2, 3, idx + 1)

    trend_data = df_simulated.groupby(['gender', 'attempt'])[subject].mean().reset_index()

    for gender_type in ['male', 'female']:
        gender_trend = trend_data[trend_data['gender'] == gender_type]
        plt.plot(gender_trend['attempt'], gender_trend[subject],
                 marker='o', linewidth=3, label=gender_type.title(),
                 color=color_palette[gender_type], markersize=6)

    plt.xlabel("Learning Attempt", fontsize=11, weight='bold')
    plt.ylabel("Average Score", fontsize=11, weight='bold')
    plt.title(f"{subject_titles[idx]}\nLearning Progression", fontsize=12, weight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks([1, 2, 3, 4, 5])

for idx, subject in enumerate(['math_score', 'reading_score', 'writing_score']):
    plt.subplot(2, 3, idx + 4)

    gender_types = ['male', 'female']
    speed_values = [speed_summary.loc[g, subject] for g in gender_types]
    bars = plt.bar(gender_types, speed_values,
                   color=[color_palette[g] for g in gender_types],
                   alpha=0.7, width=0.6)

    for bar, value in zip(bars, speed_values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                 f'{value:.3f}', ha='center', va='bottom',
                 fontweight='bold', fontsize=10)

    result_info = results_dict[subject]
    significance_star = "***" if result_info['significant'] else ""
    plt.title(f"Learning Speed{significance_star}\n(Slope Coefficient)", fontsize=12, weight='bold')
    plt.ylabel("Points per Attempt", fontsize=10)

plt.tight_layout()
plt.savefig("learning_trends_dashboard.png", dpi=300, bbox_inches='tight')
plt.show()

overall_speeds = speed_summary.mean(axis=1)
winning_gender = overall_speeds.idxmax()
winning_speed = overall_speeds[winning_gender]
losing_speed = overall_speeds['female' if winning_gender == 'male' else 'male']

plt.figure(figsize=(14, 10))
plt.suptitle("Hackathon Analysis: Detailed Learning Speed Conclusions", fontsize=16, weight='bold', y=0.95)

plt.subplot(2, 2, 1)
subjects_display = ['Math', 'Reading', 'Writing']
male_speeds = [speed_summary.loc['male', 'math_score'],
               speed_summary.loc['male', 'reading_score'],
               speed_summary.loc['male', 'writing_score']]
female_speeds = [speed_summary.loc['female', 'math_score'],
                 speed_summary.loc['female', 'reading_score'],
                 speed_summary.loc['female', 'writing_score']]

x_pos = np.arange(len(subjects_display))
width = 0.35

plt.bar(x_pos - width / 2, male_speeds, width, label='Male', color='#4C78A8', alpha=0.7)
plt.bar(x_pos + width / 2, female_speeds, width, label='Female', color='#E64C80', alpha=0.7)

for i, (m, f) in enumerate(zip(male_speeds, female_speeds)):
    plt.text(i - width / 2, m + 0.002, f'{m:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
    plt.text(i + width / 2, f + 0.002, f'{f:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=9)

plt.xlabel('Subjects', fontsize=12, weight='bold')
plt.ylabel('Learning Speed (Slope)', fontsize=12, weight='bold')
plt.title('Learning Speed by Subject and Gender', fontsize=14, weight='bold')
plt.xticks(x_pos, subjects_display)
plt.legend()
plt.grid(True, alpha=0.3, axis='y')

plt.subplot(2, 2, 2)
performance_gap = [male_speeds[i] - female_speeds[i] for i in range(3)]
colors = ['red' if gap > 0 else 'blue' for gap in performance_gap]
bars = plt.bar(subjects_display, performance_gap, color=colors, alpha=0.7)

for i, (bar, gap) in enumerate(zip(bars, performance_gap)):
    plt.text(i, bar.get_height() + (0.001 if gap > 0 else -0.01),
             f'{gap:.3f}', ha='center', va='bottom' if gap > 0 else 'top',
             fontweight='bold', fontsize=10)

plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
plt.xlabel('Subjects', fontsize=12, weight='bold')
plt.ylabel('Speed Difference (Male - Female)', fontsize=12, weight='bold')
plt.title('Learning Speed Gap Analysis', fontsize=14, weight='bold')
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 3)
subject_winners = []
for subject in ['math_score', 'reading_score', 'writing_score']:
    winner = results_dict[subject]['faster_gender']
    subject_winners.append(winner)

winner_counts = pd.Series(subject_winners).value_counts()
plt.pie(winner_counts.values, labels=winner_counts.index.str.title(),
        autopct='%1.0f%%', colors=['#4C78A8', '#E64C80'], startangle=90)
plt.title('Subject Wins by Gender', fontsize=14, weight='bold')

plt.subplot(2, 2, 4)
plt.axis('off')

conclusion_text = [
    "HACKATHON FINDINGS SUMMARY",
    "",
    f"OVERALL WINNER: {winning_gender.upper()} STUDENTS",
    f"Average Learning Speed: {winning_speed:.3f} vs {losing_speed:.3f}",
    "",
    "SUBJECT-SPECIFIC RESULTS:",
    f"• MATHEMATICS: {results_dict['math_score']['faster_gender'].title()} learn faster",
    f"  (Male: {results_dict['math_score']['male_slope']:.3f}, Female: {results_dict['math_score']['female_slope']:.3f})",
    f"• READING: {results_dict['reading_score']['faster_gender'].title()} learn faster",
    f"  (Male: {results_dict['reading_score']['male_slope']:.3f}, Female: {results_dict['reading_score']['female_slope']:.3f})",
    f"• WRITING: {results_dict['writing_score']['faster_gender'].title()} learn faster",
    f"  (Male: {results_dict['writing_score']['male_slope']:.3f}, Female: {results_dict['writing_score']['female_slope']:.3f})",
    "",
    "STATISTICAL SIGNIFICANCE:",
    f"• Math: {'SIGNIFICANT' if results_dict['math_score']['significant'] else 'Not Significant'}",
    f"• Reading: {'SIGNIFICANT' if results_dict['reading_score']['significant'] else 'Not Significant'}",
    f"• Writing: {'SIGNIFICANT' if results_dict['writing_score']['significant'] else 'Not Significant'}",
    "",
    "METHODOLOGY:",
    "• Simulated 5 learning attempts per student",
    "• Learning speed = slope of linear regression",
    "• Statistical testing with t-test (p < 0.05)",
    "• Dataset: 1,000 students with baseline scores"
]

for i, line in enumerate(conclusion_text):
    weight = 'bold' if any(
        word in line.upper() for word in ['WINNER', 'SIGNIFICANT', 'METHODOLOGY', 'FINDINGS']) else 'normal'
    color = 'darkgreen' if 'WINNER' in line else 'black'
    plt.text(0.1, 0.95 - i * 0.05, line, fontsize=10, weight=weight, color=color,
             transform=plt.gca().transAxes, verticalalignment='top')

plt.tight_layout()
plt.savefig("detailed_conclusions_dashboard.png", dpi=300, bbox_inches='tight')
plt.show()

speed_summary.to_csv("learning_speed_analysis.csv")


print(f"Overall Winner: {winning_gender.title()} students")
print(f"Dashboard 1 saved: learning_trends_dashboard.png")
print(f"Dashboard 2 saved: detailed_conclusions_dashboard.png")
print(f"Data exported: learning_speed_analysis.csv")