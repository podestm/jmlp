// Function to update form fields based on the selected option
function updateFormFields() {
    // Get the selected option value
    var selectedRacer = document.getElementById('racers').value;
    // Split the value into parts (assuming space-separated values)
    var racerParts = selectedRacer.split('!');
    // Update the form fields with the corresponding values
    document.getElementById('racer_firstName').value = racerParts[0] || '';
    document.getElementById('racer_lastName').value = racerParts[1] || '';
    document.getElementById('racer_birthYear').value = racerParts[2] || '';
    document.getElementById('racer_teamName').value = racerParts[3] || '';
    document.getElementById('racer_gender').value = racerParts[4] || '';
}

// Call the updateFormFields function when the page loads
window.onload = function () {
    updateFormFields(); // Initial update
    // Add an event listener to the racers select element
    document.getElementById('racers').addEventListener('change', updateFormFields);
};

function downloadFile(fileName) {
    window.open('/download/' + fileName, '_blank');
}
