import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import io
import streamlit as st

web_apps = st.sidebar.selectbox("Select Web Apps", ("Exploratory Data Analysis", "Distributions"))

if web_apps == "Exploratory Data Analysis":
    uploaded_file = st.sidebar.file_uploader("Choose a file")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        show_df = st.checkbox("Show Data Frame", key="disabled")

        if show_df:
            st.write(df)

        st.header("Statistics")
        st.write("Number of Rows:", df.shape[0])
        st.write("Number of Columns:", df.shape[1])

        column_types = df.dtypes.value_counts()
        num_categorical = column_types.get('object', 0)
        num_numerical = column_types.get('int64', 0) + column_types.get('float64', 0)
        num_bool = column_types.get('bool', 0)

        st.write("Number of Categorical Variables:", num_categorical)
        st.write("Number of Numerical Variables:", num_numerical)
        st.write("Number of Boolean Variables:", num_bool)

        column_type = st.sidebar.selectbox('Select Data Type',
                                           ("Numerical", "Categorical", "Bool", "Date"))

        if column_type == "Numerical":
            numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            plot_type = st.sidebar.selectbox('Select Plot Type', ('Histogram', 'Scatter Plot'))

            if plot_type == 'Histogram':
                # Calculate 5-number summary for the selected column
                numerical_column = st.sidebar.selectbox('Select a Numerical Column', numerical_columns)
                # drop NAs
                column_data = df[numerical_column].dropna()
                summary = np.percentile(column_data, [0, 25, 50, 75, 100])
                min_val, q1, median, q3, max_val = summary

                st.header("5 number summary")
                st.write("Min:", min_val)
                st.write("Q1:", q1)
                st.write("Median:", median)
                st.write("Q3:", q3)
                st.write("Max:", max_val)

                bins = st.slider('Number of bins', min_value=5, max_value=150, value=30)
                choose_color = st.color_picker('Pick a Color', "#69b3a2")

                fig, ax = plt.subplots()
                ax.hist(df[numerical_column], bins=bins, edgecolor="black", color=choose_color)
                ax.set_title('Histogram')
                ax.set_xlabel(numerical_column)
                ax.set_ylabel('Count')
                st.pyplot(fig)

            elif plot_type == 'Scatter Plot':
                x_column = st.sidebar.selectbox('Select X-axis Column', numerical_columns)
                y_column = st.sidebar.selectbox('Select Y-axis Column', numerical_columns)

                choose_color = st.color_picker('Pick a Color', "#69b3a2")

                fig, ax = plt.subplots()
                ax.scatter(df[x_column], df[y_column], color=choose_color)
                ax.set_title('Scatter Plot')
                ax.set_xlabel(x_column)
                ax.set_ylabel(y_column)
                st.pyplot(fig)

        elif column_type == "Categorical":
            categorical_column = st.sidebar.selectbox('Select a Column', df.select_dtypes(include=['object']).columns)

            # Calculate proportions of each category level
            category_counts = df[categorical_column].value_counts()
            category_proportions = category_counts / category_counts.sum()

            # Display proportions in a table
            st.header("Category Proportions:")
            st.table(pd.DataFrame({"Category": category_proportions.index, "Proportion": category_proportions}))

            # barplot
            st.header("Barplot")
            choose_color = st.color_picker('Pick a Color', "#69b3a2")
            title = st.text_input('Set Title', 'Bar Plot')
            xtitle = st.text_input('Set x-axis Title', categorical_column)
            ytitle = st.text_input('Set y-axis Title', 'Proportion')

            fig, ax = plt.subplots()
            ax.bar(category_proportions.index, category_proportions.values, color=choose_color)
            ax.set_title(title)
            ax.set_xlabel(xtitle)
            ax.set_ylabel(ytitle)
            st.pyplot(fig)
    