import gradio as gr

# -----------------------------
# Food Categories (Pakistan Based)
# -----------------------------
fruits = [
    "Apple", "Banana", "Orange", "Mango",
    "Papaya", "Pineapple", "Pomegranate"
]

vegetables = [
    "Spinach", "Carrot", "Tomato",
    "Cabbage", "Cauliflower", "Okra", "Onion"
]

fast_foods = [
    "Burger", "Pizza", "French Fries",
    "Fried Chicken", "Samosa"
]

dry_fruits = [
    "Almonds", "Walnuts", "Cashews",
    "Raisins", "Dates"
]

all_foods = fruits + vegetables + fast_foods + dry_fruits

# -----------------------------
# Disease Rules
# -----------------------------
disease_food_rules = {
    "Diabetes": {
        "avoid": ["Burger", "Pizza", "French Fries", "Fried Chicken", "Samosa", "Mango", "Dates"],
        "recommend": ["Spinach", "Carrot", "Tomato", "Apple", "Almonds", "Walnuts"]
    },
    "High BP": {
        "avoid": ["Burger", "Pizza", "Fried Chicken", "Samosa"],
        "recommend": ["Spinach", "Cabbage", "Tomato", "Carrot", "Apple"]
    },
    "High Cholesterol": {
        "avoid": ["Fried Chicken", "Burger", "Pizza", "French Fries", "Cashews"],
        "recommend": ["Spinach", "Carrot", "Tomato", "Apple", "Walnuts"]
    },
    "Kidney Problem": {
        "avoid": ["Spinach", "Banana", "Dates", "Mango"],
        "recommend": ["Apple", "Carrot", "Cauliflower"]
    },
    "Heart Disease": {
        "avoid": ["Fried Chicken", "Burger", "Pizza", "French Fries", "Samosa"],
        "recommend": ["Spinach", "Carrot", "Tomato", "Apple", "Walnuts"]
    }
}

# -----------------------------
# Main Logic Function
# -----------------------------
def diet_advisor(diseases, foods):

    if not diseases:
        diseases_list = []
    else:
        diseases_list = [d.strip().title() for d in diseases.split(",")]

    foods_list = foods if foods else []

    healthy = set()
    unhealthy = set()
    recommended = set()

    for disease in diseases_list:
        if disease in disease_food_rules:
            avoid_list = disease_food_rules[disease]["avoid"]
            recommend_list = disease_food_rules[disease]["recommend"]

            for food in foods_list:
                if food in avoid_list:
                    unhealthy.add(food)
                elif food in recommend_list:
                    healthy.add(food)

            for item in recommend_list:
                if item not in foods_list:
                    recommended.add(item)

    # -----------------------------
    # HTML OUTPUT (Dark Boxes + White Text)
    # -----------------------------

    html_output = ""

    # Disease Box
    html_output += f"""
    <div style='background-color:#8B0000;padding:15px;margin-bottom:10px;border-radius:10px;color:white;'>
        <h3>🩺 Your Diseases</h3>
        {", ".join(diseases_list) if diseases_list else "None"}
    </div>
    """

    # Healthy Box
    html_output += f"""
    <div style='background-color:#006400;padding:15px;margin-bottom:10px;border-radius:10px;color:white;'>
        <h3>✅ Healthy Foods You Have</h3>
        {", ".join(healthy) if healthy else "None"}
    </div>
    """

    # Unhealthy Box
    html_output += f"""
    <div style='background-color:#B22222;padding:15px;margin-bottom:10px;border-radius:10px;color:white;'>
        <h3>❌ Foods You Should Avoid</h3>
        {", ".join(unhealthy) if unhealthy else "None"}
    </div>
    """

    # Recommendation Box
    html_output += f"""
    <div style='background-color:#00008B;padding:15px;margin-bottom:10px;border-radius:10px;color:white;'>
        <h3>💡 Recommended Foods To Add</h3>
        {", ".join(recommended) if recommended else "None"}
    </div>
    """

    # Final Advice
    html_output += """
    <div style='background-color:#4B0082;padding:15px;border-radius:10px;color:white;'>
        <h3>🍽 Overall Diet Advice</h3>
        Maintain balanced diet.<br>
        Avoid fried and fast foods.<br>
        Increase vegetables and fiber intake.<br>
        Drink plenty of water.<br>
        Follow doctor advice for your condition.
    </div>
    """

    return html_output


# -----------------------------
# Clear Function
# -----------------------------
def clear_all():
    return "", [], ""


# -----------------------------
# Gradio UI
# -----------------------------
with gr.Blocks() as demo:

    gr.Markdown(
        "<h2 style='text-align:center;color:#e67e22;'>🥗 Advanced Diet Advisor — Pakistani Foods</h2>"
    )

    with gr.Row():

        with gr.Column():
            diseases_input = gr.Textbox(
                label="Enter Diseases (e.g., Diabetes, High BP)",
                placeholder="Type diseases separated by comma"
            )

            food_input = gr.CheckboxGroup(
                choices=all_foods,
                label="Select Foods You Have"
            )

            submit_btn = gr.Button("Get Diet Advice 🍽")
            clear_btn = gr.Button("Clear 🧹")

        with gr.Column():
            output_box = gr.HTML()

    submit_btn.click(diet_advisor, inputs=[diseases_input, food_input], outputs=output_box)
    clear_btn.click(clear_all, outputs=[diseases_input, food_input, output_box])

# Launch
demo.launch()
