def route_intent(user_input: str):
    text = user_input.lower()

    if "tahun" in text:
        return "plot_per_year"
    
    elif "bulan" in text:
        return "plot_per_month"
    
    elif "store" in text:
        return "plot_per_store"
    
    else:
        return "unknown"