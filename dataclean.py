import pandas as pd

# Read the animation movies dataset
file_path = "Animation_Movies.csv"
df = pd.read_csv(file_path)

# Convert the release_date column to datetime format and extract the release year
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['release_year'] = df['release_date'].dt.year

# Handle missing values - fill numerical columns with median or zero
df['vote_average'].fillna(df['vote_average'].median(), inplace=True)
df['vote_count'].fillna(0, inplace=True)
df['revenue'].fillna(0, inplace=True)
df['runtime'].fillna(df['runtime'].median(), inplace=True)

df.dropna(subset=['release_year'], inplace=True)  # Remove rows with missing release year

# Process categorical data, split genres column
df['genres'] = df['genres'].fillna('Unknown')  # Fill missing values
df['genres'] = df['genres'].apply(lambda x: x.split(',') if isinstance(x, str) else [])

# Process production companies, split the production_companies column
df['production_companies'] = df['production_companies'].fillna('Unknown')
df['production_companies'] = df['production_companies'].apply(lambda x: x.split(',') if isinstance(x, str) else [])

# Save the cleaned dataset
df.to_csv("cleaned_animation_movies.csv", index=False)

print("Data cleaning completed. Saved as cleaned_animation_movies.csv")