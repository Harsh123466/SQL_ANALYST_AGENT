
import matplotlib.pyplot as plt


def generate_chart(result, chart_type="bar"):
    if result.empty:
        print("No data available for visualization.")
        return

    numeric_columns = result.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = result.select_dtypes(
        exclude="number"
    ).columns.tolist()

    if not numeric_columns:
        print("No numeric columns available.")
        return

    y_column = numeric_columns[-1]

    if categorical_columns:
        x_column = categorical_columns[0]
        x = result[x_column].astype(str)
    else:
        x_column = "Records"
        x = result.index.astype(str)

    plt.figure(figsize=(10, 5))

    if chart_type == "bar":
        plt.bar(x, result[y_column])

    elif chart_type == "line":
        plt.plot(x, result[y_column], marker="o")

    elif chart_type == "pie":
        plt.pie(
            result[y_column],
            labels=x,
            autopct="%1.1f%%"
        )

    else:
        raise ValueError("Unsupported chart type.")

    if chart_type != "pie":
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.xticks(rotation=45, ha="right")

    plt.title(f"{chart_type.title()} Chart: {y_column}")
    plt.tight_layout()
    plt.show()
