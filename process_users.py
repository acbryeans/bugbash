import pandas as pd
import csv

# Read the CSV data
df = pd.read_csv('/Users/abryeans/Documents/Portfolio Pres/User_Data.csv')

# Function to check if user has all zero values (except bugs filed)
def has_all_zero_values(row):
    # Check if Views, Saves, Archives, Underwritten, Offers are all 0
    # But allow them to stay if they filed bugs
    activity_cols = ['Views', 'Saves', 'Archives', 'Underwritten', 'Offers']
    all_zero = all(row[col] == 0 for col in activity_cols)
    has_bugs = row['Bugs Filed'] > 0
    return all_zero and not has_bugs

# Filter out rows:
# 1. Exclude "Q" team
# 2. Exclude "Total" row  
# 3. Exclude users with all zero values (except if they filed bugs)
filtered_df = df[
    (df['Team'] != 'Q') &
    (df['Team'] != 'Total') &
    (~df.apply(has_all_zero_values, axis=1))
].copy()

# Calculate activity level (Views + Underwritten + Bugs Filed)
filtered_df['Activity_Level'] = filtered_df['Views'] + filtered_df['Underwritten'] + filtered_df['Bugs Filed']

# Sort by team (The Newgotiators first), then by activity level descending
def sort_key(row):
    if row['Team'] == 'The Newgotiators':
        return (0, -row['Activity_Level'])  # 0 for first position, negative for descending
    else:
        return (1, row['Team'], -row['Activity_Level'])  # 1 for later, then team name, then activity

sorted_df = filtered_df.sort_values(by=['Team', 'Activity_Level'], 
                                   key=lambda x: x.map(lambda row: sort_key(row) if isinstance(row, pd.Series) else row),
                                   ascending=[True, False])

# Actually, let's do this more simply
newgotiators = filtered_df[filtered_df['Team'] == 'The Newgotiators'].sort_values('Activity_Level', ascending=False)
others = filtered_df[filtered_df['Team'] != 'The Newgotiators'].sort_values(['Team', 'Activity_Level'], ascending=[True, False])
sorted_df = pd.concat([newgotiators, others])

print("Filtered and sorted data:")
print(f"Total rows: {len(sorted_df)}")
print("\nThe Newgotiators team:")
print(sorted_df[sorted_df['Team'] == 'The Newgotiators'][['User', 'Views', 'Underwritten', 'Bugs Filed', 'Activity_Level']])

print("\nOther teams (first few):")
others_preview = sorted_df[sorted_df['Team'] != 'The Newgotiators'].head(10)
print(others_preview[['Team', 'User', 'Views', 'Underwritten', 'Bugs Filed', 'Activity_Level']])

# Generate HTML table rows
html_rows = []

for _, row in sorted_df.iterrows():
    team = row['Team']
    user = row['User']
    views = int(row['Views'])
    saves = int(row['Saves'])
    archives = int(row['Archives']) 
    underwritten = int(row['Underwritten'])
    offers = int(row['Offers'])
    imported_feeds = int(row['Imported Feeds'])
    sessions = int(row['Total Unique Sessions'])
    bugs_filed = int(row['Bugs Filed'])
    
    # Special styling for The Newgotiators
    if team == 'The Newgotiators':
        style = ' style="background: rgba(168, 85, 247, 0.15); font-weight: 600;"'
    else:
        style = ''
    
    html_row = f'''                            <tr{style}>
                                <td>{team}</td>
                                <td>{user}</td>
                                <td>{views}</td>
                                <td>{saves}</td>
                                <td>{archives}</td>
                                <td>{underwritten}</td>
                                <td>{offers}</td>
                                <td>{imported_feeds}</td>
                                <td>{sessions}</td>
                                <td>{bugs_filed}</td>
                            </tr>'''
    
    html_rows.append(html_row)

# Join all rows
tbody_content = '\n'.join(html_rows)

print(f"\nGenerated {len(html_rows)} HTML table rows")
print("\nFirst few rows:")
for i, row in enumerate(html_rows[:3]):
    print(f"Row {i+1}:")
    print(row)
    print()

# Save to file
with open('/Users/abryeans/Documents/Portfolio Pres/user_table_tbody.html', 'w') as f:
    f.write(tbody_content)

print("HTML tbody content saved to user_table_tbody.html")