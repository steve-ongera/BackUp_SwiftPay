document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById("myPieChart");
  const topProductsNames = JSON.parse(document.getElementById("top_products_names").value);
  const topProductsQuantity = JSON.parse(document.getElementById("top_products_quantity").value);

  new Chart(ctx, {
      type: 'doughnut',
      data: {
          labels: topProductsNames,
          datasets: [{
              data: topProductsQuantity,
              backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
              hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
              hoverBorderColor: "rgba(234, 236, 244, 1)",
          }],
      },
      options: {
          maintainAspectRatio: false,
          cutoutPercentage: 70,
          plugins: {
              tooltip: {
                  backgroundColor: "rgb(255,255,255)",
                  bodyFontColor: "#858796",
                  borderColor: '#dddfeb',
                  borderWidth: 1,
                  displayColors: false,
              },
              legend: {
                  display: true,
                  position: 'bottom',
              },
          },
      },
  });
});
