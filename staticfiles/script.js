let currentExpression = "";
let newCalculation = true;
const display = document.getElementById("display");

function handleInput(value) {
    if (value === "AC") {
        currentExpression = "";
        updateDisplay("0");
        newCalculation = true;
    } else if (value === "CE") {
        if (newCalculation) {
            currentExpression = "";
            updateDisplay("0");
        } else if (currentExpression.length > 0) {
            currentExpression = currentExpression.slice(0, -1);
            updateDisplay(currentExpression || "0");
        }
    } else {
        const operators = ['+', '-', '×', '÷', '%'];
        if (newCalculation) {
            if (/^\d|\./.test(value)) {
                currentExpression = value;
            } else {
                currentExpression += value;
            }
            newCalculation = false;
        } else {
            // Prevent consecutive operators
            if (operators.includes(value) && operators.includes(currentExpression.slice(-1))) {
                currentExpression = currentExpression.slice(0, -1) + value;
            } else {
                currentExpression += value;
            }
        }
        updateDisplay(currentExpression);
    }
}

function updateDisplay(text) {
    display.value = text;
}

document.getElementById("equals-btn").addEventListener("click", async () => {
    if (!currentExpression) return;

    try {
        const response = await fetch("/calculate/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ expression: currentExpression }),
        });

        const data = await response.json();

        if (data.success) {
            updateDisplay(data.result);
            currentExpression = data.result.toString();
            newCalculation = true;
        } else {
            updateDisplay(data.error);
            currentExpression = "";
            newCalculation = true;
        }
    } catch (error) {
        updateDisplay("Error");
        currentExpression = "";
        newCalculation = true;
    }
});
