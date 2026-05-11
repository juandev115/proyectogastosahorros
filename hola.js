// 1. CLASE (Siempre primero)
class GestorNomina {
    constructor(pagoHora) {
        this.pagoHora = pagoHora;
    }

    // Método para calcular salario usando ciclos y condiciones
    calcular(fila) {
        let normales = 0;
        let extras = 0;
        for (let i = 0; i < fila.length; i++) {
            if (fila[i] === 1) {
                normales++;
            } else if (fila[i] === 2) {
                extras++;
            }
        }
        let total = (normales * this.pagoHora) + (extras * this.pagoHora * 1.5);
        return { total, normales, extras };
    }
}

// 2. DATOS INICIALES (Matrices y Arreglos)
const nombres = ["Juan", "Lizeth", "Cristina"];
const miGestor = new GestorNomina(20);
let matrizAsistencia = [
    [1, 1, 1, 1, 1, 1, 1, 1, 0], // Juan
    [1, 1, 1, 1, 1, 1, 1, 1, 2], // Lizeth
    [1, 1, 0, 0, 1, 1, 1, 1, 0]  // Cristina
];

// 3. LÓGICA PARA LA TERMINAL (Node.js)
const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
});

function mostrarMenu() {
    console.log("\n=== SISTEMA DE ASISTENCIA (8:00 AM - 4:00 PM+) ===");
    console.table(matrizAsistencia); // Esto se ve genial en la terminal de VS
    
    console.log("1. Modificar Registro");
    console.log("2. Generar Reporte de Pagos");
    console.log("3. Salir");
    
    readline.question("\nSelecciona una opción: ", (opcion) => {
        if (opcion === "1") {
            modificar();
        } else if (opcion === "2") {
            reporte();
        } else if (opcion === "3") {
            console.log("Saliendo del sistema...");
            readline.close();
        } else {
            console.log("Opción no válida.");
            mostrarMenu();
        }
    });
}

function modificar() {
    readline.question("ID del trabajador (0:Juan, 1:Lizeth, 2:Cristina): ", (id) => {
        readline.question("Hora a modificar (Columna 0-8): ", (col) => {
            readline.question("Nuevo estado (0:Falta, 1:Normal, 2:Extra): ", (val) => {
                
                let i = parseInt(id);
                let j = parseInt(col);
                let v = parseInt(val);

                if (matrizAsistencia[i] && matrizAsistencia[i][j] !== undefined) {
                    matrizAsistencia[i][j] = v;
                    console.log("\n✅ Registro actualizado.");
                } else {
                    console.log("\n❌ Error: Datos fuera de rango.");
                }
                mostrarMenu();
            });
        });
    });
}

function reporte() {
    console.log("\n--- REPORTE FINAL DE NÓMINA ---");
    for (let i = 0; i < matrizAsistencia.length; i++) {
        let res = miGestor.calcular(matrizAsistencia[i]);
        console.log(`${nombres[i].padEnd(10)} | Pago: $${res.total} | Horas Norm: ${res.normales} | Extras: ${res.extras}`);
    }
    mostrarMenu();
}

// Iniciar programa
mostrarMenu();