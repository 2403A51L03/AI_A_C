from flask import Flask, request, render_template_string, url_for

app = Flask(__name__)

# -----------------------------
# Algorithm Implementations
# -----------------------------


def merge_sort(arr, key=None):
    """
    Stable merge sort implementation.

    Parameters
    ----------
    arr : list
        List of comparable items, or list of objects/dicts when used with `key`.
    key : callable, optional
        Function that takes an element of `arr` and returns a value to sort by.
        If None, elements are compared directly.

    Time Complexity
    ---------------
    Best case:    O(n log n)
    Average case: O(n log n)
    Worst case:   O(n log n)

    Space Complexity
    ----------------
    O(n) extra space for the temporary merged lists.
    """
    if key is None:
        key = lambda x: x

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key=key)
    right = merge_sort(arr[mid:], key=key)

    merged = []
    i = j = 0

    # Merge step keeps sort stable and costs O(n)
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append remaining elements
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def binary_search(arr, target):
    """
    Iterative binary search on a sorted array.

    Parameters
    ----------
    arr : list
        Sorted list of comparable items (ascending order).
    target : any
        Value to search for.

    Returns
    -------
    int
        Index of `target` in `arr` if found, otherwise -1.

    Time Complexity
    ---------------
    Best case:    O(1)
        Target is found at the middle position on the first comparison.
    Average case: O(log n)
        Each step halves the search space until the target is found or the
        range is empty.
    Worst case:   O(log n)
        Target is not present or at an extreme end; still only log₂(n)
        comparisons are required.

    Space Complexity
    ----------------
    O(1) extra space, since the search uses only a few index variables.
    """
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


# -----------------------------
# Sample Data
# -----------------------------

INVENTORY_ITEMS = [
    {"id": 101, "name": "Laptop", "price": 75000, "quantity": 10},
    {"id": 102, "name": "Mouse", "price": 800, "quantity": 150},
    {"id": 103, "name": "Keyboard", "price": 1500, "quantity": 80},
    {"id": 104, "name": "Monitor", "price": 12000, "quantity": 25},
    {"id": 105, "name": "Headphones", "price": 2500, "quantity": 60},
]

PATIENTS = [
    {"id": 201, "name": "Alice", "severity": 4, "bill_amount": 45000},
    {"id": 202, "name": "Bob", "severity": 2, "bill_amount": 15000},
    {"id": 203, "name": "Charlie", "severity": 5, "bill_amount": 80000},
    {"id": 204, "name": "Diana", "severity": 3, "bill_amount": 25000},
    {"id": 205, "name": "Ethan", "severity": 1, "bill_amount": 5000},
]

STUDENTS = [
    {"roll_no": 1, "name": "Rahul", "marks": 89},
    {"roll_no": 2, "name": "Sneha", "marks": 95},
    {"roll_no": 3, "name": "Ankit", "marks": 72},
    {"roll_no": 4, "name": "Meera", "marks": 81},
    {"roll_no": 5, "name": "Vikram", "marks": 60},
]

ORDERS = [
    {"order_id": 301, "customer": "Harsh", "delivery_time": 35, "price": 450},
    {"order_id": 302, "customer": "Isha", "delivery_time": 20, "price": 250},
    {"order_id": 303, "customer": "Nikhil", "delivery_time": 50, "price": 780},
    {"order_id": 304, "customer": "Pooja", "delivery_time": 15, "price": 300},
    {"order_id": 305, "customer": "Anuj", "delivery_time": 40, "price": 600},
]

# -----------------------------
# Shared HTML Template (embedded)
# -----------------------------

BASE_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{{ page_title }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Modern UI with Bootstrap CDN -->
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-gpw6rW5wEcidZ6DpudI8g1cY6q7r3gmlhlK8Z9Kc6h1zK6yS4bK1xX8bD8fr7mz9"
      crossorigin="anonymous"
    >

    <style>
        :root {
            --bg-gradient: radial-gradient(circle at top left, #4f46e5, #0ea5e9);
            --glass-bg: rgba(15, 23, 42, 0.8);
        }

        body {
            min-height: 100vh;
            margin: 0;
            background: radial-gradient(circle at top left, #1e293b, #020617);
            color: #e5e7eb;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        .gradient-overlay {
            position: fixed;
            inset: 0;
            pointer-events: none;
            background-image: radial-gradient(circle at 0% 0%, rgba(96, 165, 250, 0.35), transparent 60%),
                              radial-gradient(circle at 100% 0%, rgba(244, 114, 182, 0.22), transparent 55%),
                              radial-gradient(circle at 0% 100%, rgba(52, 211, 153, 0.18), transparent 55%);
            opacity: 0.9;
            z-index: -2;
        }

        .blur-layer {
            position: fixed;
            inset: 0;
            backdrop-filter: blur(36px);
            -webkit-backdrop-filter: blur(36px);
            z-index: -1;
        }

        .navbar {
            background: linear-gradient(90deg, rgba(15, 23, 42, 0.96), rgba(30, 64, 175, 0.96));
            border-bottom: 1px solid rgba(148, 163, 184, 0.35);
        }

        .navbar-brand {
            font-weight: 700;
            letter-spacing: 0.03em;
        }

        .nav-link {
            font-weight: 500;
        }

        .nav-link.active {
            position: relative;
        }

        .nav-link.active::after {
            content: "";
            position: absolute;
            left: 0.75rem;
            right: 0.75rem;
            bottom: -0.35rem;
            height: 2px;
            border-radius: 999px;
            background: linear-gradient(to right, #38bdf8, #a855f7);
        }

        .page-shell {
            max-width: 1120px;
            margin: 1.75rem auto 3rem auto;
        }

        .card {
            background: radial-gradient(circle at top left, rgba(15, 23, 42, 0.96), rgba(15, 23, 42, 0.92));
            border-radius: 1rem;
            border: 1px solid rgba(148, 163, 184, 0.45);
            box-shadow:
                0 22px 60px rgba(15, 23, 42, 0.75),
                0 0 0 1px rgba(15, 23, 42, 0.7),
                0 22px 70px rgba(56, 189, 248, 0.12);
            color: #e5e7eb;
        }

        .card-ghost {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(24, 35, 55, 0.95));
        }

        .card:hover {
            transform: translateY(-3px);
            transition: transform 160ms ease-out, box-shadow 160ms ease-out;
            box-shadow:
                0 26px 80px rgba(15, 23, 42, 0.9),
                0 0 0 1px rgba(56, 189, 248, 0.35);
        }

        .page-title {
            font-size: 2.1rem;
            font-weight: 700;
            letter-spacing: 0.02em;
        }

        .page-subtitle {
            color: #9ca3af;
        }

        table {
            color: #e5e7eb;
        }

        table thead th {
            border-bottom-color: rgba(148, 163, 184, 0.5) !important;
            color: #cbd5f5;
            font-weight: 600;
        }

        table tbody tr {
            border-color: rgba(55, 65, 81, 0.9);
        }

        .badge {
            border-radius: 999px;
        }

        .algo-badge {
            font-size: 0.75rem;
        }

        .metric-pill {
            border-radius: 999px;
            background: linear-gradient(90deg, rgba(56, 189, 248, 0.2), rgba(244, 114, 182, 0.16));
            border: 1px solid rgba(59, 130, 246, 0.4);
            color: #e5e7eb;
            font-size: 0.75rem;
            padding-inline: 0.8rem;
            padding-block: 0.25rem;
        }
    </style>
</head>
<body>
<div class="gradient-overlay"></div>
<div class="blur-layer"></div>
<nav class="navbar navbar-expand-lg navbar-dark mb-4">
    <div class="container-fluid">
        <a class="navbar-brand" href="{{ url_for('index') }}">Algo Demo Suite</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false"
                aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item"><a class="nav-link {% if active_page=='inventory' %}active{% endif %}" href="{{ url_for('inventory') }}">Inventory</a></li>
                <li class="nav-item"><a class="nav-link {% if active_page=='hospital' %}active{% endif %}" href="{{ url_for('hospital') }}">Hospital</a></li>
                <li class="nav-item"><a class="nav-link {% if active_page=='university' %}active{% endif %}" href="{{ url_for('university') }}">University</a></li>
                <li class="nav-item"><a class="nav-link {% if active_page=='food' %}active{% endif %}" href="{{ url_for('food_delivery') }}">Food Delivery</a></li>
            </ul>
        </div>
    </div>
</nav>

<div class="container page-shell">
    {% block content %}{% endblock %}
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-hhrWciC0OX71srvs3Bps+/oF2t0Dty0fC8dZErNdJ9v8z3W4Z4gw+1HSuJ6dXv5L"
        crossorigin="anonymous"></script>
</body>
</html>
"""


def render_with_base(content_fragment: str, **context):
    """
    Helper to inject a page-specific content fragment into the shared
    BASE_TEMPLATE. Avoids Jinja inheritance issues inside a single file.
    """
    full_template = BASE_TEMPLATE.replace(
        "{% block content %}{% endblock %}", content_fragment
    )
    return render_template_string(full_template, **context)

# -----------------------------
# Home Page with Algorithm Recommendation Table
# -----------------------------


@app.route("/")
def index():
    algorithm_recommendations = [
        {
            "operation": "Inventory: search by product ID",
            "algorithm": "Binary Search",
            "justification": "IDs are numeric; after sorting by ID we can find an item in O(log n) instead of O(n).",
        },
        {
            "operation": "Inventory: sort by price/quantity",
            "algorithm": "Merge Sort",
            "justification": "Stable O(n log n) sorting even for large lists.",
        },
        {
            "operation": "Hospital: search patient by ID",
            "algorithm": "Binary Search",
            "justification": "Critical patient lookup benefits from predictable logarithmic time.",
        },
        {
            "operation": "Hospital: sort by severity/bill amount",
            "algorithm": "Merge Sort",
            "justification": "Allows frequent resorting as patients' states change.",
        },
        {
            "operation": "University: rank list by marks",
            "algorithm": "Merge Sort",
            "justification": "Stable sorting ensures students with equal marks keep consistent relative order.",
        },
        {
            "operation": "Food delivery: search by order ID",
            "algorithm": "Binary Search",
            "justification": "Quick lookup of a specific order among many.",
        },
        {
            "operation": "Food delivery: sort by delivery time/price",
            "algorithm": "Merge Sort",
            "justification": "Helps analyze performance and pricing trends in O(n log n).",
        },
    ]

    content = (
        "<div class='mb-4'>"
        "  <div class='card card-ghost p-4 p-md-5 mb-3'>"
        "    <div class='d-flex flex-column flex-md-row align-items-md-center justify-content-between gap-3'>"
        "      <div>"
        "        <div class='metric-pill mb-2 d-inline-flex align-items-center gap-2'>"
        "          <span class='badge bg-info-subtle text-info border-0'>Algorithms</span>"
        "          <span>Merge Sort · Binary Search · Real-world modules</span>"
        "        </div>"
        "        <h1 class='page-title mb-1'>Algorithm Demo Suite</h1>"
        "        <p class='page-subtitle mb-0'>"
        "          Explore how classic algorithms power <strong>Inventory</strong>, <strong>Hospital</strong>, "
        "          <strong>University</strong> and <strong>Food Delivery</strong> systems."
        "        </p>"
        "      </div>"
        "      <div class='text-md-end'>"
        "        <div class='small text-uppercase text-slate-300 mb-2'>Overall Complexity</div>"
        "        <div class='d-flex flex-wrap gap-2 justify-content-md-end'>"
        "          <span class='metric-pill'>Merge Sort – O(n log n)</span>"
        "          <span class='metric-pill'>Binary Search – O(log n)</span>"
        "        </div>"
        "      </div>"
        "    </div>"
        "  </div>"
        "</div>"
        "<div class='row g-4'>"
        "  <div class='col-lg-7'>"
        "    <div class='card p-4'>"
        "      <h2 class='h5 mb-3'>Algorithm Recommendation Table</h2>"
        "      <p class='page-subtitle mb-4'>"
        "        How the suite chooses between <strong>merge sort</strong> and <strong>binary search</strong> for each domain."
        "      </p>"
        "      <div class='table-responsive'>"
        "        <table class='table table-sm align-middle'>"
        "          <thead class='table-light'>"
        "            <tr>"
        "              <th>Operation</th>"
        "              <th>Algorithm</th>"
        "              <th>Justification</th>"
        "            </tr>"
        "          </thead>"
        "          <tbody>"
        "            {% for row in algorithm_recommendations %}"
        "            <tr>"
        "              <td>{{ row.operation }}</td>"
        "              <td><span class='badge bg-primary algo-badge'>{{ row.algorithm }}</span></td>"
        "              <td>{{ row.justification }}</td>"
        "            </tr>"
        "            {% endfor %}"
        "          </tbody>"
        "        </table>"
        "      </div>"
        "    </div>"
        "  </div>"
        "  <div class='col-lg-5'>"
        "    <div class='card p-4 mb-3'>"
        "      <h2 class='h5 mb-3'>Complexity Overview</h2>"
        "      <ul class='list-unstyled small mb-0'>"
        "        <li class='mb-2'><strong>Merge Sort</strong> – time: O(n log n), space: O(n).</li>"
        "        <li class='mb-2'><strong>Binary Search</strong> – time: best O(1), average/worst O(log n), space: O(1).</li>"
        "        <li class='mb-0'>All modules reuse the same implementations to keep logic consistent and testable.</li>"
        "      </ul>"
        "    </div>"
        "    <div class='card p-4'>"
        "      <h2 class='h5 mb-3'>Modules</h2>"
        "      <ul class='list-group list-group-flush small'>"
        "        <li class='list-group-item d-flex justify-content-between align-items-center'>"
        "          Inventory Management<span><a href='{{ url_for('inventory') }}' class='btn btn-sm btn-outline-primary'>Open</a></span>"
        "        </li>"
        "        <li class='list-group-item d-flex justify-content-between align-items-center'>"
        "          Hospital Management<span><a href='{{ url_for('hospital') }}' class='btn btn-sm btn-outline-primary'>Open</a></span>"
        "        </li>"
        "        <li class='list-group-item d-flex justify-content-between align-items-center'>"
        "          University Results<span><a href='{{ url_for('university') }}' class='btn btn-sm btn-outline-primary'>Open</a></span>"
        "        </li>"
        "        <li class='list-group-item d-flex justify-content-between align-items-center'>"
        "          Food Delivery<span><a href='{{ url_for('food_delivery') }}' class='btn btn-sm btn-outline-primary'>Open</a></span>"
        "        </li>"
        "      </ul>"
        "    </div>"
        "  </div>"
        "</div>"
    )

    return render_with_base(
        content,
        page_title="Algorithm Demo Suite",
        active_page="home",
        algorithm_recommendations=algorithm_recommendations,
    )


# -----------------------------
# Helper functions for modules
# -----------------------------


def binary_search_on_field(data, field, target):
    """
    Use merge_sort + binary_search to find a single record by a given field.

    data : list[dict]
        List of records.
    field : str
        Dictionary key to search on (must be comparable).
    target : any
        Value to search for.

    Returns a list with either 0 or 1 record for UI simplicity.
    """
    # First, sort by the field using merge_sort to guarantee ordering.
    sorted_data = merge_sort(data, key=lambda x: x[field])
    keys = [row[field] for row in sorted_data]
    index = binary_search(keys, target)
    if index == -1:
        return []
    return [sorted_data[index]]


def linear_search_on_name(data, field, query):
    """
    Simple case-insensitive linear search for textual fields.

    This complements binary search, which is better suited for
    numeric or uniquely ordered keys.
    """
    q = str(query).strip().lower()
    if not q:
        return []
    return [row for row in data if q in str(row[field]).lower()]


# -----------------------------
# Inventory Management Module
# -----------------------------


@app.route("/inventory")
def inventory():
    search_field = request.args.get("search_field", "id")
    search_query = request.args.get("search_query", "").strip()
    sort_by = request.args.get("sort_by", "")

    records = INVENTORY_ITEMS.copy()
    results = []

    # Apply sorting using merge sort when requested
    if sort_by == "price":
        records = merge_sort(records, key=lambda x: x["price"])
    elif sort_by == "quantity":
        records = merge_sort(records, key=lambda x: x["quantity"])

    # Apply search: for ID use binary search, for name use linear search
    if search_query:
        if search_field == "id":
            try:
                target_id = int(search_query)
                results = binary_search_on_field(INVENTORY_ITEMS, "id", target_id)
            except ValueError:
                results = []
        elif search_field == "name":
            results = linear_search_on_name(INVENTORY_ITEMS, "name", search_query)

    content = (
        "<div class='card p-4'>"
        "  <div class='d-flex justify-content-between align-items-center mb-3'>"
        "    <div>"
        "      <h2 class='h4 mb-1'>Inventory Management</h2>"
        "      <p class='text-muted mb-0 small'>"
        "        Search products by <strong>ID</strong> (binary search) or <strong>name</strong> (linear search), "
        "        and sort by <strong>price</strong> or <strong>quantity</strong> using merge sort."
        "      </p>"
        "    </div>"
        "    <span class='badge bg-secondary'>Sample size: {{ records|length }} products</span>"
        "  </div>"

        "  <form class='row gy-2 gx-3 align-items-end mb-4' method='get'>"
        "    <div class='col-md-3'>"
        "      <label class='form-label'>Search Field</label>"
        "      <select name='search_field' class='form-select form-select-sm'>"
        "        <option value='id' {% if search_field=='id' %}selected{% endif %}>Product ID (binary search)</option>"
        "        <option value='name' {% if search_field=='name' %}selected{% endif %}>Name (linear search)</option>"
        "      </select>"
        "    </div>"
        "    <div class='col-md-3'>"
        "      <label class='form-label'>Search Query</label>"
        "      <input type='text' name='search_query' value='{{ search_query }}' class='form-control form-control-sm'>"
        "    </div>"
        "    <div class='col-md-3'>"
        "      <label class='form-label'>Sort By (merge sort)</label>"
        "      <select name='sort_by' class='form-select form-select-sm'>"
        "        <option value='' {% if not sort_by %}selected{% endif %}>None</option>"
        "        <option value='price' {% if sort_by=='price' %}selected{% endif %}>Price</option>"
        "        <option value='quantity' {% if sort_by=='quantity' %}selected{% endif %}>Quantity</option>"
        "      </select>"
        "    </div>"
        "    <div class='col-md-3 d-flex gap-2'>"
        "      <button type='submit' class='btn btn-sm btn-primary mt-auto'>Apply</button>"
        "      <a href='{{ url_for('inventory') }}' class='btn btn-sm btn-outline-secondary mt-auto'>Reset</a>"
        "    </div>"
        "  </form>"

        "  {% if search_query %}"
        "    <h6 class='mb-2'>Search Results</h6>"
        "    {% if results %}"
        "      <div class='table-responsive mb-4'>"
        "        <table class='table table-striped table-sm align-middle'>"
        "          <thead class='table-light'>"
        "            <tr>"
        "              <th>ID</th><th>Name</th><th>Price (₹)</th><th>Quantity</th>"
        "            </tr>"
        "          </thead>"
        "          <tbody>"
        "            {% for row in results %}"
        "            <tr>"
        "              <td>{{ row.id }}</td>"
        "              <td>{{ row.name }}</td>"
        "              <td>{{ row.price }}</td>"
        "              <td>{{ row.quantity }}</td>"
        "            </tr>"
        "            {% endfor %}"
        "          </tbody>"
        "        </table>"
        "      </div>"
        "    {% else %}"
        "      <p class='text-muted small mb-4'>No matching products found.</p>"
        "    {% endif %}"
        "  {% endif %}"

        "  <h6 class='mb-2'>All Products {% if sort_by %}<span class='text-muted'>(sorted by {{ sort_by }})</span>{% endif %}</h6>"
        "  <div class='table-responsive'>"
        "    <table class='table table-hover table-sm align-middle'>"
        "      <thead class='table-light'>"
        "        <tr>"
        "          <th>ID</th><th>Name</th><th>Price (₹)</th><th>Quantity</th>"
        "        </tr>"
        "      </thead>"
        "      <tbody>"
        "        {% for row in records %}"
        "        <tr>"
        "          <td>{{ row.id }}</td>"
        "          <td>{{ row.name }}</td>"
        "          <td>{{ row.price }}</td>"
        "          <td>{{ row.quantity }}</td>"
        "        </tr>"
        "        {% endfor %}"
        "      </tbody>"
        "    </table>"
        "  </div>"

        "  <p class='text-muted small mt-3 mb-0'>"
        "    Complexity: sorting uses merge sort (O(n log n) time, O(n) space), "
        "    searching by ID uses binary search (O(log n)) after sorting."
        "  </p>"
        "</div>"
    )

    class Obj(dict):
        __getattr__ = dict.get

    records_objs = [Obj(r) for r in records]
    results_objs = [Obj(r) for r in results]

    return render_with_base(
        content,
        page_title="Inventory Management",
        active_page="inventory",
        records=records_objs,
        results=results_objs,
        search_field=search_field,
        search_query=search_query,
        sort_by=sort_by,
    )


# -----------------------------
# Hospital Management Module
# -----------------------------


@app.route("/hospital")
def hospital():
    search_field = request.args.get("search_field", "id")
    search_query = request.args.get("search_query", "").strip()
    sort_by = request.args.get("sort_by", "")

    records = PATIENTS.copy()
    results = []

    if sort_by == "severity":
        # Higher severity first, so sort ascending and then reverse for display
        records = merge_sort(records, key=lambda x: x["severity"])
        records.reverse()
    elif sort_by == "bill_amount":
        records = merge_sort(records, key=lambda x: x["bill_amount"])

    if search_query:
        if search_field == "id":
            try:
                target_id = int(search_query)
                results = binary_search_on_field(PATIENTS, "id", target_id)
            except ValueError:
                results = []
        elif search_field == "name":
            results = linear_search_on_name(PATIENTS, "name", search_query)

    content = (
        "<div class='card p-4'>"
        "  <div class='d-flex justify-content-between align-items-center mb-3'>"
        "    <div>"
        "      <h2 class='h4 mb-1'>Hospital Management</h2>"
        "      <p class='text-muted mb-0 small'>"
        "        Search patients by <strong>ID</strong> (binary search) or <strong>name</strong>, "
        "        and sort by <strong>severity</strong> or <strong>bill amount</strong>."
        "      </p>"
        "    </div>"
        "    <span class='badge bg-secondary'>Sample size: {{ records|length }} patients</span>"
        "  </div>"

        "  <form class='row gy-2 gx-3 align-items-end mb-4' method='get'>"
        "    <div class='col-md-3'>"
        "      <label class='form-label'>Search Field</label>"
        "      <select name='search_field' class='form-select form-select-sm'>"
        "        <option value='id' {% if search_field=='id' %}selected{% endif %}>Patient ID (binary search)</option>"
        "        <option value='name' {% if search_field=='name' %}selected{% endif %}>Name (linear search)</option>"
        "      </select>"
        "    </div>"
        "    <div class='col-md-3'>"
        "      <label class='form-label'>Search Query</label>"
        "      <input type='text' name='search_query' value='{{ search_query }}' class='form-control form-control-sm'>"
        "    </div>"
        "    <div class='col-md-3'>"
        "      <label class='form-label'>Sort By (merge sort)</label>"
        "      <select name='sort_by' class='form-select form-select-sm'>"
        "        <option value='' {% if not sort_by %}selected{% endif %}>None</option>"
        "        <option value='severity' {% if sort_by=='severity' %}selected{% endif %}>Severity (high → low)</option>"
        "        <option value='bill_amount' {% if sort_by=='bill_amount' %}selected{% endif %}>Bill Amount</option>"
        "      </select>"
        "    </div>"
        "    <div class='col-md-3 d-flex gap-2'>"
        "      <button type='submit' class='btn btn-sm btn-primary mt-auto'>Apply</button>"
        "      <a href='{{ url_for('hospital') }}' class='btn btn-sm btn-outline-secondary mt-auto'>Reset</a>"
        "    </div>"
        "  </form>"

        "  {% if search_query %}"
        "    <h6 class='mb-2'>Search Results</h6>"
        "    {% if results %}"
        "      <div class='table-responsive mb-4'>"
        "        <table class='table table-striped table-sm align-middle'>"
        "          <thead class='table-light'>"
        "            <tr>"
        "              <th>ID</th><th>Name</th><th>Severity (1-5)</th><th>Bill Amount (₹)</th>"
        "            </tr>"
        "          </thead>"
        "          <tbody>"
        "            {% for row in results %}"
        "            <tr>"
        "              <td>{{ row.id }}</td>"
        "              <td>{{ row.name }}</td>"
        "              <td>{{ row.severity }}</td>"
        "              <td>{{ row.bill_amount }}</td>"
        "            </tr>"
        "            {% endfor %}"
        "          </tbody>"
        "        </table>"
        "      </div>"
        "    {% else %}"
        "      <p class='text-muted small mb-4'>No matching patients found.</p>"
        "    {% endif %}"
        "  {% endif %}"

        "  <h6 class='mb-2'>All Patients {% if sort_by %}<span class='text-muted'>(sorted by {{ sort_by }})</span>{% endif %}</h6>"
        "  <div class='table-responsive'>"
        "    <table class='table table-hover table-sm align-middle'>"
        "      <thead class='table-light'>"
        "        <tr>"
        "          <th>ID</th><th>Name</th><th>Severity (1-5)</th><th>Bill Amount (₹)</th>"
        "        </tr>"
        "      </thead>"
        "      <tbody>"
        "        {% for row in records %}"
        "        <tr>"
        "          <td>{{ row.id }}</td>"
        "          <td>{{ row.name }}</td>"
        "          <td>{{ row.severity }}</td>"
        "          <td>{{ row.bill_amount }}</td>"
        "        </tr>"
        "        {% endfor %}"
        "      </tbody>"
        "    </table>"
        "  </div>"

        "  <p class='text-muted small mt-3 mb-0'>"
        "    Complexity: merge sort provides O(n log n) sorting when triaging by severity or billing; "
        "    binary search gives O(log n) lookups by patient ID."
        "  </p>"
        "</div>"
    )

    class Obj(dict):
        __getattr__ = dict.get

    records_objs = [Obj(r) for r in records]
    results_objs = [Obj(r) for r in results]

    return render_with_base(
        content,
        page_title="Hospital Management",
        active_page="hospital",
        records=records_objs,
        results=results_objs,
        search_field=search_field,
        search_query=search_query,
        sort_by=sort_by,
    )


# -----------------------------
# University Result Processing
# -----------------------------


@app.route("/university")
def university():
    search_roll = request.args.get("roll_no", "").strip()
    sort_by = request.args.get("sort_by", "marks")

    records = STUDENTS.copy()
    results = []

    # Rank list is naturally sorted by marks (descending)
    if sort_by == "marks":
        records = merge_sort(records, key=lambda x: x["marks"])
        records.reverse()

    if search_roll:
        try:
            roll = int(search_roll)
            results = binary_search_on_field(STUDENTS, "roll_no", roll)
        except ValueError:
            results = []

    content = (
        "<div class='card p-4'>"
        "  <div class='d-flex justify-content-between align-items-center mb-3'>"
        "    <div>"
        "      <h2 class='h4 mb-1'>University Result Processing</h2>"
        "      <p class='text-muted mb-0 small'>"
        "        Search students by <strong>roll number</strong> using binary search and "
        "        generate a <strong>rank list</strong> sorted by marks with merge sort."
        "      </p>"
        "    </div>"
        "    <span class='badge bg-secondary'>Sample size: {{ records|length }} students</span>"
        "  </div>"

        "  <form class='row gy-2 gx-3 align-items-end mb-4' method='get'>"
        "    <div class='col-md-3'>"
        "      <label class='form-label'>Roll Number (binary search)</label>"
        "      <input type='text' name='roll_no' value='{{ search_roll }}' class='form-control form-control-sm'>"
        "    </div>"
        "    <div class='col-md-3'>"
        "      <label class='form-label'>Sort By (merge sort)</label>"
        "      <select name='sort_by' class='form-select form-select-sm'>"
        "        <option value='marks' selected>Marks (high → low)</option>"
        "      </select>"
        "    </div>"
        "    <div class='col-md-3 d-flex gap-2'>"
        "      <button type='submit' class='btn btn-sm btn-primary mt-auto'>Apply</button>"
        "      <a href='{{ url_for('university') }}' class='btn btn-sm btn-outline-secondary mt-auto'>Reset</a>"
        "    </div>"
        "  </form>"

        "  {% if search_roll %}"
        "    <h6 class='mb-2'>Search Result</h6>"
        "    {% if results %}"
        "      <div class='table-responsive mb-4'>"
        "        <table class='table table-striped table-sm align-middle'>"
        "          <thead class='table-light'>"
        "            <tr><th>Roll No</th><th>Name</th><th>Marks</th></tr>"
        "          </thead>"
        "          <tbody>"
        "            {% for row in results %}"
        "            <tr>"
        "              <td>{{ row.roll_no }}</td>"
        "              <td>{{ row.name }}</td>"
        "              <td>{{ row.marks }}</td>"
        "            </tr>"
        "            {% endfor %}"
        "          </tbody>"
        "        </table>"
        "      </div>"
        "    {% else %}"
        "      <p class='text-muted small mb-4'>No student found with that roll number.</p>"
        "    {% endif %}"
        "  {% endif %}"

        "  <h6 class='mb-2'>Rank List (by marks)</h6>"
        "  <div class='table-responsive'>"
        "    <table class='table table-hover table-sm align-middle'>"
        "      <thead class='table-light'>"
        "        <tr><th>Rank</th><th>Roll No</th><th>Name</th><th>Marks</th></tr>"
        "      </thead>"
        "      <tbody>"
        "        {% for row in records %}"
        "        <tr>"
        "          <td>{{ loop.index }}</td>"
        "          <td>{{ row.roll_no }}</td>"
        "          <td>{{ row.name }}</td>"
        "          <td>{{ row.marks }}</td>"
        "        </tr>"
        "        {% endfor %}"
        "      </tbody>"
        "    </table>"
        "  </div>"

        "  <p class='text-muted small mt-3 mb-0'>"
        "    Complexity: ranking uses merge sort (O(n log n)) while roll-number lookup uses binary search (O(log n))."
        "  </p>"
        "</div>"
    )

    class Obj(dict):
        __getattr__ = dict.get

    records_objs = [Obj(r) for r in records]
    results_objs = [Obj(r) for r in results]

    return render_with_base(
        content,
        page_title="University Results",
        active_page="university",
        records=records_objs,
        results=results_objs,
        search_roll=search_roll,
        sort_by=sort_by,
    )


# -----------------------------
# Food Delivery System
# -----------------------------


@app.route("/food")
def food_delivery():
    search_field = request.args.get("search_field", "order_id")
    search_query = request.args.get("search_query", "").strip()
    sort_by = request.args.get("sort_by", "")

    records = ORDERS.copy()
    results = []

    if sort_by == "delivery_time":
        records = merge_sort(records, key=lambda x: x["delivery_time"])
    elif sort_by == "price":
        records = merge_sort(records, key=lambda x: x["price"])

    if search_query:
        if search_field == "order_id":
            try:
                target_id = int(search_query)
                results = binary_search_on_field(ORDERS, "order_id", target_id)
            except ValueError:
                results = []
        elif search_field == "customer":
            results = linear_search_on_name(ORDERS, "customer", search_query)

    content = (
        "<div class='card p-4'>"
        "  <div class='d-flex justify-content-between align-items-center mb-3'>"
        "    <div>"
        "      <h2 class='h4 mb-1'>Food Delivery System</h2>"
        "      <p class='text-muted mb-0 small'>"
        "        Search orders by <strong>order ID</strong> (binary search) or <strong>customer name</strong>, "
        "        and sort by <strong>delivery time</strong> or <strong>price</strong>."
        "      </p>"
        "    </div>"
        "    <span class='badge bg-secondary'>Sample size: {{ records|length }} orders</span>"
        "  </div>"

        "  <form class='row gy-2 gx-3 align-items-end mb-4' method='get'>"
        "    <div class='col-md-3'>"
        "      <label class='form-label'>Search Field</label>"
        "      <select name='search_field' class='form-select form-select-sm'>"
        "        <option value='order_id' {% if search_field=='order_id' %}selected{% endif %}>Order ID (binary search)</option>"
        "        <option value='customer' {% if search_field=='customer' %}selected{% endif %}>Customer Name (linear search)</option>"
        "      </select>"
        "    </div>"
        "    <div class='col-md-3'>"
        "      <label class='form-label'>Search Query</label>"
        "      <input type='text' name='search_query' value='{{ search_query }}' class='form-control form-control-sm'>"
        "    </div>"
        "    <div class='col-md-3'>"
        "      <label class='form-label'>Sort By (merge sort)</label>"
        "      <select name='sort_by' class='form-select form-select-sm'>"
        "        <option value='' {% if not sort_by %}selected{% endif %}>None</option>"
        "        <option value='delivery_time' {% if sort_by=='delivery_time' %}selected{% endif %}>Delivery Time (min)</option>"
        "        <option value='price' {% if sort_by=='price' %}selected{% endif %}>Price</option>"
        "      </select>"
        "    </div>"
        "    <div class='col-md-3 d-flex gap-2'>"
        "      <button type='submit' class='btn btn-sm btn-primary mt-auto'>Apply</button>"
        "      <a href='{{ url_for('food_delivery') }}' class='btn btn-sm btn-outline-secondary mt-auto'>Reset</a>"
        "    </div>"
        "  </form>"

        "  {% if search_query %}"
        "    <h6 class='mb-2'>Search Results</h6>"
        "    {% if results %}"
        "      <div class='table-responsive mb-4'>"
        "        <table class='table table-striped table-sm align-middle'>"
        "          <thead class='table-light'>"
        "            <tr><th>Order ID</th><th>Customer</th><th>Delivery Time (min)</th><th>Price (₹)</th></tr>"
        "          </thead>"
        "          <tbody>"
        "            {% for row in results %}"
        "            <tr>"
        "              <td>{{ row.order_id }}</td>"
        "              <td>{{ row.customer }}</td>"
        "              <td>{{ row.delivery_time }}</td>"
        "              <td>{{ row.price }}</td>"
        "            </tr>"
        "            {% endfor %}"
        "          </tbody>"
        "        </table>"
        "      </div>"
        "    {% else %}"
        "      <p class='text-muted small mb-4'>No matching orders found.</p>"
        "    {% endif %}"
        "  {% endif %}"

        "  <h6 class='mb-2'>All Orders {% if sort_by %}<span class='text-muted'>(sorted by {{ sort_by }})</span>{% endif %}</h6>"
        "  <div class='table-responsive'>"
        "    <table class='table table-hover table-sm align-middle'>"
        "      <thead class='table-light'>"
        "        <tr><th>Order ID</th><th>Customer</th><th>Delivery Time (min)</th><th>Price (₹)</th></tr>"
        "      </thead>"
        "      <tbody>"
        "        {% for row in records %}"
        "        <tr>"
        "          <td>{{ row.order_id }}</td>"
        "          <td>{{ row.customer }}</td>"
        "          <td>{{ row.delivery_time }}</td>"
        "          <td>{{ row.price }}</td>"
        "        </tr>"
        "        {% endfor %}"
        "      </tbody>"
        "    </table>"
        "  </div>"

        "  <p class='text-muted small mt-3 mb-0'>"
        "    Complexity: sorting by time/price uses merge sort (O(n log n)); "
        "    searching by order ID uses binary search (O(log n))."
        "  </p>"
        "</div>"
    )

    class Obj(dict):
        __getattr__ = dict.get

    records_objs = [Obj(r) for r in records]
    results_objs = [Obj(r) for r in results]

    return render_with_base(
        content,
        page_title="Food Delivery System",
        active_page="food",
        records=records_objs,
        results=results_objs,
        search_field=search_field,
        search_query=search_query,
        sort_by=sort_by,
    )


# -----------------------------
# App entry point
# -----------------------------

if __name__ == "__main__":
    # Debug=True for development; turn off in production.
    app.run(debug=True)

