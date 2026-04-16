(() => {
  const implementationRadios = document.querySelectorAll(
    'input[name="implementation"]'
  );
  const contactForm = document.getElementById("contact-form");
  const nameInput = document.getElementById("name");
  const phoneInput = document.getElementById("phone");
  const searchNameInput = document.getElementById("search-name");
  const searchBtn = document.getElementById("search-btn");
  const deleteBtn = document.getElementById("delete-btn");
  const refreshBtn = document.getElementById("refresh-btn");
  const searchResultEl = document.getElementById("search-result");
  const contactsTable = document.getElementById("contacts-table");
  const contactsTbody = contactsTable.querySelector("tbody");
  const contactsEmpty = document.getElementById("contacts-empty");
  const toast = document.getElementById("toast");

  function getImplementation() {
    const selected = Array.from(implementationRadios).find((r) => r.checked);
    return selected ? selected.value : "array";
  }

  function showToast(message, isError = false) {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.remove("hidden", "error");
    if (isError) {
      toast.classList.add("error");
    }
    requestAnimationFrame(() => {
      toast.classList.add("show");
    });
    setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => {
        toast.classList.add("hidden");
      }, 200);
    }, 2600);
  }

  async function fetchJson(url, options) {
    const res = await fetch(url, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
    const text = await res.text();
    let json;
    try {
      json = text ? JSON.parse(text) : {};
    } catch {
      json = { error: text || "Unexpected response from server." };
    }
    if (!res.ok) {
      const message = json.error || `Request failed with status ${res.status}`;
      throw new Error(message);
    }
    return json;
  }

  async function loadContacts() {
    const implementation = getImplementation();
    try {
      const data = await fetchJson(
        `/api/contacts?implementation=${encodeURIComponent(implementation)}`
      );
      const contacts = data.contacts || [];
      renderContacts(contacts);
    } catch (err) {
      console.error(err);
      showToast(err.message || "Failed to load contacts.", true);
    }
  }

  function renderContacts(contacts) {
    contactsTbody.innerHTML = "";
    if (!contacts.length) {
      contactsTable.classList.add("hidden");
      contactsEmpty.classList.remove("hidden");
      return;
    }
    contactsEmpty.classList.add("hidden");
    contactsTable.classList.remove("hidden");

    for (const c of contacts) {
      const tr = document.createElement("tr");
      const tdName = document.createElement("td");
      const tdPhone = document.createElement("td");
      tdName.textContent = c.name;
      tdPhone.textContent = c.phone;
      tr.appendChild(tdName);
      tr.appendChild(tdPhone);
      contactsTbody.appendChild(tr);
    }
  }

  contactForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = nameInput.value.trim();
    const phone = phoneInput.value.trim();
    if (!name || !phone) {
      showToast("Name and phone are required.", true);
      return;
    }
    const implementation = getImplementation();

    try {
      await fetchJson("/api/contacts", {
        method: "POST",
        body: JSON.stringify({ implementation, name, phone }),
      });
      showToast("Contact saved.");
      await loadContacts();
      contactForm.reset();
      nameInput.focus();
    } catch (err) {
      console.error(err);
      showToast(err.message || "Failed to save contact.", true);
    }
  });

  searchBtn.addEventListener("click", async () => {
    const name = searchNameInput.value.trim();
    if (!name) {
      showToast("Enter a name to search.", true);
      return;
    }
    const implementation = getImplementation();
    searchResultEl.textContent = "";
    searchResultEl.classList.remove("success", "error");

    try {
      const data = await fetchJson(
        `/api/contacts/${encodeURIComponent(
          name
        )}?implementation=${encodeURIComponent(implementation)}`
      );
      searchResultEl.textContent = `${data.name} - ${data.phone}`;
      searchResultEl.classList.add("success");
    } catch (err) {
      searchResultEl.textContent = err.message || "Contact not found.";
      searchResultEl.classList.add("error");
    }
  });

  deleteBtn.addEventListener("click", async () => {
    const name = searchNameInput.value.trim();
    if (!name) {
      showToast("Enter a name to delete.", true);
      return;
    }
    const implementation = getImplementation();

    if (
      !window.confirm(
        `Delete contact "${name}" from the ${implementation} implementation?`
      )
    ) {
      return;
    }

    try {
      await fetchJson(
        `/api/contacts/${encodeURIComponent(
          name
        )}?implementation=${encodeURIComponent(implementation)}`,
        { method: "DELETE" }
      );
      showToast("Contact deleted.");
      searchResultEl.textContent = "";
      searchResultEl.classList.remove("success", "error");
      await loadContacts();
    } catch (err) {
      console.error(err);
      showToast(err.message || "Failed to delete contact.", true);
    }
  });

  implementationRadios.forEach((radio) => {
    radio.addEventListener("change", () => {
      loadContacts();
      searchResultEl.textContent = "";
      searchResultEl.classList.remove("success", "error");
    });
  });

  refreshBtn.addEventListener("click", () => {
    loadContacts();
  });

  // Initial load
  loadContacts();
})();

