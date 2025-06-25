from flask import Flask, request, render_template
from logic import trendyol, hepsiburada, lcwaikiki, mavi, koton, zara
from logic.koton import check_product

app = Flask(__name__)

stores = {
    "Trendyol": trendyol,
    "Hepsiburada": hepsiburada,
    "LC Waikiki": lcwaikiki,
    "Mavi": mavi,
    "Koton": koton,
    "Zara": zara,
}

@app.route("/", methods=["GET", "POST"])
def satista():
    result = None
    selected_store = None
    product = None

    if request.method == "POST":
        product = request.form.get("product", "").strip()
        selected_store = request.form.get("store")

        if selected_store == "all":
            result = {}
            for store_name, module in stores.items():
                res = module.check_product(product)
                if res is None:
                    res = {"available": False, "url": None}
                result[store_name] = res
        else:
            module = stores.get(selected_store)
            if module:
                res = module.check_product(product)
                if res is None:
                    res = {"available": False, "url": None}
                result = {selected_store: res}

    return render_template("satista.html", result=result, stores=stores.keys(), selected_store=selected_store, product=product)

if __name__ == "__main__":
    app.run(debug=True)
