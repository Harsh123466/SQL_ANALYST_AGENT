def display_result(response):
    print("\n========== BUSINESS ANSWER ==========")
    print(response["answer"])

    print("\n========== GENERATED SQL ==========")
    print(response["sql"])

    print("\n========== QUERY RESULT ==========")
    print(response["result"].to_string(index=False))