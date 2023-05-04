function addSymptoms() {
  // Отримати введені симптоми з поле вводу
  const symptomsInput = document.getElementsById("symptoms");
  const symptoms = symptomsInput.value;

  // Створити новий елемент для відображення симптомів
  const symptomElement = document.createElement("p");
  symptomElement.innerText = symptoms;

  // Отримати контейнер для відображення симптомів
  const container = document.getElementsByClassName("symptom-container");

  // Додати новий елемент з симптомами до контейнера
  container.appendChild(symptomElement);

  // Очистити поле вводу
  symptomsInput.value = "";
}

