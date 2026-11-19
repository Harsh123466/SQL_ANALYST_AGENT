
FEW_SHOT_EXAMPLES = [
    {
        "question": "Show total sales by product category.",
        "sql": """
            SELECT
                ProdCategory,
                SUM(OrderTotal) AS TotalSales
            FROM retail_sales
            GROUP BY ProdCategory
            ORDER BY TotalSales DESC
        """
    },
    {
        "question": "Show total revenue by customer type.",
        "sql": """
            SELECT
                CustomerType,
                SUM(OrderTotal) AS TotalRevenue
            FROM retail_sales
            GROUP BY CustomerType
            ORDER BY TotalRevenue DESC
        """
    },
    {
        "question": "Show the top 5 products by revenue.",
        "sql": """
            SELECT
                ProdName,
                SUM(OrderTotal) AS TotalRevenue
            FROM retail_sales
            GROUP BY ProdName
            ORDER BY TotalRevenue DESC
            LIMIT 5
        """
    },
    {
        "question": "Count the number of orders for each order type.",
        "sql": """
            SELECT
                OrderType,
                COUNT(*) AS TotalOrders
            FROM retail_sales
            GROUP BY OrderType
        """
    }
]
