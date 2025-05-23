$("#slider1, #slider2, #slider3, #slider4").owlCarousel({
  loop: true,
  margin: 20,
  responsiveClass: true,
  responsive: {
    0: {
      items: 1,
      nav: false,
      autoplay: true,
    },
    600: {
      items: 3,
      nav: true,
      autoplay: true,
    },
    1000: {
      items: 5,
      nav: true,
      loop: true,
      autoplay: true,
    },
  },
});

$(".plus-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var eml = $(this).siblings(".quantity")[0];
  $.ajax({
    type: "GET",
    url: "/pluscart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      eml.innerText = data.quantity;
      document.getElementById("amount").innerText =
        "Rs. " + data.amount.toFixed(2);
      document.getElementById("totalamount").innerText =
        "Rs. " + data.totalamount.toFixed(2);
    },
  });
});

$(".minus-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var eml = $(this).siblings(".quantity")[0];
  $.ajax({
    type: "GET",
    url: "/minuscart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      eml.innerText = data.quantity;
      document.getElementById("amount").innerText =
        "Rs. " + data.amount.toFixed(2);
      document.getElementById("totalamount").innerText =
        "Rs. " + data.totalamount.toFixed(2);
    },
  });
});

$(".remove-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var eml = this;
  $.ajax({
    type: "GET",
    url: "/removecart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      document.getElementById("amount").innerText =
        "Rs. " + data.amount.toFixed(2);
      document.getElementById("totalamount").innerText =
        "Rs. " + data.totalamount.toFixed(2);
      eml.parentNode.parentNode.parentNode.parentNode.remove();
    },
  });
});
