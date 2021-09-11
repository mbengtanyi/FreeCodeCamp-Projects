import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")
print(df.head())
df_copy = df.copy()
print(df.columns)

#The result of comparing two variables like 4>5 returns a boolean(False in this case). So when we get the True or False values, we convert to int that'll be either 0(for False) or 1(for True)

# Add 'overweight' column
df['overweight'] = (df['weight'] / ((df['height']/100)**2) > 25).astype(int)
 

print(df['overweight'].head())

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['gluc'] = (df['gluc']>1).astype(int)

df['cholesterol'] =  (df['cholesterol'] >1).astype(int)



# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    #print(df_cat)


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = pd.DataFrame(
        df_cat.groupby(['cardio', 'variable',
                        'value'])['value'].count()).rename(columns={
                            'value': 'total'
                        }).reset_index()

    df_cat_plot = sns.catplot(
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        data=df_cat,
        kind='bar', legend=True)

    # Draw the catplot with 'sns.catplot()'
    fig= df_cat_plot.fig
    #plt.show()


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[
                  (df['ap_lo'] <= df['ap_hi']) &
                  (df['height'] >= df['height'].quantile(0.025)) &
                  (df['height'] <= df['height'].quantile(0.975)) &
                  (df['weight'] >= df['weight'].quantile(0.025)) &
                  (df['weight'] <= df['weight'].quantile(0.975))
                  ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 12))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr,
        linewidths=1,
        annot=True,
        fmt='.1f',
        mask=mask,
        square=True,
        center=0.08,
        cbar_kws={
            'shrink': .45,
            'format': '%.2f'
        })
    
    plt.show()



    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
