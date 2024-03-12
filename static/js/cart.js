console.log("Are you there?");

document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("update-cart-btn")
    .addEventListener("click", function () {
      // Get all the rows in the table
      const rows = document.querySelectorAll(".table tbody tr");

      // Iterate through each row
      rows.forEach((row) => {
        // Get the quantity input and unit price elements
        const quantityInput = row.querySelector(".cart-plus-minus-box");
        const unitPriceSpan = row.querySelector(".uren-product-price .amount");

        // Parse the quantity and unit price values
        const quantity = parseInt(quantityInput.value);
        const unitPrice = parseFloat(
          unitPriceSpan.innerText.replace("Ksh. ", "")
        );

        // Calculate the subtotal
        const subtotal = quantity * unitPrice;

        // Set the subtotal value
        row.querySelector(".product-subtotal .subtotal").innerText =
          subtotal.toFixed(2);
      });

      // Calculate the new total
      const subtotalSpans = document.querySelectorAll(
        ".product-subtotal .subtotal"
      );
      let newTotal = 0;
      subtotalSpans.forEach((span) => {
        newTotal += parseFloat(span.innerText);
      });

      // Set the new total value
      const totalSpan = document.querySelector(
        ".cart-page-total li:last-child span:last-child .subtotal"
      );
      totalSpan.innerText = newTotal.toFixed(2);
    });
});

const quantityInputs = document.querySelectorAll(".cart-plus-minus-box");

quantityInputs.forEach((input) => {
  input.addEventListener("change", (event) => {
    const itemId = event.target.dataset.productId;
    const quantity = event.target.value;

    // Send AJAX request to update the quantity
    updateQuantity(itemId, quantity);
  });
});

function updateQuantity(itemId, quantity) {
  const url = "/update_item_quantity/";
  const data = {
    item_id: itemId,
    quantity: quantity,
    csrfmiddlewaretoken: "{{ csrf_token }}",
  };

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      // Update the checkout.html page with the new total value and item quantities
      updateCheckout(data.new_total, data.cart_items);
    })
    .catch((error) => console.error("Error:", error));
}

function updateCheckout(new_total, cart_items) {
  // Update the total value on the checkout.html page
  const checkoutTotal = document.querySelector(".order-total .amount");
  checkoutTotal.innerText = new_total;

  // Update the item quantities on the checkout.html page
  const checkoutItems = document.querySelectorAll(".cart_item");

  checkoutItems.forEach((item) => {
    const itemId = item.dataset.itemId;
    const itemQuantity = cart_items.find(
      (cartItem) => cartItem.id == itemId
    ).quantity;

    const itemQuantityElement = item.querySelector(".product-quantity");
    itemQuantityElement.innerText = ` × ${itemQuantity}`;
  });
}

document.addEventListener("DOMContentLoaded", function () {
  // Get the checkout link element
  const checkoutLink = document.getElementById("checkout-link");

  if (checkoutLink) {
    // Set the href attribute to the checkout URL with a query parameter
    checkoutLink.setAttribute(
      "href",
      "{{ url 'checkout' }}?new_total=" + newTotal
    );
  } else {
    console.error('Failed to find element with ID "checkout-link"');
  }
});

$(document).on("click", "add-to-wishlist", function () {
  let product_id = $(this).attr("data-product-item");
  let this_val = $(this);

  console.log("product ID is", product_id);
});
