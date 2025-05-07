const diseaseName = localStorage.getItem("predictedDisease");

const tips = {
  "Anthracnose": [
    "Remove and destroy infected leaves and twigs.",
    "Avoid overhead watering to reduce moisture.",
    "Apply a fungicide if the infection is severe.",
    "Maintain good air circulation around the plants."
  ],
  "Blight": [
    "Use resistant plant varieties when available.",
    "Prune infected branches and destroy debris.",
    "Apply copper-based fungicide preventively.",
    "Avoid watering late in the day."
  ],
  "Leaf Rust": [
    "Remove rust-infected leaves immediately.",
    "Improve airflow through proper spacing.",
    "Use sulfur or neem oil sprays as treatment.",
    "Avoid excessive nitrogen fertilization."
  ],
  "Powdery Mildew": [
    "Apply neem oil or baking soda spray regularly.",
    "Ensure the plant receives enough sunlight.",
    "Water from below, not overhead.",
    "Prune affected areas and discard them."
  ],
  "Gray Light": [
    "Ensure proper sunlight exposure to the plants.",
    "Use a fungicide to treat the affected areas.",
    "Avoid over-watering as this may worsen the condition.",
    "Prune infected leaves to prevent further spread."
  ]
};

function displayTips(tipsList) {
  const tipsContainer = document.getElementById("tipsList");
  tipsContainer.innerHTML = "";

  if (tipsList.length > 0) {
    tipsList.forEach(tip => {
      const li = document.createElement("li");
      li.textContent = tip;
      tipsContainer.appendChild(li);
    });
  } else {
    tipsContainer.innerHTML = "<li>No tips available for this disease.</li>";
  }
}

if (diseaseName) {
  document.getElementById("diseaseName").textContent = `Tips for ${diseaseName}`;

  const diseaseTips = tips[diseaseName] || [];
  displayTips(diseaseTips);
} else {
  // If no disease is detected
  document.getElementById("diseaseName").textContent = "No Disease Detected!";
  document.getElementById("tipsList").innerHTML = "<li>Please detect a disease first.</li>";
}

function goBack() {
  window.location.href = "result.html";
}
