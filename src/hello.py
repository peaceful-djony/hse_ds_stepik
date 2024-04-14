import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


def get_zp_data():
    url = "https://raw.githubusercontent.com/peaceful-djony/hse_ds_stepik/main/data/tab3-zpl_2023.xlsx"
    df_zp_after_2017 = st.cache_data(pd.read_excel)(url, sheet_name=0, skiprows=4)
    df_zp_before_2017 = st.cache_data(pd.read_excel)(url, sheet_name=1, skiprows=2)

    # Номер строки в excel с учетом пропуска первых неинформативных строк (параметр skiprows) и строки с заголовком
    df_zp = df_zp_before_2017.iloc[[28, 29]].reset_index(drop=True)
    df_zp_after_2017_subset = df_zp_after_2017.iloc[[43, 44]].reset_index(drop=True)
    df_zp = df_zp.merge(df_zp_after_2017_subset, left_index=True, right_index=True)

    # Удаление дубликатов заголовков и их переименование
    df_zp['Unnamed: 0_x'] = df_zp['Unnamed: 0_y'].str.capitalize()
    df_zp = df_zp.drop(columns=['Unnamed: 0_y']).rename(columns={'Unnamed: 0_x': 'Вид деятельности'})

    # Корректировка неправильных годов в заголовках
    df_zp = df_zp.rename(columns={'20171)': '2017', '20222)': '2022', '20232), 3)': '2023'})

    return df_zp


def setup_plot_style(plot, label):
    plot.tick_params(axis='x', rotation=70)
    plot.set_title(label)
    plot.set_ylim(0, 175000)


def display_plots(data):
    st.write(f"Зарплата по секторам:")

    fig, axes = plt.subplots(figsize=(15, 10), ncols=2)

    it_salary_bar = sns.barplot(data=data.iloc[0, 1:], ax=axes[0])
    setup_plot_style(it_salary_bar, 'IT salary')

    fin_salary_bar = sns.barplot(data=data.iloc[1, 1:], ax=axes[1])
    setup_plot_style(fin_salary_bar, 'Finance salary')

    st.pyplot(fig)


df = get_zp_data()

st.title("Зарплата в России в 2000-2023 годах")
st.subheader("в бесплатной версии представлены два сектора: IT и финансы")
st.dataframe(df)

year = st.sidebar.selectbox("Выберите год:", df.columns[1:])

if year:
    st.write(f"Зарплата в {year} году:")
    df_year = df[['Вид деятельности', year]]
    st.dataframe(df_year)

display_plots(df)

