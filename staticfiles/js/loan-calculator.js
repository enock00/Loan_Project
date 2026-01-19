const calculateBtn = document.getElementById('calculate-btn');

if (calculateBtn) {
  calculateBtn.addEventListener('click', function () {
    const amount = parseFloat(document.getElementById('amount').value);
    const interest = parseFloat(document.getElementById('interest').value) / 100 / 12;
    const months = parseFloat(document.getElementById('years').value);

    if (!amount || !interest || !months) {
      alert("Please fill in all fields");
      return;
    }

    const x = Math.pow(1 + interest, months);
    const monthly = (amount * x * interest) / (x - 1);
    const total = monthly * months;
    const totalInterest = total - amount;

    document.getElementById('monthly-payment').innerText = `KES ${monthly.toFixed(2)}`;
    document.getElementById('total-payment').innerText = `KES ${total.toFixed(2)}`;
    document.getElementById('total-interest').innerText = `KES ${totalInterest.toFixed(2)}`;
  });
}
